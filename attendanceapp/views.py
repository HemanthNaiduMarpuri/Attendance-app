from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import AttendanceRecord, AttendanceSession, Holiday
from .forms import AttendanceMarkForm, HolidayMarkForm
from timetable.models import TimeTable
from datetime import date as today_date, datetime
from .services import sessions_for_students
from django.views.decorators.http import require_POST
from academics.models import Semester
import calendar
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login')
def student_timetable(request):
    student = request.user.user_profile
    selected_date = today_date.today()

    asked_date = request.GET.get('date')

    if asked_date:
        try:
            selected_date = datetime.strptime(asked_date, "%Y-%m-%d").date()
        except ValueError as e:
            return render(request, 'student/error.html', {'error':str(e)})

    try:
        sessions = sessions_for_students(student, selected_date)
    except ValueError as e:
        return render(request, 'student/error.html', {'error':str(e)})

    return render(request, 'student/student_timetable.html', {
        'sessions':sessions,
        'date':selected_date,
        'today_date':now().date()
    })

@login_required(login_url='/accounts/login')
@require_POST
def mark_attendance(request, timetable_id):
    student = request.user.user_profile
    date = today_date.today()
    timetable = get_object_or_404(TimeTable, id=timetable_id, section=student.section)
    form = AttendanceMarkForm(request.POST)
    if not form.is_valid():
        return redirect('timetable')
    status = form.cleaned_data['status']
    date = form.cleaned_data['date']

    session, _ = AttendanceSession.objects.get_or_create(
        section=student.section,
        time_table=timetable,
        date=date
    )

    AttendanceRecord.objects.update_or_create(
        student=student,
        attendance_session=session,
        status=status   
    )

    return redirect('timetable')

@login_required(login_url='/accounts/login')
@require_POST
def mark_holiday(request):
    student = request.user.user_profile
    section = student.section
    today = today_date.today()
    
    form = HolidayMarkForm(request.POST)
    if not form.is_valid():
        return redirect('timetable')
    date = form.cleaned_data['date']
    if date > today:
        return redirect('timetable')    
    if AttendanceRecord.objects.filter(student=student, attendance_session__date=date).exists():
        return redirect('timetable')
    
    if Holiday.objects.filter(section=section, date=date):
        return redirect('timetable')

    Holiday.objects.create(
        section=section,
        date=date,
        created_by=student
    )

    return redirect('timetable')

@login_required(login_url='/accounts/login')
def semester_calendar(request):
    semester_id = request.user.user_profile.section.id
    semester = get_object_or_404(Semester, id=semester_id)

    semester_months = semester.get_months()
    attendance_data = {}
    if request.user.is_authenticated:
        student = request.user.user_profile
        section = student.section
        attendances = AttendanceRecord.objects.filter(
            student = student,
            attendance_session__section = section
        )
        for att in attendances:
            key = (att.attendance_session.date.year, att.attendance_session.date.month, att.attendance_session.date.day)
            attendance_data[key] = att.status

    calendars = []
    for year, month in semester_months:
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]

        calendar_with_weekdates = []
        for week in cal:
            weeK_data = []
            for day in week:
                if day == 0:
                    weeK_data.append({'day':0, 'status':'', 'disabled':True})
                else:
                    date_obj = datetime(year, month, day).date()
                    in_semester = semester.semester_start_date <= date_obj <= semester.semester_end_date
                    status = attendance_data.get((year, month, day), '') if in_semester else ''

                    weeK_data.append({
                        'day':day,
                        'status':status,
                        'disabled':not in_semester,
                        'date':date_obj
                    })
            calendar_with_weekdates.append(weeK_data)
        calendars.append({
            'year':year,
            'month':month,
            'month_name':month_name,
            'calendar':calendar_with_weekdates
        })

    context = {
        'semester':semester,
        'calendars':calendars,
        'days_of_week':['Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    }

    return render(request, 'student/semcalendar.html', context)

@login_required(login_url='/accounts/login')
def attendance_percentage(request):
    context = {
        'total_days': 0,
        'present_days': 0,
        'absent_days': 0,
        'leave_days': 0,
        'percentage': 0,
        'error': None
    }
    if not request.user.is_authenticated:
        context['error'] = "Please Login to Continue"
        return render(request, 'student/percentage.html', context)
    try:
        student = request.user.user_profile
        section = student.section

        attendances = AttendanceRecord.objects.filter(
            student=student,
            attendance_session__section=section
        )

        total_days = attendances.filter(status__in=['Present','Absent','Leave']).count()
        present_days = attendances.filter(status__in=['Present']).count()
        absent_days = attendances.filter(status__in=['Absent']).count()
        leave_days = attendances.filter(status__in=['Leave']).count()
        percentage = (present_days/ total_days * 100) if total_days > 0 else 0

        context = {
            'total_days':total_days,
            'present_days':present_days,
            'absent_days':absent_days,
            'leave_days':leave_days,
            'percentage':round(percentage,2),
            'student':student,
            'error':None
        }

    except AttributeError:
        context['error'] = "User profile is not found"
    except Exception as e:
        context['error'] = f"An error occured:{str(e)}"

    return render(request, 'student/percentage.html', context)


