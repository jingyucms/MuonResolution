import subprocess

command = ["python","makeMassRes.py","-i","2016MassBinned","-o","default2016","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2016MassBinned","-o","crystal2016","-f","crystal"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2016MassBinned","-o","cruijff2016"]
subprocess.call(command)
#~ command = ["python","makeMassRes.py","-i","2016MassBinned","-o","default2016","-f","doubleCB"]
#~ subprocess.call(command)
#~ command = ["python","makeMassRes.py","-i","2016MassBinned","-o","cruijff2016"]
#~ subprocess.call(command)
command = ["python","makeMassRes.py","-i","2016MassBinned","-o","Rebin22016","--rebin","2","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2016MassBinned","-o","Rebin82016","--rebin","8","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2016MassBinned","-o","Rebin22016Cruijff","--rebin","2"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2016MassBinned","-o","Rebin82016Cruijff","--rebin","8"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2016MassBinned","-o","WindowSmall2016","--xMinFac","-1","--xMaxFac","1","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2016MassBinned","-o","WindowLarge2016","--xMinFac","-2","--xMaxFac","2","-f","doubleCB"]
subprocess.call(command)
