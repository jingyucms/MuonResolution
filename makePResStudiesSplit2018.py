import subprocess

command = ["python","makePResSplit.py","-i","2018MassBinned","-o","default2018PSplit","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2018MassBinned","-o","crystal2018PSplit","-f","crystal"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2018MassBinned","-o","cruijff2018PSplit"]
subprocess.call(command)
#~ command = ["python","makePRes.py","-i","2018MassBinned","-o","default2018","-f","doubleCB"]
#~ subprocess.call(command)
#~ command = ["python","makePRes.py","-i","2018MassBinned","-o","cruijff2018"]
#~ subprocess.call(command)
command = ["python","makePResSplit.py","-i","2018MassBinned","-o","Rebin22018PSplit","--rebin","2","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2018MassBinned","-o","Rebin82018PSplit","--rebin","8","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2018MassBinned","-o","Rebin22018CruijffPSplit","--rebin","2"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2018MassBinned","-o","Rebin82018CruijffPSplit","--rebin","8"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2018MassBinned","-o","WindowSmall2018PSplit","--xMinFac","-1","--xMaxFac","1","-f","doubleCB"]
subprocess.call(command)
command = ["python","makePResSplit.py","-i","2018MassBinned","-o","WindowLarge2018PSplit","--xMinFac","-2","--xMaxFac","2","-f","doubleCB"]
subprocess.call(command)
