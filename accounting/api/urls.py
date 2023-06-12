from rest_framework.routers import SimpleRouter
from .views import SalaryViewSet
from rest_framework.authtoken import views
from django.urls import path

router = SimpleRouter(trailing_slash=False)
router.register('salary', SalaryViewSet, basename='salary')

urlpatterns = [
    path('token-auth/', views.obtain_auth_token)
]
urlpatterns += router.urls