# Quick Reference: Django-Crontab Setup

## ✅ Already Done
- [x] django-crontab installed
- [x] Added to INSTALLED_APPS in settings.py
- [x] CRONJOBS configured (daily at 9 AM)
- [x] Created library/cron.py with job functions
- [x] Three cron jobs available

## 🚀 Next: Register Cron Jobs (One-Time Setup)

### Run this command:
```bash
cd /home/rajeevsaini12/django_project/LMS
python manage.py crontab add
```

### Expected output:
```
Adding crontab entry: '0 9 * * * /home/rajeevsaini12/django_project/venv/bin/python ... send_daily_reminders'
```

## ✨ Verify Installation

```bash
# View installed jobs
python manage.py crontab show

# View system crontab
crontab -l

# Check logs
tail -f /var/log/django-cron.log
```

## 📋 Current Configuration

**Daily Reminders Job:**
- **When:** Every day at 9:00 AM
- **What:** Sends due date and overdue notifications
- **Log:** `/var/log/django-cron.log`
- **Cron Format:** `0 9 * * *`

## 🧪 Test It Now

```bash
# Test manually (for immediate verification)
python manage.py crontab run library.cron.send_daily_reminders

# Or from shell:
python manage.py shell
>>> from library.cron import send_daily_reminders
>>> send_daily_reminders()
```

## 🔧 Common Tasks

| Task | Command |
|------|---------|
| Add jobs | `python manage.py crontab add` |
| Remove jobs | `python manage.py crontab remove` |
| List jobs | `python manage.py crontab show` |
| View logs | `tail -f /var/log/django-cron.log` |
| Test job | `python manage.py crontab run library.cron.send_daily_reminders` |

## 📊 Available Cron Functions

### 1. send_daily_reminders() ⭐ Primary
- Sends reminders for books due tomorrow
- Sends notifications for overdue books
- **Schedule:** 0 9 * * * (9 AM daily)

### 2. send_weekly_summary()
- Weekly library statistics
- **Schedule:** 0 10 * * 1 (Monday 10 AM)
- **Status:** Configured but disabled (add to CRONJOBS to enable)

### 3. cleanup_old_records()
- Archives old transactions
- **Schedule:** 0 2 1 * * (1st of month at 2 AM)
- **Status:** Configured but disabled

## ⏰ Change Reminder Time

Edit `LMS/settings.py`, find CRONJOBS section:

```python
# Default (9 AM)
CRONJOBS = [
    ('0 9 * * *', 'library.cron.send_daily_reminders'),
]

# Change to 6 AM
CRONJOBS = [
    ('0 6 * * *', 'library.cron.send_daily_reminders'),
]
```

Then:
```bash
python manage.py crontab remove
python manage.py crontab add
```

## 📧 Email Requirements

Emails will be sent using configured settings:
- **From:** 0112it201031@gmail.com
- **To:** Student email addresses from DB
- **Subject:** Due date/overdue reminders
- **Status:** ✅ Configured

## ❌ Troubleshooting

**Cron not running?**
1. Check: `python manage.py crontab show`
2. Verify: `crontab -l`
3. Debug: `tail -f /var/log/django-cron.log`

**Emails not sending?**
1. Verify email config in settings.py
2. Test manually: `python manage.py shell > from library.cron import send_daily_reminders > send_daily_reminders()`

**Permission denied?**
```bash
sudo python manage.py crontab add
```

---

**Ready?** → Run: `python manage.py crontab add` ✅
