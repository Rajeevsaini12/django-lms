from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import IssueRecord
from .notifications import (
    send_login_notification,
    send_book_issue_notification,
    send_book_return_notification,
)


@receiver(user_logged_in)
def notify_on_login(sender, request, user, **kwargs):
    """
    Signal handler for user login notifications
    Sends an email when a user logs in
    """
    print(f"User {user.username} logged in - sending notification")
    send_login_notification(user)


@receiver(post_save, sender=IssueRecord)
def notify_on_book_issue(sender, instance, created, **kwargs):
    """
    Signal handler for book issue notifications
    Sends an email when a book is issued to a student
    """
    if created:
        print(f"Book {instance.book.title} issued to {instance.member.user.username} - sending notification")
        send_book_issue_notification(instance)


@receiver(post_save, sender=IssueRecord)
def notify_on_book_return(sender, instance, created, update_fields, **kwargs):
    """
    Signal handler for book return notifications
    Sends an email when a book is returned
    """
    if not created and instance.return_date:
        # Check if return_date was just set (by checking if it's in update_fields or if it exists)
        # We need to verify this is actually a return (return_date is set)
        # To avoid sending duplicate emails, we check if this is a new return
        if update_fields is None or 'return_date' in update_fields:
            print(f"Book {instance.book.title} returned by {instance.member.user.username} - sending notification")
            send_book_return_notification(instance)
