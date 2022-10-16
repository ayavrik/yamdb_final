from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'genres', views.GenreViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'titles', views.TitleViewSet)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='title_reviews'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='review_comments'
)
router.register(
    'users', views.UsersViewSet, basename='users_list'
)
urlpatterns = [
    path(
        'v1/auth/signup/',
        views.GetConfirmationCodeView.as_view(),
        name='signup'
    ),
    path('v1/auth/token/', views.GetJwtTokenView.as_view(), name='get_token'),
    path('v1/users/me/', views.CurrentUserView.as_view(), name='CurrentUser'),
    path('v1/', include(router.urls))
]
