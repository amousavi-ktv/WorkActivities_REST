
# views.py
from datetime import timedelta
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.shortcuts import redirect, render
from django.urls import path, include
from django.utils import timezone
from requests import get
from social_django.models import UserSocialAuth
from TimesheetApp.decorators import require_auth_user
from urllib.parse import urlencode
from django.utils import timezone
from TimesheetApp.models import  tblAuthUser, tblTaskLogStaff, tblTaskLogSupervisor, vewTaskLogStaff, vewTaskLogSupervisor
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig
from TimesheetApp.models import vewUserDetails
from TimesheetApp.forms_supervisor import TaskSelectionFormSupervisor
from TimesheetApp.tables_supervisor import TaskLogSupervisorTable
import datetime
from django.utils.timezone import localtime
from TimesheetApp.Forms.forms_staff import TaskSelectionFormStaff
from TimesheetApp.models import tblAppUser, tblTask  # Ensure these are imported
from TimesheetApp.tables_staff import TaskLogStaffTable
from django.db import IntegrityError
from TimesheetApp.models import tblTaskLogStaff
from django.utils import timezone
from TimesheetApp.models import tblTaskLogSupervisor
from django.utils import timezone

# for REST:
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    vewTaskLogAdmin, vewTaskLogAdminSerializer, vewTaskLogSupervisorSerializer, 
    vewTaskLogStaffSerializer, vewUserDetailsSerializer, vewActivitiesTimesheetFullRange_GSheet, vewTimesheetSerializer
)

def dashboard(request):
    auth_user = getattr(request, 'auth_user', None)
    if not auth_user:
        return HttpResponseForbidden("Unauthorized")

    if not request.user.is_authenticated:
        return redirect('/auth/login/google-oauth2/?prompt=select_account&hd=karbalatv.com')

    auth_user_id = auth_user.fk_userid.id
    # Load user details
    # user_details = vewUserDetails.objects.filter(email_address=request.user.username).first()

    try:
        # auth_user = tblAuthUser.objects.select_related('fk_userid__fk_roleid').get(email_address=request.user.username) - no need; defined in middleway.py
        
        # Get the user details (based on PID or ID, depending on your view design)
        user_details = vewUserDetails.objects.filter(id=auth_user_id).first()

    except tblAuthUser.DoesNotExist:
        logout(request)
        return HttpResponseForbidden("Unauthorized Access - Please contact admin.")

    role = getattr(auth_user.fk_userid.fk_roleid, 'role_key', '').upper()
    if not role:
        return HttpResponseForbidden("No role assigned")

    if role == "STAFF":
        form = TaskSelectionFormStaff(request.POST, user_id=auth_user_id)
        if request.method == 'POST':
            if form.is_valid():
                try:
                    selected_task = form.cleaned_data.get('task')
                    work_activities = form.cleaned_data.get('work_activities', '')
                    remarks = form.cleaned_data.get('remarks', '')

                    # Ensure all required fields are present
                    if not selected_task:
                        form.add_error(None, "Task is required.")
                    else:
                        tblTaskLogStaff.objects.create(
                            fk_userid=auth_user.fk_userid,
                            fk_taskid=selected_task,
                            activity_timestamp=timezone.now(),
                            work_activities=work_activities,
                            remarks=remarks
                        )
                        return redirect('/dashboard/')

                except Exception as e:
                    form.add_error(None, f"Error: {str(e)}")

            # Load table data
            logs = vewTaskLogStaff.objects.filter(fk_userid=auth_user_id).order_by('-activity_timestamp')
            table = TaskLogStaffTable(logs)
            RequestConfig(request).configure(table)

            return render(request, 'dashboard_staff.html', {
                'form': form,
                'table': table,
                'user_key': user_details.user_key if user_details else 'Staff'
            })
        else:
            form = TaskSelectionFormStaff()

        logs = vewTaskLogStaff.objects.filter(fk_userid=auth_user_id).order_by('-activity_timestamp')
        table = TaskLogStaffTable(logs)
        RequestConfig(request).configure(table)

        form = TaskSelectionFormStaff(user_id=auth_user_id)
        return render(request, 'dashboard_staff.html', {
            'form': form,
            'table': TaskLogStaffTable(logs),
            'user_key': user_details.user_key if user_details else 'User'
        })

    if role == "SUPERVISOR":
        form = TaskSelectionFormSupervisor(request.POST or None, user_id=auth_user_id)
        if request.method == 'POST':
            if form.is_valid():
                try:
                    selected_task = form.cleaned_data.get('task')
                    selected_date = form.cleaned_data.get('date')
                    selected_time = form.cleaned_data.get('time')
                    work_activities = form.cleaned_data.get('work_activities', '')
                    remarks = form.cleaned_data.get('remarks', '')

                    # Ensure all required fields are present
                    if not selected_task or not selected_date or not selected_time:
                        form.add_error(None, "Task, Date, and Time are required.")
                    else:
                        tblTaskLogSupervisor.objects.create(
                            fk_userid=auth_user.fk_userid,
                            fk_taskid=selected_task,
                            date=selected_date,
                            time=selected_time,
                            action_timestamp=timezone.now(),
                            work_activities=work_activities,
                            remarks=remarks
                        )
                        return redirect('/dashboard/')

                except Exception as e:
                    form.add_error(None, f"Error: {str(e)}")

            # Load table data
            logs = vewTaskLogSupervisor.objects.filter(fk_userid=auth_user_id).order_by('-date')
            table = TaskLogSupervisorTable(logs)
            RequestConfig(request).configure(table)

            return render(request, 'dashboard_supervisor.html', {
                'form': form,
                'table': table,
                'user_key': user_details.user_key if user_details else 'Supervisor'
            })
        else:
            form = TaskSelectionFormSupervisor()

        logs = vewTaskLogSupervisor.objects.filter(fk_userid=auth_user_id).order_by('-date')
        table = TaskLogSupervisorTable(logs)
        RequestConfig(request).configure(table)

        return render(request, 'dashboard_supervisor.html', {
            'form': form,
            'table': table,
            'user_key': user_details.user_key if user_details else 'Supervisor'
        })

    # xxxxx
    else:
        return HttpResponseForbidden("Unknown role")

@login_required
def dashboard_supervisor(request):
    auth_user = getattr(request, 'auth_user', None)
    if not auth_user or auth_user.fk_userid.fk_roleid.role_key != 'SUPERVISOR':
        return redirect('dashboard')
    auth_user_id = auth_user.fk_userid.id
    if request.method == 'POST':
        form = TaskSelectionFormSupervisor(request.POST)
        if form.is_valid():
            vewTaskLogSupervisor.objects.create(
                fk_userid=auth_user_id,
                fk_taskid=form.cleaned_data['task'].id,
                date=form.cleaned_data['date'],
                time=form.cleaned_data['time'],
                actiontimestamp=timezone.now()
            )
            return redirect('dashboard')
    else:
        form = TaskSelectionFormSupervisor()

    logs = vewTaskLogSupervisor.objects.filter(fk_userid=auth_user_id).order_by('-date')
    table = TaskLogSupervisorTable(logs)

    return render(request, "dashboard_supervisor.html", {"form": form, "table": table, "user": auth_user.fk_userid})

def task_list(request):
    user = getattr(request, 'auth_user', None)
    if not user:
        return redirect('login')

    tasklogs = vewTaskLogStaff.objects.filter(fk_userid=user.fk_userid.id).order_by('-activity_timestamp')
    return render(request, 'task_list.html', {'tasklogs': tasklogs})

def admin_view(request):
    user = request.auth_user
    # Your logic here

def welcome(request):
    if not hasattr(request, 'auth_user') or request.auth_user is None:
        return redirect('/auth/login/google-oauth2/?prompt=select_account&hd=karbalatv.com')
    return redirect('dashboard')

def logout_view(request):
    logout(request)
    return redirect('login')  # or Google logout

def full_logout(request):
    logout(request)
    request.session.flush()
    return redirect('/auth/login/google-oauth2/?prompt=select_account&hd=karbalatv.com')

class ForceGoogleAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            try:
                social = UserSocialAuth.objects.get(user=user, provider='google-oauth2')
                access_token = social.extra_data.get('access_token')
                if not access_token:
                    return redirect('login')

                # Check token validity directly with Google
                response = get('https://www.googleapis.com/oauth2/v1/tokeninfo', params={'access_token': access_token})
                if response.status_code != 200:
                    # Token is no longer valid (maybe user logged out of Google)
                    return redirect('login')
            except UserSocialAuth.DoesNotExist:
                return redirect('login')

        return self.get_response(request)

@login_required
def task_selection_staff(request):
    auth_user = getattr(request, 'auth_user', None)
    if not auth_user or not auth_user.fk_userid.fk_roleid.role.lower() == 'staff':
        return redirect('dashboard')
    auth_user_id = auth_user.fk_userid.id
    if request.method == 'POST':
        # form = TaskSelectionFormStaff(request.POST)
        form = TaskSelectionFormStaff(request.POST, user_id=auth_user_id)
        if form.is_valid():
            selected_task = form.cleaned_data['task']
            vewTaskLogStaff.objects.create(
                fk_userid=auth_user_id,  # use fk_userid
                fk_taskid=selected_task.id,
                activity_timestamp=timezone.now()
            )
            return redirect('dashboard')
    else:
        # form = TaskSelectionFormStaff()
        form = TaskSelectionFormStaff(user_id=auth_user_id)

    return render(request, 'staff_task_selection.html', {'form': form})

class vewTaskLogAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = vewTaskLogAdmin.objects.all()
    serializer_class = vewTaskLogAdminSerializer
    permission_classes = [IsAuthenticated]

class vewTaskLogSupervisorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = vewTaskLogSupervisor.objects.all()
    serializer_class = vewTaskLogSupervisorSerializer
    permission_classes = [IsAuthenticated]

class vewTaskLogStaffViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = vewTaskLogStaff.objects.all()
    serializer_class = vewTaskLogStaffSerializer
    permission_classes = [IsAuthenticated]

class vewUserDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = vewUserDetails.objects.all()
    serializer_class = vewUserDetailsSerializer
    permission_classes = [IsAuthenticated]

def timesheet_report(request):
    return render(request, 'TimesheetApp/timesheet_report.html')

class vewTimesheetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = vewActivitiesTimesheetFullRange_GSheet.objects.all()
    serializer_class = vewTimesheetSerializer
    permission_classes = [IsAuthenticated]
    
    # Manual filtering instead of using django-filter
    def get_queryset(self):
        queryset = vewActivitiesTimesheetFullRange_GSheet.objects.all()
        
        # Get query parameters
        employee_id = self.request.query_params.get('employee_id', None)
        date_from = self.request.query_params.get('activity_date__gte', None)
        date_to = self.request.query_params.get('activity_date__lte', None)
        
        # Apply filters if parameters exist
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        if date_from:
            queryset = queryset.filter(activity_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(activity_date__lte=date_to)
            
        return queryset
