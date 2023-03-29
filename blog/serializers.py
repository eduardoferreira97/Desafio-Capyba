from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post

        fields = ['id', 'title', 'sub_title', 'text', 'author']

        author = serializers.StringRelatedField()

    def validate_title(self, value):

        title = value

        if len(title) < 5:
            raise serializers.ValidationError(
                'Precisa ter pelo menos 5 caracteres.')

        return title

    def validate(self, attrs):
        super_validate = super().validate(attrs)

        sub_title = attrs.get('sub_title')
        title = attrs.get('title')

        if sub_title == title:

            raise serializers.ValidationError({
                "sub_title": ["Não pode ser igual ao título"]
            })

        return super_validate
