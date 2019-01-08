import subprocess

command = ["python","makePtResSplit.py","-i","2018MassBinned","-o","default2018PtSplit","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2018MassBinned","-o","crystal2018PtSplit","-f","crystal"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2018MassBinned","-o","cruijff2018PtSplit"]
subprocess.call(command)
#~ command = ["python","makePtRes.py","-i","2018MassBinned","-o","default2018","-f","doubleCB"]
#~ subprocess.call(command)
#~ command = ["python","makePtRes.py","-i","2018MassBinned","-o","cruijff2018"]
#~ subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2018MassBinned","-o","Rebin22018PtSplit","--rebin","2","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2018MassBinned","-o","Rebin82018PtSplit","--rebin","8","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2018MassBinned","-o","Rebin22018CruijffPtSplit","--rebin","2"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2018MassBinned","-o","Rebin82018CruijffPtSplit","--rebin","8"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2018MassBinned","-o","WindowSmall2018PtSplit","--xMinFac","-1","--xMaxFac","1","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePtResSplit.py","-i","2018MassBinned","-o","WindowLarge2018PtSplit","--xMinFac","-2","--xMaxFac","2","-f","doubleCB"]
subprocess.call(command)
