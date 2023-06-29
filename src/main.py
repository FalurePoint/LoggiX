# main.py
#
# Copyright 2023 Asa Lorentzen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi


gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import Loggix44Window

_display_global_string = ""
_debug_global_string = ""
_aprint_ticker = 1

print("Begin run log:")

class Loggix44Application(Adw.Application):
    """The main application singleton class."""
    global _display_global_string
    global _debug_global_string

    def __init__(self):
        self.aprint("Started LoggiXApplicationWindow class running from there...")
        self.aprint("application id set to 'org.failurepoint.loggix'")
        super().__init__(application_id='org.failurepoint.loggix',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)

        self.aprint("Setting internal actions list from hard-coded defienitions.")
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('connect_account', self.on_connect_account, ['<primary>a'])
        self.create_action('focus_new_entry', self.on_log_button_clicked, ['<ctrl><alt>n'])
        self.create_action('export_cab', self.not_implemented_yet, ['<primary>e'])
        self.create_action('refresh_gui', self.refresh_display, ['<primary><super>r'])
        self.create_action('get_inputs', self.read_from_inputs, ['<primary><super>i'])
        self.create_action('debug_data', self.live_debug, ['<primary><super>d'])
        self.aprint("Done.")


    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.aprint("checking if window is active")
        win = self.props.active_window
        if not win:
            self.aprint("Window not found! Raising winodw now.")
            win = Loggix44Window(application=self)
        else:
            self.aprint("Window found and is already running.")
        self.aprint("Done.")
        win.present()

        """connect the signals"""
        #TODO clean redundant unnecessary code here.
        self.aprint("re-routing ui signals to in internal aliases.")
        self.aprint("the alias system is overly complex. please address this soon.", msg_text="Warning")
        win.logit.connect("clicked", self.on_log_button_clicked)
        self.display = win.textview
        self.input_time = win.time_entry
        self.input_date = win.date_entry
        self.input_freq = win.freq_entry
        self.input_callsign = win.callsign_entry
        self.input_power = win.power_entry
        self.input_mode = win.mode_entry
        self.input_rst = win.rst_entry
        self.input_txch = win.txch_entry
        self.input_rxch = win.rxch_entry

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        self.aprint("About action called. Showing window.")
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='loggiX',
                                application_icon='org.failurepoint.loggix',
                                developer_name='Asa Lorentzen',
                                version='0.1.0 Pre-Alpha',
                                developers=['Asa Lorentzen'],
                                copyright='© 2023 Asa Lorentzen')
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        self.aprint('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)
        self.aprint(f"action '{str(name)}' registered with shortcut '{shortcuts}'")

    def read_from_inputs(self, widget=None, _=None):
        a = self.input_time.get_text()
        b = self.input_date.get_text()
        c = self.input_freq.get_text()
        d = self.input_callsign.get_text()
        e = self.input_power.get_text()
        f = self.input_mode.get_text()
        g = self.input_rst.get_text()
        h = self.input_rxch.get_text()
        i = self.input_txch.get_text()
         # widget only becomes something if called from the shortcut command.
        if widget != None:
            self.aprint(f"input values refreshed values are '{a} | {b} | {c} | {d} | {e} | {f} | {g} | {h} | {i}'")
        return a, b, c, d, e, f, g, h, i, f"{a} | {b} | {c} | {d} | {e} | {f} | {g} | {h} | {i}"

    def on_log_button_clicked(self, widget, load=None):
        global _display_global_string
        self.aprint("log button activated")
        _display_global_string = str(self.read_from_inputs()[9] + "\n\n" + _display_global_string)
        self.aprint(f"new input string: {self.read_from_inputs()[9]}")
        self.refresh_display(source=_display_global_string)


    def on_connect_account(self, widget=None, _=None):
        self.aprint("Connect account activated!")


    def not_implemented_yet(self, widget, _=None):
        self.aprint("A request for a non-existent callback was made, showing feature implementation warning dialog.")
        warning = Adw.MessageDialog.new(
        self.props.active_window,
        "404! this feature seems to be QRT!",
        "Sorry you had to see this! this feature is in the works but not ready yet! check back later and it may be working then!")
        warning.add_response("OK","OK")
        warning.present()

    #TODO remove debug ticker system remainants in favor of a "Entry:" system.
    def aprint(self, source, msg_text="Entry", widget=None, _=None):
        global _debug_global_string
        global _aprint_ticker
        _debug_global_string = _debug_global_string + f"{msg_text:}:    " + source + "\n"
        self.live_debug(if_none_create=False)
        _aprint_ticker += 1
        print(f"{msg_text}:    " + source )

    #TODO fix multi window opening ability bug
    def live_debug(self, widget=None, _=None, if_none_create=True):
        try:
            self.debugtextview.get_buffer().set_text(_debug_global_string)
        except:
            pass
        if if_none_create:
            self.aprint("Live debug signal emitted. Opening window...")
            window = Gtk.Window(title="LoggiX live debug feed")
            window.set_default_size(500, 300)
            self.debugtextview = Gtk.TextView()
            self.debugtextview.set_editable(True)
            scrolled_window = Gtk.ScrolledWindow()
            scrolled_window.set_child(self.debugtextview)
            window.set_child(scrolled_window)
            self.debugtextview.get_buffer().set_text(_debug_global_string)
            window.present()




    def refresh_display(self, widget=None, _=None, source=_display_global_string):
        # widget only becomes something if called from the shortcut command.
        if widget != None:
            self.aprint("Display updated! id=textview from: _display_global_string")
        global _display_global_string
        self.display.get_buffer().set_text(source)


def main(version):
    """The application's entry point."""
    app = Loggix44Application()
    return app.run(sys.argv)
