from rest_framework.routers import SimpleRouter
from warehouse.api.views import ItemViewSet


router = SimpleRouter(trailing_slash=False)
router.register('items', ItemViewSet, basename='items')
urlpatterns = []
urlpatterns += router.urls