import os.path

from gi.repository import Gtk
from api import EightTracksAPI
from playlistview import PlaylistView

"""
	Syntaxis in this program (please obey when contributing):
	"double quotes for names as strings"
	'single quotes for parameters as strings'
	widget names separated-with-dashes
	widget references separated_with_underscores
"""

PLAYER_UI_FILE = "player-modern.ui"

class Player:	
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(PLAYER_UI_FILE)
		self.builder.connect_signals(self)
		self.notebook = self.builder.get_object("notebook-main")
		
		"""dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL,
			message_type=Gtk.MessageType.QUESTION,
			buttons=Gtk.ButtonsType.OK)
		dialog.set_title("blabla")
		dialog.set_markup("You like bla?")
		dialog.run()
		dialog.destroy()"""
		
		self.api = EightTracksAPI()
		
		# create playlist tab
		self.box_playlist = Gtk.Box().new(Gtk.Orientation.VERTICAL, 10)
		self.searchentry = Gtk.SearchEntry().new()
		self.searchentry.connect('search-changed', self.onSearchentryChanged)
		self.view_playlist = PlaylistView()
		self.box_playlist.pack_start(self.searchentry, False, False, 10)
		self.box_playlist.pack_end(self.view_playlist.get_grid(), True, True, 10)
		
		# create now playing tab
		self.box_nowplaying = Gtk.Box().new(Gtk.Orientation.HORIZONTAL, 6)
		self.test = Gtk.Label().new("asd")
		self.box_nowplaying.pack_start(self.test, True, True, 0)
		
		# add playlist tab, set properties
		self.notebook.append_page(self.box_playlist, Gtk.Label().new("Search Playlists"))
		self.notebook.child_set_property(self.box_playlist, 'tab-expand', True)
		self.notebook.child_set_property(self.box_playlist, 'tab-fill', True)
		
		# add now playing tab, set properties
		self.notebook.append_page(self.box_nowplaying, Gtk.Label().new("Now Playing"))
		self.notebook.child_set_property(self.box_nowplaying, 'tab-expand', True)
		self.notebook.child_set_property(self.box_nowplaying, 'tab-fill', True)
		
		self.box_playlist = Gtk.Box().new(Gtk.Orientation.HORIZONTAL, 6)
		self.notebook.show_all()
		
		self.window_player = self.builder.get_object("window-player")
		self.window_player.connect("delete-event", Gtk.main_quit)
		self.window_player.show_all()
		
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)
		
	def onToolbuttonAboutClicked(self, toolbutton):
		print("lol")
		
	def onSearchentryChanged(self, searchentry):
		print(searchentry.get_text())
		search = searchentry.get_text()
		self.put_mixes_in_grid(self.get_mixes('tag', search, 1))
		
		# actual functions are_named_like_this
	
	def get_mixes(self, search_type, search_keyword, page):
		results = self.api.search_mix(search_type, search_keyword, 'hot', page, 10)
		return results[0]
			
	def put_mixes_in_grid(self, mixes):
		self.view_playlist.remove_all_items()
		#print("mixes "+mixes)
		for i, mix in enumerate(mixes):
			print("mix "+mix['name'])
			self.view_playlist.add_item(mixes[i])

def main():
	player = Player()
	Gtk.main()

if __name__ == '__main__':
	main()
