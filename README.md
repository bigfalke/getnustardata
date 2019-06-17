# getnustardata
Python based scripts to download and process NuSTAR data and filter for common GTIs with XMM-Newton (optional).

First steps is to look up a source name in SIMBAD and identify the cooresponding NuSTAR observations via the coordinates in numastertable.

User can then select which observations to download (either by number or ObsID), or select all to get all archived data (obviously data listed as 'accepted' don't exist yet and will not be downloaded).

In a second step the selected ObsIDs are downloaded from HEASARC and (if HEASOFT/nustardas is installed) 'nupipeline' is run, to obtain freshly calibrated event files.

Common GTIs with XMM-Newton can be created if the XMM-Newton data are availble in the right format and ISIS and the ISIS script 'get_XMM_Nu_GTIs.sl' is avaibele. This still needs updating.

Scripts are still work in progress and have not been thoroughly tested. Use at your own risk.
