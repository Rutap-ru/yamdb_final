from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    AuthTokenJwt,
    UserConfirmCodeViewSet,
    UserViewSet,
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
    ReviewViewSet,
    CommentViewSet
)

router_v1 = DefaultRouter()
router_v1.register('auth/email', UserConfirmCodeViewSet)
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('titles', TitleViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('auth/token/', AuthTokenJwt.as_view()),
    path('', include(router_v1.urls)),
]
