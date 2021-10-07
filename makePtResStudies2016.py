import subprocess

command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","default2016Pt","-f","doubleCB"]
subprocess.call(command)
# ~ command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","crystal2016Pt","-f","crystal"]
# ~ subprocess.call(command)
# ~ command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","cruijff2016Pt"]
# ~ subprocess.call(command)
#~ command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","default2016","-f","doubleCB"]
#~ subprocess.call(command)
#~ command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","cruijff2016"]
#~ subprocess.call(command)
# ~ command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","Rebin22016Pt","--rebin","2","-f","doubleCB"]
# ~ subprocess.call(command)
# ~ command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","Rebin82016Pt","--rebin","8","-f","doubleCB"]
# ~ subprocess.call(command)
# ~ command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","Rebin22016CruijffPt","--rebin","2"]
# ~ subprocess.call(command)
# ~ command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","Rebin82016CruijffPt","--rebin","8"]
# ~ subprocess.call(command)
# ~ command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","WindowSmall2016Pt","--xMinFac","-1","--xMaxFac","1","-f","doubleCB"]
# ~ subprocess.call(command)
# ~ command = ["python","makePtResSplit.py","-i","2016MassBinned","-o","WindowLarge2016Pt","--xMinFac","-2","--xMaxFac","2","-f","doubleCB"]
# ~ subprocess.call(command)
