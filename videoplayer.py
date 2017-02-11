
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
import socket

gtk.gdk.threads_init()

import sys
import vlc

import serial
ser = serial.Serial("/dev/ttyACM0", 9600)

from gettext import gettext as _

import threading


def send_message(message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip='localhost'
        port = 8080
        BUFFER_SIZE = 1024
        sock.connect((ip, port))
        sock.send(message)
        sock.close()
    except:
        print 'Couldnt send message'

def parse_input(gui):
    current_word = []

    entire_message = []

    abvs = {'btw': 'BY THE WAY', 'hhu': 'HI HOW ARE YOU? ', 'afaik': 'AS FAR AS I KNOW',
            'pot': 'POINT OF VIEW', 'ge': 'GOOD EVERNING', 'ind': 'INDIA', 'gn': 'GOOD NIGHT',
            'gm': 'GOOD MORNING',
            'txt': 'TEXT', 'ie': 'THAT IS', 'brb': 'BE RIGHT BACK', 'cu': 'SEE YOU', 'grt': 'GREAT', 'thnx': 'THANKS', 'lol': 'LAUGHING OUT LOUD', '2': 'TO', '4': 'FOR', 'msg': 'MESSAGE', 'omg': 'OH MY GOD!!', 'asap': 'AS SOON AS POSSIBLE', 'plz': 'PLEASE', 'np': 'NO PROBLEM', '2moro': 'TOMMOROW', 'thku': 'THANK YOU', 'c': 'SEE', 'k': 'OK', 'coz': 'BECAUSE', 'sos': 'SAVE OUR SOULS',
            'bcc': 'BRING ME A CUP OF COFFEE',
            'idk': "I DON'T KNOW", 'y': 'WHY', 'ot': 'OUT OF CONTEXT', 'ily': ' I LOVE YOU'}

    while True:
        data = ser.readline().strip()


        if data == "its a dit":
            current_word.append("0")
        elif data == "its a dash":
            current_word.append("1")

        print current_word

        if len(current_word) == 5:
            number = int(''.join(current_word), 2)
            buffer = gui.control_box.talk.message.get_buffer()

            if not number:
                # @ToDo Send Message to Rocky
                message = ''.join(entire_message)
                if message.strip() in abvs:
                    message = abvs[message.strip()].lower()
                    message = message[0].upper() + message[1:]
                else:
                    print 'Entire Message: %s' %(message)

                buffer.set_text(message)

                send_message(message)
                entire_message = []
                current_word = []
                continue
            elif number < 26:
                message = chr(ord('a') + number - 1)
                buffer.set_text(message)
                print 'Character: %s' %(message)
            elif number == 27:
                message = " "
            elif number == 28:
                # @ToDO Gyani independent sendall this asap
                message = "change_mode"
                current_word = []
                data = s.recv(BUFFER_SIZE)
                buffer.set_text(message)
                send_message(message)
                continue
            elif number == 29:
                # @ToDO independent sendall
                gui.control_box.talk.message.get_buffer().set_text(message)
                message = "this_is_an_sos"
                send_message(message)
                buffer.set_text(message)
                current_word = []
                continue
            else:
                message = "invalid-command"
                buffer.set_text(message)

            entire_message.append(message)
            current_word = []
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
        self.le = gtk.Button("Le")
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
        self.dw.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.le.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.ri.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.st.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        send_message("move_forward")

    def dwc(self, p):
        self.up.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.dw.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#00ff00'))
        self.le.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.ri.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.st.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        send_message("move_backward")

    def lec(self, p):
        self.up.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.dw.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.le.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#00ff00'))
        self.ri.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.st.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        send_message("move_left")

    def ric(self, p):
        self.up.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.dw.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.le.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.ri.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#00ff00'))
        self.st.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        send_message("move_right")


    def stc(self, p):
        self.up.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.dw.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.le.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.ri.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ffffff'))
        self.st.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#00ff00'))
        send_message("move_stop")


class Talk(gtk.VBox):

    def __init__(self, *p):
        gtk.VBox.__init__(self)

        self.message = gtk.TextView()

        ibufer = gtk.TextBuffer
        self.input = gtk.TextView()
        self.message.set_editable(setting=False)

        self.input.set_editable(setting=True)
        self.send = gtk.Button("Send Input")
        self.send.connect("clicked", self.send_data)


        self.message.set_size_request(30,30)
        self.input.set_size_request(30,30)

        self.add(self.message)
        self.add(HackPad())
        self.add(HackPad())

        self.add(self.input)
        self.add(self.send)

    def send_data(self, p):
        buffer_ = self.input.get_buffer()
        s,e = buffer_.get_bounds()
        data = buffer_.get_text(s, e)

        buffer_ = self.input.get_buffer()
        buffer_.set_text("")
        send_message(data)



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
        if self.outer.loco not in self.outer:
            self.outer.add(self.outer.loco)
        self.Loco.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#00ff00'))
        self.Talk.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#ff0000'))

    def talkb(self, p=None):
        if self.outer.loco in self.outer:
            self.outer.remove(self.outer.loco)
        if self.outer.talk not in self.outer:
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

        self.control_box = Controller()
        controls.add(self.control_box)


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

        self.control_box.top.locob()

        gtk.main()

if __name__ == '__main__':
    # Multiple files.
    p=MultiVideoPlayer()

    gui_thread = threading.Thread(target=p.main, kwargs={"filenames": ["rtp://@192.168.43.132"]})
    gui_thread.start()

    audio_thread = threading.Thread(target=parse_input, kwargs={"gui": p})
    audio_thread.start()

    # parse_input(p)