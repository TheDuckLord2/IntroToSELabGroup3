from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView
from .views import CartView
from .views import StaticDataView
from .views import LoginView
from . import views

router = DefaultRouter()
#router.register(r'users', UserCreationView) #this is sign up
#router.register(r'cart', CartView, basename = 'cart') #this is cart
#router.register(r'products', ProductViewSet) #Products view
#router.register(r'register', RegisterView) #this is login


urlpatterns = [
    path('', include(router.urls)),
    path('data/', StaticDataView.as_view(), name='html_data'),
    path('home/', views.gethome, name='home'),
    path('contact/', views.getcontact, name='contact'),
    path('about/', views.getabout, name='about'),
    path('admin/', views.admin_dashboard, name='admin'),
    path('base/', views.getbase, name='base'),
    path('cart/', views.getcart, name='cart_html'),
    path('cart/', views.getcart, name='cart'),
    path('cart/', CartView.as_view({'get': 'list'}), name='cart_api'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('register/', RegisterView.as_view(), name='register'),
    path('product/', views.products_view, name='product'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/', include(router.urls)),
    path('new-product/', views.new_product, name='new_product'),
    path('manage/update/<int:item_id>/', views.update_storestock, name='update_storestock'),
    path('manage/remove/<int:item_id>/', views.remove_from_storestock, name='remove_from_storestock'),
    path('manage/', views.manage_products_view, name='manage'),
    path('approve_product/<int:item_id>/', views.approve_product, name='approve_product'),
    path('reject_product/<int:item_id>/', views.reject_product, name='reject_product'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('compare/', views.compare_products_view, name='compare_products'),
    path('delete_account/', views.delete_account, name='delete_account'),

]
