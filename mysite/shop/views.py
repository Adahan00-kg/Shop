from drf_yasg.openapi import ReferenceResolver
from rest_framework import viewsets, generics, status,permissions
from .models import *
from .serializers import *
from .filters import ProductFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .permission import *

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self,request,*args,**kwargs ):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        return Response({

            'user':{

                'email':user.email,
                'username':user.username,
                'token':str(token.access_token),
            }
        }, status=status.HTTP_201_CREATED
        )

class LogoutView(generics.GenericAPIView):
    def post(self,request,*args,**kwargs ):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail":"Невернные учетные данные "}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        response = HttpResponseRedirect(reverse('product_list'))
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend , SearchFilter , OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    ordering_fields = ['price','date']
    permission_classes = [CheckOwner]


    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)



class ProductListViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializers


class ProductPhotoViewSet(viewsets.ModelViewSet):
    queryset = ProductPhoto.objects.all()
    serializer_class = ProductPhotosSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UserProfileAllViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileAllSerializer



class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer


    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


    def retrieve(self, request,*args,**kwargs ):
        cart,created = Cart.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CarItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializers

    def get_queryset(self):
        return CarItem.objects.filter(user=self.request.user)


    def perform_create(self,serializer):
        cart,created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

