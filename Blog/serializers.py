from rest_framework import serializers
from .models import Blog_table
from django.conf import settings


class BlogSerializer(serializers.ModelSerializer):
    # writable ImageField: accepts uploads and returns URL when request context is present
    image = serializers.ImageField(use_url=True, allow_null=True, required=False)

    class Meta:
        model = Blog_table
        exclude = ['user_id']
