''' This file is used to get the path of the resource files in the executable. '''

import sys, os

# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

	return os.path.join(base_path, relative_path)