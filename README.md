📊 Attendance Management System (Django)

A modern, role-based Attendance Management System built with Django, featuring a clean UI, calendar-based attendance, role-based access control, and admin dashboards.

🚀 Features

👤 Authentication & Roles

User authentication (Login / Signup)

Role-based access:

Admin

Student

Secure access using custom mixins

Custom 403 Access Restricted UI

🗓️ Attendance Management

Daily timetable-based attendance

Calendar view for semester attendance

Mark Present / Absent / Holiday

Prevent future-date attendance

Attendance percentage calculation

📅 Calendar View

Monthly attendance calendar

Color-coded status:

🟢 Present

🔴 Absent

🟡 Holiday

🟣 Leave

Click any date → redirect to that day’s timetable

📈 Reports & Analytics

Overall attendance percentage

Subject-wise attendance report

Status indicators (Good / Warning / Critical)

🎨 UI & UX

Bootstrap 5 based modern UI

Responsive design (mobile-friendly)

Separate base templates:

base.html (main app)

base_auth.html (auth pages)

Clean forms with proper alignment

Custom error pages (403)

🛠️ Tech Stack

Backend: Django 5.x

Frontend: HTML, Bootstrap 5, CSS

Database: SQLite (default, easily switchable)

Authentication: Django Auth + django-allauth

Version Control: Git & GitHub

📂 Project Structure (Simplified)
attendance-app/
│
├── accounts/
│   ├── forms.py
│   ├── views.py
│   ├── mixins.py
│
├── academics/
│   ├── models.py
│   ├── views.py
│
├── attendance/
│   ├── views.py
│   ├── templates/
│
├── templates/
│   ├── base.html
│   ├── base_auth.html
│   ├── login.html
│   ├── signup.html
│   ├── 403.html
│
├── static/
├── media/
├── manage.py
├── requirements.txt
└── README.md

⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/your-username/Attendance-app.git
cd Attendance-app

2️⃣ Create Virtual Environment
python -m venv env
env\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment

Create a .env file (optional but recommended):

DEBUG=True
SECRET_KEY=your-secret-key

5️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create Superuser
python manage.py createsuperuser

7️⃣ Run Server
python manage.py runserver


Visit:

http://127.0.0.1:8000/

🔐 Email Configuration (Development)

To avoid signup errors during development:

ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = False


OR (to view emails in console):

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

🧪 Default Roles

Admin

Manage timetables

View all attendance

Access admin-only pages

Student

View timetable

Mark attendance

View attendance percentage & calendar

🚫 Access Control

Custom AdminRequiredMixin

Unauthorized access shows a custom 403 page

No raw Django error pages exposed to users


📌 Future Enhancements

Email / OTP verification

Export attendance reports (PDF / Excel)

Faculty role

Notifications & reminders

REST API integration

👨‍💻 Author

Hemanth Naidu
Backend Developer (Django)
📌 Focused on clean architecture & production-ready apps

📄 License

This project is for educational and learning purposes.
You are free to modify and use it.

