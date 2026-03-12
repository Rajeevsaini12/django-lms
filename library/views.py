from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from .models import Book, Member, IssueRecord
from .serializers import BookSerializer, MemberSerializer, IssueRecordSerializer
from .permissions import IsAdmin
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes


# ============================================
# API VIEWS
# ============================================

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


FINE_PER_DAY = 5  # ₹5 per day


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_dashboard_api(request):

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



class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer


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


# ============================================
# FRONTEND VIEWS
# ============================================

def register_student(request):
    """Registration view for new students"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        from .forms import StudentRegistrationForm
        import string
        import random
        
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Extract form data
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                
                # Generate username from email (before @)
                username = email.split('@')[0]
                
                # Handle duplicate username
                counter = 1
                original_username = username
                while User.objects.filter(username=username).exists():
                    username = f"{original_username}{counter}"
                    counter += 1
                
                # Generate a secure random password
                characters = string.ascii_letters + string.digits + '!@#$%'
                password = ''.join(random.choice(characters) for _ in range(12))
                
                # Create User
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Create Member profile (student role)
                member = Member.objects.create(
                    user=user,
                    role='student',
                    phone=phone
                )
                
                # Send registration email with credentials
                from django.core.mail import send_mail
                from django.conf import settings
                
                subject = '🎉 Welcome to Library Management System - Your Login Credentials'
                
                html_message = f"""
                <html>
                    <body style="font-family: Arial, sans-serif;">
                        <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px;">
                            <h2 style="color: #667eea;">Welcome to LMS! 📚</h2>
                            <p>Hello <strong>{first_name} {last_name}</strong>,</p>
                            <p>Thank you for registering with the Library Management System! Your account has been successfully created.</p>
                            
                            <p style="margin-top: 30px;"><strong>Your Login Credentials:</strong></p>
                            <div style="background-color: white; padding: 15px; border-left: 4px solid #667eea; margin: 20px 0;">
                                <p><strong>Username:</strong> <code>{username}</code></p>
                                <p><strong>Password:</strong> <code>{password}</code></p>
                                <p><strong>Email:</strong> {email}</p>
                            </div>
                            
                            <p style="color: #d9534f;"><strong>⚠️ Important Security Notes:</strong></p>
                            <ul style="color: #666;">
                                <li>Your password is case-sensitive. Keep it safe and never share it.</li>
                                <li>We recommend changing your password after your first login.</li>
                                <li>If you didn't register, please contact the administrator immediately.</li>
                            </ul>
                            
                            <p><strong>Login Link:</strong></p>
                            <p><a href="http://localhost:4000/login/" style="color: #667eea; text-decoration: none; font-weight: bold;">Click here to login</a></p>
                            
                            <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
                            <p style="color: #666; font-size: 12px;">
                                <strong>Account Details:</strong><br>
                                Phone: {phone}<br>
                                Role: Student<br>
                                Registration Date: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
                            </p>
                            
                            <p style="color: #999; font-size: 11px; margin-top: 20px;">
                                This is an automated email. Please do not reply directly to this email.
                            </p>
                        </div>
                    </body>
                </html>
                """
                
                plain_message = f"""
                Welcome to LMS!
                
                Hello {first_name} {last_name},
                
                Your account has been successfully created.
                
                LOGIN CREDENTIALS:
                Username: {username}
                Password: {password}
                Email: {email}
                
                Please keep these credentials safe and change your password after first login.
                
                Login at: http://localhost:4000/login/
                
                Thank you!
                """
                
                try:
                    send_mail(
                        subject,
                        plain_message,
                        settings.EMAIL_FROM_USER,
                        [email],
                        html_message=html_message,
                        fail_silently=False,
                    )
                    print(f"Registration email sent to {email}")
                except Exception as e:
                    print(f"Error sending registration email: {str(e)}")
                
                # Redirect to login with success message
                from django.contrib import messages
                messages.success(
                    request,
                    f'✅ Registration successful! Your login credentials have been sent to {email}. Please check your inbox and login.'
                )
                return redirect('login')
                
            except Exception as e:
                print(f"Registration error: {str(e)}")
                from django.contrib import messages
                messages.error(request, f'❌ Registration failed: {str(e)}')
                return render(request, 'register.html', {'form': form})
        else:
            # Form has errors
            pass
    else:
        from .forms import StudentRegistrationForm
        form = StudentRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Login view for frontend with role-based validation"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_role = request.POST.get('user_role', 'student')  # Get which panel they used
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user has a Member profile
            if hasattr(user, 'member'):
                # Verify user's role matches the login panel they used
                if user.member.role == user_role:
                    # Role matches - allow login
                    login(request, user)
                    return redirect('dashboard')
                else:
                    # Role mismatch - deny access
                    error_msg = f"❌ Access Denied! This is a {user_role.upper()} login panel. "
                    error_msg += f"Your account is registered as a {user.member.role.upper()}."
                    return render(request, 'login.html', {
                        'error': error_msg,
                        'user_role': user_role,
                        'form': request.POST
                    })
            else:
                return render(request, 'login.html', {
                    'error': '❌ User profile not found. Please contact administrator.',
                    'user_role': user_role
                })
        else:
            return render(request, 'login.html', {
                'error': '❌ Invalid username or password',
                'user_role': user_role
            })
    
    return render(request, 'login.html')


@login_required(login_url='login')
def logout_view(request):
    """Logout view"""
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def book_list_view(request):
    """Book list view with search, filter, and pagination"""
    books_queryset = Book.objects.all()
    
    # Search functionality
    search_query = request.GET.get('q', '').strip()
    if search_query:
        books_queryset = books_queryset.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )
    
    # Filter by availability
    availability = request.GET.get('availability', '').strip()
    if availability == 'available':
        books_queryset = books_queryset.filter(available_copies__gt=0)
    elif availability == 'unavailable':
        books_queryset = books_queryset.filter(available_copies=0)
    
    # Sorting
    sort_by = request.GET.get('sort', 'title').strip()
    if sort_by in ['title', '-title', 'author', '-available_copies']:
        books_queryset = books_queryset.order_by(sort_by)
    else:
        books_queryset = books_queryset.order_by('title')
    
    # Statistics for dashboard
    total_books = Book.objects.count()
    available_books = sum(book.available_copies for book in Book.objects.all())
    issued_books = IssueRecord.objects.filter(return_date__isnull=True).count()
    unique_titles = Book.objects.count()
    
    # Pagination
    paginator = Paginator(books_queryset, 20)  # 20 books per page
    page_number = request.GET.get('page', 1)
    books = paginator.get_page(page_number)
    
    context = {
        'books': books,
        'total_books': total_books,
        'available_books': available_books,
        'issued_books': issued_books,
        'books_count': unique_titles,
        'search_query': search_query,
        'selected_availability': availability,
        'selected_sort': sort_by,
    }
    
    return render(request, 'library/book_list.html', context)


@login_required(login_url='login')
def add_book(request):
    """Add a new book - Admin only"""
    if not hasattr(request.user, 'member') or request.user.member.role != 'admin':
        return redirect('book_list')
    
    if request.method == 'POST':
        from .forms import BookForm
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        from .forms import BookForm
        form = BookForm()
    
    return render(request, 'library/book_form.html', {'form': form, 'title': 'Add New Book'})


@login_required(login_url='login')
def edit_book(request, book_id):
    """Edit a book - Admin only"""
    if not hasattr(request.user, 'member') or request.user.member.role != 'admin':
        return redirect('book_list')
    
    from .forms import BookForm
    book = Book.objects.get(id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'library/book_form.html', {'form': form, 'title': f'Edit {book.title}'})


@login_required(login_url='login')
def delete_book(request, book_id):
    """Delete a book - Admin only"""
    if not hasattr(request.user, 'member') or request.user.member.role != 'admin':
        return redirect('book_list')
    
    book = Book.objects.get(id=book_id)
    
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    
    return render(request, 'library/book_form.html', {'book': book, 'action': 'delete'})


def api_books_list_view(request):
    """API Books List view - fetches data from /api/books/ using JavaScript"""
    return render(request, 'library/api_books_list.html')


def test_email(request):
    """Test email endpoint to verify email configuration"""
    from django.core.mail import send_mail
    from django.conf import settings
    
    test_email_address = request.GET.get('email', 'test@example.com')
    
    try:
        print("\n=== TESTING EMAIL CONFIGURATION ===")
        print(f"Email Backend: {settings.EMAIL_BACKEND}")
        print(f"Email Host: {settings.EMAIL_HOST}")
        print(f"Email Port: {settings.EMAIL_PORT}")
        print(f"Email Use TLS: {settings.EMAIL_USE_TLS}")
        print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")
        print(f"To Email: {test_email_address}")
        
        subject = "Test Email - Library Management System"
        message = "This is a test email from Library Management System"
        html_message = "<h2>Test Email</h2><p>This is a test email to verify the email configuration is working properly.</p>"
        
        result = send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [test_email_address],
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"✅ Email sent successfully! Result: {result}")
        return JsonResponse({
            'status': 'success',
            'message': f'✅ Test email sent successfully to {test_email_address}',
            'result': result
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error sending test email: {error_msg}")
        import traceback
        traceback.print_exc()
        
        return JsonResponse({
            'status': 'error',
            'message': f'❌ Failed to send test email: {error_msg}',
            'error': error_msg
        }, status=400)


@login_required(login_url='login')
def dashboard(request):
    """Dashboard view - routes to admin or student dashboard"""
    if hasattr(request.user, 'member'):
        if request.user.member.role == 'admin':
            return admin_dashboard(request)
        else:
            return student_dashboard_view(request)
    return redirect('login')


@login_required(login_url='login')
def admin_dashboard(request):
    """Admin dashboard view"""
    if not hasattr(request.user, 'member') or request.user.member.role != 'admin':
        return redirect('student_dashboard_view')
    
    books = Book.objects.count()
    members = Member.objects.count()
    issued = IssueRecord.objects.filter(return_date__isnull=True).count()
    overdue = IssueRecord.objects.filter(
        return_date__isnull=True,
        due_date__lt=timezone.now().date()
    ).count()
    
    # Get recent issues
    recent_issues = IssueRecord.objects.all().order_by('-issue_date')[:10]
    
    context = {
        'dashboard': {
            'books': books,
            'members': members,
            'issued': issued,
            'overdue': overdue,
        },
        'recent_issues': recent_issues,
    }
    
    return render(request, 'library/admin_dashboard.html', context)


@login_required(login_url='login')
def issue_book_page(request):
    """Page for admin to issue books to students"""
    # Check if user is admin
    if not hasattr(request.user, 'member') or request.user.member.role != 'admin':
        return redirect('dashboard')
    
    if request.method == 'POST':
        from .forms import IssueBookForm
        form = IssueBookForm(request.POST)
        
        if form.is_valid():
            try:
                student = form.cleaned_data['student']
                book = form.cleaned_data['book']
                issue_days = form.cleaned_data.get('issue_days', 7)
                notes = form.cleaned_data.get('notes', '')
                
                # Create issue record
                issue_date = timezone.now()
                due_date = issue_date + timedelta(days=issue_days)
                
                issue_record = IssueRecord.objects.create(
                    book=book,
                    member=student,
                    issue_date=issue_date,
                    due_date=due_date
                )
                
                # Decrease available copies
                book.available_copies -= 1
                book.save()
                
                # Send notification email
                from .notifications import send_book_issue_notification
                send_book_issue_notification(issue_record)
                
                # Show success message
                from django.contrib import messages
                messages.success(
                    request,
                    f'✅ Book "{book.title}" successfully issued to {student.user.get_full_name() or student.user.username} until {due_date.strftime("%d/%m/%Y")}'
                )
                
                # Clear form by redirecting
                return redirect('issue_book_page')
                
            except Exception as e:
                from django.contrib import messages
                messages.error(request, f'❌ Error issuing book: {str(e)}')
        else:
            # Form has errors - will display below
            pass
    else:
        from .forms import IssueBookForm
        form = IssueBookForm()
    
    # Get statistics
    students = Member.objects.filter(role='student').count()
    available_books = Book.objects.filter(available_copies__gt=0).count()
    issued_books = IssueRecord.objects.filter(return_date__isnull=True).count()
    
    context = {
        'form': form,
        'students_count': students,
        'available_books_count': available_books,
        'issued_books_count': issued_books,
    }
    
    return render(request, 'library/issue_book.html', context)


@login_required(login_url='login')
def return_book_page(request):
    """Page for students to return books"""
    # Check if user is student
    if not hasattr(request.user, 'member') or request.user.member.role != 'student':
        return redirect('dashboard')
    
    member = request.user.member
    
    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        
        try:
            record = IssueRecord.objects.get(id=record_id, member=member)
            
            if record.return_date:
                from django.contrib import messages
                messages.error(request, '❌ This book has already been returned.')
                return redirect('return_book_page')
            
            # Update return date
            record.return_date = timezone.now()
            record.save()
            
            # Increment available copies
            book = record.book
            book.available_copies += 1
            book.save()
            
            # Send notification email
            from .notifications import send_book_return_notification
            send_book_return_notification(record)
            
            # Show success message
            from django.contrib import messages
            messages.success(
                request,
                f'✅ Book "{book.title}" successfully returned. Thank you!'
            )
            
            # Redirect to student dashboard
            return redirect('student_dashboard_view')
            
        except IssueRecord.DoesNotExist:
            from django.contrib import messages
            messages.error(request, '❌ Book record not found.')
            return redirect('return_book_page')
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'❌ Error returning book: {str(e)}')
    
    # Get currently issued books for this student
    current_books = IssueRecord.objects.filter(
        member=member,
        return_date__isnull=True
    ).select_related('book')
    
    # Calculate fine for each book
    today = timezone.now().date()
    books_with_fine = []
    for record in current_books:
        fine = 0
        is_overdue = False
        if record.due_date < today:
            fine = (today - record.due_date).days * FINE_PER_DAY
            is_overdue = True
        
        books_with_fine.append({
            'record': record,
            'fine': fine,
            'is_overdue': is_overdue,
        })
    
    context = {
        'books_with_fine': books_with_fine,
        'total_books': len(books_with_fine),
    }
    
    return render(request, 'library/return_book.html', context)


@login_required(login_url='login')
def student_dashboard_view(request):
    """Student dashboard view"""
    if not hasattr(request.user, 'member') or request.user.member.role == 'admin':
        return redirect('admin_dashboard')
    
    member = request.user.member
    
    # Get current issued books
    current_books = IssueRecord.objects.filter(
        member=member,
        return_date__isnull=True
    )
    
    # Calculate statistics
    total_fine = 0
    today = timezone.now().date()
    
    for record in current_books:
        if record.due_date < today:
            overdue_days = (today - record.due_date).days
            total_fine += overdue_days * FINE_PER_DAY
    
    history = IssueRecord.objects.filter(member=member)
    
    student_data = {
        'books_currently_issued': current_books.count(),
        'overdue_books': current_books.filter(due_date__lt=today).count(),
        'total_books_history': history.count(),
        'total_fine': total_fine,
    }
    
    student_info = {
        'phone': member.phone,
    }
    
    context = {
        'student_data': student_data,
        'student_info': student_info,
        'current_books': current_books,
    }
    
    return render(request, 'library/student_dashboard.html', context)


@login_required(login_url='login')
def confirm_return_page(request):
    """Admin page to confirm book returns"""
    # Check if user is admin
    if not hasattr(request.user, 'member') or request.user.member.role != 'admin':
        return redirect('dashboard')
    
    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        
        try:
            record = IssueRecord.objects.get(id=record_id)
            
            if record.return_date:
                from django.contrib import messages
                messages.error(request, '❌ This book has already been returned.')
                return redirect('confirm_return_page')
            
            # Confirm return - update return date
            record.return_date = timezone.now()
            record.save(update_fields=['return_date'])
            
            # Increment available copies
            book = record.book
            book.available_copies += 1
            book.save()
            
            # Send notification email to student with error handling
            try:
                from .notifications import send_book_return_notification
                send_book_return_notification(record)
                email_sent = True
            except Exception as email_error:
                print(f"Email error: {str(email_error)}")
                email_sent = False
                email_error_msg = str(email_error)
            
            # Show success message
            from django.contrib import messages
            if email_sent:
                messages.success(
                    request,
                    f'✅ Return confirmed for "{book.title}" from {record.member.user.get_full_name() or record.member.user.username}. Email sent to student.'
                )
            else:
                messages.warning(
                    request,
                    f'⚠️ Return confirmed for "{book.title}" but email failed to send. Error: {email_error_msg}'
                )
            
            return redirect('confirm_return_page')
            
        except IssueRecord.DoesNotExist:
            from django.contrib import messages
            messages.error(request, '❌ Book record not found.')
            return redirect('confirm_return_page')
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'❌ Error confirming return: {str(e)}')
            import traceback
            traceback.print_exc()
            return redirect('confirm_return_page')
    
    # Get all currently issued books (not yet returned)
    pending_returns = IssueRecord.objects.filter(
        return_date__isnull=True
    ).select_related('book', 'member__user').order_by('due_date')
    
    # Calculate fine for each book
    today = timezone.now().date()
    returns_data = []
    for record in pending_returns:
        fine = 0
        is_overdue = False
        if record.due_date < today:
            fine = (today - record.due_date).days * FINE_PER_DAY
            is_overdue = True
        
        returns_data.append({
            'record': record,
            'fine': fine,
            'is_overdue': is_overdue,
        })
    
    context = {
        'returns_data': returns_data,
        'total_pending': len(returns_data),
        'overdue_count': sum(1 for r in returns_data if r['is_overdue']),
    }
    
    return render(request, 'library/confirm_return.html', context)


@login_required(login_url='login')
def admin_history(request):
    """Admin history view - all transactions"""
    if not hasattr(request.user, 'member') or request.user.member.role != 'admin':
        return redirect('student_history')
    
    records = IssueRecord.objects.all()
    
    # Filter by status
    status = request.GET.get('status')
    if status == 'issued':
        records = records.filter(return_date__isnull=True)
    elif status == 'returned':
        records = records.filter(return_date__isnull=False)
    elif status == 'overdue':
        records = records.filter(
            return_date__isnull=True,
            due_date__lt=timezone.now().date()
        )
    
    # Search
    q = request.GET.get('q')
    if q:
        records = records.filter(
            Q(book__title__icontains=q) |
            Q(member__user__first_name__icontains=q) |
            Q(member__user__last_name__icontains=q) |
            Q(member__user__username__icontains=q)
        )
    
    # Sorting
    sort = request.GET.get('sort', '-issue_date')
    records = records.order_by(sort)
    
    # Pagination
    paginator = Paginator(records, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'records': page_obj,
        'total_records': records.count(),
        'issued_count': IssueRecord.objects.filter(return_date__isnull=True).count(),
        'returned_count': IssueRecord.objects.filter(return_date__isnull=False).count(),
    }
    
    return render(request, 'library/admin_history.html', context)


@login_required(login_url='login')
def update_due_date_page(request, record_id):
    """Page for admin to update due date of an issued book"""
    # Check if user is admin
    if not hasattr(request.user, 'member') or request.user.member.role != 'admin':
        return redirect('dashboard')
    
    try:
        record = IssueRecord.objects.get(id=record_id, return_date__isnull=True)
    except IssueRecord.DoesNotExist:
        from django.contrib import messages
        messages.error(request, '❌ Book record not found or already returned.')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        from .forms import UpdateDueDateForm
        form = UpdateDueDateForm(request.POST)
        
        if form.is_valid():
            try:
                old_due_date = record.due_date
                new_due_date = form.cleaned_data['new_due_date']
                reason = form.cleaned_data.get('reason', '')
                
                # Update due date
                record.due_date = new_due_date
                record.save()
                
                # Send notification email to student
                from .notifications import send_due_date_update_notification
                send_due_date_update_notification(record, old_due_date, new_due_date, reason)
                
                from django.contrib import messages
                messages.success(
                    request,
                    f'✅ Due date updated successfully! New due date: {new_due_date.strftime("%d/%m/%Y")}'
                )
                
                return redirect('admin_dashboard')
                
            except Exception as e:
                from django.contrib import messages
                messages.error(request, f'❌ Error updating due date: {str(e)}')
    else:
        from .forms import UpdateDueDateForm
        form = UpdateDueDateForm()
    
    context = {
        'form': form,
        'record': record,
        'old_due_date': record.due_date,
    }
    
    return render(request, 'library/update_due_date.html', context)


@login_required(login_url='login')
def student_history_view(request):
    """Student history view - personal transactions"""
    if not hasattr(request.user, 'member'):
        return redirect('login')
    
    member = request.user.member
    
    records = IssueRecord.objects.filter(member=member)
    
    # Filter by status
    status = request.GET.get('status')
    if status == 'current':
        records = records.filter(return_date__isnull=True)
    elif status == 'returned':
        records = records.filter(return_date__isnull=False)
    elif status == 'overdue':
        records = records.filter(
            return_date__isnull=True,
            due_date__lt=timezone.now().date()
        )
    
    records = records.order_by('-issue_date')
    
    # Pagination
    paginator = Paginator(records, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    all_records = IssueRecord.objects.filter(member=member)
    total_books = all_records.count()
    current_books = all_records.filter(return_date__isnull=True).count()
    completed_books = all_records.filter(return_date__isnull=False).count()
    overdue_count = all_records.filter(return_date__isnull=True,due_date__lt=timezone.now().date()).count()
    
    context = {
        'records': page_obj,
        'total_books': total_books,
        'current_books': current_books,
        'completed_books': completed_books,
        'overdue_count': overdue_count,
    }
    
    return render(request, 'library/student_history.html', context)


@login_required(login_url='login')
def student_overdue(request):
    """Student overdue books view"""
    if not hasattr(request.user, 'member'):
        return redirect('login')
    
    member = request.user.member
    today = timezone.now().date()
    
    records = IssueRecord.objects.filter(
        member=member,
        return_date__isnull=True,
        due_date__lt=today
    )
    
    context = {
        'records': records,
    }
    
    return render(request, 'library/student_history.html', context)
