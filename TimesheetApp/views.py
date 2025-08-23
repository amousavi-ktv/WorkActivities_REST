# TimesheetApp/views.py
import json
from datetime import datetime

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import connection, IntegrityError
from django.db.models import Q
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django_tables2 import RequestConfig

# Tables (django-tables2)
from TimesheetApp.tables_staff import TaskLogStaffTable
from TimesheetApp.tables_supervisor import TaskLogSupervisorTable
from TimesheetApp.tables_admin import TaskLogAdminTable

# Forms
from TimesheetApp.forms import (
    TaskSelectionFormStaff,
    TaskSelectionFormSupervisor,
    AdminTimesheetForm,
)

# Models
from TimesheetApp.models import (
    tblAuthUser,
    tblAppUser,
    tblTask,
    tblTaskLog,        # <-- your DB table for inserts (note: Tas, not Tasklog)
    vewTaskLog,       # SQL view for reading
    vewUserDetails,
    vewTransferViewToGoogleSheet,
    vewUserKey,
)

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
def get_role_key(request):
    """
    Prefer the role stored by the router in session; fall back to auth_user.
    Returns an uppercase string like 'STAFF', 'SUPERVISOR', 'ADMIN', or 'UNKNOWN'.
    """
    rk = request.session.get("role_key")
    if rk:
        return rk.upper()
    auth_user = getattr(request, "auth_user", None)
    if auth_user and getattr(auth_user.fk_userID.fk_roleID, "role_key", None):
        return (auth_user.fk_userID.fk_roleID.role_key or "").upper()
    return "UNKNOWN"


def admin_code_from_pid(pid: str, acting_as_admin: bool) -> str:
    """
    Build AdminID to store in tblTasLog.adminID:
      - Staff/Supervisor entries: keep PID as-is (e.g., 'P0123')
      - Admin entries: replace leading 'P' with 'A' (e.g., 'A0123')
    """
    if not pid:
        return ""
    if acting_as_admin:
        return ("A" + pid[1:]) if pid[:1].upper() == "P" else pid
    return pid


# -------------------------------------------------------------------
# Entry / Auth
# -------------------------------------------------------------------
@login_required
def welcome(request):
    if not hasattr(request, "auth_user") or request.auth_user is None:
        return redirect("/auth/login/google-oauth2/?prompt=select_account&hd=karbalatv.com")
    return redirect("timesheet:dashboard")


def logout_view(request):
    logout(request)
    return redirect("timesheet:welcome")


# -------------------------------------------------------------------
# Role Router
#   - STAFF       -> staff dashboard
#   - SUPERVISOR  -> supervisor dashboard
#   - ADMIN       -> supervisor dashboard by default (Actions ▾ can open admin)
# -------------------------------------------------------------------
@login_required
def dashboard(request):
    auth_user = getattr(request, "auth_user", None)
    if not auth_user:
        return HttpResponseForbidden("Unauthorized")

    auth_user_id = auth_user.fk_userID.id
    user_details = vewUserDetails.objects.filter(id=auth_user_id).first()
    role_key = getattr(auth_user.fk_userID.fk_roleID, "role_key", "").upper()

    # cache for later views/templates
    request.session["user_key"] = getattr(user_details, "user_key", "User")
    request.session["role_key"] = role_key

    if role_key == "STAFF":
        return redirect("timesheet:dashboard_staff")
    if role_key in ("SUPERVISOR", "ADMIN"):
        return redirect("timesheet:dashboard_supervisor")

    return HttpResponseForbidden("Unknown role")


# -------------------------------------------------------------------
# STAFF
#   - action_timestamp = now
#   - activity_timestamp = now
#   - adminID = PID (as-is)
# -------------------------------------------------------------------
@login_required
def dashboard_staff(request):
    if get_role_key(request) != "STAFF":
        return redirect("timesheet:dashboard")

    auth_user = getattr(request, "auth_user", None)
    if not auth_user:
        return HttpResponseForbidden("Unauthorized")

    app_user = auth_user.fk_userID
    auth_user_id = app_user.id
    current_pid = app_user.pid  # e.g. 'P1234'

    # Most recent activity to exclude from picker
    last_log = (
        tblTasLog.objects
        .filter(fk_userID=app_user)
        .order_by("-activity_timestamp")
        .only("fk_taskID_id")
        .first()
    )
    last_task_id = last_log.fk_taskID_id if last_log else None

    if request.method == "POST":
        form = TaskSelectionFormStaff(request.POST, user_id=auth_user_id)

        # Fallback queryset if JS/AJAX is off
        if "task" in form.fields and not form.fields["task"].queryset.exists():
            base = tblTask.objects.all()
            if last_task_id:
                base = base.exclude(id=last_task_id)
            form.fields["task"].queryset = base.order_by("task")

        if form.is_valid():
            now = timezone.now()
            try:
                tblTaskLog.objects.create(
                    fk_userID=app_user,
                    fk_taskID=form.cleaned_data["task"],
                    action_timestamp=now,
                    activity_timestamp=now,
                    work_activities=form.cleaned_data.get("work_activities", ""),
                    remarks=form.cleaned_data.get("remarks", ""),
                    adminID=admin_code_from_pid(current_pid, acting_as_admin=False),
                )
                return redirect("timesheet:dashboard_staff")
            except IntegrityError:
                form.add_error(None, "Duplicate entry: same task/time already exists for this person.")
            except Exception as e:
                form.add_error(None, f"Could not save entry: {e}")

    else:
        form = TaskSelectionFormStaff(user_id=auth_user_id)
        if "task" in form.fields and not form.fields["task"].queryset.exists():
            base = tblTask.objects.all()
            if last_task_id:
                base = base.exclude(id=last_task_id)
            form.fields["task"].queryset = base.order_by("task")

    # vewTaskLog exposes user_id; order by activity chronology
    logs_qs = vewTaskLog.objects.filter(user_id=auth_user_id).order_by("-activity_timestamp")
    table = TaskLogStaffTable(logs_qs)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)

    task_search_url = reverse("timesheet:task_search")
    return render(
        request,
        "dashboard_staff.html",
        {
            "form": form,
            "table": table,
            "user_key": request.session.get("user_key", "Staff"),
            "task_search_url": task_search_url,
        },
    )


# -------------------------------------------------------------------
# SUPERVISOR  (Admins are allowed to use this screen too)
#   - action_timestamp = now
#   - activity_timestamp = date + time
#   - adminID = PID (as-is)
# -------------------------------------------------------------------
@login_required
def dashboard_supervisor(request):
    role_key = get_role_key(request)
    # Allow both supervisor and admin to open this page
    if role_key not in ("SUPERVISOR", "ADMIN"):
        return redirect("timesheet:dashboard")

    auth_user = getattr(request, "auth_user", None)
    if not auth_user:
        return HttpResponseForbidden("Unauthorized")

    app_user = auth_user.fk_userID
    auth_user_id = app_user.id
    user_details = vewUserDetails.objects.filter(id=auth_user_id).first()

    if request.method == "POST":
        form = TaskSelectionFormSupervisor(request.POST, user_id=auth_user_id)
        if "task" in form.fields and not form.fields["task"].queryset.exists():
            form.fields["task"].queryset = tblTask.objects.all().order_by("task")

        if form.is_valid():
            task = form.cleaned_data["task"]
            d    = form.cleaned_data["date"]
            t    = form.cleaned_data["time"]
            at_ts = datetime.combine(d, t)
            now   = timezone.now()
            try:
                pid = getattr(app_user, "pid", "") or ""
                tblTaskLog.objects.create(
                    fk_userID=app_user,
                    fk_taskID=task,
                    activity_timestamp=at_ts,
                    action_timestamp=now,
                    work_activities=form.cleaned_data.get("work_activities", ""),
                    remarks=form.cleaned_data.get("remarks", ""),
                    adminID=pid,
                )
                return redirect("timesheet:dashboard_supervisor")
            except IntegrityError:
                form.add_error(None, "Duplicate entry: same person, task, date & time already exists.")
            except Exception as e:
                form.add_error(None, f"Could not save entry: {e}")

    else:
        form = TaskSelectionFormSupervisor(user_id=auth_user_id)
        if "task" in form.fields and not form.fields["task"].queryset.exists():
            form.fields["task"].queryset = tblTask.objects.all().order_by("task")

    logs_qs = vewTaskLog.objects.filter(user_id=auth_user_id).order_by("-activity_timestamp")
    table = TaskLogSupervisorTable(logs_qs)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)

    task_search_url = reverse("timesheet:task_search")

    return render(
        request,
        "dashboard_supervisor.html",
        {
            "form": form,
            "table": table,
            "user_key": (user_details.user_key if user_details else "Supervisor"),
            "task_search_url": task_search_url,
            "is_admin": (role_key == "ADMIN"),
            "admin_panel_url": reverse("timesheet:dashboard_admin"),
        },
    )


# -------------------------------------------------------------------
# ADMIN
#   - action_timestamp = now
#   - activity_timestamp = date + time
#   - adminID = PID with P→A
# -------------------------------------------------------------------
@login_required
def dashboard_admin(request):
    if get_role_key(request) != "ADMIN":
        return redirect("timesheet:dashboard")

    auth_user = getattr(request, "auth_user", None)
    if not auth_user:
        return HttpResponseForbidden("Unauthorized")

    admin_pid = auth_user.fk_userID.pid  # e.g. P0001
    admin_code = admin_code_from_pid(admin_pid, acting_as_admin=True)  # e.g. A0001

    if request.method == "POST":
        form = AdminTimesheetForm(request.POST)

        # Ensure the dropdowns are populated even when JS is off
        if "user_key" in form.fields and not form.fields["user_key"].queryset.exists():
            form.fields["user_key"].queryset = vewUserKey.objects.all().order_by("user_key")
        if "task" in form.fields and not form.fields["task"].queryset.exists():
            form.fields["task"].queryset = tblTask.objects.all().order_by("task")

        try:
            if form.is_valid():
                selected_user_key = form.cleaned_data["user_key"]
                # vewUserKey instance or plain string
                uk = selected_user_key.user_key if hasattr(selected_user_key, "user_key") else str(selected_user_key)

                target_user = tblAppUser.objects.filter(user_key=uk, is_active=True).first()
                if not target_user:
                    messages.error(request, "Selected employee is not active or not found.")
                else:
                    activity_dt = datetime.combine(form.cleaned_data["date"], form.cleaned_data["time"])
                    tblTaskLog.objects.create(
                        fk_userID=target_user,
                        fk_taskID=form.cleaned_data["task"],
                        action_timestamp=timezone.now(),
                        activity_timestamp=activity_dt,
                        work_activities=form.cleaned_data.get("work_activities", ""),
                        remarks=form.cleaned_data.get("remarks", ""),
                        adminID=admin_code,  # Axxxx indicates acting as admin
                    )
                    return redirect("timesheet:dashboard_admin")
            else:
                messages.error(request, "Please correct the highlighted fields.")
        except IntegrityError:
            messages.error(request, "Duplicate entry exists for this task and timestamp.")
        except Exception as e:
            messages.error(request, f"Could not save entry: {e}")

    else:
        form = AdminTimesheetForm()
        if "user_key" in form.fields and not form.fields["user_key"].queryset.exists():
            form.fields["user_key"].queryset = vewUserKey.objects.all().order_by("user_key")
        if "task" in form.fields and not form.fields["task"].queryset.exists():
            form.fields["task"].queryset = tblTask.objects.all().order_by("task")

    logs_qs = vewTaskLog.objects.order_by("-activity_timestamp")
    table = TaskLogAdminTable(logs_qs)
    RequestConfig(request, paginate={"per_page": 25}).configure(table)

    task_search_url = reverse("timesheet:task_search")
    admin_user_search_url = reverse("timesheet:admin_userkey_search")
    return render(
        request,
        "dashboard_admin.html",
        {
            "form": form,
            "table": table,
            "task_search_url": task_search_url,
            "admin_user_search_url": admin_user_search_url,
        },
    )


# -------------------------------------------------------------------
# AJAX for Select2
# -------------------------------------------------------------------
@login_required
def task_search(request):
    """
    Select2 AJAX for tasks.
    For STAFF, exclude the user's most recently selected task (by activity chronology).
    Return only the task text (no task key).
    """
    q = (request.GET.get("q") or "").strip()
    qs = tblTask.objects.all()

    role_key = get_role_key(request)
    auth_user = getattr(request, "auth_user", None)

    if role_key == "STAFF" and auth_user:
        last_log = (
            tblTasLog.objects
            .filter(fk_userID=auth_user.fk_userID)
            .order_by("-activity_timestamp")
            .select_related("fk_taskID")
            .first()
        )
        if last_log and last_log.fk_taskID_id:
            qs = qs.exclude(id=last_log.fk_taskID_id)

    if q:
        qs = qs.filter(Q(task__icontains=q) | Q(task_key__icontains=q))

    qs = qs.order_by("task")[:20]
    return JsonResponse({
        "results": [{"id": t.id, "text": t.task} for t in qs]  # show only task name
    })


@login_required
def admin_userkey_search(request):
    """
    Select2 AJAX for Admin employee dropdown; shows plain UserKey values.
    """
    q = (request.GET.get("q") or "").strip()
    qs = vewUserKey.objects.all()
    if q:
        qs = qs.filter(user_key__icontains=q)

    qs = qs.order_by("user_key")[:20]
    return JsonResponse({
        "results": [{"id": row.user_key, "text": row.user_key} for row in qs]
    })


# -------------------------------------------------------------------
# Misc
# -------------------------------------------------------------------
@login_required
def task_list(request):
    user = getattr(request, "auth_user", None)
    if not user:
        return redirect("timesheet:welcome")
    tasklogs = vewTaskLog.objects.filter(user_id=user.fk_userID.id).order_by("-activity_timestamp")
    return render(request, "task_list.html", {"tasklogs": tasklogs})


@login_required
def timesheet_report(request):
    return render(request, "TimesheetApp/timesheet_report.html")


# -------------------------------------------------------------------
# Admin: Google Sheets export
# -------------------------------------------------------------------
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
    creds = ServiceAccountCredentials.from_json_keyfile_name(str(settings.GOOGLE_CREDENTIALS_FILE), scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(google_sheets_id)
    try:
        worksheet = sheet.worksheet(view_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=view_name, rows="100", cols="20")

    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    return JsonResponse({"status": "success"})
