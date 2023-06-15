from rest_framework.routers import SimpleRouter
from .views import OrderItemViewSet
from rest_framework.authtoken import views
from django.urls import path

router = SimpleRouter(trailing_slash=False)
router.register('order_items', OrderItemViewSet, basename='order_item')

urlpatterns = [
    path('token-auth/', views.obtain_auth_token)
]
urlpatterns += router.urls