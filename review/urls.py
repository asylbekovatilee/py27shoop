from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentSerializer, FavoriteSerializer, CommentViewSet, FavoriteViewSet, AddRatingAPIView

router = DefaultRouter()
router.register("comments", CommentViewSet)
router.register("favorites", FavoriteViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("rating/ ", AddRatingAPIView.as_view()),
]