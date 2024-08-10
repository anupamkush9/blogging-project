from rest_framework import serializers
from .models import Blog_table

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog_table
        exclude = ['user_id']
