from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import Base, Home, PRODUCT_DETAILS
from app import views

# from django.conf import Settings
# from django.conf.urls.static import static


urlpatterns = [
    # error
    path('404', views.Error404, name='404'),

    path('base/', Base, name='base'),
    path('', Home, name='home'),
    path('about/', views.About, name='about'),
    path('contact/', views.Contact, name='contact'),
    path('product/', views.PRODUCTS, name='product'),
    path('product/filter-data',views.filter_data,name="filter-data"),

    # path('Prof/', Prof, name='Prof'),
    # path('update/<id>/', update, name='update'),
    # path('delete/<id>/', delete, name='delete'),
    # #path('search/', search, name='search'),

    path('product/<slug:slug>', views.PRODUCT_DETAILS, name="product_detail"),

    # account urls
    path('account/my-account', views.My_Account, name='my_account'),
    path('account/register', views.Register, name='handelregister'),
    path('account/login', views.Login, name='handlelogin'),
    path('account/profile',views.Profile, name='profile'),
    path('account/profile/update',views.Profile_Update, name='profile_update'),

    # cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    path('checkout/', views.Checkout, name='checkout'),


] +static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)