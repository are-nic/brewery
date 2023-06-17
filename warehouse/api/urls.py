from rest_framework.routers import SimpleRouter
from .views import ItemViewSet
from rest_framework.authtoken import views
from django.urls import path

router = SimpleRouter(trailing_slash=False)
router.register('items', ItemViewSet, basename='items')

urlpatterns = [
    path('token-auth/', views.obtain_auth_token, name='token')
]
urlpatterns += router.urls