import kivy
kivy.require('1.0.7')

from kivy.app import App
from os.path import join
from glob import glob
from xdg import Menu, DesktopEntry

class LauncherApp(App):
	pass

if __name__ == '__main__':
	application_directories = [join(p,'applications') for p in Menu.xdg_data_dirs]

	entries = []

	for directory in application_directories: 
		for f in glob(join(directory,"**/*.desktop"), recursive=True):
			entry = DesktopEntry.DesktopEntry(f)
			if not entry.getNoDisplay():
				entries.append(entry)

	for e in entries:
		print(e.getName())

	LauncherApp().run()
