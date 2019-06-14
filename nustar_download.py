""" Download NuSTAR data based on source name

Usage:
   nustar_all.py [-h] [-s] [-d DIR] [--no_runpipe] [--keep_orig_cl_ev] [--getgti XMMOBS] [--xmmpath PATH] [--browser] SOURCE ...

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
    --browser             display the results from numster query in the default webbrowser

"""

from nu_downproc import downproc
from nu_findobs import findobs

from astropy.table import Table, hstack
import numpy as np
import sys

from docopt import docopt

if __name__ == '__main__':

    args = docopt(__doc__)

    target = findobs(args['SOURCE'])
    
    for t in target:
        # adding number at the beginning for easier identifying of observations 
        t =hstack([Table({'num':np.arange(len(t))}),t])

        if (args['--browser']):
            t.show_in_browser()
        else:
            print(t)
        
        insel = input("Which data do you want to download (separate by comma, start at 0)? ")
        
        if (insel=='all'):
            selobs = t['OBSID']
        else:
            ## split at comma and change into integer list
            ## (can this be done more elegantly?!)
            sellst_int= list(map(int, insel.split(',')))
           
            ## User select by number not by OBSID
            if (sellst_int[0] < 100000):
                selobs = t['OBSID'][sellst_int]
            else:
                selobs = []
                for s in sellst_int:
### This piece of code doesn't currenlty work
                    print(s)
                    obss = np.array
                    x = (np.where(t['OBSID'] == s))
                    print(x)
                    # selobs.append(x)
#####
 
        # else:
        #     print("Invalid selection, aborting!")
        #     sys.exit(1)
         
        if (False):
            for obs in selobs:
                print(f'Working on observation {obs}!...........')
                downproc(obs, args)
            
            
        
    
