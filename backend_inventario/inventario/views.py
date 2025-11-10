from rest_framework import viewsets
from .models import Producto, Bodega, InventarioBodega, Movimiento, Alerta
from .serializers import (ProductoSerializer,BodegaSerializer,InventarioSerializer,AlertaSerializer
)


# vista api pal react

# Productos
class ProductoViewSet(viewsets.ModelViewSet):
    """
    Permite listar, crear, editar o eliminar productos.
    Endpoint: /api/productos/
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


# Bodegas
class BodegaViewSet(viewsets.ModelViewSet):
    """
    Permite administrar las bodegas (crear, listar, editar, eliminar).
    Endpoint: /api/bodegas/
    """
    queryset = Bodega.objects.all()
    serializer_class = BodegaSerializer


# Inventario (producto por bodega)
class InventarioViewSet(viewsets.ModelViewSet):
    """
    Muestra la relación producto --bodega-cantidad.
    Endpoint: /api/inventario/
    """
    queryset = InventarioBodega.objects.all()
    serializer_class = InventarioSerializer


# Alertas pal stock
class AlertaViewSet(viewsets.ModelViewSet):
    """
    alertas generadas por bajo o sobre stock.  #funca to god
    Endpoint: /api/alertas/
    """
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer


# (Opcional) Vista para probar el movimiento entre bodegas por API en el futuro
# class MovimientoViewSet(viewsets.ModelViewSet):
#     queryset = Movimiento.objects.all()
#     serializer_class = MovimientoSerializer
