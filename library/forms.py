from django import forms
from .models import Book, IssueRecord, Member
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from datetime import datetime, timedelta
from django.utils import timezone

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'author', 'total_copies', 'available_copies']


class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ['user', 'phone']


class IssueBookForm(forms.Form):
    """Form for admin to issue books to students"""
    
    student = forms.ModelChoiceField(
        queryset=Member.objects.filter(role='student'),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'student-select'
        }),
        label='Select Student',
        empty_label='-- Choose a student --'
    )
    
    book = forms.ModelChoiceField(
        queryset=Book.objects.filter(available_copies__gt=0),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'book-select'
        }),
        label='Select Book',
        empty_label='-- Choose a book --'
    )
    
    issue_days = forms.IntegerField(
        required=False,
        initial=7,
        min_value=1,
        max_value=90,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'number',
            'min': '1',
            'max': '90',
            'placeholder': 'Number of days for issue'
        }),
        label='Issue Duration (Days)',
        help_text='How many days the student can keep the book (1-90 days)'
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional notes (e.g., reason for issue)'
        }),
        label='Notes',
        max_length=500
    )
    
    def clean_issue_days(self):
        """Validate issue days"""
        issue_days = self.cleaned_data.get('issue_days')
        if issue_days is None:
            issue_days = 7
        return issue_days
    
    def clean(self):
        """Validate form data"""
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        book = cleaned_data.get('book')
        
        if student and book:
            # Check if book has available copies
            if book.available_copies <= 0:
                raise ValidationError(f'❌ Book "{book.title}" has no available copies.')
            
            # Check if student already has this book issued
            existing_issue = IssueRecord.objects.filter(
                member=student,
                book=book,
                return_date__isnull=True
            ).exists()
            
            if existing_issue:
                raise ValidationError(f'❌ This student already has "{book.title}" issued and hasn\'t returned it yet.')
        
        return cleaned_data


class StudentRegistrationForm(forms.Form):
    """Form for student self-registration"""
    
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name',
            'autocomplete': 'given-name'
        }),
        label='First Name'
    )
    
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name',
            'autocomplete': 'family-name'
        }),
        label='Last Name'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email'
        }),
        label='Email Address'
    )
    
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your 10-digit phone number',
            'autocomplete': 'tel',
            'type': 'tel'
        }),
        label='Mobile Number'
    )
    
    terms_agreed = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='I agree to the terms and conditions'
    )
    
    def clean_email(self):
        """Validate that email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered. Please use a different email or try logging in.')
        return email.lower()
    
    def clean_phone(self):
        """Validate phone number format"""
        phone = self.cleaned_data.get('phone')
        # Remove any non-digit characters
        cleaned_phone = re.sub(r'\D', '', phone)
        
        if len(cleaned_phone) < 10:
            raise ValidationError('Phone number must be at least 10 digits.')
        
        if len(cleaned_phone) > 15:
            raise ValidationError('Phone number must not exceed 15 digits.')
        
        return cleaned_phone
    
    def clean_first_name(self):
        """Validate first name"""
        first_name = self.cleaned_data.get('first_name').strip()
        if not first_name:
            raise ValidationError('First name cannot be empty.')
        return first_name
    
    def clean_last_name(self):
        """Validate last name"""
        last_name = self.cleaned_data.get('last_name').strip()
        if not last_name:
            raise ValidationError('Last name cannot be empty.')
        return last_name


class IssueForm(forms.ModelForm):

    class Meta:
        model = IssueRecord
        fields = ['book', 'member', 'issue_date', 'due_date']


class UpdateDueDateForm(forms.Form):
    """Form for admin to update due date of an issued book"""
    
    new_due_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'new-due-date'
        }),
        label='New Due Date',
        help_text='Select the new due date for this book'
    )
    
    reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional: Reason for changing due date'
        }),
        label='Reason (Optional)',
        max_length=500
    )
    
    def clean_new_due_date(self):
        """Validate the new due date"""
        new_due_date = self.cleaned_data.get('new_due_date')
        if new_due_date and new_due_date < timezone.now().date():
            raise ValidationError('Due date cannot be in the past.')
        return new_due_date