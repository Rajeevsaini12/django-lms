from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now


class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, null=True, blank=True)

    total_copies = models.IntegerField()
    available_copies = models.IntegerField()

    def __str__(self):
        return self.title


'''class Member(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15)

    role = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Admin'),
            ('librarian', 'Librarian'),
            ('student', 'Student')
        ],
        default='student'
    )

    def __str__(self):
        return self.user.username '''



class Member(models.Model):

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("student", "Student"),
         
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username    


class IssueRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField(default=now)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.issue_date + timedelta(days=14)
        super().save(*args, **kwargs)

    @property
    def fine(self):
        if self.return_date:
            late_days = (self.return_date - self.due_date).days
        else:
            late_days = (now().date() - self.due_date).days

        if late_days > 0:
            return late_days * 5
        return 0    

    def __str__(self):
        return f"{self.book.title} issued to {self.member.user.username}"
    

@property
def is_overdue(self):
    if self.return_date is None and self.due_date < now().date():
        return True
    return False
