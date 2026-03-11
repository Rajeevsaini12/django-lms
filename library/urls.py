from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('issue/', views.issue_book, name='issue_book'),
    path('return/<int:record_id>/', views.return_book, name='return_book'),
    path('books/', views.search_books, name='search_books'),
    path('history/<int:book_id>/', views.book_history, name='book_history'),
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.create_book, name='create_book'),
    path('books/edit/<int:book_id>/', views.update_book, name='update_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('members/', views.member_list, name='member_list'),
    path('members/add/', views.create_member, name='create_member'),
    path('members/edit/<int:member_id>/', views.update_member, name='update_member'),
    path('members/delete/<int:member_id>/', views.delete_member, name='delete_member'),
    path('issues/', views.issue_list, name='issue_list'),
    path("update-issue/<int:record_id>/", views.update_issue_record, name="update_issue_record"),

]

