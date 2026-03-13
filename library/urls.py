from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, MemberViewSet, IssueRecordViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register("api/books", BookViewSet, basename="book-api")
router.register("api/members", MemberViewSet, basename="member-api")
router.register("api/issues", IssueRecordViewSet, basename="issue-api")


urlpatterns = [
    
    # Frontend Views
    path('login/', views.login_view, name='login'),
    path('register/', views.register_student, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('all-students/', views.all_students_view, name='all_students'),
    path('student-dashboard/', views.student_dashboard_view, name='student_dashboard_view'),
    path('admin-history/', views.admin_history, name='admin_history'),
    path('student-history/', views.student_history_view, name='student_history'),
    path('student-overdue/', views.student_overdue, name='student_overdue'),
    path('books/', views.book_list_view, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('issue-book/', views.issue_book_page, name='issue_book_page'),
    path('confirm-return/', views.confirm_return_page, name='confirm_return_page'),
    path('return-book/', views.return_book_page, name='return_book_page'),
    path('update-due-date/<int:record_id>/', views.update_due_date_page, name='update_due_date_page'),
    path('api-books/', views.api_books_list_view, name='api_books_list'),
    path('test-email/', views.test_email, name='test_email'),
    
    # Static Pages
    path('issue/', views.admin_dashboard, name='issue_book'),

    # Simple API Views
    path('api/dashboard/', views.dashboard_api),
    path('api/search-books/', views.search_books_api),

    path('api/issue-book/', views.issue_book_api),
    path('api/return-book/<int:record_id>/', views.return_book_api),

    path('api/student/dashboard/', views.student_dashboard_api),
    path('api/student/books/', views.student_books),
    path('api/student/history/', views.student_history),
    path('api/student/profile/', views.student_profile),
    path('api/student/books/', views.student_issued_books),
    path('api/student/history/', views.student_book_history),
    path('api/student/overdue/', views.student_overdue_books),

    path("api/login/", TokenObtainPairView.as_view(), name="jwt_login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/login/", views.jwt_login, name="jwt_login"),

]

# Add router URLs for RESTful API endpoints
urlpatterns += router.urls
