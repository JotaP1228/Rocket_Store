from django.contrib import admin
from django.utils.html import mark_safe
from .models import *

# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	list_display = ["id", "nombre", "descripcion"]
	search_fields = ["nombre"]


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
	list_display = ["id", "nombre", "precio", "inventario", "fecha_creacion", "categoria", 'foto', 'ver_foto','informacion']
	search_fields = ["nombre"]
	list_filter = ["categoria", "fecha_creacion"]
	list_editable = ["categoria",'informacion']

	def ver_foto(self, obj):
		return mark_safe(f"<a href='{obj.foto.url}'><img src='{obj.foto.url}' width='25%'></a>")


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre', 'nombre_en_plural', 'email', 'password', 'rol', 'foto', 'ver_foto']

	def nombre_en_plural(self, obj):
		return mark_safe(f"<span style='color:red'>{obj.nombre}'s<span>")

	def ver_foto(self, obj):
		return mark_safe(f"<a href='{obj.foto.url}'><img src='{obj.foto.url}' width='15%'></a>")
	


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'venta', 'producto', 'cantidad', 'precio_historico', 'subtotal']

    def subtotal(self, obj):
        return f"{obj.cantidad * obj.precio_historico}"
    
    
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
	list_display = ['id', 'fecha_venta', 'usuario']


@admin.register(CategoriaEtiqueta)
class CategoriaEtiquetaAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre']


@admin.register(SubCategoriaEtiqueta)
class SubCategoriaEtiquetaAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre', 'id_categoria_etiqueta']


@admin.register(ProductoSubCategoria)
class ProductoSubCategoriaAdmin(admin.ModelAdmin):
	list_display = ['id', 'id_producto', 'id_sub_categoria_etiqueta']

@admin.register(Comentarios)
class Comentarios(admin.ModelAdmin):
	list_display = ["id", "comentarios", "descripcion", "fecha_creacion"]

@admin.register(Devoluciones)
class Devoluciones(admin.ModelAdmin):
	list_display = ["id", "nombre", "email", "telefono", "descripcion", "estado"]

@admin.register(CarouselItem)
class CarouselItem(admin.ModelAdmin):
    list_display = ['titulo','descripcion','imagen']

@admin.register(Tallas)
class TallasAdmin(admin.ModelAdmin):
    list_display = ['id', 'talla']