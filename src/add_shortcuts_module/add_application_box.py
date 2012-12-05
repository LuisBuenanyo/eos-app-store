import gtk
import cairo
from eos_util import image_util
from eos_util import screen_util
from osapps.desktop_preferences_datastore import DesktopPreferencesDatastore
from application_row_box import ApplicationRowBox

class AddApplicationBox(gtk.VBox):
    def __init__(self, parent, add_remove_widget=None, desktop_preference_class = DesktopPreferencesDatastore, default_category=''):
        super(AddApplicationBox, self).__init__()
        self.set_homogeneous(False)

        self._presenter = parent._presenter
        self._parent = parent
        self.x = 0
        self.y = 0
        self._refresh = True
        self._scrolling = False

        self._desktop_preferences = desktop_preference_class.get_instance()
        self._background = self._desktop_preferences.get_scaled_background_image(
                screen_util.get_width(parent.window), screen_util.get_height(parent.window))

        self._viewport = gtk.ScrolledWindow()
        self._viewport.set_policy(hscrollbar_policy=gtk.POLICY_NEVER, vscrollbar_policy=gtk.POLICY_AUTOMATIC)
        self._viewport.connect("show", self._on_show)

        self._active_category = default_category
        apps = self._presenter.get_category(self._active_category)
        self._fill_applications(apps)

        self._vbox.set_homogeneous(False)

        self._vbox.connect("expose-event", self._handle_expose_event)
        self._viewport.add_with_viewport(self._vbox)
        self.add(self._viewport)
        self.show_all()

    def _fill_applications(self, apps):
        self._vbox = gtk.VBox()
        if apps:
            for app in apps:
                self._display_application(app)

    def _display_application(self, app):
        row = ApplicationRowBox(app, parent=self, presenter=self._presenter)
        row.connect("enter-notify-event", self._draw_active, row)
        row.connect("leave-notify-event", self._draw_inactive, row)
        self._vbox.pack_start(row, False, False, 0)

    def _on_show(self, widget):
        widget.get_child().set_shadow_type(gtk.SHADOW_NONE)
        
    def _handle_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        x, y = self._vbox.window.get_origin()
        top_x, top_y = self._viewport.window.get_toplevel().get_origin()
        self.draw(cr, x - top_x, y - top_y, self.allocation.width, self.allocation.height)
        
        # TODO what is the purpose of self._refresh?
        # In the current implementation, things look better for the website box
        # without the check, so I'm disabling it here as well
        # if not self._refresh and event:
        if event:
            self._draw_gradient(cr, event.area.width, event.area.height, event.area.x, event.area.y)

        return False

    def draw(self, cr, x, y, w, h):
        self._viewport.get_child().set_shadow_type(gtk.SHADOW_NONE)
        # Only copy/crop the background the first time through
        # to avoid needless memory copies and image manipulation
        if not self._scrolling:
            self._background = self._background.copy().crop(x, 0, w, h)
            self._scrolling = True
        scroll_y = self._viewport.get_vscrollbar().get_value()
        self._background.draw(lambda pixbuf: cr.set_source_pixbuf(pixbuf, 0, scroll_y))
        cr.paint()

    def _draw_gradient(self, cr, w, h, x=0, y=0):
        pat = cairo.LinearGradient (0.0, 0.0, w, 0.0)
        pat.add_color_stop_rgba (0.001, 0.0, 0.0, 0.0, 0.8)
        pat.add_color_stop_rgba (1, 0.2, 0.2, 0.2, 0.8)

        cr.rectangle(x, y, w, h)
        cr.set_source(pat)
        cr.fill()

    def _draw_active(self, widget, event, row):
        self._refresh = False
        widget.name_label.set_markup('<span color="#ffffff" font="Novecento wide" font_weight="bold">' + widget._name + '</span>')
        widget.description_label.set_markup('<span color="#ffffff" font-style="italic">' + widget._description + '</span>')
        widget._plus_image.set_from_file(image_util.image_path("add_folder_icon.png"))
        widget._plus_image.show()
        pixbuf = image_util.load_pixbuf(image_util.image_path('category_separator_inactive.png'))
        pixbuf = pixbuf.scale_simple(self.allocation.width, pixbuf.get_height(), gtk.gdk.INTERP_BILINEAR)
        widget._bottom_active_line.set_from_pixbuf(pixbuf)
        widget._top_active_line.set_from_pixbuf(pixbuf)
        widget.draw(widget.get_allocation())

        return False

    def _draw_inactive(self, widget, event, row=None):
        self._refresh = True
        widget.name_label.set_markup('<span color="#aaaaaa" font="Novecento wide" font_weight="bold">' + widget._name + '</span>')
        widget.description_label.set_markup('<span color="#aaaaaa" font-style="italic">' + widget._description + '</span>')
        widget._plus_image.hide()
        widget._bottom_active_line.set_from_pixbuf(None)
        widget._top_active_line.set_from_pixbuf(None)
        widget.draw(widget.get_allocation())

        return False

    def install_app(self, app):
        self._parent.install_app(app)
        self._parent.destroy(None, None)

