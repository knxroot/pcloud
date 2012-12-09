# put me at /usr/share/glipper/plugins/portapapeles.py

import httplib, gtk, urllib, webbrowser, threading
import glipper
import pynotify

from gettext import gettext as _

def info():
    info = {"Name": _("Portapapeles en las Nubes"), 
            "Description": _("Paste your clipboard iin the cloud"),
            "Preferences": False}
    return info

class Portapapel(threading.Thread):
    def __init__(self, text):
        threading.Thread.__init__(self)
        self.text = text

    def run(self):
        conn = httplib.HTTPConnection("127.0.0.1:8080")
        params = urllib.urlencode({"portapapel": self.text})
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        conn.request("POST", "", params, headers)
        url = conn.getresponse().read()
        conn.close()
        pynotify.init("lacosox")
        print "bbb"
        print url
        info=pynotify.Notification("Portapapeles en las Nubes",url,"dialog-information")
        info.show()


def activated(menu):
    sp = Portapapel(glipper.get_history_item(0))
    sp.start()

def init():
    item = gtk.MenuItem(_("Portapapel.es"))
    item.connect('activate', activated)
    glipper.add_menu_item(item)


