import subprocess

command = ["python","makeMassRes.py","-i","2017MassBinned","-o","default","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","crystal","-f","crystal"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","gaussExp","-f","gaussExp"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","gauss","-f","gaus"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","cruijff"]
subprocess.call(command)
#~ command = ["python","makeMassRes.py","-i","2017MassBinned","-o","default","-f","doubleCB"]
#~ subprocess.call(command)
#~ command = ["python","makeMassRes.py","-i","2017MassBinned","-o","cruijff"]
#~ subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","Rebin2","--rebin","2","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","Rebin2Cruijff","--rebin","2"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","Rebin2Crystal","--rebin","2","-f","crystal"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","Rebin8","--rebin","8","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","Rebin8Cruijff","--rebin","8"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","Rebin8Crystal","--rebin","8","-f","crystal"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","WindowSmall","--xMinFac","-1","--xMaxFac","1","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","WindowSmallCruijff","--xMinFac","-1","--xMaxFac","1"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","WindowSmallCrystal","--xMinFac","-1","--xMaxFac","1","-f","crystal"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","WindowLarge","--xMinFac","-3","--xMaxFac","3","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","WindowLargeCruijff","--xMinFac","-3","--xMaxFac","3"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","WindowLargeCrystal","--xMinFac","-3","--xMaxFac","3","-f","crystal"]
subprocess.call(command)
