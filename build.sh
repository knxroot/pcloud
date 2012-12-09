servername="127.0.0.1:8080"

cp SERVER/portapapeles/portapapeles-init.py SERVER/portapapeles/portapapeles.py
sed -i -e 's/NOMBRESERVIDOR/'$servername'/g' SERVER/portapapeles/portapapeles.py
cp CLIENT/glipper_pluggin/portapapeles-init.py CLIENT/glipper_pluggin/portapapeles.py
sed -i -e 's/NOMBRESERVIDOR/'$servername'/g' CLIENT/glipper_pluggin/portapapeles.py
