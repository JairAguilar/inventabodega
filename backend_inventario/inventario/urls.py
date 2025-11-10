from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, BodegaViewSet, InventarioViewSet, AlertaViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'bodegas', BodegaViewSet)
router.register(r'inventario', InventarioViewSet)
router.register(r'alertas', AlertaViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
