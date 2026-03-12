"""
Email Notification Testing Utility
Usage: python manage.py shell < library/utils/email_test_helper.py
"""

from library.models import User, Member, Book, IssueRecord
from library.notifications import (
    send_login_notification,
    send_book_issue_notification,
    send_book_return_notification,
    send_due_date_reminder,
    send_overdue_notification,
)
from django.utils.timezone import now
from datetime import timedelta


def test_login_notification():
    """Test login notification"""
    print("\n=== Testing Login Notification ===")
    try:
        user = User.objects.first()
        if user:
            send_login_notification(user)
            print(f"✓ Login notification test sent to {user.email}")
        else:
            print("✗ No users found in the database")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_book_issue_notification():
    """Test book issue notification"""
    print("\n=== Testing Book Issue Notification ===")
    try:
        issue_record = IssueRecord.objects.filter(return_date__isnull=True).first()
        if issue_record:
            send_book_issue_notification(issue_record)
            print(f"✓ Book issue notification test sent to {issue_record.member.user.email}")
        else:
            print("✗ No incomplete issue records found in the database")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_book_return_notification():
    """Test book return notification"""
    print("\n=== Testing Book Return Notification ===")
    try:
        issue_record = IssueRecord.objects.filter(return_date__isnull=False).first()
        if issue_record:
            send_book_return_notification(issue_record)
            print(f"✓ Book return notification test sent to {issue_record.member.user.email}")
        else:
            print("✗ No returned issue records found in the database")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_due_date_reminder():
    """Test due date reminder"""
    print("\n=== Testing Due Date Reminder ===")
    try:
        issue_record = IssueRecord.objects.filter(return_date__isnull=True).first()
        if issue_record:
            send_due_date_reminder(issue_record)
            print(f"✓ Due date reminder test sent to {issue_record.member.user.email}")
        else:
            print("✗ No incomplete issue records found in the database")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_overdue_notification():
    """Test overdue notification"""
    print("\n=== Testing Overdue Notification ===")
    try:
        # Find an overdue record or use the first incomplete one for testing
        issue_record = IssueRecord.objects.filter(
            return_date__isnull=True,
            due_date__lt=now().date()
        ).first()
        
        if not issue_record:
            issue_record = IssueRecord.objects.filter(return_date__isnull=True).first()
        
        if issue_record:
            send_overdue_notification(issue_record)
            print(f"✓ Overdue notification test sent to {issue_record.member.user.email}")
        else:
            print("✗ No incomplete issue records found in the database")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def run_all_tests():
    """Run all email notification tests"""
    print("\n" + "="*50)
    print("Email Notification System - Test Suite")
    print("="*50)
    
    test_login_notification()
    test_book_issue_notification()
    test_book_return_notification()
    test_due_date_reminder()
    test_overdue_notification()
    
    print("\n" + "="*50)
    print("Test Suite Completed")
    print("="*50 + "\n")


# Run tests when imported
if __name__ == "__main__":
    run_all_tests()

# Also run automatically when loaded in shell
run_all_tests()
