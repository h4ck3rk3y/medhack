
#! /usr/bin/python

"""VLC Gtk Widget classes + example application.

This module provides two helper classes, to ease the embedding of a
VLC component inside a pygtk application.

VLCWidget is a simple VLC widget.

DecoratedVLCWidget provides simple player controls.

When called as an application, it behaves as a video player.

$Id$
"""

import gtk
gtk.gdk.threads_init()

import sys
import vlc

from gettext import gettext as _

def send_message(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip='192.168.43.132'
    port = 8080
    BUFFER_SIZE = 1024
    sock.connect((ip, port))
    sock.send(message)
    sock.close()

# Create a single vlc.Instance() to be shared by (possible) multiple players.
instance = vlc.Instance()

class VLCWidget(gtk.DrawingArea):
    """Simple VLC widget.

    Its player can be controlled through the 'player' attribute, which
    is a vlc.MediaPlayer() instance.
    """
    def __init__(self, *p):
        gtk.DrawingArea.__init__(self)
        self.player = instance.media_player_new()
        def handle_embed(*args):
            if sys.platform == 'win32':
                self.player.set_hwnd(self.window.handle)
            else:
                self.player.set_xwindow(self.window.xid)
            return True
        self.connect("map", handle_embed)
        self.set_size_request(320, 200)



class HackPad(gtk.VBox):

    def __init__(self, *p):
        gtk.VBox.__init__(self)



class Loco(gtk.VBox):

    def __init__(self, *p):
        gtk.VBox.__init__(self)

        self.up = gtk.Button("Up")
        self.dw = gtk.Button("Dw")
        self.le = gtk.Button("Dw")
        self.ri = gtk.Button("Ri")
        self.st = gtk.Button("st")

        self.up.connect("clicked", self.upc)
        self.dw.connect("clicked", self.dwc)
        self.le.connect("clicked", self.lec)
        self.ri.connect("clicked", self.ric)
        self.st.connect("clicked", self.stc)

        self.add(self.up)
        self.add(self.dw)
        self.add(self.le)
        self.add(self.ri)
        self.add(self.st)

        self.st.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#00ff00'))

    def upc(self, p):
        self.up.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#00ff00'))
        self.dw.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.le.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.ri.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.st.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))


    def dwc(self, p):
        self.up.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.dw.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#00ff00'))
        self.le.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.ri.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.st.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))

    def lec(self, p):
        self.up.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.dw.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.le.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#00ff00'))
        self.ri.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.st.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))

    def ric(self, p):
        self.up.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.dw.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.le.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.ri.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#00ff00'))
        self.st.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))




    def stc(self, p):
        self.up.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.dw.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.le.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.ri.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
        self.st.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#00ff00'))


class Talk(gtk.VBox):

    def __init__(self, *p):
        gtk.VBox.__init__(self)

        self.message = gtk.TextView(buffer=None)

        self.input = gtk.TextView(buffer=None)

        self.input.set_editable(True)
        self.send = gtk.Button("Send Input")

        self.message.set_size_request(30,30)
        self.input.set_size_request(30,30)

        self.add(self.message)
        self.add(self.input)
        self.add(self.send)


class Top(gtk.HBox):

    def __init__(self, outer):
        gtk.HBox.__init__(self)

        self.outer = outer

        self.Loco = gtk.Button("Loco")

        self.Loco.connect("clicked", self.locob)

        self.Loco.set_size_request(100,20)

        self.Talk = gtk.Button("Talk")

        self.Talk.connect("clicked", self.talkb)

        self.Talk.set_size_request(100,20)


        self.pack_start(self.Loco, expand=False, padding=20)
        self.pack_start(self.Talk, expand=False, padding=0)


    def locob(self, p=None):
        if self.outer.talk in self.outer:
            self.outer.remove(self.outer.talk)
        self.outer.add(self.outer.loco)
        self.Loco.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#00ff00'))
        self.Talk.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ff0000'))

    def talkb(self, p=None):
        if self.outer.loco in self.outer:
            self.outer.remove(self.outer.loco)

        self.outer.add(self.outer.talk)

        self.Loco.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ff0000'))
        self.Talk.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#00ff00'))



class Controller(gtk.VBox):

    def __init__(self, *p):
        gtk.VBox.__init__(self)


        self.loco = Loco()
        self.talk = Talk()

        self.top = Top(self)

        self.add(self.top)
        self.add(HackPad())
        self.add(HackPad())

        self.add(self.loco)
        self.add(self.talk)


class DecoratedVLCWidget(gtk.VBox):
    """Decorated VLC widget.

    VLC widget decorated with a player control toolbar.

    Its player can be controlled through the 'player' attribute, which
    is a Player instance.
    """
    def __init__(self, *p):
        gtk.VBox.__init__(self)
        self._vlc_widget = VLCWidget(*p)
        self.player = self._vlc_widget.player
        self.pack_start(self._vlc_widget, expand=True)
        self._toolbar = self.get_player_control_toolbar()
        self.pack_start(self._toolbar, expand=False)

    def get_player_control_toolbar(self):
        """Return a player control toolbar
        """
        tb = gtk.Toolbar()
        tb.set_style(gtk.TOOLBAR_ICONS)
        for text, tooltip, stock, callback in (
            (_("Play"), _("Play"), gtk.STOCK_MEDIA_PLAY, lambda b: self.player.play()),
            (_("Pause"), _("Pause"), gtk.STOCK_MEDIA_PAUSE, lambda b: self.player.pause()),
            (_("Stop"), _("Stop"), gtk.STOCK_MEDIA_STOP, lambda b: self.player.stop()),
            ):
            b=gtk.ToolButton(stock)
            b.set_tooltip_text(tooltip)
            b.connect("clicked", callback)
            tb.insert(b, -1)
        tb.show_all()
        return tb

class VideoPlayer:
    """Example simple video player.
    """
    def __init__(self):
        self.vlc = DecoratedVLCWidget()

    def main(self, fname):
        self.vlc.player.set_media(instance.media_new(fname))
        w = gtk.Window()
        w.add(self.vlc)
        w.show_all()
        w.connect("destroy", gtk.main_quit)
        gtk.main()

class MultiVideoPlayer:
    """Example multi-video player.

    It plays multiple files side-by-side, with per-view and global controls.
    """
    def main(self, filenames):
        # Build main window
        window=gtk.Window()
        mainbox=gtk.HBox()
        videos=gtk.HBox()

        controls = gtk.HBox()

        window.add(mainbox)
        mainbox.add(videos)
        mainbox.add(controls)

        control_box = Controller()
        controls.add(control_box)


        # Create VLC widgets
        for fname in filenames:
            v = DecoratedVLCWidget()
            v.player.set_media(instance.media_new(fname))
            videos.add(v)

        def execute(b, methodname):
            """Execute the given method on all VLC widgets.
            """
            for v in videos.get_children():
                getattr(v.player, methodname)()
            return True

        window.show_all()
        window.connect("destroy", gtk.main_quit)

        control_box.top.locob()

        gtk.main()

if __name__ == '__main__':
    # Multiple files.
    p=MultiVideoPlayer()
    p.main(["do.mp4"])