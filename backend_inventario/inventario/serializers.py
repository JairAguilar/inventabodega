from rest_framework import serializers
from .models import Producto, Bodega, InventarioBodega, Alerta, Movimiento

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodega
        fields = '__all__'

class InventarioSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    bodega = BodegaSerializer()

    class Meta:
        model = InventarioBodega
        fields = '__all__'

class AlertaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    bodega = BodegaSerializer()

    class Meta:
        model = Alerta
        fields = '__all__'
