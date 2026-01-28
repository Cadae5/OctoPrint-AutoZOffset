/*
 * View model for OctoPrint-AutoZOffset
 *
 * Author: Antigravity
 * License: AGPLv3
 */
$(function () {
    function AutozoffsetViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];

        self.calibration_in_progress = ko.observable(false);
        self.calibration_status = ko.observable("Ready");

        self.calibrate_z_offset = function () {
            self.calibration_in_progress(true);
            self.calibration_status("Calibrating...");

            OctoPrint.simpleApiCommand("autozoffset", "calibrate")
                .done(function (response) {
                    console.log("Calibration started", response);
                })
                .fail(function () {
                    self.calibration_status("Failed to start");
                    self.calibration_in_progress(false);
                });

            // In a real implementation we would listen for events to clear the status
            // For now, reset after 5s or depend on user interaction
            setTimeout(function () {
                self.calibration_in_progress(false);
                self.calibration_status("Done (Check Terminal)");
            }, 10000);
        };
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: AutozoffsetViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: ["settingsViewModel"],
        // Elements to bind to, e.g. #settings_plugin_autozoffset, #tab_plugin_autozoffset, ...
        elements: ["#sidebar_plugin_autozoffset"]
    });
});
