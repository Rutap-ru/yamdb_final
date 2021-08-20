from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import EMAIL_FOR_MAILING

from .filters import TitleFilter
from .mixins import DeleteViewSet
from .models import Title, Genre, Category, User, Review
from .permissions import IsAdminRole, IsAdminOrReadOnly, IsAuthorOrStaff
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    JWTRequestSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleSerializerGET,
    UserSerializer,
    UserConfirmCodeSerializer
)


class UserConfirmCodeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserConfirmCodeSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        confirmation_code = get_random_string(length=32)
        data_validated = serializer.validated_data
        user_email = data_validated.get('email')
        serializer.save(
            password=confirmation_code,
            username=user_email,
        )
        send_mail(
            'confirmation_code',
            confirmation_code,
            EMAIL_FOR_MAILING,
            [user_email],
            fail_silently=False,
        )


class AuthTokenJwt(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = JWTRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            confirmation_code = serializer.validated_data['confirmation_code']
            user = get_object_or_404(
                User,
                email=email,
                password=confirmation_code
            )
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            return Response({'token': token})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    filterset_fields = ('email',)
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    @action(
        detail=False, methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('id')
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'patch']:
            return TitleSerializerGET
        return TitleSerializer


class GenreViewSet(DeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ('name', 'slug')
    lookup_field = 'slug'
    pagination_class = PageNumberPagination


class CategoryViewSet(DeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ('name', 'slug')
    lookup_field = 'slug'
    pagination_class = PageNumberPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrStaff]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        data = {
            'title': title,
            'author': self.request.user
        }
        serializer.save(**data)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrStaff]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        queryset = review.comments.all()
        return queryset
