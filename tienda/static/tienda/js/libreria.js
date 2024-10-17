console.log("Hola mundo...!")
//alert("Hola mundo!!")

function eliminar(url){
    if(confirm("Está seguro?")){
        location.href = url;
    }
}

function add_carrito(url, id_producto){
    csrf_token = $("[name='csrfmiddlewaretoken']")[0].value;
    id = $(`#id_${id_producto}`).val()
    cantidad = $(`#cantidad_${id_producto}`).val()
    items_carrito = $("#items_carrito")

    // Capturo referencia a dom de carrito del offCanvas
    contenido = $("#respuesta_carrito")
    loader = $("#loader")

    loader.removeClass("d-none");
    loader.addClass("d-block");

    offCanvas_carrito = $("#offcanvasRight");
    offCanvas_carrito.offcanvas('toggle');

    $.ajax({
        url: url,
        type: "POST",
        data: {"csrfmiddlewaretoken": csrf_token, "id": id, "cantidad": cantidad}
    })
    .done(function(respuesta){

        if (respuesta != "Error"){

            loader.removeClass("d-block");
            loader.addClass("d-none");
            // Pintar respuesta en offCanvas
            contenido.html(respuesta);

            //Buscar items en html resultante
            let position_ini = respuesta.search(" ");
            let position_final = respuesta.search("</h1>");
            let result = respuesta.substring(position_ini+2, position_final-1);
            items_carrito.html(result);
        }
        else{
            location.href="/tienda/inicio/";
        }
    })
    .fail(function(respuesta){
        location.href="/tienda/inicio/";
    });
}


function ver_carrito(url){
    // Capturo referencia a dom de carrito del offCanvas
    contenido = $("#respuesta_carrito")
    loader = $("#loader")

    loader.removeClass("d-none");
    loader.addClass("d-block");

    offCanvas_carrito = $("#offcanvasRight");
    offCanvas_carrito.offcanvas('toggle');

    $.ajax({
        url: url
    })
    .done(function(respuesta){

        if (respuesta != "Error"){
            /*setTimeout(()=>{
                loader.removeClass("d-block");
                loader.addClass("d-none");
                // Pintar respuesta en offCanvas
                contenido.html(respuesta);
            }, 3000);*/

            loader.removeClass("d-block");
            loader.addClass("d-none");
            // Pintar respuesta en offCanvas
            contenido.html(respuesta);

        }
        else{
            location.href="/tienda/inicio/";
        }
    })
    .fail(function(respuesta){
        location.href="/tienda/inicio/";
    });
}

function eliminar_item_carrito(url){
    contenido = $("#respuesta_carrito")
    items_carrito = $("#items_carrito")
    loader = $("#loader")

    loader.removeClass("d-none");
    loader.addClass("d-block");

    $.ajax({
        url: url
    })
    .done(function(respuesta){

        if (respuesta != "Error"){

            loader.removeClass("d-block");
            loader.addClass("d-none");
            // Pintar respuesta en offCanvas
            contenido.html(respuesta);

            //Buscar items en html resultante
            let position_ini = respuesta.search(" ");
            let position_final = respuesta.search("</h1>");
            let result = respuesta.substring(position_ini+2, position_final-1);
            items_carrito.html(result);
        }
        else{
            location.href="/tienda/inicio/";
        }
    })
    .fail(function(respuesta){
        location.href="/tienda/inicio/";
    });
}

function actualizar_totales_carrito(url, id){
    contenido = $("#respuesta_carrito")
    loader = $("#loader")
    cantidad = $("#cantidad_carrito_"+id)

    loader.removeClass("d-none");
    loader.addClass("d-block");

    $.ajax({
        url: url,
        type: "GET",
        data: {"cantidad": cantidad.val()}
    })
    .done(function(respuesta){

        if (respuesta != "Error"){

            loader.removeClass("d-block");
            loader.addClass("d-none");
            // Pintar respuesta en offCanvas
            contenido.html(respuesta);
        }
        else{
            location.href="http://127.0.0.1:8000";
        }
    })
    .fail(function(respuesta){
        location.href="/tienda/inicio/";
    });
}

function darLike(id_comentario) {
    console.log("Dar like al comentario ID:", id_comentario);
    const csrf_token = $("#csrf-token").text().trim();

    $.ajax({
        url: `/comentarios_like/${id_comentario}/`,
        type: "POST",
        data: {
            "csrfmiddlewaretoken": csrf_token
        }
    })
    .done(function(respuesta) {
        if (respuesta.likes !== undefined) {
            document.getElementById(`likes-count-${id_comentario}`).innerText = respuesta.likes;
        } else {
            mostrarError(respuesta.error);
        }
    })
    .fail(function(jqXHR) {
        mostrarError("Ocurrió un error al intentar dar like.");
    });
}

function mostrarError(mensaje) {
    alert(mensaje);
    console.error(mensaje);
}

