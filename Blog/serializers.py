from rest_framework import serializers
from .models import Blog_table
from django.conf import settings


class BlogSerializer(serializers.ModelSerializer):
    # return absolute URL for image when request is available; otherwise return stored URL or None
    image = serializers.SerializerMethodField()

    class Meta:
        model = Blog_table
        exclude = ['user_id']

    def get_image(self, obj):
        # obj.image may be a FieldFile or empty
        if not obj.image:
            return None
        try:
            url = obj.image.url
        except Exception:
            return None

        request = self.context.get('request') if isinstance(self.context, dict) else None
        if request:
            return request.build_absolute_uri(url)

        # fallback to returning the relative URL
        return url
