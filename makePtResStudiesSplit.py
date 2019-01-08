import subprocess

command = ["python","makePtResSplit.py","-i","2017MassBinned","-o","defaultPtSplit","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2017MassBinned","-o","crystalPtSplit","-f","crystal"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2017MassBinned","-o","cruijffPtSplit"]
subprocess.call(command)
#~ command = ["python","makePtRes.py","-i","2016MassBinned","-o","default2016","-f","doubleCB"]
#~ subprocess.call(command)
#~ command = ["python","makePtRes.py","-i","2016MassBinned","-o","cruijff2016"]
#~ subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2017MassBinned","-o","Rebin2PtSplit","--rebin","2","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2017MassBinned","-o","Rebin8PtSplit","--rebin","8","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2017MassBinned","-o","Rebin2CruijffPtSplit","--rebin","2"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2017MassBinned","-o","Rebin8CruijffPtSplit","--rebin","8"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2017MassBinned","-o","WindowSmallPtSplit","--xMinFac","-1","--xMaxFac","1","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2017MassBinned","-o","WindowLargePtSplit","--xMinFac","-2","--xMaxFac","2","-f","doubleCB"]
subprocess.call(command)
