from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, MemberViewSet, IssueRecordViewSet


router = DefaultRouter()
router.register("books", BookViewSet)
router.register("members", MemberViewSet)
router.register("issues", IssueRecordViewSet)


urlpatterns = [

    path('api/dashboard/', views.dashboard_api),

    path('api/books/', views.book_list_api),
    path('api/books/create/', views.create_book_api),
    path('api/books/update/<int:book_id>/', views.update_book_api),
    path('api/books/delete/<int:book_id>/', views.delete_book_api),

    path('api/search-books/', views.search_books_api),

    path('api/members/', views.member_list_api),
    path('api/members/create/', views.create_member_api),

    path('api/issue-book/', views.issue_book_api),
    path('api/return-book/<int:record_id>/', views.return_book_api),

    path('api/issues/', views.issue_list_api),

    path('api/student/dashboard/', views.student_dashboard),
    path('api/student/books/', views.student_books),
    path('api/student/history/', views.student_history),
    path('api/student/dashboard/', views.student_dashboard),
    path('api/student/profile/', views.student_profile),
    path('api/student/books/', views.student_issued_books),
    path('api/student/history/', views.student_book_history),
    path('api/student/overdue/', views.student_overdue_books),

]

# add router urls
urlpatterns += router.urls