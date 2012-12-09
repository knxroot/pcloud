wget https://launchpad.net/glipper/trunk/2.4/+download/glipper-2.4.tar.gz
tar -xvzf glipper*
cd glipper*
yum install -y intltool py-notify pygtk-2.6 python-keybinder python-distutils-extra python-appindicator python-xdg python-prctl python-crypto
python setup.py install
echo "instalando pluggin a glipper"
cp glipper_pluggin/portapapeles.py /usr/share/glipper/plugins/
glipper&
