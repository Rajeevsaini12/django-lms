# 📚 Library Management System (LMS)

A modern, full-featured Library Management System built with **Django** and **Bootstrap 5** for managing books, student members, and book issuance/return workflows.

---

## ✨ Features

### 📖 **Book Management**
- ✅ Add, edit, delete books with ISBN tracking
- ✅ Track total and available copies
- ✅ Store author, title, and publication details
- ✅ Search and filter books
- ✅ API endpoints for book management

### 👥 **User Management**
- ✅ Dual-role system: **Admin** and **Student**
- ✅ Student registration and login
- ✅ Role-based access control
- ✅ User profile management
- ✅ Forgot password with OTP verification
- ✅ Student listing with search functionality

### 📤 **Book Issuance & Return**
- ✅ Issue books to students
- ✅ Track issue and return dates
- ✅ Automatic due date calculation
- ✅ Multi-book issuance (up to 3 books at a time)
- ✅ Searchable student and book selection
- ✅ Return book with condition tracking
- ✅ Update due dates when needed

### ⏰ **Overdue Management**
- ✅ Automatic fine calculation (₹5/day)
- ✅ Overdue book tracking
- ✅ Late fee computation
- ✅ Overdue notifications
- ✅ Overdue book view for admins and students

### 📧 **Email Notifications**
- ✅ Book issue confirmation emails
- ✅ Book return reminders
- ✅ Overdue warnings
- ✅ New issue notifications to admin
- ✅ HTML email templates
- ✅ Automatic OTP-based password reset

### 📊 **Dashboard & Analytics**
- ✅ Admin dashboard with statistics
- ✅ Student dashboard with personal info
- ✅ Total books, available books, issued books count
- ✅ All issued books tracking with status
- ✅ Issue history for students
- ✅ Overdue books listing
- ✅ Clickable cards for detailed views

### 🤖 **Automated Tasks**
- ✅ Cron jobs for automated reminders
- ✅ Daily overdue notifications
- ✅ Periodic email reminders
- ✅ Background task scheduling

### 🔌 **API Endpoints**
- ✅ RESTful API with JWT authentication
- ✅ Book management endpoints
- ✅ Member management endpoints
- ✅ Issue record endpoints
- ✅ Complete CRUD operations

---

## 🛠️ **Technology Stack**

| Component | Technology |
|-----------|-----------|
| **Backend** | Django 6.0+ |
| **Frontend** | Bootstrap 5, HTML5, CSS3, JavaScript |
| **Database** | SQLite (default) / PostgreSQL (production) |
| **API** | Django REST Framework + JWT |
| **Email** | Django Mail with SMTP |
| **Task Scheduling** | Django-Crontab |
| **Authentication** | Django Auth + CustomMember Roles |
| **ORM** | Django ORM |

---

## 📋 **Requirements**

- Python 3.8+
- Django 6.0+
- pip (Python package manager)
- Virtual environment (recommended)

---

## 🚀 **Installation & Setup**

### **1. Clone Repository**
```bash
git clone <repository-url>
cd LMS
```

### **2. Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Apply Migrations**
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### **5. Create Superuser (Admin)**
```bash
python3 manage.py createsuperuser
# Follow the prompts to create admin account
```

### **6. Collect Static Files** (Production)
```bash
python3 manage.py collectstatic --noinput
```

### **7. Run Development Server**
```bash
python3 manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

---

## 📖 **Usage Guide**

### **Admin Access**
1. Navigate to `http://127.0.0.1:8000/login`
2. Login with admin credentials
3. Access **Admin Dashboard** to manage books and students
4. Features:
   - View all books, students, and issued books
   - Issue new books to students
   - Track overdue books
   - Update due dates
   - Delete books with confirmation

### **Student Access**
1. Navigate to `http://127.0.0.1:8000/register` to create account
2. Login at `http://127.0.0.1:8000/login`
3. Access **Student Dashboard** to:
   - View issued books
   - Check due dates and fine calculations
   - View book history
   - Check overdue books
   - Return books

### **Forgot Password**
1. Click **" Forgot Password?"** on login page
2. Enter email address
3. Receive OTP via email
4. Verify OTP and set new password

---

## 📂 **Project Structure**

```
LMS/
├── manage.py                      # Django management script
├── db.sqlite3                     # Database (development)
├── requirements.txt               # Python dependencies
├── README.md                      # This file
│
├── LMS/                           # Project settings
│   ├── settings.py               # Django configuration
│   ├── urls.py                   # Main URL router
│   ├── wsgi.py                   # WSGI configuration
│   └── asgi.py                   # ASGI configuration
│
├── library/                       # Main app
│   ├── models.py                 # Database models
│   ├── views.py                  # View functions
│   ├── forms.py                  # Django forms
│   ├── urls.py                   # App URL routes
│   ├── serializers.py            # DRF serializers
│   ├── permissions.py            # Custom permissions
│   ├── signals.py                # Django signals
│   ├── notifications.py          # Email templates & logic
│   ├── utils.py                  # Utility functions
│   ├── admin.py                  # Django admin config
│   ├── cron.py                   # Cron job definitions
│   │
│   ├── migrations/               # Database migrations
│   │   └── *.py
│   │
│   ├── management/               # Custom commands
│   │   └── commands/
│   │       └── send_book_reminders.py
│   │
│   ├── static/                   # Static files
│   │   ├── js/
│   │   │   └── auth.js
│   │   └── css/
│   │
│   └── templates/                # HTML templates
│       ├── base.html
│       ├── login.html
│       ├── register.html
│       ├── forgot_password.html
│       ├── emails/               # Email templates
│       │   ├── book_issue.html
│       │   ├── book_return.html
│       │   ├── overdue_notice.html
│       │   └── due_reminder.html
│       └── library/              # App templates
│           ├── admin_dashboard.html
│           ├── student_dashboard.html
│           ├── book_list.html
│           ├── issue_book.html
│           ├── return_book.html
│           ├── all_students.html
│           ├── all_issued_books.html
│           └── ...
```

---

## 🗄️ **Database Models**

### **Book Model**
```python
- title (CharField) - Book title
- author (CharField) - Author name
- isbn (CharField) - ISBN code
- total_copies (IntegerField) - Total copies in library
- available_copies (IntegerField) - Currently available copies
```

### **Member Model**
```python
- user (OneToOneField) - Django User
- role (CharField) - 'admin' or 'student'
- phone (CharField) - Phone number
```

### **IssueRecord Model**
```python
- book (ForeignKey) - Issued book
- member (ForeignKey) - Student who issued
- issue_date (DateField) - Date of issue
- due_date (DateField) - Return due date
- return_date (DateField/Nullable) - Actual return date
- fine (Property) - Calculated late fee (₹5/day)
- is_overdue (Property) - Check if overdue
```

---

## 🔌 **API Endpoints**

### **Authentication**
```
POST   /api/token/login/         - JWT Login
```

### **Books**
```
GET    /api/books/               - List all books
POST   /api/books/               - Create book
GET    /api/books/{id}/          - Get book details
PUT    /api/books/{id}/          - Update book
DELETE /api/books/{id}/          - Delete book
```

### **Members**
```
GET    /api/members/             - List all members
POST   /api/members/             - Create member
```

### **Issue Records**
```
GET    /api/issues/              - List all issues
POST   /api/issues/              - Create issue
GET    /api/issues/{id}/return/  - Return book
```

### **Dashboard**
```
GET    /api/dashboard/           - Dashboard statistics
GET    /api/student-dashboard/   - Student dashboard data
```

---

## 🔑 **Key URLs**

| URL | Purpose |
|-----|---------|
| `/` | Home page |
| `/login` | User login |
| `/register` | Student registration |
| `/forgot-password` | Password reset start |
| `/verify-forgot-password` | OTP verification |
| `/admin-dashboard` | Admin main dashboard |
| `/student-dashboard` | Student main dashboard |
| `/books` | View all books |
| `/issue-book` | Issue book to student |
| `/return-book` | Return a book |
| `/all-students` | View all students |
| `/all-issued-books` | View all issued books |
| `/admin/history` | Issue/return history |
| `/student/history` | Student's book history |

---

## ⚙️ **Configuration**

### **Email Setup** (in `settings.py`)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### **Cron Jobs** (in `settings.py`)
```python
CRONJOBS = [
    ('0 9 * * *', 'library.cron.send_due_reminders'),
    ('0 10 * * *', 'library.cron.send_overdue_reminders'),
]
```

### **Session Timeout**
- Default: 5 minutes inactivity timeout
- Configure in `settings.py`: `SESSION_COOKIE_AGE`

---

## 🧪 **Running Tests**

```bash
# Run all tests
python3 manage.py test

# Run specific app tests
python3 manage.py test library

# With verbose output
python3 manage.py test -v 2
```

---

## 🚨 **Troubleshooting**

### **Issue: "ModuleNotFoundError: No module named 'django'"**
```bash
# Solution: Activate virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt
```

### **Issue: "No such table" error**
```bash
# Solution: Run migrations
python3 manage.py migrate
```

### **Issue: Static files not loading**
```bash
# Solution: Collect static files
python3 manage.py collectstatic --noinput
```

### **Issue: Email not sending**
- Verify SMTP settings in `settings.py`
- Check Gmail app password (not regular password)
- Ensure "Less secure apps" access is enabled
- Check firewall/antivirus blocking SMTP

### **Issue: Cron jobs not running**
```bash
# Install cron service
python3 manage.py crontab add

# View installed cron jobs
python3 manage.py crontab show

# Remove cron jobs
python3 manage.py crontab remove
```

---

## 📊 **Admin Features**

- ✅ Superuser management
- ✅ Book CRUD operations
- ✅ Member management
- ✅ Issue record management
- ✅ View issued books
- ✅ Track overdue books
- ✅ Fine calculations
- ✅ User activity logs

---

## 🔒 **Security Features**

- ✅ CSRF protection
- ✅ SQL injection protection (ORM)
- ✅ Cross-site scripting (XSS) protection
- ✅ Session management with auto-logout
- ✅ Password hashing with bcrypt
- ✅ Role-based access control
- ✅ JWT token-based API authentication
- ✅ Form validation and sanitization

---

## 🎯 **Future Enhancements**

- [ ] Book categories and classification
- [ ] Book ratings and reviews
- [ ] Book reservation system
- [ ] SMS notifications
- [ ] Fine payment gateway integration
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Book scans and image uploads
- [ ] Barcode/QR code support
- [ ] Multi-language support

---

## 📞 **Support & Contribution**

For questions, bug reports, or contributions:
1. Open an issue on GitHub
2. Submit a pull request
3. Contact the development team

---

## 📄 **License**

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👨‍💻 **Developer**

Built with ❤️ for efficient library management.

---

## 📝 **Changelog**

### **v1.0 - Initial Release**
- ✅ User authentication (Admin/Student)
- ✅ Book management system
- ✅ Issue/return workflow
- ✅ Fine calculation
- ✅ Email notifications
- ✅ REST API
- ✅ Admin dashboard
- ✅ Student dashboard
- ✅ Forgot password with OTP
- ✅ Cron-based reminders
- ✅ Book history tracking

---

**Last Updated:** March 2026  
**Version:** 1.0  
**Status:** ✅ Production Ready
