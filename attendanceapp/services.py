from datetime import date
from timetable.models import TimeTable
from .models import AttendanceRecord


def sessions_for_students(student, selected_date):
    section = student.section
    semester = section.semester

    if selected_date > date.today():
        raise ValueError("Cannot access future")
    
    if not (semester.semester_start_date <= selected_date <= semester.semester_end_date):
        raise ValueError("Cannot access Outside the semester dates.")
    
    day = selected_date.strftime("%A")

    timetable_entries = TimeTable.objects.filter(
        section=section,
        day=day
    ).order_by('period__period_number')

    sessions = []
    for entries in timetable_entries:
        record = AttendanceRecord.objects.filter(
            student=student, 
            attendance_session__time_table=entries,
            attendance_session__date=selected_date
            ).first()

        sessions.append({
            'subject':entries.subject,
            'span_count':entries.span_count,
            'session_type':entries.session_type,
            'period':entries.period.period_number,
            'timetable_id':entries.id,
            'attendance_status':record.status if record else None
        })
    return sessions
