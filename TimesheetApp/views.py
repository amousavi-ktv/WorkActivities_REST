# TimesheetApp/views.py
from datetime import timedelta
import json
import gspread
import pandas as pd

from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Q
from django.db import IntegrityError
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django_tables2 import RequestConfig
from oauth2client.service_account import ServiceAccountCredentials

from TimesheetApp.forms import (
    TaskSelectionFormStaff,
    TaskSelectionFormSupervisor,
    AdminTimesheetForm,
)
from TimesheetApp.models import (
    tblAuthUser,
    tblAppUser,
    tblTask,
    tblTaskLogStaff,
    tblTaskLogSupervisor,
    tblTaskLogAdmin,
    vewTaskLogStaff,
    vewTaskLogSupervisor,
    vewTaskLogAdmin,
    vewUserDetails,
    vewTransferViewToGoogleSheet,
    vewUserKey,   # <-- use the plain user_key view for Admin picker
)
from TimesheetApp.tables_staff import TaskLogStaffTable
from TimesheetApp.tables_supervisor import TaskLogSupervisorTable


# --------------------------
# Helpers
# --------------------------
def get_role_key(request):
    """Return role key from session (preferred) or from attached auth_user."""
    rk = request.session.get("role_key")
    if rk:
        return rk.upper()
    auth_user = getattr(request, "auth_user", None)
    if auth_user and getattr(auth_user.fk_userID.fk_roleID, "role_key", None):
        return auth_user.fk_userID.fk_roleID.role_key.upper()
    return "UNKNOWN"


# --------------------------
# Entry / Auth
# --------------------------
@login_required
def welcome(request):
    """Land here, then route to the appropriate dashboard."""
    if not hasattr(request, "auth_user") or request.auth_user is None:
        return redirect("/auth/login/google-oauth2/?prompt=select_account&hd=karbalatv.com")
    return redirect("timesheet:dashboard")


def logout_view(request):
    logout(request)
    return redirect("timesheet:welcome")


# --------------------------
# Role Router
# --------------------------
@login_required
def dashboard(request):
    """
        Lightweight router:
        - STAFF      -> dashboard_staff
        - SUPERVISOR -> dashboard_supervisor
        - ADMIN      -> dashboard_admin
    """
    auth_user = getattr(request, "auth_user", None)
    if not auth_user:
        return HttpResponseForbidden("Unauthorized")

    # cache user details in session for headers
    auth_user_id = auth_user.fk_userID.id
    user_details = vewUserDetails.objects.filter(id=auth_user_id).first()
    role_key = getattr(auth_user.fk_userID.fk_roleID, "role_key", "").upper()
    request.session["user_key"] = getattr(user_details, "user_key", "User")
    request.session["role_key"] = role_key

    if role_key == "STAFF":
        return redirect("timesheet:dashboard_staff")
    if role_key == "SUPERVISOR":
        return redirect("timesheet:dashboard_supervisor")
    if role_key == "ADMIN":
        return redirect("timesheet:dashboard_admin")

    return HttpResponseForbidden("Unknown role")


# --------------------------
# Staff Dashboard
# --------------------------
@login_required
def dashboard_staff(request):
    # Only STAFF should access this page directly
    role_key = get_role_key(request)
    if role_key != 'STAFF':
        return redirect('timesheet:dashboard')

    auth_user = getattr(request, 'auth_user', None)
    if not auth_user:
        return HttpResponseForbidden("Unauthorized")

    auth_user_id = auth_user.fk_userID.id
    user_details = vewUserDetails.objects.filter(id=auth_user_id).first()

    # Helper: compute the last picked task id for this user (to exclude)
    last_log = (
        tblTaskLogStaff.objects
        .filter(fk_userID=auth_user.fk_userID)
        .order_by('-activity_timestamp')
        .only('fk_taskID_id')
        .first()
    )
    last_task_id = last_log.fk_taskID_id if last_log else None

    if request.method == 'POST':
        form = TaskSelectionFormStaff(request.POST, user_id=auth_user_id)

        # ---- Fallback queryset (if Select2/JS is off): exclude last task ----
        if "task" in form.fields and not form.fields["task"].queryset.exists():
            base = tblTask.objects.all()
            if last_task_id:
                base = base.exclude(id=last_task_id)
            form.fields["task"].queryset = base.order_by("task")
        # --------------------------------------------------------------------

        if form.is_valid():
            tblTaskLogStaff.objects.create(
                fk_userID=auth_user.fk_userID,               # pass FK object
                fk_taskID=form.cleaned_data['task'],         # pass FK object
                activity_timestamp=timezone.now(),
                work_activities=form.cleaned_data.get('work_activities', ''),
                remarks=form.cleaned_data.get('remarks', ''),
            )
            return redirect('timesheet:dashboard_staff')
    else:
        form = TaskSelectionFormStaff(user_id=auth_user_id)

        # ---- Fallback queryset (if Select2/JS is off): exclude last task ----
        if "task" in form.fields and not form.fields["task"].queryset.exists():
            base = tblTask.objects.all()
            if last_task_id:
                base = base.exclude(id=last_task_id)
            form.fields["task"].queryset = base.order_by("task")
        # --------------------------------------------------------------------

    logs = vewTaskLogStaff.objects.filter(fk_userID=auth_user_id).order_by('-activity_timestamp')
    table = TaskLogStaffTable(logs)
    RequestConfig(request).configure(table)

    return render(
        request,
        'dashboard_staff.html',
        {
            'form': form,
            'table': table,
            'user_key': (user_details.user_key if user_details else 'Staff'),
        },
    )


# --------------------------
# Supervisor Dashboard (independent)
# --------------------------
@login_required
def dashboard_supervisor(request):
    role_key = get_role_key(request)
    if role_key != "SUPERVISOR":
        return redirect("timesheet:dashboard")

    auth_user = getattr(request, "auth_user", None)
    if not auth_user:
        return HttpResponseForbidden("Unauthorized")

    auth_user_id = auth_user.fk_userID.id
    user_details = vewUserDetails.objects.filter(id=auth_user_id).first()

    if request.method == "POST":
        form = TaskSelectionFormSupervisor(request.POST, user_id=auth_user_id)
        # --- Fallback queryset to avoid empty dropdowns ---
        if "task" in form.fields and not form.fields["task"].queryset.exists():
            form.fields["task"].queryset = tblTask.objects.all().order_by("task")
        # --------------------------------------------------
        try:
            if form.is_valid():
                tblTaskLogSupervisor.objects.create(
                    fk_userID=auth_user.fk_userID,
                    fk_taskID=form.cleaned_data["task"],
                    date=form.cleaned_data["date"],
                    time=form.cleaned_data["time"],
                    action_timestamp=timezone.now(),
                    work_activities=form.cleaned_data.get("work_activities", ""),
                    remarks=form.cleaned_data.get("remarks", ""),
                )
                messages.success(request, "Entry saved.")
                return redirect("timesheet:dashboard_supervisor")
        except IntegrityError:
            messages.error(
                request,
                "Duplicate entry: a record with the same task, date and time already exists."
            )
    else:
        form = TaskSelectionFormSupervisor(user_id=auth_user_id)
        # --- Fallback queryset to avoid empty dropdowns ---
        if "task" in form.fields and not form.fields["task"].queryset.exists():
            form.fields["task"].queryset = tblTask.objects.all().order_by("task")
        # --------------------------------------------------

    logs = vewTaskLogSupervisor.objects.filter(fk_userID=auth_user_id).order_by("-date")
    table = TaskLogSupervisorTable(logs)
    RequestConfig(request).configure(table)

    return render(
        request,
        "dashboard_supervisor.html",
        {
            "form": form,
            "table": table,
            "user_key": (user_details.user_key if user_details else "Supervisor"),
        },
    )


# --------------------------
# Admin Dashboard (independent) – uses vewUserKey
# --------------------------
@login_required
def dashboard_admin(request):
    role_key = get_role_key(request)
    if role_key != "ADMIN":
        return redirect("timesheet:dashboard")

    auth_user = getattr(request, "auth_user", None)
    if not auth_user:
        return HttpResponseForbidden("Unauthorized")

    if request.method == "POST":
        form = AdminTimesheetForm(request.POST)

        # --- Fallback queryset: employee & task, so the selects are never empty ---
        if "user_key" in form.fields and not form.fields["user_key"].queryset.exists():
            form.fields["user_key"].queryset = vewUserKey.objects.all().order_by("user_key")
        if "task" in form.fields and not form.fields["task"].queryset.exists():
            form.fields["task"].queryset = tblTask.objects.all().order_by("task")
        # -------------------------------------------------------------------------

        try:
            if form.is_valid():
                selected_user_key = form.cleaned_data["user_key"]   # vewUserKey instance
                target_user = tblAppUser.objects.filter(
                    user_key=selected_user_key.user_key,
                    is_active=True
                ).first()

                if not target_user:
                    messages.error(request, "Selected employee is not active or not found.")
                else:
                    tblTaskLogAdmin.objects.create(
                        fk_userID=target_user,
                        fk_taskID=form.cleaned_data["task"],
                        date=form.cleaned_data["date"],
                        time=form.cleaned_data["time"],
                        action_timestamp=timezone.now(),
                        work_activities=form.cleaned_data.get("work_activities", ""),
                        remarks=form.cleaned_data.get("remarks", ""),
                        fk_operatorID=auth_user.fk_userID,
                    )
                    messages.success(request, "Entry saved.")
                    return redirect("timesheet:dashboard_admin")
        except IntegrityError:
            messages.error(
                request,
                "Duplicate entry: a record with the same employee, task, date and time already exists."
            )
        except Exception as e:
            messages.error(request, f"Could not save entry: {e}")
    else:
        form = AdminTimesheetForm()

        # --- Fallback queryset: employee & task, so the selects are never empty ---
        if "user_key" in form.fields and not form.fields["user_key"].queryset.exists():
            form.fields["user_key"].queryset = vewUserKey.objects.all().order_by("user_key")
        if "task" in form.fields and not form.fields["task"].queryset.exists():
            form.fields["task"].queryset = tblTask.objects.all().order_by("task")
        # -------------------------------------------------------------------------

    logs = vewTaskLogAdmin.objects.order_by("-action_timestamp")[:50]
    return render(request, "dashboard_admin.html", {"form": form, "logs": logs})


# --------------------------
# AJAX search for Select2
# --------------------------
@login_required
def task_search(request):
    """
        Select2 AJAX for tasks.
        For STAFF, exclude the user's most recently selected task (by activity_timestamp).
        For others, return all tasks.
    """
    q = (request.GET.get("q") or "").strip()

    # Base queryset
    qs = tblTask.objects.all()

    # If staff, compute last selected task and exclude it
    role_key = get_role_key(request)
    auth_user = getattr(request, 'auth_user', None)

    if role_key == "STAFF" and auth_user:
        last_log = (
            tblTaskLogStaff.objects
            .filter(fk_userID=auth_user.fk_userID)
            .order_by('-activity_timestamp')
            .select_related('fk_taskID')
            .first()
        )
        if last_log and last_log.fk_taskID_id:
            qs = qs.exclude(id=last_log.fk_taskID_id)

    if q:
        qs = qs.filter(Q(task__icontains=q) | Q(task_key__icontains=q))

    qs = qs.order_by("task")[:20]
    return JsonResponse({
        "results": [{"id": t.id, "text": f"{t.task} ({t.task_key})"} for t in qs]
    })


@login_required
def admin_userkey_search(request):
    """
    Select2 AJAX for Admin employee dropdown using vewUserKey.
    Shows plain UserKey values.
    Returns: {"results":[{"id":"<user_key>","text":"<user_key>"}, ...]}
    """
    q = (request.GET.get("q") or "").strip()
    qs = vewUserKey.objects.all()
    if q:
        qs = qs.filter(user_key__icontains=q)

    qs = qs.order_by("user_key")[:20]
    return JsonResponse({
        "results": [{"id": row.user_key, "text": row.user_key} for row in qs]
    })


# --------------------------
# Misc
# --------------------------
@login_required
def task_list(request):
    user = getattr(request, "auth_user", None)
    if not user:
        return redirect("timesheet:welcome")
    tasklogs = vewTaskLogStaff.objects.filter(fk_userID=user.fk_userID.id).order_by(
        "-activity_timestamp"
    )
    return render(request, "task_list.html", {"tasklogs": tasklogs})


@login_required
def timesheet_report(request):
    return render(request, "TimesheetApp/timesheet_report.html")


@login_required
def get_transfer_views(request):
    views = vewTransferViewToGoogleSheet.objects.all()
    data = [{"view_name": v.view_name, "google_sheets_id": v.google_sheets_id} for v in views]
    return JsonResponse({"views": data})


@login_required
def export_to_gsheet(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    data = json.loads(request.body or "{}")
    view_name = data.get("view_name")
    google_sheets_id = data.get("google_sheets_id")
    if not view_name or not google_sheets_id:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    # Read SQL view rows
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM [{view_name}]")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=columns)

    # Push to Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("path/to/your/creds.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(google_sheets_id)
    try:
        worksheet = sheet.worksheet(view_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=view_name, rows="100", cols="20")

    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    return JsonResponse({"status": "success"})
