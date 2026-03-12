from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
from library.models import IssueRecord
from library.notifications import send_due_date_reminder, send_overdue_notification


class Command(BaseCommand):
    help = 'Send email reminders for books due soon and overdue books'

    def add_arguments(self, parser):
        parser.add_argument(
            '--due-days',
            type=int,
            default=3,
            help='Days before due date to send reminder (default: 3)',
        )

    def handle(self, *args, **options):
        due_days = options['due_days']
        today = now().date()
        
        # Send reminders for books due in the next N days
        self.send_due_date_reminders(today, due_days)
        
        # Send notifications for overdue books
        self.send_overdue_notifications(today)

    def send_due_date_reminders(self, today, due_days):
        """
        Send reminders for books that are due in the next due_days days
        """
        reminder_date = today + timedelta(days=due_days)
        
        # Find books due on the reminder_date
        due_soon = IssueRecord.objects.filter(
            return_date__isnull=True,
            due_date=reminder_date
        )
        
        count = 0
        for record in due_soon:
            try:
                send_due_date_reminder(record)
                count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error sending reminder for {record.book.title} to {record.member.user.email}: {str(e)}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully sent {count} due date reminders for books due on {reminder_date}'
            )
        )

    def send_overdue_notifications(self, today):
        """
        Send notifications for all overdue books that haven't been returned
        """
        overdue_records = IssueRecord.objects.filter(
            return_date__isnull=True,
            due_date__lt=today
        )
        
        count = 0
        for record in overdue_records:
            try:
                send_overdue_notification(record)
                count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error sending overdue notification for {record.book.title} to {record.member.user.email}: {str(e)}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully sent {count} overdue notifications'
            )
        )
