from rest_framework import serializers
from blog.models import Post, Comment

# первый способ создать сериализатор
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance


# второй способ создать сериализатор(в классе-родители 
# уже реализованы методы create() и update())
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "author",
            "title",
            "body",
            "created",
            "status",
            "slug",
        )
        model = Post