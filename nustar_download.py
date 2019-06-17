""" Download NuSTAR data based on source name

Usage:
   nustar_all.py [-h] [-s] [-d DIR] [--no_runpipe] [--keep_orig_cl_ev] [--getgti XMMOBS] [--xmmpath PATH] [--browser] [--lstpath PATH] SOURCE ...

This script queries SIMBAD to get the coordiantes of SOURCE, 
then finds the corresponding ObsIDs fur NuSTAR in the numaster table at HEASARC.
It will then download those OBSIDs and process them with nupipeline.

Options:
    SOURCE       source name (one or multiple), put in quotes if it contains whitespaces. To download all archived data, type 'all'.
    -q, --quiet  don't print OBSIDs on screen
    -d DIR, --outdir DIR  move OBSID folder to this directory [default: /xdata/xcaldata/NUSTAR/]
    -h, --help            show this help message and exit
    --no_runpipe          do not run nustardas task 'nupipeline'
    --keep_orig_cl_ev     keep the standard cleaned event directory
    --getgti XMMOBS       get common GTI with XMM observation ID XMMOBS
    --xmmpath PATH        path to XMM GTI [default: /xdata/xcaldata/NUSTAR/XMM_NUSTAR/]
    --browser             display the results from numster query in the default webbrowser
    --lstpath PATH        path where to store the file with downloaded/existing ObsIDs [default: /xdata/xcaldata/NUSTAR/lists]

"""

from nu_downproc import downproc
from nu_findobs import findobs

from astropy.table import Table, hstack, vstack, unique
import numpy as np
import sys

from docopt import docopt

if __name__ == '__main__':

    args = docopt(__doc__)

    target = findobs(args['SOURCE'])
    
    for t in target:
        # adding number at the beginning for easier identifying of observations 
        t =hstack([Table({'num':np.arange(len(t))}),t])

        ## display in browser is  nicer, but needs a browswe window
        ## if not selected, only printing standard way on screen
        ## should this be maybe t.more? or depending on table size?
        if (args['--browser']):
            t.show_in_browser()
        else:
            print(t)
        
        insel = input("Which data would you like to download?\n(enter either 'num' or 'obsid' (separate multiple observations by comma),\nor type 'all' for all observations):  ")

        ## split at comma, so that every list entry can be an integer
        inselspl = insel.split(',')
        
        if (inselspl[0].isdigit()):
            ##change into integer list
            sellst_int= list(map(int, inselspl))
           
            ## User select by number not by OBSID
            if (sellst_int[0] < 100000):
                selobs = sellst_int
            ## select by OBSIDs
            else:
                selobs = []
                for s in sellst_int:
                    ## need to transfer OBSID column to integers first, as we 
                    ## now have selected OBSID stored as integer as well
                    obss = np.array(t['OBSID'], dtype=int)
                    selobs.append( (np.where(obss == s))[0][0])
                    print(selobs)

        elif (inselspl[0]=='all'):
            ## all means only all archived data, not planned observations
            selobs = np.where(t['STATUS']=='ARCHIVED')
        else:
            print("Invalid selection, aborting!")
            sys.exit(1)
         
        
        ## path to store the file with downloaded/existing ObsIDs
        lpath = args['--lstpath']
        
        if (True):
            for obs in t['OBSID'][selobs]:
                print(f'Working on observation {obs}!...........')
                # downproc(obs, args)
            
            oldtable=1
            try:
                t2 = Table.read('{}/nuobsids_{}.txt'.format(lpath,(t[0]['NAME']).strip()),format='ascii')
            except:
                oldtable = 0
                
            if (oldtable):
                ## it seems writing out the file and reading it back it changes the column variable types
                t[selobs].write('tmp.txt',format='ascii',overwrite='True')
                ttmp = Table.read('tmp.txt', format='ascii')
                ## using 'unique' (Table method) to only keep entries that not already exist!
                nutab = unique((vstack([t2,ttmp])))
                nutab.write('{}/nuobsids_{}.txt'.format(lpath,(t[0]['NAME']).strip()),format='ascii',overwrite='True')
                # print("Found old table")
                # print(nutab)
                
            else:
                t[selobs].write('{}/nuobsids_{}.txt'.format(lpath,(t[0]['NAME']).strip()),format='ascii',overwrite='True')
                # print("no old table found")
                # print(t[selobs])

            
            
        
    
