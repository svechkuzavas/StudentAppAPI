from django.urls import path, include
from rest_framework import routers
from .views import *

#router = routers.DefaultRouter()
#router.register(r'hello', HelloView)

urlpatterns = [
    #path('', include(router.urls)),
    path('hello/', HelloView.as_view())
]