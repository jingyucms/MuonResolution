import subprocess

command = ["python","makePRes.py","-i","2016MassBinned","-o","default2016P","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePRes.py","-i","2016MassBinned","-o","crystal2016P","-f","crystal"]
subprocess.call(command)
command = ["python","makePRes.py","-i","2016MassBinned","-o","cruijff2016P"]
subprocess.call(command)
#~ command = ["python","makePRes.py","-i","2016MassBinned","-o","default2016","-f","doubleCB"]
#~ subprocess.call(command)
#~ command = ["python","makePRes.py","-i","2016MassBinned","-o","cruijff2016"]
#~ subprocess.call(command)
command = ["python","makePRes.py","-i","2016MassBinned","-o","Rebin22016P","--rebin","2","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePRes.py","-i","2016MassBinned","-o","Rebin82016P","--rebin","8","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePRes.py","-i","2016MassBinned","-o","Rebin22016CruijffP","--rebin","2"]
subprocess.call(command)
command = ["python","makePRes.py","-i","2016MassBinned","-o","Rebin82016CruijffP","--rebin","8"]
subprocess.call(command)
command = ["python","makePRes.py","-i","2016MassBinned","-o","WindowSmall2016P","--xMinFac","-1","--xMaxFac","1","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePRes.py","-i","2016MassBinned","-o","WindowLarge2016P","--xMinFac","-2","--xMaxFac","2","-f","doubleCB"]
subprocess.call(command)
