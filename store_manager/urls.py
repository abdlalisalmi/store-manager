from django.contrib import admin
from django.urls import path, include

from .views import homePage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("products.urls")),
    path('', homePage, name='home'),
]
