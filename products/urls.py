from django.urls import path

from .API.endpoints import LoginView, LogoutView, CategoryView, ProductView

app_name = 'products'
urlpatterns = [
    path('api/login/', LoginView.as_view(), name="LoginAPI"),
    path('api/logout/', LogoutView.as_view(), name="LogoutAPI"),

    path('api/categories/', CategoryView.as_view(), name="CategoriesAPI"),
    path('api/categories/<int:id>/', CategoryView.as_view(), name="OneCategoriesAPI"),

    path('api/products/', ProductView.as_view(), name="ProductsAPI"),
    path('api/products/<int:id>/', ProductView.as_view(), name="OneProductsAPI"),

]
