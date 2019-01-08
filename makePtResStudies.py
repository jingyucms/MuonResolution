import subprocess

command = ["python","makePtRes.py","-i","2017MassBinned","-o","defaultPt","--weight","True","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtRes.py","-i","2017MassBinned","-o","crystalPt","--weight","True","-f","crystal"]
subprocess.call(command)
command = ["python","makePtRes.py","-i","2017MassBinned","-o","cruijffPt","--weight","True"]
subprocess.call(command)
#~ command = ["python","makePtRes.py","-i","2016MassBinned","-o","default2016","-f","doubleCB"]
#~ subprocess.call(command)
#~ command = ["python","makePtRes.py","-i","2016MassBinned","-o","cruijff2016"]
#~ subprocess.call(command)
command = ["python","makePtRes.py","-i","2017MassBinned","-o","Rebin2Pt","--weight","True","--rebin","2","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtRes.py","-i","2017MassBinned","-o","Rebin8Pt","--weight","True","--rebin","8","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtRes.py","-i","2017MassBinned","-o","Rebin2CruijffPt","--weight","True","--rebin","2"]
subprocess.call(command)
command = ["python","makePtRes.py","-i","2017MassBinned","-o","Rebin8CruijffPt","--weight","True","--rebin","8"]
subprocess.call(command)
command = ["python","makePtRes.py","-i","2017MassBinned","-o","WindowSmallPt","--weight","True","--xMinFac","-1","--xMaxFac","1","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtRes.py","-i","2017MassBinned","-o","WindowLargePt","--weight","True","--xMinFac","-2","--xMaxFac","2","-f","doubleCB"]
subprocess.call(command)
