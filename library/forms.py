from django import forms
from .models import Book, IssueRecord

# library/forms.py
from .models import Member
from django.contrib.auth.models import User      

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'author', 'total_copies', 'available_copies']


class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ['user', 'phone']



class IssueForm(forms.ModelForm):

    class Meta:
        model = IssueRecord
        fields = ['book', 'member', 'issue_date', 'due_date']        


        