from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'categoria', views.CategoriaViewSet)
router.register(r'producto', views.ProductoViewSet)
router.register(r'usuario', views.UsuarioViewSet)
router.register(r'categoria-etiqueta', views.CategoriaEtiquetaViewSet)
router.register(r'subcategoria-etiqueta', views.SubCategoriaEtiquetaViewSet)
router.register(r'producto-subcategoria', views.ProductoSubCategoriaViewSet)
router.register(r'venta', views.VentaViewSet)
router.register(r'detalle-venta', views.DetalleVentaViewSet)
#router.register(r'registrar-usuario', views.DetalleVentaViewSet)
router.register(r'comentarios', views.ComentariosViewSet)

urlpatterns = [
	path('index/', views.index, name="index"),
	path('', views.inicio, name="inicio"),
    
	#API
    path('api/1.0/', include(router.urls)),
    path('api/1.0/token-auth/', views.CustomAuthToken.as_view()),
	path('api/1.0/api-auth/', include('rest_framework.urls')),

	# Autenticación de usuarios del sistema
	path('login/', views.login, name="login"),
	path('logout/', views.logout, name="logout"),
	path('registrar_usuario/', views.registrar_usuario, name="registrar_usuario"),
    path("recuperar_clave/", views.recuperar_clave, name="recuperar_clave"),
	path("verificar_recuperar/", views.verificar_recuperar, name="verificar_recuperar"),
 
 	# Usuarios CRUD
	path("usuarios_listar/", views.usuarios, name="usuarios_listar"),
	path("usuarios_form/", views.usuarios_form, name="usuarios_form"),
	path("usuarios_eliminar/<int:id>", views.usuarios_eliminar, name="usuarios_eliminar"),
	path("usuarios_formulario_editar/<int:id>", views.usuarios_formulario_editar, name="usuarios_formulario_editar"),
	path("usuarios_actualizar/", views.usuarios_actualizar, name="usuarios_actualizar"),
    path('edite_profile',views.editeUser,name='edite_profile'),
	
	# CRUD de Categorías
	path("categorias_listar/", views.categorias, name="categorias_listar"),
	path("categorias_form/", views.categorias_form, name="categorias_form"),
	path("categorias_crear/", views.categorias_crear, name="categorias_crear"),
	path("categorias_eliminar/<int:id>", views.categorias_eliminar, name="categorias_eliminar"),
	path("categorias_formulario_editar/<int:id>", views.categorias_formulario_editar, name="categorias_formulario_editar"),
	path("categorias_actualizar/", views.categorias_actualizar, name="categorias_actualizar"),

	# CRUD de Productos
	path("productos_listar/", views.productos, name="productos_listar"),
	path("productos_form/", views.productos_form, name="productos_form"),
	path("productos_crear/", views.productos_crear, name="productos_crear"),
	path("productos_eliminar/<int:id>", views.productos_eliminar, name="productos_eliminar"),
	path("productos_formulario_editar/<int:id>", views.productos_formulario_editar, name="productos_formulario_editar"),
	path("productos_actualizar/", views.productos_actualizar, name="productos_actualizar"),

	path("ver_perfil/", views.ver_perfil, name="ver_perfil"),
	path("cc_formulario/", views.cambio_clave_formulario, name="cc_formulario"),
	path("cambiar_clave/", views.cambiar_clave, name="cambiar_clave"),
 
	# CRUD de Devoluciones
	path("devoluciones/", views.devoluciones, name="devoluciones"),
	path("devoluciones_form/", views.devoluciones_form, name="devoluciones_form"),
	path("devoluciones_crear/", views.devoluciones_crear, name="devoluciones_crear"),
	path("devoluciones_formulario_editar/<int:id>", views.devoluciones_formulario_editar, name="devoluciones_formulario_editar"),
	path("devoluciones_actualizar/", views.devoluciones_actualizar, name="devoluciones_actualizar"),
	path("devoluciones_eliminar/<int:id>", views.devoluciones_eliminar, name="devoluciones_eliminar"),

    path('cargar/', views.cargar_image, name='cargar_image'),

	# carrito de compra
	path("carrito_add/", views.carrito_add, name="carrito_add"),
	path("visualizar_carrito/", views.visualizar_carrito, name="visualizar_carrito"),
	path("ver_carrito/", views.ver_carrito, name="ver_carrito"),
	path("vaciar_carrito/", views.vaciar_carrito, name="vaciar_carrito"),
	path("eliminar_item_carrito/<int:id_producto>", views.eliminar_item_carrito, name="eliminar_item_carrito"),
    path("eliminar_item_carrito_ver/<int:id_producto>", views.eliminar_item_carrito_ver, name="eliminar_item_carrito_ver"),
	path("actualizar_totales_carrito/<int:id_producto>/", views.actualizar_totales_carrito, name="actualizar_totales_carrito"),
    path("actualizar_totales_carrito_ver/<int:id_producto>/", views.actualizar_totales_carrito_ver, name="actualizar_totales_carrito_ver"),
 
	#ventas
	path("realizar_venta/", views.realizar_venta, name="realizar_venta"),
    path("ventas_ver/", views.ventas_ver, name="ventas_ver"),
	path("eliminar_venta/<int:id_venta>", views.eliminar_venta, name="eliminar_venta"),
	path("prueba_correo/", views.prueba_correo, name="prueba_correo"),
	path("estado_venta/<int:id>/", views.estado_venta, name="estado_venta"),
	path('lista_pedidos/', views.lista_pedidos, name='lista_pedidos'),

	#etiquetas
    path("etiquetas_listar/", views.etiquetas_listar, name="etiquetas_listar"),
    path("etiquetas_crear/", views.etiquetas_crear, name="etiquetas_crear"),
    path("etiquetas_eliminar/<int:id>", views.etiquetas_eliminar, name="etiquetas_eliminar"),
    path("etiquetas_form_editar/<int:id>", views.etiquetas_formulario_editar, name="etiquetas_form_editar"),
    path("etiquetas_actualizar", views.etiquetas_actualizar, name="etiquetas_actualizar"),
    path("etiquetas_form/", views.etiquetas_form, name="etiquetas_form"),

	#Terminos y condiciones
 	path("term_y_cond/", views.term_y_cond, name="term_y_cond"),

    # Comentarios
    path('comentarios_listar/', views.comentarios_listar, name='comentarios_listar'),
    path("comentarios_form/", views.comentarios_form, name="comentarios_form"),
    path("comentarios_crear/", views.comentarios_crear, name="comentarios_crear"),
    path("comentarios_actualizar/", views.comentarios_actualizar, name="comentarios_actualizar"),
    path('comentarios_eliminar/<int:id>/', views.comentarios_eliminar, name='comentarios_eliminar'),
    path("comentarios_editar/<int:id>", views.comentarios_editar, name="comentarios_editar"),
    path("comentarios_like/<int:id>/", views.comentarios_like, name='comentarios_like'),

	# tallas
	path("tallas_listar/", views.tallas_listar, name="tallas_listar"),
	path("talla_form/", views.tallas_form, name="tallas_form"),
	path("tallas_crear/", views.tallas_crear, name="tallas_crear"),
	path("tallas_actualizar/", views.tallas_actualizar, name="tallas_actualizar"),
	path("tallas_eliminar/<int:id>", views.tallas_eliminar, name="tallas_eliminar"),
 	path("tallas_editar/<int:id>", views.tallas_editar, name="tallas_editar"),
     
	#Trabaja con nosotros
 	path("trabaja_nosotros/", views.trabaja_nosotros, name="trabaja_nosotros"),

	#Pedidos y devoluciones
	path('mis_pedidos/', views.ver_pedidos_cliente, name='mis_pedidos'),
	path('cancelar_pedido/<int:pedido_id>/', views.cancelar_pedido, name='cancelar_pedido'),
    path('admin_pedidos/', views.lista_usuarios, name="lista_usuarios"),
    path('usuarios/<int:usuario_id>/pedidos/', views.ver_pedidos_usuario, name="ver_pedidos_usuario"),
    path('pedidos/<int:pedido_id>/cambiar_estado/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    
    path('pedido/<int:pedido_id>/apelar/', views.apelar_devolucion, name="apelar_devolucion"),
    path('mis_devoluciones/', views.ver_mis_devoluciones, name='ver_mis_devoluciones'),
    path('devoluciones_admin/', views.listar_devoluciones, name='listar_devoluciones'),
    path('devoluciones/<int:devolucion_id>/cambiar_estado/', views.cambiar_estado_devolucion, name='cambiar_estado_devolucion'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)