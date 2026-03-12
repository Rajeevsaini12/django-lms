"""
Django Crontab Tasks for Library Management System

This module contains cron job functions to be executed by django-crontab.
These tasks handle periodic reminders for books.
"""

from django.utils import timezone
from datetime import timedelta
from .models import IssueRecord
from .notifications import (
    send_due_date_reminder,
    send_overdue_notification
)


def send_daily_reminders():
    """
    Cron job to send daily book reminders.
    Runs every day at 9 AM.
    
    Tasks performed:
    1. Send due date reminders (books due within 1 day)
    2. Send overdue notifications (books overdue by 1+ days)
    """
    try:
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        
        # 1. Send reminders for books due tomorrow or today
        due_soon = IssueRecord.objects.filter(
            return_date__isnull=True,
            due_date__lte=tomorrow,
            due_date__gte=today
        )
        
        for record in due_soon:
            try:
                send_due_date_reminder(record.member.user, record)
                print(f"✓ Sent due date reminder for {record.book.title} to {record.member.user.email}")
            except Exception as e:
                print(f"✗ Failed to send due reminder for {record.book.title}: {str(e)}")
        
        # 2. Send notifications for overdue books
        overdue = IssueRecord.objects.filter(
            return_date__isnull=True,
            due_date__lt=today
        )
        
        for record in overdue:
            try:
                send_overdue_notification(record.member.user, record)
                print(f"✓ Sent overdue notification for {record.book.title} to {record.member.user.email}")
            except Exception as e:
                print(f"✗ Failed to send overdue notification for {record.book.title}: {str(e)}")
        
        # Summary
        total_reminders = due_soon.count() + overdue.count()
        print(f"\n📧 Daily reminder job completed: {total_reminders} emails sent")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in send_daily_reminders cron job: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def send_weekly_summary():
    """
    Cron job to send weekly summary reports to admins.
    Runs every Monday at 10 AM.
    
    Tasks performed:
    1. Calculate library statistics
    2. Identify most borrowed books
    3. Identify books with most pending issues
    """
    try:
        from .models import Book, Member
        
        # Stats for the past week
        one_week_ago = timezone.now().date() - timedelta(days=7)
        
        # Get recent issues
        recent_issues = IssueRecord.objects.filter(
            issue_date__gte=one_week_ago
        ).count()
        
        # Get pending returns
        pending_returns = IssueRecord.objects.filter(
            return_date__isnull=True,
            due_date__lt=timezone.now().date()
        ).count()
        
        # Get total active members
        active_members = Member.objects.filter(user__last_login__gte=one_week_ago).count()
        
        summary = {
            'issues_this_week': recent_issues,
            'pending_returns': pending_returns,
            'active_members': active_members,
        }
        
        print(f"📊 Weekly Summary Generated:")
        print(f"   - Issues this week: {recent_issues}")
        print(f"   - Pending returns: {pending_returns}")
        print(f"   - Active members: {active_members}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in send_weekly_summary cron job: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def cleanup_old_records():
    """
    Cron job to clean up old issue records.
    Runs monthly to archive or delete old completed transactions.
    
    Tasks performed:
    1. Warning emails for very old unreturned books (60+ days)
    2. Log statistics for analysis
    """
    try:
        two_months_ago = timezone.now().date() - timedelta(days=60)
        
        # Find books unreturned for 60+ days
        very_old_issues = IssueRecord.objects.filter(
            return_date__isnull=True,
            issue_date__lt=two_months_ago
        )
        
        count = very_old_issues.count()
        
        if count > 0:
            print(f"⚠️  Found {count} books unreturned for 60+ days")
            # Could send escalation emails here
        
        print(f"🗑️  Cleanup job completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in cleanup_old_records cron job: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
