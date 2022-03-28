# Requisitos #

Jersey Shop es una exportadora y tienda de ropa que se dedica a la venta de estos productos a nivel
municipal en la ciudad de Armenia, Quindío, en Colombia. La idea de implementar software se centra básicamente en el desarrollo
de una tienda virtual que permita a los usuarios visitantes del aplicativo, realizar compras en la aplicación. Por otro lado
para los encargados o administrativos del sistema, deberían poder tener la capacidad de implementar nuevos productos
en la tienda, gestionar las estadisticas, anunciar o notificar a los usuarios de la plataforma sobre nuevos productos, promociones, etc.

## Roles del aplicativo ##

Se definen los roles principales que componen el aplicativo, resaltándolos en órden jerargico y teniendo en cuenta
que existe la posibilidad que se creen nuevos roles. También cabe aclarar que el administrativo o administrativos, tendrán
la posibilidad anteriormente mencionada, se listan así:

1. Visitante
2. Cliente?
3. Vendedor?
4. Administrativo/Encargado?

## Requisitos funcionales ##

Hacen referencia a como actuará el sistema o que funcionalidades serán implementadas.

1. Visitante
   1. El sistema permitirá que el visitante pueda visualizar de forma explicita los productos disponibles en la plataforma sin la necesidad de registrarse o iniciar sesión.
   2. El aplicativo permitirá que los visitantes puedan consultar los anuncios disponibles.
   3. Los visitantes no podrán realizar compras dentro del aplicativo, deberán registrarse o iniciar sesión en caso de tener una cuenta.
   4. El aplicativo les permitirá cambiar el idioma, el tema y otros detalles dentro de la aplicación.
   5. El sistema deberá permitir que los visitantes inicien sesión o se registren de forma local o utilizando una red social como Facebook o Google.
2. Cliente
   1. El sistema le dará la posibilidad al cliente de configurar su perfil con los datos personales y detalles asociados.
   2. Podrá realizar compras por medio del aplicativo.
   3. Podrá agregar productos a la sección de favoritos.
   4. Podrá agregar multiples productos al carrito de compra y realizar un pedido.
   5. Tendrá la posibilidad de acceder a todas las funciones a las cuales tiene acceso el visitante.
   6. Podrá acceder a las salas de soporte para hacer preguntas referentes a productos y demás asociados.
   7. Tendrá el beneficio de aplicar cupones de descuentos a los productos que hayan habilitados.
3. Vendedor
   1. El sistema identificará al vendedor como un asistente del sistema.
   2. Podrá crear salas de soporte para atender a los clientes que lo requieran.
   3. Podrá realizar gestionar los tickets de un cliente.
   4. Tendrá acceso parcial a información no íntima o confidencial de los clientes registrados en la plataforma para poder gestionar problemas con pedidos u otros inconvenientes.
   5. Podrá generar recibos de forma manual.
   6. Podrá acceder a los modulos de dashboard e inventario de productos, limitando su operabilidad.
4. Administrador
   1. Podrá gestionar todos los anuncios del sistema
   2. Podrá gestionar el inventario de productos agregando, eliminando, editando o consultando los ya existentes.
   3. Podrá gestionar los usuarios del sistema.
   4. Podrá gestionar las salas de soporte que hayan creado los vendedores.
   5. Tendrá la posibilidad de notificar cuando se hayan implementado nuevos productos al aplicativo.
   6. Tendrán acceso a todo el panel de herramientas que tendrá la plataforma, tales como estadísticas, inventario, dashboard, salas de soporte, entre otros.
   7. Podrá gestionar los grupos y permisos del aplicativo.
   8. Tendrá acceso completo al sistema y a todas las funciones anteriormente mencionadas.
   9. Podrá visualizar todos los pedidos realizados por clientes ordenandolos por categoria: en proceso, vencido, entregado, devolución, etc.

## Requisitos no funcionales ##

Los requisitos funcionales establecen el funcionamiento interno o como deberá actuar el sistema en determinados contextos.

1. El sistemá deberá permitir la conexión de multiples usuarios en el sistema independientemente del rol que estos posean.
2. El aplicativo deberá poder mostrarse de forma adecuada en un dispositivo movil
3. El sistemá deberá administrar los modulos que se cargarán en el navegador para que el tiempo de respuesta sea optimo para el usuario.
4. El sistema deberá contar con un diseño optimo para afianzar las experiencia del usuario
5. Los datos almacenados para cada usuario deberán seguir con un proceso que garantice que no serán vulnerados de ninguna forma.
6. El sistema deberá refrescar o detectar los cambios que se realicen con la base de datos.
7. EL sistema tendrá la posibilidad de usar un idioma especifico dejando escoger entre dos, los cuales serán inglés y español.
8. El sistema deberá dejar descargar a los usuarios información que requieran, tal como facturación.
9. Los permisos o grupos solo podrán ser gestionados por el administrador.
10. El sistema deberá pedir una confirmación al usuario cada que se intente eliminar un dato vulnerable, tal como un producto, inhabilitar una cuenta, eliminar un anuncio, un cupón, etc.
