from rest_framework import serializers

from .fields import CategoryField, GenreField
from .models import Category, Comment, Genre, Review, Title, User


class UserConfirmCodeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['email']
        model = User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        ]
        model = User


class JWTRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializerGET(serializers.ModelSerializer):
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(
        read_only=True,
        required=False
    )

    class Meta:
        fields = '__all__'
        model = Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        lookup_field = 'slug'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        lookup_field = 'slug'
        model = Category


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate(self, attrs):
        author = self.context.get('request').user.id,
        title = self.context.get('view').kwargs.get('title_id')
        if (not self.instance
           and Review.objects.filter(title_id=title, author=author).exists()):
            raise serializers.ValidationError('error')
        return attrs

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
