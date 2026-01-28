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

        self.calibrate_z_offset = function () {
            OctoPrint.simpleApiCommand("autozoffset", "calibrate")
                .done(function (response) {
                    // console.log("Calibration started");
                });
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
        elements: ["#settings_plugin_autozoffset"]
    });
});
