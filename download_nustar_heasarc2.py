"""Downloand NuSTAR data and pre-process

Usage: 
    download_nustar_heasarc.py [-h] [-d DIR] [--no_runpipe] [--keep_orig_cl_ev] [--getgti XMMOBS] [--xmmpath PATH]
    OBSID ...

This script will download NuSTAR data for all given ObsIDs from the HEASARC 
and run the 'nupipeline' to produce new cleaned event files
    
Options:
    OBSID   data to be downloaded an processed
    -d DIR, --outdir DIR  move OBSID folder to this directory [default: /xdata/xcaldata/NUSTAR/]
    -h, --help            show this help message and exit
    --no_runpipe          do not run nustardas task 'nupipeline'
    --keep_orig_cl_ev     keep the standard cleaned event directory
    --getgti XMMOBS       get common GTI with XMM observation ID XMMOBS
    --xmmpath PATH        path to XMM GTI [default: /xdata/xcaldata/NUSTAR/XMM_NUSTAR/]

"""
        
# updated for xsa v8.3 by rmj and ekara, 25 March 2015 
# http://nxsa.esac.esa.int/nxsa-web/#aio_sampleurls

# import urllib.request, urllib.error, urllib.parse
# import re
import os
# import glob
import subprocess
# import argparse
import sys
import shutil

from docopt import docopt

def call(*args):
    print("#", ' '.join(args))
    subprocess.check_call(args)

def downloadODF(obsid, args):

    print("\n")
    print(f"Downloading and processing ObsID {obsid}.............\n")
   
    outdir = args['--outdir']
    
    nuurl = 'https://heasarc.gsfc.nasa.gov/FTP/nustar/data/obs/{0}/{1}//{2}/'.format(obsid[1:3],obsid[0], obsid)
    # print nuurl
    
    print(("wget --verbose=1 -nH --no-check-certificate --cut-dirs=6 -r -l0 -c -N -np -R \'index*\' -erobots=off --retr-symlinks {0}".format(nuurl)))
    try:
        print(('wget running ({0})'.format('e')))
        # call("wget", "-q", "-nH", "--no-check-certificate", "--cut-dirs=6", "-r", "-l0", "-c", "-N", "-np", "-R", "\'index*\'", "-erobots=off", "--retr-symlinks", "{0}".format(nuurl))
    except subprocess.CalledProcessError as e:
        print(('wget failed ({0})'.format(e)))
        sys.exit(1)
   
    # move it to taget directory
    # (default the XCAL archive data structure)
    xcalpath = outdir  # '/xdata/xcaldata/NUSTAR/'
    fullpath = xcalpath+'/'+obsid 
    
    ## no need to create a directory, as we move complete directories
    ## code remains here in case this changes in the future
    # try:  
    #     os.mkdir(fullpath)
    # except OSError:  
    #     print ("Creation of the directory %s failed (file exists?)" % fullpath)
                    
    try:
        print ('move running to {0}/{1}'.format(xcalpath,obsid))
        # call('mv', '{0}'.format(obsid), '{0}/{1}'.format(xcalpath,obsid))
    except subprocess.CalledProcessError:
        print(('Could not move files to {0}/{1}'.format(xcalpath,obsid)))
        sys.exit(1)
        
    if not (args['--no_runpipe']):
        print("Running the nustardas pipeline!")
        
        ## these parameters are all the default parameters of nupipline
        ## as long as we don't change them, no need to set them
        ## (or give them to the call of nupipeline)
        # ENTRYSTAGE=1
        # EXITSTAGE=2
        # GTISCREEN='yes'
        # EVTSCREEN='yes'
        # GRADEEXPR='DEFAULT'
        # STATUSEXPR='DEFAULT'
        # CREATEATTGTI='yes'
        # CREATEINSTRGTI='yes'
        
        STEMINPUTS='nu{}'.format(obsid)
        ## default here is no, but we want to be able to use mode06, 
        ## so split by CHU combination
        RUNSPLITSC='yes'
        
        # call("nupipeline",'clobber=yes',
        # 'indir={0}'.format(fullpath),
        # f'steminput={STEMINPUTS}',
        # 'outdir={0}/{1}'.format(fullpath,'event_cl_py'),
        # f'runsplitsc={RUNSPLITSC}')
        # f'entrystage={ENTRYSTAGE}',
        # f'exitstage={EXITSTAGE}')
        # f'gtiscreen={GTISCREEN}',
        # f'evtscreen={EVTSCREEN}',
        # f'gradeexpr={GRADEEXPR}',
        # f'statusexp={STATUSEXPR}',
        # f'createattgti={CREATEATTGTI}',
        # f'createinstrgti={CREATEINSTRGTI}',

        ## this is set to 'POINT' by default, which is probably more correct
        ## (don't know why my script set it to OBJECT)
        # 'pntra=OBJECT', 'pntdec=OBJECT',

    if not (args['--keep_orig_cl_ev']):
        try:
            print ('removing {0}/{1}'.format(fullpath,'event_cl'))
            # shutil.rmtree('{0}/{1}'.format(fullpath,'event_cl'))
        except OSError as e:
            print(('Could not delete folder {0} ({1})'.format(e.filename, e.strerror)))
            sys.exit(1)
        
    if (args['--getgti']):
        print(args['--getgti'])
        
        try:
            call('isis','get_XMM_Nu_GTIs.sl',fullpath+'/event_cl_py/',obsid,'3','4')
        except subprocess.CalledProcessError as e:
            print('Call to ISIS to get common GTIs failed {}'.format(e)) 
       
if __name__ == '__main__':

    args = docopt(__doc__) 
    
    # do downloading
    for obs in args['OBSID']:
        downloadODF(obs, args  )

