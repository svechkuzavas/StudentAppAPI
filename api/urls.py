from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'user_profile', UserProfileViewSet)
router.register(r'register', UserCreateView)
router.register(r'reference', ReferenceViewSet)
router.register(r'article', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('hello/', HelloView.as_view())
]