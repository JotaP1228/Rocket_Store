from django.contrib.auth.models import AbstractUser
from .authentication import CustomUserManager
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.

class Usuario(AbstractUser):
	username = None
	nombre = models.CharField(max_length=254)
	email = models.EmailField(max_length=254, unique=True)
	image = models.ImageField(upload_to='edite_profile', null=True, blank=True)
	ROLES = (
		(1, "Administrador"),
		(2, "Despachador"),
		(3, "Cliente"),
	)
	rol = models.IntegerField(choices=ROLES, default=3)
	foto = models.ImageField(upload_to="fotos/", default="fotos/default.png", blank=True)
	token_recuperar = models.CharField(max_length=254, default="", blank=True, null=True)
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["nombre"]
	objects = CustomUserManager()

	def __str__(self):
		return self.nombre

class Categoria(models.Model):
	nombre = models.CharField(max_length=254)
	descripcion = models.TextField()
 

	def __str__(self):
		return self.nombre


class CategoriaEtiqueta(models.Model):
	nombre = models.CharField(max_length=254, unique=True)

	def __str__(self):
		return self.nombre
	
class SubCategoriaEtiqueta(models.Model):
	nombre = models.CharField(max_length=254)
	id_categoria_etiqueta = models.ForeignKey(CategoriaEtiqueta, on_delete=models.DO_NOTHING)

	def __str__(self):
		return self.nombre
	

class Producto(models.Model):
	nombre = models.CharField(max_length=254)
	informacion = models.CharField(max_length=254)
	precio = models.IntegerField()
	inventario = models.IntegerField()
	fecha_creacion = models.DateField()
	categoria = models.ForeignKey(CategoriaEtiqueta,on_delete=models.CASCADE)
	foto = models.ImageField(upload_to="fotos_productos/", default="fotos_productos/default.png")

	def __str__(self):
		return self.nombre


class ProductoSubCategoria(models.Model):
	id_producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
	id_sub_categoria_etiqueta = models.ForeignKey(SubCategoriaEtiqueta, on_delete=models.DO_NOTHING)

	def __str__(self):
		return f'{self.id_producto}, {self.id_sub_categoria_etiqueta}'

class Venta(models.Model):
	fecha_venta = models.DateTimeField(auto_now=True)
	usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
	ESTADOS = (
		(1, 'Pendiente'),
		(2, 'Pagada'),
		(3, 'Rechazada'),
		(4, 'Enviado'),
	)
	estado = models.IntegerField(choices=ESTADOS, default=1)
	motivo_rechazo = models.TextField(blank=True, null=True)

	def __str__(self):
		return f"{self.id} - {self.usuario}"


class DetalleVenta(models.Model):
	venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING)
	producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
	cantidad = models.IntegerField()
	precio_historico = models.IntegerField()
	id_usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

	def __str__(self):
		
		return f"{self.id} - {self.venta}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Devoluciones(models.Model):
    nombre = models.CharField(max_length=254)
    email = models.EmailField(max_length=254, unique=True)
    telefono = models.IntegerField()
    descripcion = models.TextField()
    estado = models.IntegerField(choices=[(1, 'Pendiente'), (2, 'Aceptada'), (3, 'Rechazada')], default=1)
    image = models.ImageField(upload_to='devoluciones/', null=True, blank=True)

    def __str__(self):
        return self.nombre
	
class Comentarios(models.Model):
    comentarios = models.TextField()
    descripcion = models.TextField()
    fecha_creacion = models.DateField(null=True, blank=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.comentarios


class CarouselItem(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='carousel/')
    

    def __str__(self):
        return self.titulo   
	
class Tallas(models.Model):    
	talla = models.CharField(max_length=254)
 
	def __str__(self):
    		return self.talla
	
class ProductoTallas(models.Model):
	id_producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
	id_talla = models.ForeignKey(Tallas, on_delete=models.DO_NOTHING)
 
	def __str__(self):
    		return self.nombre