# Email Notification System - Quick Start Guide

## Installation Checklist

✓ **Email configuration added to settings.py**
  - Console backend for development
  - Ready for SMTP configuration in production

✓ **Core notification system implemented**
  - `library/notifications.py` - All email sending functions
  - `library/signals.py` - Django signal handlers
  - `library/apps.py` - Signal registration

✓ **Automatic notifications enabled**
  - Login notifications via Django signals
  - Book issue notifications on creation
  - Book return notifications on return

✓ **Periodic reminders available**
  - Management command: `send_book_reminders`
  - Due date reminders (3 days before)
  - Overdue notifications

✓ **Email templates created**
  - `library/templates/emails/` directory with all templates

---

## Get Started in 3 Steps

### Step 1: Verify Installation
```bash
cd /home/rajeevsaini12/django_project/LMS
python manage.py shell
>>> from library.notifications import send_login_notification
>>> print("✓ Notifications module imported successfully")
```

### Step 2: Test Email Sending
```bash
python manage.py shell
>>> exec(open('library/utils.py').read())
```

### Step 3: Enable Production Emails
Edit `LMS/settings.py` to configure your email provider.

---

## Email Types Implemented

| Notification Type | Trigger | Auto/Manual |
|---|---|---|
| Login | User logs in | Auto (Signal) |
| Book Issue | Book issued | Auto (Signal) |
| Book Return | Book returned | Auto (Signal) |
| Due Reminder | 3 days before due | Manual Command |
| Overdue Notice | Past due date | Manual Command |

---

## Running Periodic Reminders

### One-time execution:
```bash
python manage.py send_book_reminders
```

### Custom due days:
```bash
python manage.py send_book_reminders --due-days 5
```

### Schedule with cron (Linux/Mac):
```bash
# Edit crontab
crontab -e

# Add this line to send reminders daily at 9:00 AM
0 9 * * * cd /home/rajeevsaini12/django_project/LMS && python manage.py send_book_reminders
```

---

## Configuration Options

### Development (Console Backend)
```python
# In LMS/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FROM_USER = 'library@lms.com'
```

### Gmail
```python
# In LMS/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
EMAIL_FROM_USER = 'your-email@gmail.com'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

---

## Features

✓ **Automatic Notifications**
  - Sent immediately via Django signals
  - No manual intervention needed
  - Fail-safe with error handling

✓ **Rich HTML Emails**
  - Professional formatting
  - Responsive design
  - Text fallback for compatibility

✓ **Detailed Information**
  - Book details (title, author, ISBN)
  - Dates (issue, return, due)
  - Fine calculations
  - Late fee warnings

✓ **Management Command**
  - Configurable reminder timing
  - Batch processing for efficiency
  - Console output for monitoring

---

## Troubleshooting

**Issue**: Emails showing in console but not sending
- **Solution**: Update EMAIL_BACKEND in settings.py to use SMTP

**Issue**: "No module named 'library.signals'"
- **Solution**: Ensure signals.py imported in LibraryConfig.ready()

**Issue**: "User object has no attribute 'member'"
- **Solution**: Ensure Member object exists for the user

---

## View Files

Key files to review:
1. [signals.py](library/signals.py) - Signal handlers
2. [notifications.py](library/notifications.py) - Email functions
3. [send_book_reminders.py](library/management/commands/send_book_reminders.py) - Management command
4. [EMAIL_NOTIFICATION_GUIDE.md](EMAIL_NOTIFICATION_GUIDE.md) - Full documentation

---

## Next Steps

1. Update user email addresses in database
2. Configure SMTP settings for production
3. Schedule periodic reminders with cron/Celery
4. Test all notification types
5. Monitor email delivery and bounce rates

---

## Support Resources

- Django Email: https://docs.djangoproject.com/en/stable/topics/email/
- Django Signals: https://docs.djangoproject.com/en/stable/topics/signals/
- Gmail App Passwords: https://myaccount.google.com/apppasswords

---

## Implementation Summary

✅ **Email Configuration** - Added to settings.py
✅ **Notification System** - 5 notification types implemented
✅ **Signal Handlers** - Auto sends on login, issue, return
✅ **Management Command** - For periodic reminders
✅ **Email Templates** - Professional HTML templates
✅ **Testing Utilities** - Helper script for testing
✅ **Documentation** - Complete implementation guide
✅ **Error Handling** - Try-catch blocks in all functions

System is ready for use!
