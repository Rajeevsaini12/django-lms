# Django-Crontab Setup Guide

## Overview
django-crontab has been successfully integrated into your Library Management System. This replaces the manual management command approach with automatic system-level cron job scheduling.

## What's Changed

### 1. **Settings Configuration** (LMS/settings.py)
- Added `django_crontab` to INSTALLED_APPS
- Configured CRONJOBS with cron job definitions

### 2. **New Cron Module** (library/cron.py)
Three cron job functions available:
- `send_daily_reminders()` - Runs daily at 9 AM
  - Sends due date reminders for books due within 1 day
  - Sends overdue notifications for unreturned books
  
- `send_weekly_summary()` - Optional, runs Monday at 10 AM
  - Generates weekly library statistics
  - Reports pending returns and active users
  
- `cleanup_old_records()` - Optional, runs monthly
  - Identifies books unreturned for 60+ days
  - Archives old transaction records

## Installation Instructions

### Step 1: Register Cron Jobs in System Crontab
Run this command to install django-crontab jobs into your system crontab:

```bash
cd /home/rajeevsaini12/django_project/LMS
python manage.py crontab add
```

**Expected output:**
```
Adding crontab entry: '0 9 * * * ... library.cron.send_daily_reminders'
```

### Step 2: Verify Installation
List all installed cron jobs:

```bash
python manage.py crontab show
```

### Step 3: View System Crontab
To see all your user cron jobs:

```bash
crontab -l
```

## Cron Job Details

### Primary Job: Daily Reminders (9 AM)
**Cron Format:** `0 9 * * *`
```
┌─────────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌─────────── day of month (1 - 31)
│ │ │ ┌───────── month (1 - 12)
│ │ │ │ ┌─────── day of week (0 - 6) [0 = Sunday]
│ │ │ │ │ 
0 9 * * * 
```

**What it does:**
1. Scans all unreturned books
2. Checks if due date is today or tomorrow
3. Sends reminder emails to students
4. Identifies overdue books and sends notifications
5. Logs results to `/var/log/django-cron.log`

### Log Output Location
django-crontab logs are stored at:
- **File:** `/var/log/django-cron.log`
- **View logs:** `tail -f /var/log/django-cron.log`

## Management Commands

### Add Cron Jobs
```bash
python manage.py crontab add
```

### Remove Cron Jobs
To remove all django-crontab jobs:
```bash
python manage.py crontab remove
```

### List Installed Jobs
```bash
python manage.py crontab show
```

### Run a Job Manually (for testing)
```bash
python manage.py crontab run library.cron.send_daily_reminders
```

## Configuration Examples

### Change Daily Reminder Time
Edit `LMS/settings.py` CRONJOBS:

**9 AM daily:**
```python
CRONJOBS = [
    ('0 9 * * *', 'library.cron.send_daily_reminders'),
]
```

**6 AM daily:**
```python
CRONJOBS = [
    ('0 6 * * *', 'library.cron.send_daily_reminders'),
]
```

**Every 6 hours (midnight, 6 AM, noon, 6 PM):**
```python
CRONJOBS = [
    ('0 */6 * * *', 'library.cron.send_daily_reminders'),
]
```

**Every 30 minutes:**
```python
CRONJOBS = [
    ('*/30 * * * *', 'library.cron.send_daily_reminders'),
]
```

**Monday at 10 AM:**
```python
CRONJOBS = [
    ('0 10 * * 1', 'library.cron.send_weekly_summary'),
]
```

After changing CRONJOBS:
1. Remove old jobs: `python manage.py crontab remove`
2. Add updated jobs: `python manage.py crontab add`

## Monitoring

### Check if Cron Job Ran
```bash
tail -20 /var/log/django-cron.log
```

### Monitor in Real-time
```bash
watch -n 5 'tail -20 /var/log/django-cron.log'
```

### System Crontab Log
System cron logs are typically in:
- `/var/log/syslog`
- `/var/log/cron` (on some Linux systems)

View relevant cron entries:
```bash
grep CRON /var/log/syslog | tail -20
```

## Email Configuration

The cron jobs use the email configuration from settings.py:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## Testing

### Test the Cron Function Directly
```bash
cd /home/rajeevsaini12/django_project/LMS
python manage.py shell

# In the shell:
>>> from library.cron import send_daily_reminders
>>> send_daily_reminders()
```

### Manual Cron Execution
```bash
python manage.py crontab run library.cron.send_daily_reminders
```

## Troubleshooting

### Cron Jobs Not Running
1. Check if jobs are installed: `python manage.py crontab show`
2. Verify Django settings are correct: `python manage.py check`
3. Check system logs: `tail -f /var/log/syslog`
4. Verify Python path and permissions

### Email Not Sending
1. Check email settings in config
2. Verify Gmail App Password is correct
3. Check logs: `/var/log/django-cron.log`

### Permission Issues
If you get permission denied errors:
```bash
sudo python manage.py crontab add
```

## Advantages Over Management Command

| Feature | Management Command | Django-Crontab |
|---------|-------------------|-----------------|
| Scheduling | Manual (Celery needed) | System crontab |
| Persistence | Only while running | Automatic restart |
| Setup | Complex | One command |
| Monitoring | Limited | Full syslog integration |
| Scalability | Limited | System-level |
| Dependencies | Needs Celery/RabbitMQ | Python + Django |

## Next Steps

1. **Install jobs:** `python manage.py crontab add`
2. **Verify:** `python manage.py crontab show`
3. **Monitor:** `tail -f /var/log/django-cron.log`
4. **Test:** Run manually to verify it works

## Emergency Removal

If you need to quickly stop all cron jobs:
```bash
python manage.py crontab remove
```

Then add them back:
```bash
python manage.py crontab add
```

---

**Last Updated:** March 12, 2026
**Django-Crontab Version:** 0.7.1+
**Django Version:** 6.0.3
