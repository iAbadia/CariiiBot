# CariiiBot

El bot de mi Cariii 😘

## Descripción

Bot de Telegram para respuestas automatizadas para mi Cariii.

## Características

### Cariii
Respuesta automatizada a mensajes que contengan la cadena `cari`. Composición del mensaje:

 - Se incluye la cadena `Cari` al principio.
 - Se añade una cadena de carácteres `i` de tamaño aleatorio entre 0 y 10.
 - Un espacio.
 - Cadena de emojis. 3 modos: `single-long`, `couple-long-short` y `party`

 #### Cadena de emojis

 - **single-long** Una cadena copuesta de un emoji elegido aleatoriamente y repetido entre 3 y 10 veces.

 - **couple-long-short** Cadena compuesta de 2 emojis A y B elegidos aleatoriamente. A es repetido entre 6 y 10 veces, B es repetido entre 1 y 5 veces.

 - **party** Compuesto por entre 10 y 15 emojis elegidos aleatoriamente. Puede haber repeticiones.

### What
Respuesta automatizada a cualquier mensaje que no contenga la cadena `cari`.

## Uso
Es necesario crear un fichero `.telegram-token` que contenga en una única línea el token del Bot. Puedes aprender como obtener uno [aqui](https://core.telegram.org/bots#6-botfather). Dicho fichero deberá situarse en el mismo directorio que el script. Una vez hecho esto ya es posible lanzar el Bot con:

`python cariiibot.py`

#### Recomendación
Es habitual querer tener el Bot activo en un servidor (E.g. RaspberryPi), una buena solución para poder hacerlo y no mantener una sesión abierta permanente es usar [`screen`](https://www.gnu.org/software/screen/manual/screen.html). En Debian puede obtenerse mediante `apt-get install screen`.