
__all__ = ['']

"""
    :format NOTIFY_FORMAT - Declara el formato a seguir
    cuando se notifica a un usuario acerca de un anuncio.
    :param name - El nombre del usuario al cual se le envia el correo.
    :param message - Mensaje acerca del anuncio realizado.
    :param hyperlink - Enlace asociado al anuncio enviado.
"""
NOTIFY_FORMAT = """
    <center>
        <div style="padding: 0%;
            margin: 0%;
            width: 75%;
            height: 100%;
            border:1px solid rgba(0,0,0,0.25);
            padding: 24px;
            border-radius: 25px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;"
        >
        <img style="width: 75%; float: left; margin-left: 16%;" 
            src="https://i.imgur.com/ezOUjf5.png" alt="Company logo">
        <br style="clear: both;">
        <center>
            <h1 style="font-weight: 400;">Nos gusta saludarte</h1> 
            <h2 style="font-weight: 400; font-size:24px;">
                <br>
                Y por ello te traemos noticias desde Jersey Shop
            </h2>
            <h2 style="font-weight: 400;">
                {0}
                <br>
                <br>
                <a style="color: white;
                    padding: 10px;
                    border-radius: 10px;
                    background-color: rgb(10, 137, 255);
                    font-style: none;
                    text-decoration: none;
                    font-size: 1.3rem;"
                    href="{1}">
                        Ver mas
                    </a>
            </h2>
        </center>
        </div>
    </center>
"""