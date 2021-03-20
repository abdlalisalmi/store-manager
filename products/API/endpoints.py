from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.db.models import Q

import cloudinary

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, authentication, status

from .serializers import CategorySerializer, ProductSerializer
from ..models import Product, Category


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


# we use this class to login and check the user if she/he logged in.
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if not username or not password:
            return Response({'message': 'Please enter both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=username,
            password=password
        )
        if user:
            login_user(request, user)
            return Response({'message': 'Logged in Successfully'}, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid Username or Password'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({'authenticate': request.user.is_authenticated}, status=200)


class CategoryView(APIView):
    # authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, id=None):
        if id:
            try:
                category = Category.objects.get(pk=int(id))
                serializer = CategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({'message': "Category matching query does not exist."},
                                status=status.HTTP_404_NOT_FOUND)
        Categories = Category.objects.all().order_by('-id')
        serializer = CategorySerializer(Categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            category = Category.objects.get(pk=int(id))
        except:
            return Response({'message': "Category matching query does not exist."}, status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(instance=category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, id):
        try:
            category = Category.objects.get(pk=int(id))
            category.delete()
            return Response({'message': "Category Deleted Successfully"}, status.HTTP_200_OK)
        except:
            return Response({'message': "Category matching query does not exist."}, status.HTTP_404_NOT_FOUND)


class ProductView(APIView):
    # authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, id=None):
        if id:
            try:
                product = Product.objects.get(pk=int(id))
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({'message': "Product matching query does not exist."}, status=status.HTTP_404_NOT_FOUND)
        elif request.GET.get('category', None):
            products = Product.objects.filter(category=request.GET.get('category', None)).order_by('-id')
            if request.GET.get('page', None):
                page = request.GET.get('page', None)
                paginator = Paginator(products, 10)
                try:
                    products = paginator.page(page)
                except PageNotAnInteger:
                    products = paginator.page(1)
                except EmptyPage:
                    return Response([], status=status.HTTP_200_OK)

        else:
            products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name'].replace('"', '').replace('\\', '')
            serializer.validated_data['name'] = name
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            product = Product.objects.get(pk=int(id))
        except:
            return Response({'message': "Product matching query does not exist."}, status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid():
            # remove the old image from cloudinary
            if request.data.get('image', None):
                try:
                    cloudinary.api.delete_resources([product.image])
                except:
                    pass

            # remove some bad characters for the name
            name = serializer.validated_data['name'].replace('"', '').replace('\\', '')
            serializer.validated_data['name'] = name
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, id):
        try:
            product = Product.objects.get(pk=int(id))
            product.delete()
            return Response({'message': "product Deleted Successfully"}, status.HTTP_200_OK)
        except:
            return Response({'message': "product matching query does not exist."}, status.HTTP_404_NOT_FOUND)


class SearchView(APIView):
    # authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        category = request.GET.get('category', None)
        search = request.GET.get('search', None)
        if category and search:
            lookups = Q(category__exact=int(category), name__contains=search)
        elif category:
            lookups = Q(category__exact=category)
        elif search:
            lookups = Q(name__contains=search)
        else:
            return Response([], status=status.HTTP_200_OK)

        products = Product.objects.filter(lookups).order_by('-id')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
