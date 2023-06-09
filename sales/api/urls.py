from rest_framework.routers import SimpleRouter
from .views import OrderViewSet, OrderItemViewSet
from rest_framework.authtoken import views
from django.urls import path
from rest_framework_nested import routers

router = SimpleRouter(trailing_slash=False)

# вложенные маршруты к заказам и рецептам заказа
# /order - all current user's Orders
# /orders/{pk} - show a order's detail via id
router.register('orders', OrderViewSet, basename='orders')
# /orders/{orders_pk}/item - all one order's items
orders_router = routers.NestedSimpleRouter(router, 'orders', lookup='orders')
# /order/{order_pk}/item/{item_pk} - детали рецепта по id рецепта
orders_router.register('item', OrderItemViewSet, basename='item')

urlpatterns = [
    path('token-auth/', views.obtain_auth_token)
]
urlpatterns += router.urls
urlpatterns += orders_router.urls