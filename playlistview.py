import requests
from gi.repository import Gtk, Gdk, GdkPixbuf, Pango

class PlaylistView():
	
	current_column = 0
	current_row = 0
	COVER_FILENAME = "/tmp/temporary_cover.jpg"
	COVER_DIMENSIONS = 150
	
	def add_item(self, item):
		box_result_item = Gtk.Fixed().new()
		box_result_item.set_size_request(self.COVER_DIMENSIONS, self.COVER_DIMENSIONS)
		label_result_item_title = Gtk.Label(item['name'])
		label_result_item_title.set_ellipsize(Pango.EllipsizeMode.END)
		label_result_item_title.set_size_request(self.COVER_DIMENSIONS, 10)
		label_result_item_title.override_color(Gtk.StateType.NORMAL, Gdk.RGBA(1,1,1,1))
		r = requests.get(item['cover_urls']['original'])
		with open(self.COVER_FILENAME, "wb") as code:
			code.write(r.content)
		box_label_result_item_title = Gtk.Box().new(Gtk.Orientation.HORIZONTAL, 0)
		box_label_result_item_title.pack_start(label_result_item_title, False, False, 0)
		box_label_result_item_title.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.5,.5,.5,.75))
		image_result_item_image = Gtk.Image()
		pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.COVER_FILENAME, self.COVER_DIMENSIONS, self.COVER_DIMENSIONS,
                                                 preserve_aspect_ratio=False)
		image_result_item_image.set_from_pixbuf(pixbuf)
		box_result_item.put(image_result_item_image, 0, 0)
		box_result_item.put(box_label_result_item_title, 0, self.COVER_DIMENSIONS - 10)
		self.playlist.attach(box_result_item, self.current_column, self.current_row, 1, 1)
		if self.current_column > 2:
			self.current_column = 0
			self.current_row += 1
			self.update()
		else:
			self.current_column += 1
		#self.playlist.pack_start(item, True, False, 0)
		
	def remove_all_items(self):
		print("lol")

	def get_grid(self):
		return self.playlist

	def update(self):
		self.playlist.show_all()

	def __init__(self):
		self.playlist = Gtk.Grid().new()
