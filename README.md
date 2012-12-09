Prueba de concepto de portapapeles compartido
============================================

Instalar cliente
==

- Instalar xclip (yum install -y xclip)
- bajar la carpeta de CLIENT y ejecutar el instalador sh adjunto
- Generar un par de llaves ssh y pasarme la llave publica:
  ssh-keygen -t rsa ~.ssh/llaveportapaples
- Agregar las siguientes lineas al fichero de bashrc:

alias pbcopy='xclip -i -sel clipboard'
alias pbpaste='xclip -o -sel clipboard'

function cpc() {
    scp "$1" portapap@soportefanatico.cl:~/public_html/img;
    echo "http://soportefanatico.cl/~portapap/img/$1" | pbcopy;
    mensaje="Copiado a portapapeles: http://soportefanatico.cl/~portapap/img/$1"
    echo $mensaje; notify-send $mensaje
}


function pbpastec() {
    curl -F 'portapapel=<-' NOMBRESERVIDOR $1 | pbcopy
    mensaje="Copiado a portapapeles: $(pbpaste)"
    echo $mensaje; notify-send $mensaje
}



