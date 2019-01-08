import subprocess

command = ["python","makePResSplit.py","-i","2016MassBinned","-o","default2016PSplit","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2016MassBinned","-o","crystal2016PSplit","-f","crystal"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2016MassBinned","-o","cruijff2016PSplit"]
subprocess.call(command)
#~ command = ["python","makePRes.py","-i","2016MassBinned","-o","default2016","-f","doubleCB"]
#~ subprocess.call(command)
#~ command = ["python","makePRes.py","-i","2016MassBinned","-o","cruijff2016"]
#~ subprocess.call(command)
command = ["python","makePResSplit.py","-i","2016MassBinned","-o","Rebin22016PSplit","--rebin","2","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2016MassBinned","-o","Rebin82016PSplit","--rebin","8","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2016MassBinned","-o","Rebin22016CruijffPSplit","--rebin","2"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2016MassBinned","-o","Rebin82016CruijffPSplit","--rebin","8"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2016MassBinned","-o","WindowSmall2016PSplit","--xMinFac","-1","--xMaxFac","1","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2016MassBinned","-o","WindowLarge2016PSplit","--xMinFac","-2","--xMaxFac","2","-f","doubleCB"]
subprocess.call(command)
