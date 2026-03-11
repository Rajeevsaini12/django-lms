from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, IssueRecord, Member
from datetime import timedelta
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import BookForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login
from .forms import BookForm, MemberForm
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Book, Member, IssueRecord
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages


def dashboard(request):

    books_count = Book.objects.count()
    members_count = Member.objects.count()

    issued_count = IssueRecord.objects.filter(return_date__isnull=True).count()

    overdue_count = IssueRecord.objects.filter(
        return_date__isnull=True,
        due_date__lt=timezone.now().date()
    ).count()

    records = IssueRecord.objects.select_related(
        "book", "member", "member__user"
    ).order_by("-issue_date")

    return render(request, "library/dashboard.html", {
        "books": books_count,
        "members": members_count,
        "issued": issued_count,
        "overdue": overdue_count,
        "records": records,
        #"issue_records": records
    })


def book_list(request):

    books = Book.objects.all()

    paginator = Paginator(books, 10)
    page = request.GET.get('page')

    books = paginator.get_page(page)

    return render(request, "library/book_list.html", {"books": books})

def search_books(request):

    query = request.GET.get('q')

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )
    else:
        books = Book.objects.all()

    return render(request, "library/book_list.html", {"books": books})


def create_book(request):

    form = BookForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('book_list')

    return render(request, "library/book_form.html", {"form": form})


def update_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    form = BookForm(request.POST or None, instance=book)

    if form.is_valid():
        form.save()
        return redirect('book_list')

    return render(request, "library/book_form.html", {"form": form})

def delete_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)
    book.delete()

    return redirect('book_list')


def issue_book(request):

    books = Book.objects.all()
    members = Member.objects.all()

    if request.method == "POST":

        book_id = request.POST.get("book")
        member_id = request.POST.get("member")

        if not member_id or not book_id:
            messages.error(request, "Please select both book and member.")
            return redirect("issue_book")
        book = Book.objects.get(id=book_id)
        member = Member.objects.get(id=member_id)

        IssueRecord.objects.create(
            book=book,
            member=member,
            issue_date=timezone.now(),
            due_date=timezone.now() + timedelta(days=7)
        )

        book.available_copies -= 1
        book.save()

        return redirect("dashboard")

    return render(request, "library/issue_book.html", {
    "books": books,
    "members": members
})

def return_book(request, record_id):

    record = get_object_or_404(IssueRecord, id=record_id)

    record.return_date = timezone.now()
    record.save()

    # increase book copies
    book = record.book
    book.available_copies += 1
    book.save()

    return redirect("dashboard")


def member_list(request):

    members = Member.objects.all()

    return render(request, "library/member_list.html", {
        "members": members
    })


def create_member(request):

    form = MemberForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('member_list')

    return render(request, "library/member_form.html", {
        "form": form
    })


def update_member(request, member_id):

    member = get_object_or_404(Member, id=member_id)

    form = MemberForm(request.POST or None, instance=member)

    if form.is_valid():
        form.save()
        return redirect('member_list')

    return render(request, "library/member_form.html", {
        "form": form
    })


def delete_member(request, member_id):

    member = get_object_or_404(Member, id=member_id)
    member.delete()

    return redirect('member_list')

def book_history(request, book_id):

    book = Book.objects.get(id=book_id)

    records = IssueRecord.objects.filter(book=book)

    return render(request, "library/book_history.html", {
        "book": book,
        "records": records
    })

def student_login(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")

    return render(request, "library/login.html")

def issue_list(request):

    records = IssueRecord.objects.select_related(
        "book", "member", "member__user"
    ).all().order_by("-issue_date")

    return render(request, "library/issue_list.html", {
        "records": records
    })

def update_issue_record(request, record_id):
    record = get_object_or_404(IssueRecord, id=record_id)

    if request.method == "POST":
        issue_date = request.POST.get("issue_date")
        due_date = request.POST.get("due_date")

        record.issue_date = issue_date
        record.due_date = due_date
        record.save()

        messages.success(request, "Issue record updated successfully.")
        return redirect("dashboard")

    return render(request, "update_issue.html", {"record": record})



