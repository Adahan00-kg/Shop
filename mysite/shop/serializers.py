from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ( 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетаные данные ")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")


class ReviewSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer()
    created_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    class Meta:
        model =  Review
        fields = ['id','author','text','created_date']
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']

class RatingSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Rating
        fields = ['user','stars']

class ProductPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ['photo']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    ratings = RatingSerializer(read_only=True,many=True)
    reviews = ReviewSerializer(read_only=True,many=True)
    product = ProductPhotosSerializer(read_only=True,many=True)
    date = serializers.DateTimeField(format='%d-%m-%Y')
    average_rating = serializers.SerializerMethodField()
    owner = UserProfileSerializer()
    class Meta:
        model = Product
        fields = ['id','product_name','category','description','average_rating','price','video',
                  'ratings','reviews','active','date', 'product','owner']

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class UserProfileAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class ProductListSerializers(serializers.ModelSerializer):
    category = CategorySerializer()
    product = ProductPhotosSerializer(read_only=True,many=True)
    class Meta:
        model = Product
        fields = ['id','product_name','category','product','price','date']


class CartItemSerializers(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = CarItem
        fields = ['id','product','product_id','quantity','get_total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializers(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['user','items','total_price']


    def get_total_price(self, obj):
        return obj.get_total_price()