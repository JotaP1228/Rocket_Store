from rest_framework import  serializers
from .models import *

# Serializers define the API representation.
class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']


class ProductoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'inventario', 'categoria', 'foto']

    
class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    foto = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'password', 'rol', 'foto']

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        print("Datos recibidos por el backend:", request.data)  # Esto mostrará el contenido completo

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)


class CategoriaEtiquetaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CategoriaEtiqueta
        fields = ['id', 'nombre']

class SubCategoriaEtiquetaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubCategoriaEtiqueta
        fields = ['id', 'nombre', 'id_categoria_etiqueta']

class ProductoSubCategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductoSubCategoria
        fields = ['id', 'id_producto', 'id_sub_categoria_etiqueta']


class VentaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Venta
        fields = ['id', 'fecha_venta', 'usuario', 'ESTADOS', 'estado']

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['venta', 'producto', 'cantidad', 'precio_historico', 'id_usuario']

class ComentariosSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comentarios
        fields = ['id', 'comentario', 'descripcion', 'fecha_creacion', 'likes']