from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
from django.db.models import Q
from datetime import timedelta

from .models import Book, Member, IssueRecord
from .serializers import BookSerializer, MemberSerializer, IssueRecordSerializer
from .permissions import IsAdmin
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
def dashboard_api(request):

    books = Book.objects.count()
    members = Member.objects.count()

    issued = IssueRecord.objects.filter(return_date__isnull=True).count()

    overdue = IssueRecord.objects.filter(
        return_date__isnull=True,
        due_date__lt=timezone.now().date()
    ).count()

    return Response({
        "books": books,
        "members": members,
        "issued": issued,
        "overdue": overdue
    })

@api_view(['GET'])
def book_list_api(request):

    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def create_book_api(request):

    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)


@api_view(['PUT'])
def update_book_api(request, book_id):

    book = Book.objects.get(id=book_id)

    serializer = BookSerializer(book, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)

@api_view(['DELETE'])
def delete_book_api(request, book_id):

    book = Book.objects.get(id=book_id)
    book.delete()

    return Response({"message": "Book deleted"})

@api_view(['GET'])
def search_books_api(request):

    query = request.GET.get("q")

    books = Book.objects.filter(
        Q(title__icontains=query) |
        Q(author__icontains=query) |
        Q(isbn__icontains=query)
    )

    serializer = BookSerializer(books, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def issue_book_api(request):

    book_id = request.data.get("book")
    member_id = request.data.get("member")

    book = Book.objects.get(id=book_id)
    member = Member.objects.get(id=member_id)

    record = IssueRecord.objects.create(
        book=book,
        member=member,
        issue_date=timezone.now(),
        due_date=timezone.now() + timedelta(days=7)
    )

    book.available_copies -= 1
    book.save()

    serializer = IssueRecordSerializer(record)

    return Response(serializer.data)

@api_view(['POST'])
def return_book_api(request, record_id):

    record = IssueRecord.objects.get(id=record_id)

    record.return_date = timezone.now()
    record.save()

    book = record.book
    book.available_copies += 1
    book.save()

    return Response({"message": "Book returned"})

@api_view(['GET'])
def member_list_api(request):

    members = Member.objects.all()
    serializer = MemberSerializer(members, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def create_member_api(request):

    serializer = MemberSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)

@api_view(['GET'])
def issue_list_api(request):

    records = IssueRecord.objects.all().order_by("-issue_date")

    serializer = IssueRecordSerializer(records, many=True)

    return Response(serializer.data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_dashboard(request):

    member = request.user.member

    issued_books = IssueRecord.objects.filter(
        member=member,
        return_date__isnull=True
    )

    overdue_books = issued_books.filter(
        due_date__lt=timezone.now().date()
    )

    history = IssueRecord.objects.filter(member=member)

    return Response({

        "issued_books": issued_books.count(),
        "overdue_books": overdue_books.count(),
        "total_books_taken": history.count()

    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_books(request):

    member = request.user.member

    records = IssueRecord.objects.filter(
        member=member,
        return_date__isnull=True
    )

    serializer = IssueRecordSerializer(records, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_history(request):

    member = request.user.member

    records = IssueRecord.objects.filter(member=member)

    serializer = IssueRecordSerializer(records, many=True)

    return Response(serializer.data)

class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class MemberViewSet(viewsets.ModelViewSet):

    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class IssueRecordViewSet(viewsets.ModelViewSet):

    queryset = IssueRecord.objects.all()
    serializer_class = IssueRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        book = serializer.validated_data["book"]

        if book.available_copies <= 0:
            raise ValueError("Book not available")

        serializer.save(
            issue_date=timezone.now(),
            due_date=timezone.now() + timedelta(days=7)
        )

        book.available_copies -= 1
        book.save()

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):

        record = self.get_object()

        if record.return_date:
            return Response({"message": "Book already returned"})

        record.return_date = timezone.now()
        record.save()

        book = record.book
        book.available_copies += 1
        book.save()

        return Response({"message": "Book returned successfully"})



FINE_PER_DAY = 5  # ₹5 per day


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_dashboard(request):

    member = request.user.member

    issued_books = IssueRecord.objects.filter(
        member=member,
        return_date__isnull=True
    )

    overdue_books = issued_books.filter(
        due_date__lt=timezone.now().date()
    )

    history = IssueRecord.objects.filter(member=member)

    # calculate fine
    total_fine = 0
    today = timezone.now().date()

    for record in overdue_books:
        overdue_days = (today - record.due_date).days
        total_fine += overdue_days * FINE_PER_DAY

    return Response({
        "student_name": request.user.username,
        "books_currently_issued": issued_books.count(),
        "overdue_books": overdue_books.count(),
        "total_books_history": history.count(),
        "total_fine": total_fine
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_profile(request):

    member = request.user.member

    return Response({
        "username": request.user.username,
        "email": request.user.email,
        "phone": member.phone,
        "role": member.role
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_issued_books(request):

    member = request.user.member

    records = IssueRecord.objects.filter(
        member=member,
        return_date__isnull=True
    )

    data = []

    for r in records:
        data.append({
            "book_title": r.book.title,
            "author": r.book.author,
            "issue_date": r.issue_date,
            "due_date": r.due_date
        })

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_book_history(request):

    member = request.user.member

    records = IssueRecord.objects.filter(member=member)

    data = []

    for r in records:
        data.append({
            "book_title": r.book.title,
            "issue_date": r.issue_date,
            "due_date": r.due_date,
            "return_date": r.return_date
        })

    return Response(data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_overdue_books(request):

    member = request.user.member
    today = timezone.now().date()

    records = IssueRecord.objects.filter(
        member=member,
        return_date__isnull=True,
        due_date__lt=today
    )

    data = []

    for r in records:

        overdue_days = (today - r.due_date).days
        fine = overdue_days * 5

        data.append({
            "book_title": r.book.title,
            "due_date": r.due_date,
            "overdue_days": overdue_days,
            "fine": fine
        })

    return Response(data)