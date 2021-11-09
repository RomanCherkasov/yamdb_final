from django.urls import include, path
from rest_framework import routers
from users.views import RegistrationsAPIView, TokenSenderAPIView, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
auth_url = [path('signup/', RegistrationsAPIView.as_view()),
            path('token/', TokenSenderAPIView.as_view())]

app_name = 'users'
urlpatterns = [
    path('v1/auth/', include(auth_url)),
    path('v1/', include(router.urls))
]
