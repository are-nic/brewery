from rest_framework.routers import SimpleRouter
from .views import ItemViewSet


router = SimpleRouter(trailing_slash=False)
router.register('items', ItemViewSet, basename='items')

urlpatterns = []
urlpatterns += router.urls