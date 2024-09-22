from django.urls import path
from .views import *


urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),

    path('', ProductListViewSet.as_view({'get':'list','post':'create'}), name='product_list'),
    path('<int:pk>/', ProductViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'}), name='product_detail'),

    path('user', UserProfileAllViewSet.as_view({'get':'list','post':'create'}), name='user_list'),
    path('user/<int:pk>/', UserProfileAllViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'}), name='user_detail'),


    path('category', CategoryViewSet.as_view({'get':'list','post':'create'}), name='category_list'),
    path('category/<int:pk>/', CategoryViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'}), name='category_detail'),


    path('photo', ProductPhotoViewSet.as_view({'get':'list','post':'create'}), name='photo_list'),
    path('photo/<int:pk>/', ProductPhotoViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'}), name='photo_detail'),

    path('rating', RatingViewSet.as_view({'get':'list','post':'create'}), name='rating_list'),
    path('rating/<int:pk>/', RatingViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'}), name='rating_detail'),


    path('review', ReviewViewSet.as_view({'get':'list','post':'create'}), name='review_list'),
    path('review/<int:pk>/', ReviewViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'}), name='review_detail'),



    path('cart/',CartViewSet.as_view({'get':'retrieve'}), name='cart_list'),


    path('cart_items', CarItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='car_list'),
    path('cart_items/<int:pk>/', CarItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='car_detail'),

]