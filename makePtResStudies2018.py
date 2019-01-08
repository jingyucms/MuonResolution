import subprocess

command = ["python","makePtRes.py","-i","2018MassBinned","-o","default2018Pt","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtRes.py","-i","2018MassBinned","-o","crystal2018Pt","-f","crystal"]
subprocess.call(command)
command = ["python","makePtRes.py","-i","2018MassBinned","-o","cruijff2018Pt"]
subprocess.call(command)
#~ command = ["python","makePtRes.py","-i","2018MassBinned","-o","default2018","-f","doubleCB"]
#~ subprocess.call(command)
#~ command = ["python","makePtRes.py","-i","2018MassBinned","-o","cruijff2018"]
#~ subprocess.call(command)
command = ["python","makePtRes.py","-i","2018MassBinned","-o","Rebin22018Pt","--rebin","2","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtRes.py","-i","2018MassBinned","-o","Rebin82018Pt","--rebin","8","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtRes.py","-i","2018MassBinned","-o","Rebin22018CruijffPt","--rebin","2"]
subprocess.call(command)
command = ["python","makePtRes.py","-i","2018MassBinned","-o","Rebin82018CruijffPt","--rebin","8"]
subprocess.call(command)
command = ["python","makePtRes.py","-i","2018MassBinned","-o","WindowSmall2018Pt","--xMinFac","-1","--xMaxFac","1","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtRes.py","-i","2018MassBinned","-o","WindowLarge2016Pt","--xMinFac","-2","--xMaxFac","2","-f","doubleCB"]
subprocess.call(command)
