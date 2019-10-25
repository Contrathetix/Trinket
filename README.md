## BreaksWhenLeastExpected

This is a kind of experimental learning project thingy that I made for automating the update of TTC price data and for converting screenshots for saving them into the Steam screenshots system when not taken through Steam originally. This is mostly just for my own use, maybe someone will find it useful, maybe not, but there is a high chance that something will break, and something may not work. So it might make sense to not use this necessarily.

The config file in

    data\config_example.json

needs to be copied to

    data\config.json

and filled with the appropriate info for the thing to work, mostly the ones in the `variables` section and some under the `screenshot` section, others should be okay probably. The values are:

| key                                | value |
| ---------------------------------- | ----- |
| `variables.path_screenshot_steam`  | Path to where Steam stores userdata and the screenshots, for me it was in the Steam install folder under userdata. |
| `variables.path_screenshot_custom` | Path to where the custom screenshots are saved. |
| `variables.path_game`              | The path to the game folder, where the executable is located. |
| `variables.path_ttc`               | The path to the TTC add-on folder. |
| `variables.ttc_realm`              | Either `eu` for the European megaserver or something else for whatever the other one is called, to get the price data from TTC for the right megaserver. |
| `screenshot.original.name`         | The name of the original screenshot, with the date and time components marked. This will be used by Python's `datetime.datetime.strptime` function to extract the timestamp for the screenshot, that will needed for Steam. |
| `screenshot.converted[0].resize`   | The new size to resize images to, in case it is somehow needed, for Steam.
| `screenshot.converted[0].quality`  | The quality used in saving the image as `jpg` for Steam. It might not have to be in that format, but to save space, it really makes sense. |
