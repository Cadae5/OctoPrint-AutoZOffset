# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import flask
import re

class AutoZOffsetPlugin(octoprint.plugin.SettingsPlugin,
                        octoprint.plugin.AssetPlugin,
                        octoprint.plugin.TemplatePlugin,
                        octoprint.plugin.SimpleApiPlugin):

	def __init__(self):
		self.state = "IDLE"
		self.current_z_offset = 0.0

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			switch_x=0.0,
			switch_y=0.0,
			safe_z=10.0,
			reference_height=0.0
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		return dict(
			js=["js/autozoffset.js"]
		)

	##~~ TemplatePlugin mixin

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False),
			dict(type="sidebar", icon="arrows-v", list=True)
		]

	##~~ SimpleApiPlugin mixin

	def get_api_commands(self):
		return dict(
			calibrate=[]
		)

	def on_api_command(self, command, data):
		if command == "calibrate":
			self.run_calibration()
			return flask.jsonify(result="started")

	##~~ Logic

	def run_calibration(self):
		self._logger.info("Starting Auto Z-Offset Calibration")
		self.state = "FETCHING_OFFSET"
		self._printer.commands("M851")

	def hook_gcode_received(self, comm, line, *args, **kwargs):
		if self.state == "IDLE":
			return line

		if self.state == "FETCHING_OFFSET":
			self._logger.info("FETCHING_OFFSET checking line: '{}'".format(line.strip()))
			# Parse "echo:Z Offset : -1.23" or "Probe Z Offset: -1.23" (Marlin variations)
			if "Z Offset" in line:
				# Regex to find decimal number after "Z Offset" and optional colon/spaces
				match = re.search(r"Z Offset.*:?\s+([-+]?\d*\.?\d+)", line, re.IGNORECASE)
				if match:
					self.current_z_offset = float(match.group(1))
					self._logger.info("Current Z Offset: {}".format(self.current_z_offset))
					
					# Proceed to move
					self.state = "MOVING"
					
					# Move to Safe Z first
					safe_z = self._settings.get_float(["safe_z"])
					self._logger.info("Moving to Safe Z: {}".format(safe_z))
					self._printer.commands(["G0 Z{:.2f}".format(safe_z)])

					# Then Probe at switch location
					# User requested: G30 X... Y...
					x = self._settings.get_float(["switch_x"])
					y = self._settings.get_float(["switch_y"])
					self._logger.info("Probing at X: {} Y: {}".format(x, y))
					
					self.state = "PROBING"
					# Sending G30 with coordinates
					self._printer.commands(["G30 X{:.2f} Y{:.2f}".format(x, y)])
					return line
				else:
					self._logger.info("Matched 'Z Offset' but failed regex")

		if self.state == "PROBING":
			# Parse G30 response: "Bed X: 10.00 Y: 10.00 Z: 2.50"
			if "Bed X:" in line and "Z:" in line:
				match = re.search(r"Z:\s*(-?\d+(\.\d+)?)", line)
				if match:
					measured_z = float(match.group(1))
					self._logger.info("Measured Z: {}".format(measured_z))
					self.process_probe_result(measured_z)
					self.state = "IDLE"
				return line

		return line

	def process_probe_result(self, measured_z):
		ref_height = self._settings.get_float(["reference_height"])
		# Logic: New_Offset = Old_Offset - (Measured_Z - Ref_Height)
		# Checks out: If Measured > Ref, we are effectively 'higher' than we want to be (reads 5 instead of 0).
		# We need to lower the nozzle (more negative offset).
		# So subtract positive diff.
		diff = measured_z - ref_height
		new_offset = self.current_z_offset - diff
		
		self._logger.info("Calculated New Offset: {}".format(new_offset))
		self._printer.commands(["M851 Z{:.2f}".format(new_offset), "M500"])

__plugin_name__ = 'AutoZOffset Plugin'
__plugin_pythoncompat__ = '>=3.7,<4'
__plugin_implementation__ = AutoZOffsetPlugin()
