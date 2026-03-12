from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import timedelta
from django.utils.timezone import now
from .models import IssueRecord


def send_login_notification(user):
    """
    Send login notification email to user
    """
    subject = 'Login Notification - Library Management System'
    
    html_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px;">
                <h2>Welcome to Library Management System!</h2>
                <p>Hello <strong>{user.first_name or user.username}</strong>,</p>
                <p>You have successfully logged in to your account.</p>
                <p><strong>Login Details:</strong></p>
                <ul>
                    <li>Username: {user.username}</li>
                    <li>Email: {user.email}</li>
                    <li>Login Time: {now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                </ul>
                <p>If this wasn't you, please contact the administrator immediately.</p>
                <hr>
                <p style="color: #666; font-size: 12px;">
                    This is an automated email. Please do not reply.
                </p>
            </div>
        </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_FROM_USER,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Login notification sent to {user.email}")
    except Exception as e:
        print(f"Error sending login notification: {str(e)}")


def send_book_issue_notification(issue_record):
    """
    Send book issue notification email to student
    """
    user = issue_record.member.user
    subject = f'Book Issue Confirmation - {issue_record.book.title}'
    
    html_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px;">
                <h2>Book Issue Confirmation</h2>
                <p>Hello <strong>{user.first_name or user.username}</strong>,</p>
                <p>You have successfully issued a book from the library.</p>
                <p><strong>Book Details:</strong></p>
                <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
                    <tr style="background-color: #e8f4f8;">
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>Book Title</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.book.title}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>Author</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.book.author}</td>
                    </tr>
                    <tr style="background-color: #e8f4f8;">
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>ISBN</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.book.isbn or 'N/A'}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>Issue Date</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.issue_date.strftime('%Y-%m-%d')}</td>
                    </tr>
                    <tr style="background-color: #fff3cd;">
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>Due Date</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>{issue_record.due_date.strftime('%Y-%m-%d')}</strong></td>
                    </tr>
                </table>
                <p style="color: #d9534f;"><strong>⚠️ Important:</strong> Please return the book on or before the due date to avoid late fees (₹5 per day).</p>
                <hr>
                <p style="color: #666; font-size: 12px;">
                    This is an automated email. Please do not reply.
                </p>
            </div>
        </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_FROM_USER,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Book issue notification sent to {user.email}")
    except Exception as e:
        print(f"Error sending book issue notification: {str(e)}")


def send_book_return_notification(issue_record):
    """
    Send book return confirmation email to student
    Returns True if successful, False otherwise
    """
    try:
        user = issue_record.member.user
        subject = f'Book Return Confirmation - {issue_record.book.title}'
        
        print(f"\n{'='*50}")
        print(f"STARTING: Send Book Return Email")
        print(f"{'='*50}")
        print(f"User: {user.username}")
        print(f"Email: {user.email}")
        print(f"Book: {issue_record.book.title}")
        print(f"Return Date: {issue_record.return_date}")
        print(f"Due Date: {issue_record.due_date}")
        
        # Calculate fine if any
        fine = 0
        if issue_record.return_date and issue_record.due_date:
            if issue_record.return_date.date() > issue_record.due_date:
                late_days = (issue_record.return_date.date() - issue_record.due_date).days
                fine = late_days * 5
                print(f"Fine Calculated: ₹{fine} ({late_days} days × ₹5)")
        
        fine_message = ""
        if fine > 0:
            fine_message = f"""
            <tr style="background-color: #f8d7da;">
                <td style="border: 1px solid #ddd; padding: 10px;"><strong>Late Fee</strong></td>
                <td style="border: 1px solid #ddd; padding: 10px; color: #d9534f;">₹{fine}</td>
            </tr>
            """
        
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px;">
                    <h2>Book Return Confirmation</h2>
                    <p>Hello <strong>{user.first_name or user.username}</strong>,</p>
                    <p>Thank you for returning the book to the library.</p>
                    <p><strong>Return Details:</strong></p>
                    <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
                        <tr style="background-color: #e8f4f8;">
                            <td style="border: 1px solid #ddd; padding: 10px;"><strong>Book Title</strong></td>
                            <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.book.title}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #ddd; padding: 10px;"><strong>Author</strong></td>
                            <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.book.author}</td>
                        </tr>
                        <tr style="background-color: #e8f4f8;">
                            <td style="border: 1px solid #ddd; padding: 10px;"><strong>Issue Date</strong></td>
                            <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.issue_date.strftime('%Y-%m-%d')}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #ddd; padding: 10px;"><strong>Due Date</strong></td>
                            <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.due_date.strftime('%Y-%m-%d')}</td>
                        </tr>
                        <tr style="background-color: #e8f4f8;">
                            <td style="border: 1px solid #ddd; padding: 10px;"><strong>Return Date</strong></td>
                            <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.return_date.strftime('%Y-%m-%d')}</td>
                        </tr>
                        {fine_message}
                    </table>
                    <p style="color: #28a745;"><strong>✓ Book return recorded successfully.</strong></p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">
                        This is an automated email. Please do not reply.
                    </p>
                </div>
            </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        
        # Log email configuration
        print(f"Email Backend: {settings.EMAIL_BACKEND}")
        print(f"Email Host: {settings.EMAIL_HOST}")
        print(f"Email Port: {settings.EMAIL_PORT}")
        print(f"Email Use TLS: {settings.EMAIL_USE_TLS}")
        print(f"From: {settings.DEFAULT_FROM_EMAIL}")
        print(f"To: {user.email}")
        print(f"Subject: {subject}")
        
        # Send email
        print(f"\nAttempting to send email...")
        num_sent = send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"✅ SUCCESS: {num_sent} email(s) sent to {user.email}")
        print(f"{'='*50}\n")
        return True
        
    except Exception as e:
        print(f"\n{'='*50}")
        print(f"❌ ERROR: Failed to send book return notification")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"{'='*50}\n")
        return False


def send_due_date_update_notification(issue_record, old_due_date, new_due_date, reason=''):
    """
    Send email notification when due date is updated by admin
    Returns True if successful, False otherwise
    """
    try:
        user = issue_record.member.user
        subject = f'Due Date Extended - {issue_record.book.title}'
        
        print(f"\n{'='*50}")
        print(f"STARTING: Send Due Date Update Email")
        print(f"{'='*50}")
        print(f"User: {user.username}")
        print(f"Email: {user.email}")
        print(f"Book: {issue_record.book.title}")
        print(f"Old Due Date: {old_due_date}")
        print(f"New Due Date: {new_due_date}")
        
        reason_section = ""
        if reason:
            reason_section = f"""
            <tr>
                <td style="border: 1px solid #ddd; padding: 10px;"><strong>Reason for Extension</strong></td>
                <td style="border: 1px solid #ddd; padding: 10px;">{reason}</td>
            </tr>
            """
        
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px;">
                    <h2>Due Date Extended!</h2>
                    <p>Hello <strong>{user.first_name or user.username}</strong>,</p>
                    <p>The due date for your borrowed book has been extended.</p>
                    <p><strong>Updated Details:</strong></p>
                    <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
                        <tr style="background-color: #e8f4f8;">
                            <td style="border: 1px solid #ddd; padding: 10px;"><strong>Book Title</strong></td>
                            <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.book.title}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #ddd; padding: 10px;"><strong>Author</strong></td>
                            <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.book.author}</td>
                        </tr>
                        <tr style="background-color: #e8f4f8;">
                            <td style="border: 1px solid #ddd; padding: 10px;"><strong>Old Due Date</strong></td>
                            <td style="border: 1px solid #ddd; padding: 10px; text-decoration: line-through;">{old_due_date.strftime('%Y-%m-%d')}</td>
                        </tr>
                        <tr style="background-color: #d4edda;">
                            <td style="border: 1px solid #ddd; padding: 10px;"><strong>New Due Date</strong></td>
                            <td style="border: 1px solid #ddd; padding: 10px; color: #28a745; font-weight: bold;">{new_due_date.strftime('%Y-%m-%d')}</td>
                        </tr>
                        {reason_section}
                    </table>
                    <p style="color: #28a745;"><strong>✓ Your due date has been successfully extended.</strong></p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">
                        This is an automated email. Please do not reply.
                    </p>
                </div>
            </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        
        # Log email configuration
        print(f"Email Backend: {settings.EMAIL_BACKEND}")
        print(f"From: {settings.DEFAULT_FROM_EMAIL}")
        print(f"To: {user.email}")
        print(f"Subject: {subject}")
        
        # Send email
        print(f"\nAttempting to send due date update email...")
        num_sent = send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"✅ SUCCESS: {num_sent} email(s) sent to {user.email}")
        print(f"{'='*50}\n")
        return True
        
    except Exception as e:
        print(f"\n{'='*50}")
        print(f"❌ ERROR: Failed to send due date update notification")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"{'='*50}\n")
        return False


def send_due_date_reminder(issue_record):
    """
    Send book due date reminder email to student
    """
    user = issue_record.member.user
    days_remaining = (issue_record.due_date - now().date()).days
    
    subject = f'Book Due Date Reminder - {issue_record.book.title}'
    
    html_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px;">
                <h2>📚 Book Due Date Reminder</h2>
                <p>Hello <strong>{user.first_name or user.username}</strong>,</p>
                <p>This is a reminder that your book is due soon.</p>
                <p><strong>Book Details:</strong></p>
                <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
                    <tr style="background-color: #e8f4f8;">
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>Book Title</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.book.title}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>Author</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.book.author}</td>
                    </tr>
                    <tr style="background-color: #e8f4f8;">
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>Issue Date</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.issue_date.strftime('%Y-%m-%d')}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>Due Date</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px; color: #ff9800;"><strong>{issue_record.due_date.strftime('%Y-%m-%d')}</strong></td>
                    </tr>
                    <tr style="background-color: #fff3cd;">
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>Days Remaining</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>{days_remaining} day(s)</strong></td>
                    </tr>
                </table>
                <p style="color: #d9534f;"><strong>⚠️ Late Fee:</strong> Late return charges are ₹5 per day.</p>
                <p>Please return the book on time to avoid penalties.</p>
                <hr>
                <p style="color: #666; font-size: 12px;">
                    This is an automated email. Please do not reply.
                </p>
            </div>
        </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_FROM_USER,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Due date reminder sent to {user.email}")
    except Exception as e:
        print(f"Error sending due date reminder: {str(e)}")


def send_overdue_notification(issue_record):
    """
    Send overdue book notification email to student
    """
    user = issue_record.member.user
    days_overdue = (now().date() - issue_record.due_date).days
    fine = days_overdue * 5
    
    subject = f'⚠️ OVERDUE - {issue_record.book.title}'
    
    html_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px;">
                <h2 style="color: #d9534f;">📖 OVERDUE BOOK NOTICE</h2>
                <p>Hello <strong>{user.first_name or user.username}</strong>,</p>
                <p style="color: #d9534f;"><strong>Your book is OVERDUE. Please return it immediately to avoid additional charges.</strong></p>
                <p><strong>Book Details:</strong></p>
                <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
                    <tr style="background-color: #e8f4f8;">
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>Book Title</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.book.title}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>Author</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.book.author}</td>
                    </tr>
                    <tr style="background-color: #e8f4f8;">
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>Issue Date</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px;">{issue_record.issue_date.strftime('%Y-%m-%d')}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>Due Date</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px; color: #d9534f;"><strong>{issue_record.due_date.strftime('%Y-%m-%d')}</strong></td>
                    </tr>
                    <tr style="background-color: #f8d7da;">
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>Days Overdue</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px; color: #d9534f;"><strong>{days_overdue} day(s)</strong></td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 10px;"><strong>Accumulated Fine</strong></td>
                        <td style="border: 1px solid #ddd; padding: 10px; color: #d9534f;"><strong>₹{fine}</strong></td>
                    </tr>
                </table>
                <p style="color: #d9534f;"><strong>⚠️ URGENT:</strong> Each additional day will add ₹5 to your fine.</p>
                <p>Please contact the library administrator if you need an extension.</p>
                <hr>
                <p style="color: #666; font-size: 12px;">
                    This is an automated email. Please do not reply.
                </p>
            </div>
        </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_FROM_USER,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Overdue notification sent to {user.email}")
    except Exception as e:
        print(f"Error sending overdue notification: {str(e)}")
