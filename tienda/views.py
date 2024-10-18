from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from rest_framework import viewsets 
from .serializers import *
# Para tomar el from desde el settings
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
import re
from .crypt import *
from django.utils import timezone
from .forms import ImageUploadForm

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# Importamos todos los modelos de la base de datos
from .models import *
from .decorador_especial import *
from django.shortcuts import render



# Create your views here.

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
class CategoriaEtiquetaViewSet(viewsets.ModelViewSet):
    queryset = CategoriaEtiqueta.objects.all()
    serializer_class = CategoriaEtiquetaSerializer

class SubCategoriaEtiquetaViewSet(viewsets.ModelViewSet):
    queryset = SubCategoriaEtiqueta.objects.all()
    serializer_class = SubCategoriaEtiquetaSerializer
    
class ComentariosViewSet(viewsets.ModelViewSet):
    queryset = Comentarios.objects.all()
    serializer_class = ComentariosSerializer

class ProductoSubCategoriaViewSet(viewsets.ModelViewSet):
    queryset = ProductoSubCategoria.objects.all()
    serializer_class = ProductoSubCategoriaSerializer
    
class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    
class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

    def perform_create(self, serializer):
        serializer.save()
    
def index(request):
	logueo = request.session.get("logueo", False)

	if logueo == False:
		return render(request, "tienda/login/login.html")
	else:
		return redirect("inicio")
	
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class CategoriaViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = Categoria.objects.all()
	serializer_class = CategoriaSerializer


from rest_framework.parsers import MultiPartParser, FormParser
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    parser_classes = [MultiPartParser, FormParser]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        print("Datos recibidos por el backend:", request.data)  # Verifica los datos del archivo

        # Verifica si hay un archivo en 'foto'
        if 'foto' in request.data:
            print("Archivo recibido:", request.data['foto'])
        else:
            print("No se recibió ningún archivo en 'foto'")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


def registrar_usuario(request):
	if request.method == "POST":
		nombre = request.POST.get("nombre")
		correo = request.POST.get("correo")
		clave1 = request.POST.get("clave1")
		clave2 = request.POST.get("clave2")
		switch = request.POST.get("switchTyC")
		if switch:
			if not nombre or not correo:
				messages.warning(request,"Campos vacios, ingrese datos!!")
				return redirect("inicio")
			if not re.match(r"^[a-zA-Z\s]+$", nombre):
				messages.error(request, f"El nombre solo puede llevar valores alfabeticos")
			if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", correo):
				messages.error(request, f"El correo ingresado no es valido")
			if clave1 == clave2:
				q = Usuario(
				nombre=nombre,
				email=correo,
				password=hash_password(clave1)
				)
				q.save()
				messages.success(request, "Usuario registrado correctamente!!")
				return redirect("inicio")
			else:
				messages.warning(request, "No concuerdan las contraseñas")
				return redirect("inicio")
		else:
			messages.error(request, "Debe aceptar los terminos y condiciones")
			return redirect("inicio")
	else:
		return redirect("inicio")
#-------------------
@admin_requerido
def usuarios(request):
	q = Usuario.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/usuarios/usuarios.html", contexto)


@admin_requerido
def usuarios_form(request):
    roles = Usuario.ROLES
    return render(request, "tienda/usuarios/usuarios_form.html", {"roles": roles})

@admin_requerido
def usuarios_crear(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        password = request.POST.get("password")
        rol = request.POST.get("rol")

        if not re.match(r"^[a-zA-Z\s]+$", nombre):
            messages.error(request, "El nombre solo puede llevar valores alfabéticos")
            return redirect("usuarios_listar")

        try:
            q = Usuario(
                nombre=nombre,
                email=email,
                rol=rol
            )
            q.set_password(password)
            q.save()
            messages.success(request, "Guardado correctamente!!")
        except Exception as e:
            messages.error(request, f"Error: {e}")

        return redirect("usuarios_listar")
    else:
        messages.warning(request, "Error: No se enviaron datos...")
        return redirect("usuarios_listar")

@admin_requerido_id
def usuarios_eliminar(request, id):
    try:
        usuario = get_object_or_404(Usuario, pk=id)

        ventas_pendientes = Venta.objects.filter(usuario=usuario, estado__in=[1, 2]).exists()

        if ventas_pendientes:
            messages.error(request, "Error al eliminar: el usuario tiene pedidos pendientes")
            return redirect("usuarios_listar")

        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente!!")

    except Exception as e:
        messages.error(request, f"Error al eliminar: {str(e)}")

    return redirect("usuarios_listar")

@admin_requerido_id
def usuarios_formulario_editar(request, id):
    print(f"ID del usuario que se intenta editar: {id}")  # Agrega esta línea
    try:
        q = Usuario.objects.get(pk=id)
        roles = Usuario.ROLES
        contexto = {"data": q, "roles": roles}
        return render(request, "tienda/usuarios/usuarios_formulario_editar.html", contexto)
    except Usuario.DoesNotExist:
        messages.error(request, "El usuario no existe.")
        return redirect("usuarios_listar")

@admin_requerido
def usuarios_actualizar(request):
    if request.method == "POST":
        id = request.POST.get("id") 
        try:
            q = Usuario.objects.get(pk=id)
            # Actualiza los campos del usuario
            q.nombre = request.POST.get("nombre")
            q.email = request.POST.get("email")
            q.rol = request.POST.get("rol")
            password = request.POST.get("password")
            
            if password:
                q.set_password(password)
            
            q.save()
            messages.success(request, "Usuario actualizado correctamente!!")
        except Usuario.DoesNotExist:
            messages.error(request, "El usuario no existe.")
    
    return redirect("usuarios_listar")

#---------------

from django.shortcuts import render, redirect
from django.contrib import messages
import re
from .models import Usuario

from django.shortcuts import redirect

def login(request):
	if request.method == "POST":
		user = request.POST.get("email")
		passw = request.POST.get("password")
		switch = request.POST.get("switchTyC")
		# select * from Usuario where correo = "user" and clave = "passw"
		if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", user):
			messages.error(request, f"El correo ingresado no es valido")
		if switch:
			try:
				q = Usuario.objects.get(email=user)
				if verify_password(passw, q.password):
				# Crear variable de sesión
					request.session["logueo"] = {
						"id": q.id,
						"nombre": q.nombre,
						"rol": q.rol,
						"nombre_rol": q.get_rol_display()
					}
					request.session["carrito"] = []
					request.session["items"] = 0
					messages.success(request, f"Bienvenido {q.nombre}!!")
				return redirect("inicio")
			except Exception as e:
				messages.error(request, f"{e} Error: Usuario o contraseña incorrectos...")
				return redirect("inicio")
		else:
			messages.error(request, "Debe aceptar los terminos y condiciones")
			return redirect('inicio')

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("inicio")


def logout(request):
	try:
		del request.session["logueo"]
		del request.session["carrito"]
		del request.session["items"]
		messages.success(request, "Sesión cerrada correctamente!")
		return redirect("inicio")
	except Exception as e:
		messages.warning(request, "No se pudo cerrar sesión...")
		return redirect("")


def inicio(request):
    logueo = request.session.get("logueo", False)

    carousel_items = CarouselItem.objects.all()
    tallas = Tallas.objects.all()
    proTallas = ProductoTallas.objects.select_related('id_talla', 'id_producto')
    categorias = CategoriaEtiqueta.objects.all()
    
    etq_categorias = []
    for categoria in categorias:
        sub_etiquetas = SubCategoriaEtiqueta.objects.filter(id_categoria_etiqueta=categoria)
        etq_categorias.append(sub_etiquetas)

    # Obtener los parámetros de filtro
    cat_id = request.GET.get("cat")
    etq_seleccionadas = request.POST.getlist("etqSeleccionadas")

    # Inicializa la consulta de productos
    productos = Producto.objects.all()

    # Filtrar por categoría
    if cat_id:
        categoria_seleccionada = get_object_or_404(CategoriaEtiqueta, pk=cat_id)
        productos = productos.filter(categoria=categoria_seleccionada)

    # Filtrar por etiquetas
    if etq_seleccionadas:
        productos = productos.filter(productosubcategoria__id_sub_categoria_etiqueta__in=etq_seleccionadas).distinct()

    contexto = {
        "data": productos,
        "cat": categorias,
        "etq": etq_categorias,
        "tallas": tallas,
        "proTallas": proTallas,
        "carousel_items": carousel_items,
    }
    return render(request, "tienda/inicio/inicio.html", contexto)
	
def recuperar_clave(request):
	if request.method == "POST":
		email = request.POST.get("correo")
		try:
			q = Usuario.objects.get(email=email)
			from random import randint
			import base64
			token = base64.b64encode(str(randint(100000, 999999)).encode("ascii")).decode("ascii")
			print(token)
			q.token_recuperar = token
			q.save()
			# enviar correo de recuperación
			destinatario = email
			mensaje = f"""
					<h1 style='color:blue;'>Tienda virtual</h1>
					<p>Usted ha solicitado recuperar su contraseña, haga clic en el link y digite el token.</p>
					<p>Token: <strong>{token}</strong></p>
					<a href='http://127.0.0.1:8000/tienda/verificar_recuperar/?correo={email}'>Recuperar...</a>
					"""
			try:
				msg = EmailMessage("Tienda ADSO", mensaje, settings.EMAIL_HOST_USER, [destinatario])
				msg.content_subtype = "html"  # Habilitar contenido html
				msg.send()
				messages.success(request, "Correo enviado!!")
			except BadHeaderError:
				messages.error(request, "Encabezado no válido")
			except Exception as e:
				messages.error(request, f"Error: {e}")
			# fin -
		except Usuario.DoesNotExist:
			messages.error(request, "No existe el usuario....")
		return redirect("recuperar_clave")
	else:
		return render(request, "tienda/login/recuperar.html")


def verificar_recuperar(request):
	if request.method == "POST":
		if request.POST.get("check"):
			# caso en el que el token es correcto
			email = request.POST.get("correo")
			q = Usuario.objects.get(email=email)

			c1 = request.POST.get("nueva1")
			c2 = request.POST.get("nueva2")

			if c1 == c2:
				# cambiar clave en DB
				q.password = hash_password(c1)
				q.token_recuperar = ""
				q.save()
				messages.success(request, "Contraseña guardada correctamente!!")
				return redirect("index")
			else:
				messages.info(request, "Las contraseñas nuevas no coinciden...")
				return redirect("verificar_recuperar")+"/?correo="+email
		else:
			# caso en el que se hace clic en el correo-e para digitar token
			email = request.POST.get("correo")
			token = request.POST.get("token")
			q = Usuario.objects.get(email=email)
			if (q.token_recuperar == token) and q.token_recuperar != "":
				contexto = {"check": "ok", "correo":email}
				return render(request, "tienda/login/verificar_recuperar.html", contexto)
			else:
				messages.error(request, "Token incorrecto")
				return redirect("verificar_recuperar")	# falta agregar correo como parametro url
	else:
		correo = request.GET.get("correo")
		contexto = {"correo":correo}
		return render(request, "tienda/login/verificar_recuperar.html", contexto)


from .decorador_especial import *






@admin_requerido
def categorias(request):
	q = CategoriaEtiqueta.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/categorias/categorias.html", contexto)

@admin_requerido
def categorias_form(request):
	return render(request, "tienda/categorias/categorias_form.html")

@admin_requerido
def categorias_crear(request):
	if request.method == "POST":
		nomb = request.POST.get("nombre")
		if not re.match(r"^[a-zA-Z\s]+$", nomb):
			messages.error(request, f"El nombre solo puede llevar valores alfabeticos")
		try:
			q = CategoriaEtiqueta(
				nombre=nomb,
			)
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
		return redirect("categorias_listar")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("categorias_listar")

@admin_requerido_id
def categorias_eliminar(request, id):
	try:
		q = CategoriaEtiqueta.objects.get(pk=id)
		q.delete()
		messages.success(request, "Categoría eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: Hay productos asociados a esa categoria")

	return redirect("categorias_listar")

@admin_requerido_id
def categorias_formulario_editar(request, id):
	q = CategoriaEtiqueta.objects.get(pk=id)
	contexto = {"data": q}
	return render(request, "tienda/categorias/categorias_formulario_editar.html", contexto)

@admin_requerido
def categorias_actualizar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nomb = request.POST.get("nombre")
		desc = request.POST.get("descripcion")

		try:
			q = CategoriaEtiqueta.objects.get(pk=id)
			q.nombre = nomb
			q.descripcion = desc
			q.save()
			messages.success(request, "Categoría actualizada correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect("categorias_listar")


@admin_requerido
def productos(request):
    q = Producto.objects.all()
    proTallas = ProductoTallas.objects.select_related('id_talla', 'id_producto')
    
    productos = []
    
    for i in q:
        producto = {
            'nombre': i.nombre,
            'id': i.id,
            'etiqueta': [],
            'precio': i.precio,
            'informacion': i.informacion,
            'inventario': i.inventario,
            'fecha_creacion': i.fecha_creacion,
            'categoria': i.categoria,
            'tallas': []
        }

        x = ProductoSubCategoria.objects.all()
        for y in x:
            if i.id == y.id_producto.id:
                tag = SubCategoriaEtiqueta.objects.get(pk=y.id_sub_categoria_etiqueta.id)
                producto["etiqueta"].append(tag)

        for pt in proTallas:
            if pt.id_producto.id == i.id:
                producto['tallas'].append(pt.id_talla.talla)

        productos.append(producto)

    contexto = { 
        "data": productos
    }

    return render(request, "tienda/productos/productos.html", contexto)


@admin_requerido
def productos_form(request):
	q = CategoriaEtiqueta.objects.all()
	e = SubCategoriaEtiqueta.objects.all()
	t = Tallas.objects.all()
	contexto = {"data": q, "etiqueta": e, "talla":t}
	return render(request, "tienda/productos/productos_form.html", contexto)

@admin_requerido
def productos_crear(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        precio = request.POST.get("precio")
        informacion = request.POST.get("informacion")
        inventario = request.POST.get("inventario")
        fecha_creacion = request.POST.get("fecha_creacion")
        categoria_id = request.POST.get("categoria")
        etiquetas = request.POST.getlist("etiqueta")
        tallas = request.POST.getlist("talla")
        foto = request.FILES.get("foto")

        # Función para validar si un campo está vacío
        def validar_campo_vacio(campo, nombre_campo):
            if not campo:
                messages.error(request, f"El campo {nombre_campo} no puede estar vacío.")
                return False
            return True

        # Validaciones
        if not validar_campo_vacio(nombre, "Nombre") or not validar_campo_vacio(precio, "Precio") or not validar_campo_vacio(inventario, "Inventario") or not validar_campo_vacio(fecha_creacion, "Fecha de creación") or not validar_campo_vacio(categoria_id, "Categoría") or not validar_campo_vacio(foto, "Foto"):
            return redirect("productos_form")

        # Validar que no contenga caracteres especiales ni números negativos
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            messages.error(request, "El nombre solo puede contener letras y espacios.")
            return redirect("productos_form")

        if not re.match(r'^\d+(\.\d{1,2})?$', precio) or int(precio) <= 0:
            messages.error(request, "El precio debe ser un número positivo y mayor que cero.")
            return redirect("productos_form")

        if not inventario.isdigit() or int(inventario) < 0:
            messages.error(request, "El inventario solo puede contener valores numéricos positivos.")
            return redirect("productos_form")

        # Validar la fecha de creación
        try:
            fecha_creacion_dt = datetime.strptime(fecha_creacion, "%Y-%m-%d").date()

            if fecha_creacion_dt > timezone.now().date():
                messages.error(request, "La fecha de creación no puede ser en el futuro.")
                return redirect("productos_form")
        except ValueError:
            messages.error(request, "La fecha de creación no tiene un formato válido.")
            return redirect("productos_form")

        try:
            categoria = CategoriaEtiqueta.objects.get(pk=categoria_id)
            producto = Producto(
                nombre=nombre,
                precio=int(precio),
                informacion=informacion,
                inventario=int(inventario),
                fecha_creacion=fecha_creacion_dt,
                categoria=categoria,
                foto=foto
            )
            producto.save()

            for etiqueta_id in etiquetas:
                if etiqueta_id:
                    etiqueta = SubCategoriaEtiqueta.objects.get(pk=etiqueta_id)
                    ProductoSubCategoria.objects.create(
                        id_producto=producto,
                        id_sub_categoria_etiqueta=etiqueta
                    )

            for talla_id in tallas:
                talla = Tallas.objects.get(pk=talla_id)
                ProductoTallas.objects.create(
                    id_producto=producto,
                    id_talla=talla
                )

            messages.success(request, "Guardado correctamente!!")
        except Exception as e:
            messages.error(request, f"Error al guardar el producto: {e}")
            return redirect("productos_form")

        return redirect("productos_listar")

    else:
        messages.warning(request, "Error: No se enviaron datos.")
        return redirect("productos_listar")


@admin_requerido_id
def productos_eliminar(request, id):
	try:
		q = Producto.objects.get(pk=id)
		q.delete()
		messages.success(request, "Producto eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: Está asociado a una o mas tablas")

	return redirect("productos_listar")

@admin_requerido_id
def productos_formulario_editar(request, id):
	q = Producto.objects.get(pk=id)
	c = CategoriaEtiqueta.objects.all()
	e = SubCategoriaEtiqueta.objects.all()
	t = Tallas.objects.all()
	pt = ProductoTallas.objects.all()
	contexto = {"data": q, "categoria": c, "etiqueta":e, "talla":t, "proTallas":pt}
	return render(request, "tienda/productos/productos_formulario_editar.html", contexto)

@admin_requerido
def productos_actualizar(request):
    if request.method == "POST":
        id_producto = request.POST.get("id")

        if not id_producto:
            messages.error(request, "ID del producto no se ha proporcionado.")
            return redirect("productos_listar")

        nombre = request.POST.get("nombre")
        precio = request.POST.get("precio")
        informacion = request.POST.get("informacion")
        inventario = request.POST.get("inventario")
        fecha_creacion = request.POST.get("fecha_creacion")
        categoria_id = request.POST.get("categoria")
        etiquetas_ids = request.POST.getlist("etiqueta")
        tallas = request.POST.getlist("talla")
        foto = request.FILES.get("foto")

        if not precio.isdigit():
            messages.error(request, "El precio solo puede llevar valores numéricos")
            return redirect("productos_listar")

        if not inventario.isdigit():
            messages.error(request, "El inventario solo puede llevar valores numéricos")
            return redirect("productos_listar")

        try:
            producto = Producto.objects.get(pk=id_producto)

            producto.nombre = nombre
            producto.precio = precio
            producto.informacion = informacion
            producto.inventario = inventario
            producto.fecha_creacion = fecha_creacion
            producto.categoria_id = categoria_id
            
            if foto:
                producto.foto = foto

            producto.save()

            ProductoSubCategoria.objects.filter(id_producto=producto).delete()

            for etiqueta_id in etiquetas_ids:
                etiqueta = SubCategoriaEtiqueta.objects.get(pk=etiqueta_id)
                ProductoSubCategoria.objects.create(
                    id_producto=producto,
                    id_sub_categoria_etiqueta=etiqueta
                )

            ProductoTallas.objects.filter(id_producto=producto).delete()  # Limpiar tallas existentes

            for talla_id in tallas:
                talla = Tallas.objects.get(pk=talla_id)
                ProductoTallas.objects.create(
                    id_producto=producto,
                    id_talla=talla
                )

            messages.success(request, "Producto actualizado correctamente")
        except Producto.DoesNotExist:
            messages.error(request, "El producto especificado no existe")
        except SubCategoriaEtiqueta.DoesNotExist:
            messages.error(request, "Una de las etiquetas especificadas no existe")
        except Exception as e:
            messages.error(request, f"Error al actualizar el producto: {e}")

    else:
        messages.warning(request, "Error: No se enviaron datos")

    return redirect("productos_listar")


def ver_perfil(request):
    logueo = request.session.get("logueo", False)
    if not logueo:
        messages.error(request, "No estás logueado")
        return redirect("inicio")
      
    q = Usuario.objects.get(pk=logueo["id"])
    contexto = {"data": q}
    return render(request, "tienda/login/perfil.html", contexto)


def cambio_clave_formulario(request):
    logueo = request.session.get("logueo", False)
    if not logueo:
        messages.error(request, "No estás logueado")
        return redirect("inicio")
    return render(request, "tienda/login/cambio_clave.html")


def cambiar_clave(request):
    logueo = request.session.get("logueo", False)
    if logueo:
        if request.method == "POST":
            try:
                q = Usuario.objects.get(pk=logueo["id"])
            except Usuario.DoesNotExist:
                messages.error(request, "Usuario no encontrado...")
                return redirect('cc_formulario')

            c1 = request.POST.get("nueva1")
            c2 = request.POST.get("nueva2")

            if q.check_password(request.POST.get("clave")):
                if c1 == c2:
                    q.set_password(c1)
                    q.save()
                    messages.success(request, "Contraseña guardada correctamente!!")
                else:
                    messages.info(request, "Las contraseñas nuevas no coinciden...")
            else:
                messages.error(request, "Contraseña no válida...")
        else:
            messages.warning(request, "Error: No se enviaron datos...")
    else:
        messages.error(request, "No estás logueado")
        return redirect("inicio")

    return redirect('cc_formulario')

def devoluciones(request):
    q = Devoluciones.objects.all()
    contexto = {"data": q}
    return render(request, "tienda/devoluciones/devoluciones.html", contexto)

def devoluciones_form(request):
	q = CategoriaEtiqueta.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/devoluciones/devoluciones_form.html", contexto)

def devoluciones_crear(request):
	if request.method == "POST":
		nombre = request.POST.get("nombre")
		email = request.POST.get("email")
		telefono = request.POST.get("telefono")
		descripcion = request.POST.get("descripcion")
		try:
			q = Devoluciones(
				nombre=nombre,
				email=email,
				telefono=telefono,
				descripcion= descripcion,
			)
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: No se enviaron datos...")
		return redirect("devoluciones")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("devoluciones")

def devoluciones_formulario_editar(request, id):
	q = Devoluciones.objects.get(pk=id)
	contexto = {"data": q}
	return render(request, "tienda/devoluciones/devoluciones_formulario_editar.html", contexto)

def devoluciones_actualizar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nombre = request.POST.get("nombre")
		email = request.POST.get("email")
		telefono = request.POST.get("telefono")
		descripcion = request.POST.get("descripcion")
		
		try:
			q = Devoluciones.objects.get(pk=id)
			q.nombre = nombre
			q.email = email
			q.telefono = telefono
			q.descripcion = descripcion
			
			q.save()
			messages.success(request, "Devolucion actualizada correctamente!!")
		except Exception as e:
			messages.error(request, f"Error {e}")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect("devoluciones")

def devoluciones_eliminar(request, id):
	try:
		q = Devoluciones.objects.get(pk=id)
		q.delete()
		messages.success(request, "Devolucion eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("devoluciones")

def carrito_add(request):
    if request.method == "POST":
        try:
            carrito = request.session.get("carrito", [])
            if not carrito:
                request.session["carrito"] = []
                request.session["items"] = 0

            id_producto = int(request.POST.get("id"))
            cantidad = int(request.POST.get("cantidad", 0))

            q = Producto.objects.get(pk=id_producto)

            producto_en_carrito = False

            for p in carrito:
                if p["id"] == id_producto:
                    producto_en_carrito = True
                    if q.inventario >= (p["cantidad"] + cantidad) and cantidad > 0:
                        p["cantidad"] += cantidad
                        p["subtotal"] = p["cantidad"] * q.precio
                    else:
                        print("Cantidad supera inventario...")
                        messages.warning(request, "Cantidad supera inventario...")
                    break

            if not producto_en_carrito:
                print("No existe en carrito... lo agregamos")
                if q.inventario >= cantidad and cantidad > 0:
                    carrito.append(
                        {
                            "id": q.id,
                            "foto": q.foto.url,
                            "producto": q.nombre,
                            "precio": q.precio,
                            "informacion": q.informacion,
                            "cantidad": cantidad,
                            "subtotal": cantidad * q.precio
                        }
                    )
                else:
                    print("Cantidad supera inventario...")
                    messages.warning(request, "No se puede agregar, no hay suficiente inventario.")

            # Actualizamos variable de sesión carrito...
            request.session["carrito"] = carrito

            contexto = {
                "items": len(carrito),
                "total": sum(p["subtotal"] for p in carrito)
            }
            request.session["items"] = len(carrito)

            return render(request, "tienda/carrito/carrito.html", contexto)
        except ValueError:
            messages.error(request, "Error: Digite un valor correcto para cantidad")
            return HttpResponse("Error")
        except Exception as e:
            messages.error(request, f"Ocurrió un Error: {e}")
            return HttpResponse("Error")
    else:
        messages.warning(request, "No se enviaron datos.")
        return HttpResponse("Error")



def visualizar_carrito(request):
	carrito = request.session.get("carrito", False)
	if not carrito:
		request.session["carrito"] = []
		request.session["items"] = 0
		contexto = {
			"items": 0,
			"total": 0
		}
	else:
		contexto = {
			"items": len(carrito),
			"total": sum(p["subtotal"] for p in carrito)
		}
		request.session["items"] = len(carrito)

	return render(request, "tienda/carrito/visualizar_carrito.html", contexto)

def ver_carrito(request):
    carrito = request.session.get("carrito", False)
    print("Carrito:", carrito)  # Para depuración
    if not carrito:
        request.session["carrito"] = []
        request.session["items"] = 0
        contexto = {
            "items": 0,
            "total": 0
        }
    else:
        contexto = {
            "items": len(carrito),
            "total": sum(p["subtotal"] for p in carrito)
        }
        request.session["items"] = len(carrito)
        print("Items en carrito:", contexto["items"])  # Para depuración

    return render(request, "tienda/carrito/carrito.html", contexto)



def vaciar_carrito(request):
	request.session["carrito"] = []
	request.session["items"] = 0
	return redirect("inicio")

def eliminar_item_carrito(request, id_producto):
	try:
		carrito = request.session.get("carrito", False)
		if carrito != False:
			for i, item in enumerate(carrito):
				if item["id"] == id_producto:
					carrito.pop(i)
					break
			else:
				messages.warning(request, "No se encontró el ítem en el carrito.")

		request.session["items"] = len(carrito)
		request.session["carrito"] = carrito
		return redirect("ver_carrito")
	except:
		return HttpResponse("Error")
	
def eliminar_item_carrito_ver(request, id_producto):
	try:
		carrito = request.session.get("carrito", False)
		if carrito != False:
			for i, item in enumerate(carrito):
				if item["id"] == id_producto:
					carrito.pop(i)
					break
			else:
				messages.warning(request, "No se encontró el ítem en el carrito.")

		request.session["items"] = len(carrito)
		request.session["carrito"] = carrito
		return redirect("visualizar_carrito")
	except:
		return HttpResponse("Error")

def actualizar_totales_carrito(request, id_producto):
	carrito = request.session.get("carrito", False)
	cantidad = request.GET.get("cantidad")

	if carrito != False:
		for i, item in enumerate(carrito):
			if item["id"] == id_producto:
				item["cantidad"] = int(cantidad)
				item["subtotal"] = int(cantidad) * item["precio"]
				break
		else:
			messages.warning(request, "No se encontró el ítem en el carrito.")

	request.session["items"] = len(carrito)
	request.session["carrito"] = carrito
	return redirect("ver_carrito")

def actualizar_totales_carrito_ver(request, id_producto):
	carrito = request.session.get("carrito", False)
	cantidad = request.GET.get("cantidad")

	if carrito != False:
		for i, item in enumerate(carrito):
			if item["id"] == id_producto:
				item["cantidad"] = int(cantidad)
				item["subtotal"] = int(cantidad) * item["precio"]
				break
		else:
			messages.warning(request, "No se encontró el ítem en el carrito.")

	request.session["items"] = len(carrito)
	request.session["carrito"] = carrito
	return redirect("visualizar_carrito")

def realizar_venta(request):
    # Verificar si el usuario está autenticado
    logueo = request.session.get("logueo")
    
    if not logueo or 'id' not in logueo:
        messages.warning(request, "Necesitas iniciar sesión para poder pagar tu pedido.")
        return redirect('inicio')  

    try:
        usuario = Usuario.objects.get(pk=logueo["id"])
        
        nueva_venta = Venta.objects.create(usuario=usuario)

        carrito = request.session.get("carrito", [])
        for item in carrito:
            producto = Producto.objects.get(pk=item["id"])
            cantidad = item["cantidad"]

            detalle_venta = DetalleVenta.objects.create(
                venta=nueva_venta,
                producto=producto,
                cantidad=cantidad,
                precio_historico=producto.precio,
                id_usuario=usuario
            )

            producto.inventario -= cantidad
            producto.save()
        
        request.session["carrito"] = []
        request.session["items"] = 0

        messages.success(request, "¡La compra se realizó con éxito!")

    except Producto.DoesNotExist as e:
        messages.error(request, f"Error al procesar la compra: {e}")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al procesar la compra: {e}")

    return redirect("inicio")

def ventas_ver(request):
    usuarios = Usuario.objects.all()
    try:
        ventas = Venta.objects.all()
        ventas_con_detalles = []
        total_precio_historico = 0

        for venta in ventas:
            detalles = DetalleVenta.objects.filter(venta=venta)
            subtotal_venta = 0  # Para calcular el subtotal de cada venta

            for detalle in detalles:
                detalle.subtotal = detalle.precio_historico * detalle.cantidad
                detalle.save()

                # Solo sumar si el estado de la venta es "Pagada" o "Enviado"
                if venta.estado in [2, 4]:  # 2: Pagada, 4: Enviado
                    subtotal_venta += detalle.subtotal
            
            # Solo agregar el subtotal a total_precio_historico si corresponde
            if venta.estado in [2, 4]:
                total_precio_historico += subtotal_venta

            # Agregar usuario a la venta
            ventas_con_detalles.append({
                'venta': venta,
                'detalles': detalles,
                'usuario': venta.usuario  # Accede al usuario desde la venta
            })

        contexto = {
            'ventas_con_detalles': ventas_con_detalles,
            'total_precio_historico': total_precio_historico  
        }
        
        return render(request, "tienda/ventas/ventas_ver.html", contexto)
    
    except Exception as e:
        messages.error(request, f"Ocurrió un error al recuperar las ventas: {e}")
        return render(request, "tienda/ventas/ventas_ver.html", {'ventas_con_detalles': [], 'total_precio_historico': 0, 'usuario': usuarios })
        
def eliminar_venta(request, id_venta):
	try:
		venta = Venta.objects.get(pk=id_venta)
		venta.delete()
		messages.success(request, 'Venta eliminada correctamente!!')
		return redirect("ventas_ver")
	except Exception as e:
		messages.warning(request, f'{e}')
		return HttpResponse("Error")

@transaction.atomic
def guardar_venta(request):
	carrito = request.session.get("carrito", False)
	logueo = request.session.get("logueo", False)
	try:
		# Genero encabezado de venta, para tener ID y guardar detalle
		r = Venta(usuario=Usuario.objects.get(pk=logueo["id"]))
		r.save()

		for i, p in enumerate(carrito):
			try:
				pro = Producto.objects.get(pk=p["id"])
				print(f"ok producto {p['producto']}")
			except Producto.DoesNotExist:
				# elimino el producto no existente del carrito...
				carrito.pop(i)
				request.session["carrito"] = carrito
				request.session["items"] = len(carrito)
				raise Exception(f"El producto '{p['producto']}' ya no existe")

			if int(p["cantidad"]) > pro.inventario:
				raise Exception(f"La cantidad del producto '{p['producto']}' supera el inventario")

			det = DetalleVenta(
				venta=r,
				producto=pro,
				cantidad=int(p["cantidad"]),
				precio_historico=int(p["precio"])
			)
			det.save()
		messages.success(request, "Venta realizada correctamente!!")
	except Exception as e:
		transaction.set_rollback(True)
		messages.error(request, f"Error: {e}")

	return redirect("inicio")

def lista_pedidos(request):
    logueo = request.session.get("logueo", False)
    if not logueo:
        messages.error(request, "No estás logueado")
        return redirect("inicio")
    logueo = request.session.get("logueo")
    if logueo:
        usuario = Usuario.objects.get(pk=logueo["id"])
        if usuario.rol == 1:
            pedidos = DetalleVenta.objects.all()
        else:
            pedidos = DetalleVenta.objects.filter(id_usuario=usuario)

        for detalle in pedidos:
            detalle.total = detalle.precio_historico * detalle.cantidad
            # Aquí debes asegurarte de que `detalle.venta.estado` esté disponible

        return render(request, 'tienda/ventas/mis_compras.html', {'pedidos': pedidos})
    else:
        return redirect("inicio")

def estado_venta(request, id):
    logueo = request.session.get("logueo", False)
    if not logueo:
        messages.error(request, "No estás logueado")
        return redirect("inicio")
    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        motivo_rechazo = request.POST.get("motivo_rechazo", '')

        try:
            venta = Venta.objects.get(pk=id)
            venta.estado = int(nuevo_estado)

            if venta.estado == 3:
                venta.motivo_rechazo = motivo_rechazo
            else:
                venta.motivo_rechazo = None

            venta.save()
            messages.success(request, "Estado actualizado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar el estado: {e}")
    else:
        messages.warning(request, "No se enviaron datos.")
    
    return redirect("ventas_ver")


def ventas_formulario_editar(request, id):
	q = Venta.objects.get(pk=id)
	contexto = {"data": q,}
	return render(request, "tienda/ventas/ventas_editar.html", contexto)

def prueba_correo(request):
	destinatario = "hammer.hernandez10@gmail.com"
	mensaje = """
		<h1 style='color:blue;'>Tienda virtual</h1>
		<p>Su pedido está listo y en estado "creado".</p>
		<h1 style='color:red;'> ESTA MUY ENAMORADO </h1>
		<p>Tienda ADSO, 2024</p>
		"""
 	
	try:
		msg = EmailMessage("Tienda ADSO", mensaje, settings.EMAIL_HOST_USER, [destinatario])
		msg.content_subtype = "html"  # Habilitar contenido html
		msg.send()
		return HttpResponse("Correo enviado")
	except BadHeaderError:
		return HttpResponse("Encabezado no válido")
	except Exception as e:
		return HttpResponse(f"Error: {e}")
	
from .models import Usuario

def editeUser(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        image = request.FILES.get("image")

        if not nombre or not email:
            messages.error(request, 'No se permite campos vacíos')
            return redirect('ver_perfil')

        try:
            q = Usuario.objects.get(pk=id)
            q.nombre = nombre
            q.email = email
            
            if image:
                q.foto = image
            
            q.save()
            messages.success(request, "Usuario actualizado correctamente!!")
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
        except Exception as e:
            messages.error(request, f"Error: {e}")

    else:
        messages.warning(request, "Error: No se enviaron datos...")
    
    return redirect('ver_perfil')

@admin_requerido
def etiquetas_listar(request):
	q = SubCategoriaEtiqueta.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/categorias/subcategoria/etiquetas.html", contexto)

@admin_requerido
def etiquetas_form(request):
	q = CategoriaEtiqueta.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/categorias/subcategoria/etiquetas_form_crear.html", contexto)

@admin_requerido
def etiquetas_crear(request):
	if request.method == "POST":
		nomb = request.POST.get("nombre")
		cat = CategoriaEtiqueta(pk=request.POST.get("categoriaEtiqueta"))
		if not re.match(r"^[a-zA-Z\s]+$", nomb):
			messages.error(request, f"El nombre solo puede llevar valores alfabeticos")
		try:
			q = SubCategoriaEtiqueta(
				nombre=nomb,
				id_categoria_etiqueta=cat
			)
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: No se enviaron los datos...")
		return redirect("etiquetas_listar")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("etiquetas_listar")

@admin_requerido_id
def etiquetas_eliminar(request, id):
	try:
		q = SubCategoriaEtiqueta.objects.get(pk=id)
		q.delete()
		messages.success(request, "Etiqueta eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("etiquetas_listar")

@admin_requerido_id
def etiquetas_formulario_editar(request, id):
	q = SubCategoriaEtiqueta.objects.get(pk=id)
	c = CategoriaEtiqueta.objects.all()
	contexto = {"data": q, "categorias": c}
	return render(request, "tienda/categorias/subcategoria/etiquetas_form_editar.html", contexto)

@admin_requerido
def etiquetas_actualizar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nomb = request.POST.get("nombre")
		cat = CategoriaEtiqueta.objects.get(pk=request.POST.get("categoriaEtiqueta"))
		if not re.match(r"^[a-zA-Z\s]+$", nomb):
			messages.error(request, f"El nombre solo puede llevar valores alfabeticos")
		try:
			q = SubCategoriaEtiqueta.objects.get(pk=id)
			q.nombre = nomb
			q.id_categoria_etiqueta = cat
			q.save()
			messages.success(request, "Etiqueta actualizada correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect("etiquetas_listar")

def term_y_cond(request):
    return render(request, "tienda/term_y_cond/term_y_cond.html")


class RegistrarUsuario(APIView):
    def post(self, request):
        print(request.data)
        if request.method == "POST":
            nombre = request.data["nombre"]
            email = request.data["correo"]
            clave1 = request.data["password"]
            clave2 = request.data["confirmPassword"]
            nick = email
            if nombre == "" or email == "" or clave1 == "" or clave2 == "":
                return Response(data={'message': 'Todos los campos son obligatorios', 'respuesta': 400}, status=400)
            elif not re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
				
                return Response(data={'message': 'El correo no es válido', 'respuesta': 400}, status=400)
            elif clave1 != clave2:
                return Response(data={'message': 'Las contraseñas no coinciden', 'respuesta': 400}, status=400)
            else:
                try:
                    q = Usuario(
                        nombre=nombre,
                        email=email,
                        password=make_password(clave1)
                    )
                    q.save()
                except Exception as e:
                    return Response(data={'message': 'El Usuario ya existe', 'respuesta': 409}, status=409)

        # Renderiza la misma página de registro con los mensajes de error
        return Response(data={'message': f'Usuario creado correctamente tu nick es: {nick}', 'respuesta': 201}, status=201)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)


class CustomAuthToken(ObtainAuthToken):
	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data,
		context={'request': request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['username']
		# traer datos del usuario para bienvenida y ROL
		usuario = Usuario.objects.get(email=user)
		token, created = Token.objects.get_or_create(user=usuario)

		return Response({
			'token': token.key,
			'user': {
				'user_id': usuario.pk,
				'email': usuario.email,
				'nombre': usuario.nombre,
				'rol': usuario.rol,
				'foto': usuario.foto.url
			}
		})

def cargar_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            return redirect('devoluciones_form')
    else:
        form = ImageUploadForm()
    
    return render(request, 'cargar.html', {'form': form})

def comentarios_listar(request):
    logueo = request.session.get("logueo", False)
    if not logueo:
        messages.error(request, "No estás logueado")
        return redirect("inicio")
    comentarios = Comentarios.objects.all()
    contexto = {"comentarios": comentarios}
    return render(request, "tienda/comentarios/comentarios_listar.html", contexto)

def comentarios_form(request):
    logueo = request.session.get("logueo", False)
    if not logueo:
        messages.error(request, "No estás logueado")
        return redirect("inicio")
    return render(request, "tienda/comentarios/comentarios_form.html")

def comentarios_crear(request):
    logueo = request.session.get("logueo", False)
    if not logueo:
        messages.error(request, "No estás logueado")
        return redirect("inicio")
    if request.method == "POST":
        comentarios = request.POST.get("comentarios")
        if comentarios is None:
            messages.error(request, "El comentario no puede estar vacío.")
            return redirect("comentarios_form")

        try:
            q = Comentarios(
				comentarios = comentarios,
				descripcion=request.POST.get("descripcion", ""),
				fecha_creacion=timezone.now()
			)
            q.save()
            messages.success(request, "Guardado correctamente!")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("comentarios_listar")


def comentarios_editar(request, id):
    logueo = request.session.get("logueo", False)
    if not logueo:
        messages.error(request, "No estás logueado")
        return redirect("inicio")
    q = Comentarios.objects.get(pk=id)
    contexto = {"comentarios": q}
    return render(request, "tienda/comentarios/comentarios_editar.html", contexto)
	         

def comentarios_actualizar(request):
    logueo = request.session.get("logueo", False)
    if not logueo:
        messages.error(request, "No estás logueado")
        return redirect("inicio")
    if request.method == "POST":
        id = request.POST.get('id')
        comentarios = request.POST.get("comentarios")
        
        try:
            q = Comentarios.objects.get(pk=id)
            if comentarios: 
                q.comentarios = comentarios
                q.save()
                messages.success(request, "Guardado correctamente!!")
            else:
                messages.error(request, "El comentario no puede estar vacío.")
        except Comentarios.DoesNotExist:
            messages.error(request, "Comentario no encontrado.")
        except Exception as e:
            messages.error(request, f"Error: {e}")

        return redirect("comentarios_listar")

			
def comentarios_eliminar(request, id):
    logueo = request.session.get("logueo", False)
    if not logueo:
        messages.error(request, "No estás logueado")
        return redirect("inicio")
    try:
        q = Comentarios.objects.get(pk=id)
        q.delete()
        messages.success(request, "Comentario eliminada correctamente!!")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect("comentarios_listar")

def comentarios_like(request, id):
    logueo = request.session.get("logueo", False)
    if not logueo:
        messages.error(request, "No estás logueado")
        return redirect("inicio")
    if request.method == "POST":
        try:
            print(f"Recibiendo like para el comentario ID: {id}")
            comentario = Comentarios.objects.get(pk=id)
            comentario.likes += 1
            comentario.save()
            return JsonResponse({'likes': comentario.likes})
        except Comentarios.DoesNotExist:
            return JsonResponse({'error': 'Comentario no encontrado.'}, status=404)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

@admin_requerido
def tallas_listar(request):
    t = Tallas.objects.all()
    contexto = {"talla":t}
    return render (request, "tienda/tallas/tallas.html", contexto)

@admin_requerido
def tallas_form(request):
	return render(request, "tienda/tallas/tallas_form.html")

@admin_requerido
def tallas_crear(request):
    if request.method == "POST":
        talla = request.POST.get("talla")
        if not re.match(r'^[a-zA-Z0-9]+$', talla):
            messages.error(request, f"La talla solo puede llevar valores numericos o letras")
        
        try:
            q = Tallas(
				talla = talla
			)
            q.save()
            messages.success(request, "Guardado correctamente!!")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("tallas_listar")

@admin_requerido_id
def tallas_editar(request, id):
	q = Tallas.objects.get(pk=id)
	contexto = {"talla": q}
	return render(request, "tienda/tallas/tallas_editar.html", contexto)
	         
@admin_requerido
def tallas_actualizar(request):
	if request.method == "POST":
		id = request.POST.get('id')
		talla = request.POST.get("talla")
		print(talla)
		if not re.match(r'^[a-zA-Z0-9]+$', talla):
				messages.error(request, f"La talla solo puede llevar valores numericos o letras")
		try:
			q = Tallas.objects.get(pk=id)
			q.talla = talla
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
		return redirect("tallas_listar")
			
@admin_requerido_id
def tallas_eliminar(request, id):
	try:
		q = Tallas.objects.get(pk=id)
		q.delete()
		messages.success(request, "Talla eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("tallas_listar")

def trabaja_nosotros(request):
    return render(request, "tienda/trabaja_nosotros/trabaja_nosotros.html")


#pedidos y devoluciones 
from django.db.models import Sum, F
from django.db.models import Sum, F

def ver_pedidos_cliente(request):
    logueo = request.session.get("logueo")
    
    if logueo:
        usuario = Usuario.objects.get(pk=logueo["id"])
        pedidos = Venta.objects.filter(usuario=usuario).prefetch_related('detalleventa_set').order_by('-id')
        devoluciones = Devolucion.objects.filter(pedido__in=pedidos)
        # Iteramos sobre cada pedido
        for pedido in pedidos:
            # Calcular el total del pedido (precio total de todos los productos)
            total_pedido = pedido.detalleventa_set.aggregate(
                total=Sum(F('cantidad') * F('precio_historico'))
            )['total']
            
            # Calcular el total de productos (suma de cantidades)
            total_productos = pedido.detalleventa_set.aggregate(
                total_productos=Sum('cantidad')
            )['total_productos']
            
            # Asignamos el total calculado al pedido
            pedido.total_pedido = total_pedido if total_pedido else 0
            pedido.total_productos = total_productos if total_productos else 0

        # Comprobamos si hay pedidos para el usuario
        '''if pedidos.exists():
            print(f"Se han encontrado {pedidos.count()} pedidos para el usuario {request.user}")
        else:
            print(f"No se han encontrado pedidos para el usuario {request.user}")'''
        
        context = {
            'pedidos': pedidos,
			'devoluciones': devoluciones
        }
    else:
        # Si el usuario no está autenticado, enviamos una lista vacía
        context = {
            'pedidos': []
        }

    return render(request, 'tienda/pedidos/mis_pedidos.html', context)

def cancelar_pedido(request, pedido_id):
    logueo = request.session.get("logueo")
    
    if logueo:
        # Obtén el pedido que se desea cancelar
        pedido = get_object_or_404(Venta, id=pedido_id, usuario__id=logueo['id'])
        
        # Eliminar el pedido
        pedido.delete()
        
        messages.success(request, 'El pedido ha sido cancelado con éxito.')
    else:
        messages.error(request, 'Debes estar logueado para cancelar un pedido.')
    
    return redirect('mis_pedidos')  # Redirige a la página de mis pedidos

def lista_usuarios(request):
    usuarios = Usuario.objects.filter(venta__isnull=False).distinct()  # Usuarios que han hecho pedidos

    context = {
        'usuarios': usuarios
    }
    return render(request, 'tienda/pedidos/lista_usuarios.html', context)

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Usuario

def ver_pedidos_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    pedidos = Venta.objects.filter(usuario=usuario).prefetch_related('detalleventa_set').order_by('-id')
    
    for pedido in pedidos:
            # Calcular el total del pedido (precio total de todos los productos)
            total_pedido = pedido.detalleventa_set.aggregate(
                total=Sum(F('cantidad') * F('precio_historico'))
            )['total']
            
            # Calcular el total de productos (suma de cantidades)
            total_productos = pedido.detalleventa_set.aggregate(
                total_productos=Sum('cantidad')
            )['total_productos']
            
            # Asignamos el total calculado al pedido
            pedido.total_pedido = total_pedido if total_pedido else 0
            pedido.total_productos = total_productos if total_productos else 0
    

    context = {
        'usuario': usuario,
        'pedidos': pedidos
    }
    return render(request, 'tienda/pedidos/ver_pedidos_usuario.html', context)

def cambiar_estado_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Venta, id=pedido_id)
        nuevo_estado = request.POST.get('estado')

        if nuevo_estado in ['1', '2', '3']:
            pedido.estado = int(nuevo_estado)
            pedido.save()

            # Redirige pasando el 'usuario_id'
            return redirect('ver_pedidos_usuario', usuario_id=pedido.usuario.id)
        else:
            return render(request, 'tienda/error.html', {'error': 'Estado inválido'})


#devoluciones

#cliente
def apelar_devolucion(request, pedido_id):
    pedido = get_object_or_404(Venta, id=pedido_id)
    # Verificamos si ya existe una devolución asociada a este pedido
    devolucion_existente = Devolucion.objects.filter(pedido=pedido).exists()

    if devolucion_existente:
        # Si ya existe una devolución, redirigimos con un mensaje de error
        return render(request, 'tienda/pedidos/devolucion_error.html', {'mensaje': 'Ya se ha solicitado una devolución para este pedido.'})
    
    
    if request.method == "POST":
        motivo = request.POST.get('motivo')
        foto = request.FILES.get('foto')
        devolucion = Devolucion.objects.create(pedido=pedido, 
                                               usuario=request.user, 
                                               motivo=motivo,
                                               foto=foto if foto else None)
        # Redirigir a la página de pedidos o a la página de devoluciones
        return redirect('mis_pedidos')  # Cambia esto a la URL que desees

    return render(request, 'tienda/devolucion/apelar_devolucion.html', {'pedido': pedido})

from django.db.models import Sum, F

from django.shortcuts import render
from tienda.models import Devolucion, Usuario, Venta
def ver_mis_devoluciones(request):
    logueo = request.session.get("logueo")
    
    if logueo:
        usuario = Usuario.objects.get(pk=logueo["id"])
        pedidos = Venta.objects.filter(usuario=usuario).prefetch_related('detalleventa_set')
        devoluciones = Devolucion.objects.filter(pedido__in=pedidos).order_by('-id')

        # Debug: imprimir URL de las fotos de las devoluciones solo si existe
        for devolucion in devoluciones:
            if devolucion.foto:
                print(f"Devolución ID: {devolucion.id}, URL de la foto: {devolucion.foto.url}")
            else:
                print(f"Devolución ID: {devolucion.id}, No tiene foto.")

        context = {
            'pedidos': pedidos,
            'devoluciones': devoluciones
        }
    else:
        # Si no está autenticado, se retorna una lista vacía
        context = {
            'pedidos': [],
            'devoluciones': []
        }

    return render(request, 'tienda/devolucion/mis_devoluciones.html', context)

#admin
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def listar_devoluciones(request):
    devoluciones = Devolucion.objects.all().order_by('-id')  # Lista de devoluciones en orden descendente
    pedidos = Venta.objects.prefetch_related('detalleventa_set').all()

    for devolucion in devoluciones:
        pedido = devolucion.pedido  # Asume que la devolución tiene un campo relacionado con el pedido
        total_pedido = pedido.detalleventa_set.aggregate(
            total=Sum(F('cantidad') * F('precio_historico'))
        )['total'] if pedido else 0

        total_productos = pedido.detalleventa_set.aggregate(
            total_productos=Sum('cantidad')
        )['total_productos'] if pedido else 0

        pedido.total_pedido = total_pedido
        pedido.total_productos = total_productos

    context = {
        'devoluciones': devoluciones,
        'pedidos': pedidos
    }
    return render(request, 'tienda/devolucion/listar_devoluciones.html', context)

def cambiar_estado_devolucion(request, devolucion_id):
    if request.method == 'POST':
        # Obtenemos la devolución correspondiente
        devolucion = get_object_or_404(Devolucion, id=devolucion_id)
        
        # Obtenemos el nuevo estado desde el formulario
        nuevo_estado = request.POST.get('estado')

        # Verificamos que el nuevo estado sea válido
        if nuevo_estado in ['1', '2', '3']:  # Asegúrate de que estos valores coincidan con los estados de tu modelo
            # Asignamos el nuevo estado a la devolución
            devolucion.estado = int(nuevo_estado)
            devolucion.save()  # Guardamos los cambios en la base de datos

            # Redirigimos al administrador a la lista de devoluciones
            messages.success(request, 'El estado de la devolución ha sido cambiado con éxito.')
            return redirect('listar_devoluciones')  # Asegúrate de que 'devoluciones_admin' sea la ruta correcta
        else:
            messages.error(request, 'Estado inválido.')
            return redirect('listar_devoluciones')  # Redirige a la lista de devoluciones si el estado no es válido
    else:
        return render(request, 'tienda/error.html', {'error': 'Método no permitido'})