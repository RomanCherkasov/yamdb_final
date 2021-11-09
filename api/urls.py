from api.views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                       ReviewViewSet, TitlesViewSet)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'titles', TitlesViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'genres', GenresViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='review')
router.register(r'titles/(?P<title_id>\d+)/reviews/'
                r'(?P<review_id>\d+)/comments',
                CommentViewSet, basename='comment')


urlpatterns = [
    path('v1/', include(router.urls)),
]
