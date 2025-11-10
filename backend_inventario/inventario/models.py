from django.db import models
from django.utils import timezone


# MODELO: BODEGA

class Bodega(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre



# MODELO: PRODUCTO

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    umbral_min = models.PositiveIntegerField(default=5)
    umbral_max = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"



# MODELO: INVENTARIO POR BODEGA

class InventarioBodega(models.Model):
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.bodega.nombre} | {self.producto.nombre}: {self.cantidad}"



# MODELO: MOVIMIENTOAS

class Movimiento(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    origen = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name="mov_salida")
    destino = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name="mov_entrada")
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.producto.nombre} ({self.cantidad}) de {self.origen} a {self.destino}"

    def aplicar_movimiento(self):
        inv_origen, _ = InventarioBodega.objects.get_or_create(bodega=self.origen, producto=self.producto)
        inv_destino, _ = InventarioBodega.objects.get_or_create(bodega=self.destino, producto=self.producto)

        inv_origen.cantidad = max(inv_origen.cantidad - self.cantidad, 0)
        inv_destino.cantidad += self.cantidad

        inv_origen.save()
        inv_destino.save()

        Alerta.verificar_alerta(inv_origen)
        Alerta.verificar_alerta(inv_destino)



#ALERTAS
#
class Alerta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20)  # “Bajo stock” o “Sobre stock”
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.fecha.strftime('%d-%m-%Y %H:%M')} - {self.tipo} - {self.producto.nombre}"

    @staticmethod
    def verificar_alerta(inventario):
        producto = inventario.producto
        bodega = inventario.bodega
        cantidad = inventario.cantidad

        # Eliminar alertas anteriores
        Alerta.objects.filter(producto=producto, bodega=bodega).delete()

        # Gener nuevas alertas
        if cantidad <= producto.umbral_min:
            Alerta.objects.create(producto=producto, bodega=bodega, tipo="Bajo stock")
        elif cantidad >= producto.umbral_max:
            Alerta.objects.create(producto=producto, bodega=bodega, tipo="Sobre stock")
