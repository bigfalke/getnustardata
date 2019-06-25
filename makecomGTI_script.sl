require("isisscripts") ;
require("/home/ffuerst/bin/isisscriptsFF/getcommonGTI_FF.sl") ;
require("/home/ffuerst/bin/isisscriptsFF/writecommonGTI.sl") ;

define gtitomjd (gti)
{
   variable sat = qualifier("sat", "XMM") ;
   
   variable gtimjd = struct{start = gti.start/86400. + MJDref_satellite(sat),
      stop= gti.stop/86400. + MJDref_satellite(sat)} ;
   
   return gtimjd ;
}

define mjdtogti (gti)
{
   variable sat = qualifier("sat", "XMM") ;
   
   variable gtimjd = struct{start = (gti.start - MJDref_satellite(sat))*86400.,
      stop= (gti.stop - MJDref_satellite(sat))*86400.} ;
   
   return gtimjd ;
}

variable nupath = __argv[1] ;
variable nuobsid = __argv[2] ;
variable nugtifil = "nu"+nuobsid+"A01_gti.fits" ;
variable nugti = fits_read_table(nupath+"/"+nugtifil) ;

variable xmpath = __argv[3] ;
variable xmobsid = __argv[4] ;
%% for now assume we're producing the GIT using the ESAS task
%% 'espfilt' (that seems the easiest to do in an automated script...)
variable xmgtifil = "P"+xmobsid+"PNS003-gti.FIT" ;
variable xmgti = fits_read_table(xmpath+"/"+xmgtifil) ;

variable xmgtimjd = gtitomjd(xmgti) ;
variable nugtimjd = gtitomjd(nugti; sat="NuSTAR") ;

variable gtipath ;

%% if a fith argument is given from the command line, use this as path
%% to store the common GTI files. If not, use the current directory.
if (__argc == 6) 
      gtipath =__argv[5] ;
else 
      gtipath = "./" ;

variable comGTI = getCommonGTIsFF(nugtimjd,xmgtimjd) ;

writecommonGTI(comGTI; xmmgti=xmpath+"/"+xmgtifil, nugti=nupath+"/"+nugtifil,
	       gtipath=gtipath, nuobsid=nuobsid, xmobsid=xmobsid) ;

