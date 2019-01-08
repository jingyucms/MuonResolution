import subprocess

command = ["python","makePRes.py","-i","2018MassBinned","-o","default2018P","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePRes.py","-i","2018MassBinned","-o","crystal2018P","-f","crystal"]
subprocess.call(command)
command = ["python","makePRes.py","-i","2018MassBinned","-o","cruijff2018P"]
subprocess.call(command)
#~ command = ["python","makePRes.py","-i","2018MassBinned","-o","default2018","-f","doubleCB"]
#~ subprocess.call(command)
#~ command = ["python","makePRes.py","-i","2018MassBinned","-o","cruijff2018"]
#~ subprocess.call(command)
command = ["python","makePRes.py","-i","2018MassBinned","-o","Rebin22018P","--rebin","2","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePRes.py","-i","2018MassBinned","-o","Rebin82018P","--rebin","8","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePRes.py","-i","2018MassBinned","-o","Rebin22018CruijffP","--rebin","2"]
subprocess.call(command)
command = ["python","makePRes.py","-i","2018MassBinned","-o","Rebin82018CruijffP","--rebin","8"]
subprocess.call(command)
command = ["python","makePRes.py","-i","2018MassBinned","-o","WindowSmall2018P","--xMinFac","-1","--xMaxFac","1","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePRes.py","-i","2018MassBinned","-o","WindowLarge2016P","--xMinFac","-2","--xMaxFac","2","-f","doubleCB"]
subprocess.call(command)
