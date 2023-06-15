from rest_framework.routers import SimpleRouter
from .views import OrderViewSet,  RegisterUserView, ItemViewSet
from rest_framework.authtoken import views
from django.urls import path

router = SimpleRouter(trailing_slash=False)

router.register('orders', OrderViewSet, basename='orders')
router.register('items', ItemViewSet, basename='items')

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('token-auth/', views.obtain_auth_token)
]
urlpatterns += router.urls