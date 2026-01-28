# coding=utf-8

plugin_identifier = "autozoffset"
plugin_package = "octoprint_autozoffset"
plugin_name = "OctoPrint-AutoZOffset"
plugin_version = "0.1.0"
plugin_description = """Automatically sets Z-offset using a limit switch probe"""
plugin_author = "Antigravity"
plugin_author_email = "antigravity@example.com"
plugin_url = "https://github.com/yourusername/OctoPrint-AutoZOffset"
plugin_license = "AGPLv3"

def plugin_load():
	import octoprint_autozoffset
	return octoprint_autozoffset.__plugin_implementation__

def plugin_unload():
	pass

if __name__ == "__main__":
	from octoprint.plugin import Plugin
	pass

try:
	import octoprint_setuptools
except:
	print("Could not import OctoPrint's setuptools, are you sure you are running that under "
	      "the same python installation that OctoPrint is installed under?")
	import sys
	sys.exit(-1)

setup_parameters = octoprint_setuptools.create_plugin_setup_parameters(
	identifier=plugin_identifier,
	package=plugin_package,
	name=plugin_name,
	version=plugin_version,
	description=plugin_description,
	author=plugin_author,
	mail=plugin_author_email,
	url=plugin_url,
	license=plugin_license,
	requires=None,
	additional_packages=[],
	ignored_packages=[],
	additional_data=[],
)

if len(setup_parameters["entry_points"]) == 0:
	setup_parameters["entry_points"] = {}

setup_parameters["entry_points"]["octoprint.plugin"] = [
	"autozoffset = octoprint_autozoffset"
]

from setuptools import setup
setup(**setup_parameters)
