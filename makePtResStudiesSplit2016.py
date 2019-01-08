import subprocess

command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","default2016PtSplit","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","crystal2016PtSplit","-f","crystal"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","cruijff2016PtSplit"]
subprocess.call(command)
#~ command = ["python","makePtRes.py","-i","2016MassBinned","-o","default2016","-f","doubleCB"]
#~ subprocess.call(command)
#~ command = ["python","makePtRes.py","-i","2016MassBinned","-o","cruijff2016"]
#~ subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","Rebin22016PtSplit","--rebin","2","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","Rebin82016PtSplit","--rebin","8","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","Rebin22016CruijffPtSplit","--rebin","2"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","Rebin82016CruijffPtSplit","--rebin","8"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","WindowSmall2016PtSplit","--xMinFac","-1","--xMaxFac","1","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","WindowLarge2016PtSplit","--xMinFac","-2","--xMaxFac","2","-f","doubleCB"]
subprocess.call(command)
