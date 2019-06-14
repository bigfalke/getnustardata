""" Download NuSTAR data based on source name

Usage:
   nustar_all.py [-h] [-s] [-d DIR] [--no_runpipe] [--keep_orig_cl_ev] [--getgti XMMOBS] [--xmmpath PATH] SOURCE ...

This script queries SIMBAD to get the coordiantes of SOURCE, 
then finds the corresponding ObsIDs fur NuSTAR in the numaster table at HEASARC.
It will then download those OBSIDs and process them with nupipeline.

Options:
    SOURCE       source name (one or multiple), put in quotes if it contains whitespaces
    -q, --quiet  don't print OBSIDs on screen
    -d DIR, --outdir DIR  move OBSID folder to this directory [default: /xdata/xcaldata/NUSTAR/]
    -h, --help            show this help message and exit
    --no_runpipe          do not run nustardas task 'nupipeline'
    --keep_orig_cl_ev     keep the standard cleaned event directory
    --getgti XMMOBS       get common GTI with XMM observation ID XMMOBS
    --xmmpath PATH        path to XMM GTI [default: /xdata/xcaldata/NUSTAR/XMM_NUSTAR/]

"""

from nu_downproc import downproc
from nu_findobs import findobs

from docopt import docopt

if __name__ == '__main__':

    args = docopt(__doc__)

    target = findobs(args['SOURCE'])
    
    # print(target[0]['OBSID'][0])
    
    downproc(target[0]['OBSID'][0], args)
