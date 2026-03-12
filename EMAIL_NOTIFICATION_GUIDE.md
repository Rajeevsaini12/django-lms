# Email Notification System - Implementation Guide

## Overview
This document describes the email notification system implemented for the Library Management System (LMS). The system automatically sends email notifications to students for various events:

1. **Login Notification** - Sent when a student logs in
2. **Book Issue Notification** - Sent when a book is issued to a student
3. **Book Return Confirmation** - Sent when a student returns a book
4. **Due Date Reminder** - Sent 3 days before the book is due
5. **Overdue Notification** - Sent when a book becomes overdue

---

## Components

### 1. **Settings Configuration** (`LMS/settings.py`)
Email backend configuration added to support email sending:

```python
# Console backend (development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production with Gmail:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'

EMAIL_FROM_USER = 'library@lms.com'
DEFAULT_FROM_EMAIL = 'library@lms.com'
```

### 2. **Notification Functions** (`library/notifications.py`)
Core module containing all email sending functions:

- `send_login_notification(user)` - Send login notification
- `send_book_issue_notification(issue_record)` - Send book issue confirmation
- `send_book_return_notification(issue_record)` - Send book return confirmation
- `send_due_date_reminder(issue_record)` - Send due date reminder
- `send_overdue_notification(issue_record)` - Send overdue notification

### 3. **Signal Handlers** (`library/signals.py`)
Django signals that automatically trigger notifications:

- `notify_on_login` - Triggers on user login
- `notify_on_book_issue` - Triggers when IssueRecord is created
- `notify_on_book_return` - Triggers when return_date is set

### 4. **App Configuration** (`library/apps.py`)
AppConfig with ready() method to register signal handlers

### 5. **Management Command** (`library/management/commands/send_book_reminders.py`)
Command to send periodic reminders:

```bash
# Send reminders for books due in 3 days (default)
python manage.py send_book_reminders

# Send reminders for books due in 5 days
python manage.py send_book_reminders --due-days 5
```

### 6. **Email Templates** (`library/templates/emails/`)
HTML email templates for all notification types:
- `base.html` - Base template structure
- `login_notification.html` - Login email template
- `book_issue.html` - Book issue email template
- `book_return.html` - Book return email template
- `due_reminder.html` - Due date reminder template
- `overdue_notice.html` - Overdue notification template

---

## Configuration

### Development Setup
For development, the console backend will print emails to the console. Edit `LMS/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FROM_USER = 'library@lms.com'
DEFAULT_FROM_EMAIL = 'library@lms.com'
```

### Gmail SMTP Configuration (Production)
For sending real emails via Gmail:

1. Generate an [App Password](https://myaccount.google.com/apppasswords) from your Gmail account
2. Update `LMS/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-specific-password'
```

### Other Email Providers
Update EMAIL_HOST and EMAIL_PORT for your email provider:
- **SendGrid**: `smtp.sendgrid.net:587`
- **AWS SES**: `email-smtp.region.amazonaws.com:587`
- **Mailgun**: `smtp.mailgun.org:587`

---

## Usage

### Automatic Notifications (via Django Signals)

#### 1. Login Notification
Automatically sent when a student logs in:
```
Triggered by: user_logged_in signal
```

#### 2. Book Issue Notification
Automatically sent when a book is issued:
```python
# In views.py or API endpoint
record = IssueRecord.objects.create(
    book=book,
    member=member,
    issue_date=timezone.now(),
    due_date=timezone.now() + timedelta(days=7)
)
# Email automatically sent via signal
```

#### 3. Book Return Notification
Automatically sent when a book is returned:
```python
# In views.py or API endpoint
record.return_date = timezone.now()
record.save()
# Email automatically sent via signal
```

### Manual Reminder Commands

#### Send Due Date Reminders
```bash
# Send reminders for books due in 3 days
python manage.py send_book_reminders

# Send reminders for books due in 5 days
python manage.py send_book_reminders --due-days 5
```

#### Send Overdue Notifications
```bash
# Included in the above command
python manage.py send_book_reminders
```

---

## Scheduling Reminders (Optional)

### Using Django-APScheduler
To schedule automatic reminders, install and configure django-apscheduler:

```bash
pip install django-apscheduler
```

Configure in `LMS/settings.py`:
```python
INSTALLED_APPS = [
    ...
    'django_apscheduler',
]
```

Create a scheduled task in a signals or apps.py:
```python
from django_apscheduler.admin import DjangoJobExecution
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

@scheduler.scheduled_job("cron", hour=9, minute=0, id="send_reminders")
def send_reminders():
    from django.core.management import call_command
    call_command('send_book_reminders')

if not scheduler.running:
    scheduler.start()
```

### Using Celery (Recommended for Production)
For production environments, use Celery for async task scheduling.

---

## Email Notifications Details

### 1. Login Notification
- **Trigger**: User login
- **Recipients**: Logged-in user
- **Content**:
  - Welcome message
  - Login details (username, email, time)
  - Security warning for unauthorized logins

### 2. Book Issue Notification
- **Trigger**: Book issued to student
- **Recipients**: Student receiving the book
- **Content**:
  - Book title, author, ISBN
  - Issue date
  - Due date (highlighted)
  - Fine warning (₹5/day)

### 3. Book Return Confirmation
- **Trigger**: Book returned by student
- **Recipients**: Student returning the book
- **Content**:
  - Book details
  - Issue and return dates
  - Late fee calculation (if any)
  - Confirmation message

### 4. Due Date Reminder
- **Trigger**: Manual (3 days before due date by default)
- **Recipients**: Students with books due
- **Content**:
  - Book details
  - Due date
  - Days remaining
  - Fine warning

### 5. Overdue Notification
- **Trigger**: Manual (books past due date)
- **Recipients**: Students with overdue books
- **Content**:
  - URGENT notice
  - Book details
  - Days overdue
  - Accumulated fine
  - Extension request information

---

## Testing

### Test Email Sending
Create a test script (`test_email.py`):

```python
from library.notifications import send_book_issue_notification
from library.models import IssueRecord

# Get any issue record
record = IssueRecord.objects.first()

# Send test notification
send_book_issue_notification(record)
```

Run with:
```bash
python manage.py shell
>>> exec(open('test_email.py').read())
```

---

## File Structure

```
library/
├── notifications.py           # Email sending functions
├── signals.py                # Signal handlers
├── apps.py                   # App configuration with signal registration
├── management/
│   └── commands/
│       └── send_book_reminders.py  # Management command
└── templates/
    └── emails/
        ├── base.html
        ├── login_notification.html
        ├── book_issue.html
        ├── book_return.html
        ├── due_reminder.html
        └── overdue_notice.html
```

---

## Troubleshooting

### Emails not being sent?
1. Check EMAIL_BACKEND setting in settings.py
2. Verify email configuration (SMTP host, port, credentials)
3. Check Django logs for errors
4. For console backend, ensure DEBUG=True

### Signals not triggering?
1. Verify signals.py is imported in apps.py ready() method
2. Check that LibraryConfig is in INSTALLED_APPS as 'library'
3. Restart Django development server

### Gmail SMTP issues?
1. Ensure "Less secure app access" is enabled OR use App Password
2. Check that 2FA is enabled on your Gmail account
3. Verify port 587 is not blocked by firewall

---

## Future Enhancements

1. **Email Template Customization**: Allow admins to customize email templates
2. **Notification Preferences**: Let students choose notification frequency
3. **SMS Notifications**: Add SMS reminders for urgent overdue notices
4. **Batch Processing**: Optimize bulk email sending for large student base
5. **Email Analytics**: Track email opens and clicks
6. **Multilingual Support**: Send emails in preferred language

---

## Important Notes

1. **User Email Required**: Ensure all users have valid email addresses in the User model
2. **MIME Types**: Emails are sent as HTML with plain text fallback
3. **Error Handling**: All email functions include try-except blocks and fail silently
4. **Performance**: Consider using async task queue (Celery) for production
5. **Privacy**: Store email logs securely and comply with privacy regulations

---

## Support

For issues or questions, refer to:
- Django Email Documentation: https://docs.djangoproject.com/en/stable/topics/email/
- Django Signals: https://docs.djangoproject.com/en/stable/topics/signals/
- REST Framework: https://www.django-rest-framework.org/
