from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user

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
            username = username,
            password = password
            )
        if user:
            login_user(request, user)
            return Response({'message': 'Logged in Successfully'}, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid Username or Password'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
            return Response({'authenticate': request.user.is_authenticated }, status=200)



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
                return Response({'message': "Category matching query does not exist."}, status=status.HTTP_404_NOT_FOUND)
        Categories = Category.objects.all()
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
        serializer = CategorySerializer(instance=category, data=request.data)
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
            products = Product.objects.filter(category__name=request.GET.get('category', None))
        else:
            products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id):
        try:
            product = Product.objects.get(pk=int(id))
        except:
            return Response({'message': "Product matching query does not exist."}, status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
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