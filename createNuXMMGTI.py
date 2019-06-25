""" Create a common GTI between XMM-Newton and NuSTAR

Usage:
    createNuXMMGTI [-h] [--xmmdir PATH] [--nudir PATH] [--nusrc FILE] 
    [--nubkg FILE] [--gtipath PATH] [--pnx COORD] [--pny COORD] 
    [--pnbkgx COORD] [--pnbkgy COORD] [--nonustar] [--noxmm] [--pninrad RAD] [--xmmname FOLDER]
    XMMOBS NUOBS

This script will create a common GTI between a given NuSTAR and XMM-Newton
Observation, by calling the 'getCommonGTIsFF' ISIS routine. If no XMM GTI
exists, it calls 'espfilt' to create a background flare corrected GTI.

Options:
    XMMOBS          ObsID of the XMM-Newton observation
    NUOBS           ObsID of the NuSTAR observation
    --xmmdir PATH   path to the XMM-Newton event and GTI file [default: /home/ffuerst/lhome/analysis/3c273/]
    --nudir PATH    path to the NuSTAR GTI file [default: /home/ffuerst/lhome/data/3c273/nustar/]
    --nusrc FILE    NuSTAR source region [default: srcA_100as.reg]
    --nubkg FILE    NuSTAR background region [default: bkgA.reg]
    --gtipath PATH  path to store GTI files [default: ./]
    --pnx COORD     x-coordinates of pn source region [default: 26500]
    --pny COORD     y-coordinates of pn source region [default: 28000]
    --pnbkgx COORD     x-coordinates of pn backgroundregion [default: 29650]
    --pnbkgy COORD     y-coordinates of pn background region [default: 25500]
    --pninrad RAD   inner radius for XMM extraction region [default: 0]
    --nonustar      don't run the NuSTAR pipeline
    --noxmm         don't run the XMM pipeline
    --xmmname FOLDER  folder name where to store extracted XMM data [default: src_720px_comgti]

"""

import numpy as np
import sys
import os
import subprocess 


from contextlib import contextmanager

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

from docopt import docopt

def call(*args):
    print("#", ' '.join(args))
    subprocess.check_call(args)
            

if __name__ == '__main__':
    
    args = docopt(__doc__)
        
    ## this needs to be improved: I don't like my current data structure!

    xmobsid = args['XMMOBS']
    nuobsid = args['NUOBS']
    gtipath = args['--gtipath']
    nusrc = args['--nusrc']
    nubkg = args['--nubkg']
    pnx = args['--pnx']
    pny = args['--pny'] 
    pnbkgx = args['--pnbkgx']
    pnbkgy = args['--pnbkgy'] 
    gtipath = args['--gtipath']
    pninrad = args['--pninrad']
    xmmexname = args['--xmmname']
    
    print(args) 
    
    print(gtipath) 
    
    xmdir = args['--xmmdir'] + xmobsid + '_tools/pn/ccf/'
    nudir = args['--nudir'] + nuobsid + '/event_cl_v18/' 
        
    print(xmdir)
    print(nudir) 
    
    print("Checking that we have a XMM GTI file")
    if not os.path.isfile(xmdir+"P"+xmobsid+"PNS003-gti.FIT"):
        with cd(xmdir):
            try:
                call('espfilt', 'eventset=P'+xmobsid+'PNS003PIEVLI0000.FIT')
            except subprocss.CalledProcessError as e:
                print("espfilt didn't run properly ({0})!".format(e))
                sys.exit(1)
    else:
        print(f'GTI file for XMM observation {xmobsid} already exists, nothing to do!\n')
            
    
    print("Calling ISIS to create commong GTI")
    try:
        call('isis-script','makecomGTI_script.sl',f'{nudir}',f'{nuobsid}',f'{xmdir}',
        f'{xmobsid}',gtipath)
    except subprocess.CalledProcessError as e:
        print("Couldn't run ISIS to create commong GTIs ({0})".format(e))

    if not args['--nonustar']:
        print("Calling NuSTAR pipeline to extract data with common GTI")
        try:
            call('nuproducts',f'indir={nudir}',f'steminputs=nu{nuobsid}',
            'instrument=FPMA',f'srcregionfile={nudir}/{nusrc}',
            f'bkgregionfile={nudir}/{nubkg}',
            f'stemout=fpmA_{nuobsid}_comgti',
            f'outdir={nudir}/extr_gti',
            f'usrgtifile={gtipath}/comgti_nu_{nuobsid}_{xmobsid}.fits')
            
            # call('fthedit',f'fpmA_{nuobsid}_comgti_sr.pha[1]','ANCRFILE',
            # 'add',f'fpmA_{nuobsid}_comgti_sr.arf')
            
        except subprocess.CalledProcessError as e:
            print("NuSTAR pipeline didn't run ({0})".format(e))

    if not args['--noxmm']:
        print("Calling XMM pipeline to extract with common GTI");
        try: 
            call('xmmextractFF_old',f'--prepdir={xmobsid}_tools','--pn',f'--name={xmmexname}',
            f'--x={pnx}', f'--y={pny}','--rad=720','--defaultpattern',
            f'--bkgx={pnbkgx}', f'--bkgy={pnbkgy}', '--bkgoutrad=720',
            f'--inrad={pninrad}', '--noflarescreen',
            f'--gtifile={gtipath}/comgti_xmm_{nuobsid}_{xmobsid}.fits')
        except subprocess.CalledProcessError as e:
            print("XMM-Newton pipeline didn't run ({0})".format(e))
    

            
            
