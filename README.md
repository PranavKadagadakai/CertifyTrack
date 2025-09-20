# CertifyTrack 🎓📄

CertifyTrack is a Django-based platform designed to streamline event management, certificate generation, and AICTE point tracking for students, clubs, and mentors.

## 🔍 Project Summary
Built a web-based portal for managing student activity points and generating verifiable certificates through mentor and club workflows. Features include role-based dashboards, certificate templates, PDF/image generation, AICTE tracking, and certificate verification.

## 📂 Features
- Student, Club, and Mentor roles with dedicated dashboards
- Event creation, participant management, and status updates
- Certificate template upload and automated generation (PDF/Image)
- AICTE activity point tracking and assignment
- Mentor-student assignment and verification workflow
- Secure login and profile management system

## 🚀 Tech Stack
- **Backend:** Django 5
- **Frontend:** HTML, CSS (Tailwind), JavaScript
- **Database:** PostgreSQL (or SQLite for development)
- **Tools:** Pillow, PyPDF2, ReportLab for certificate generation

## 📁 Directory Structure
```plaintext
CertifyTrack/
├── Cert/                  # Django app with models, views, forms, admin
├── CertifyTrack/          # Project config
├── templates/             # HTML templates for different roles and features
├── static/                # Tailwind CSS, custom JS, styles
├── media/                 # Uploaded certificate templates and generated certificates
├── requirements.txt       # Python dependencies
├── manage.py              # Django management script
```

## 🧪 Setup Instructions
1. Clone the repository:
```bash
git clone https://github.com/your-username/CertifyTrack.git
cd CertifyTrack
```
2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate
```
3. Install the dependencies:
```bash
pip install -r requirements.txt
```
4. Run the development server:
```bash
python manage.py migrate
python manage.py runserver
```

## 📌 Project Summary for Resume
Developed a Django-based certificate and event management platform with student activity tracking, certificate generation (PDF/image), and mentor-club workflows for AICTE compliance.
