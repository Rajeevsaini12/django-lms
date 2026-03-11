from rest_framework import serializers
from .models import Book, Member, IssueRecord


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class IssueRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueRecord
        fields = "__all__"