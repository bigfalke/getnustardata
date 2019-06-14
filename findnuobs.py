""" Find NuSTAR obs in the archive

Usage:
   findnuobs.py [-h] [-sq] SOURCE ...

This script queries SIMBAD to get the coordiantes of SOURCE, 
then finds the corresponding ObsIDs fur NuSTAR in the numaster table at HEASARC.

Output can be printed to screen and saved as text file.

If called as module, no output is given, but list of astropy-tables is returned with all ObsIDs.

Options:
    SOURCE       source name (one or multiple), put in quotes if it contains whitespaces
    -h, --help   show this help message and exit
    -s, --save   save ObsIDs to text file 
    -q, --quiet  don't print OBSIDs on screen

"""

import sys

import numpy as np

from astropy.time import Time
from astropy.table import Table
from astropy.coordinates import SkyCoord
from astroquery.heasarc import Heasarc
import astropy.units as u
heasarc = Heasarc()
from astroquery.simbad import Simbad

from docopt import docopt

def findmyobs (snames):
      ## query SIMBAD with source names
      ## only exit with error if none of the sources was found
      restab = Simbad.query_objects(getsnames)
      if not (restab):
          print("ERROR (findnuobs): No object found by Simbad query!")
          sys.exit(1)
  
      target = [] 
      ## for each coordinates found query numaster to find NuSTAR ObsIDs 
      for s in restab:
          coord = SkyCoord(s['RA'],s['DEC'], unit=(u.hourangle, u.deg))
          target.append(heasarc.query_region(coord, mission='numaster', radius='0.3 degree'))
          
      return target

if __name__ == '__main__':
  
  args = docopt(__doc__)

  target = findmyobs(args['SOURCE'])
 
  for t in target:
      print("Source {}".format(t[0]['NAME']))
   
      if not (args['--quiet']):
          print(t['OBSID'])
     
      if (args['--save']):
          t.write('nuobsids_{}.txt'.format((t[0]['NAME']).strip()),format='ascii',overwrite='True')

      
