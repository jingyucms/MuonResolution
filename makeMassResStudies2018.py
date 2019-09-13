import subprocess

command = ["python","makeMassRes.py","-i","2018MassBinned","-o","default2018","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2018MassBinned","-o","crystal2018","-f","crystal"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2018MassBinned","-o","cruijff2018"]
subprocess.call(command)
#~ command = ["python","makeMassRes.py","-i","2018MassBinned","-o","default2018","-f","doubleCB"]
#~ subprocess.call(command)
#~ command = ["python","makeMassRes.py","-i","2018MassBinned","-o","cruijff2018"]
#~ subprocess.call(command)
command = ["python","makeMassRes.py","-i","2018MassBinned","-o","Rebin22018","--rebin","2","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2018MassBinned","-o","Rebin82018","--rebin","8","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2018MassBinned","-o","Rebin22018Cruijff","--rebin","2"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2018MassBinned","-o","Rebin82018Cruijff","--rebin","8"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2018MassBinned","-o","WindowSmall2018","--xMinFac","-1","--xMaxFac","1","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2018MassBinned","-o","WindowLarge2018","--xMinFac","-2","--xMaxFac","2","-f","doubleCB"]
subprocess.call(command)
