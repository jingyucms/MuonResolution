import subprocess

command = ["python","makePResSplit.py","-i","2017MassBinned","-o","defaultPSplit","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2017MassBinned","-o","crystalPSplit","-f","crystal"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2017MassBinned","-o","cruijffPSplit"]
subprocess.call(command)
#~ command = ["python","makePRes.py","-i","2016MassBinned","-o","default2016","-f","doubleCB"]
#~ subprocess.call(command)
#~ command = ["python","makePRes.py","-i","2016MassBinned","-o","cruijff2016"]
#~ subprocess.call(command)
command = ["python","makePResSplit.py","-i","2017MassBinned","-o","Rebin2PSplit","--rebin","2","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2017MassBinned","-o","Rebin8PSplit","--rebin","8","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2017MassBinned","-o","Rebin2CruijffPSplit","--rebin","2"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2017MassBinned","-o","Rebin8CruijffPSplit","--rebin","8"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2017MassBinned","-o","WindowSmallPSplit","--xMinFac","-1","--xMaxFac","1","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2017MassBinned","-o","WindowLargePSplit","--xMinFac","-2","--xMaxFac","2","-f","doubleCB"]
subprocess.call(command)
