from django.urls import path
from . import views



urlpatterns=[
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logut',views.logout_page,name='logout'),
    path('addtocart',views.add_to_cart,name='addtocart'),
    path('remove_cart/<str:cid>',views.remove_cart,name='remove_cart'),
    path('view_cart',views.view_cart,name='view_cart'),
    path('fav_page',views.fav_page,name='fav_page'),
    path('collections',views.collections,name='collections'),
    path('collections_view/<str:name>',views.collections_view,name='collections_view'),
    path('collections/<str:cname>/<str:pname>/', views.product_details, name='product_details'),
    path('view_fav',views.view_fav,name='view_fav'),
    path('remove_from_fav/', views.remove_from_fav, name='remove_from_fav'),
]


