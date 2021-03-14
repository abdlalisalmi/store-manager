from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .API.endpoints import LoginView, LogoutView, CategoryView, ProductView

app_name = 'products'
urlpatterns = [
    path('api/login/', obtain_auth_token, name="obtain_auth_token"),
    # path('api/logout/', LogoutView.as_view(), name="LogoutAPI"),

    path('api/categories/', CategoryView.as_view(), name="CategoriesAPI"),
    path('api/categories/<int:id>/', CategoryView.as_view(), name="OneCategoriesAPI"),

    path('api/products/', ProductView.as_view(), name="ProductsAPI"),
    path('api/products/<int:id>/', ProductView.as_view(), name="OneProductsAPI"),

]
