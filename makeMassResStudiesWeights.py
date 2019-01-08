import subprocess

command = ["python","makeMassRes.py","-i","2017MassBinned","-o","defaultWeights","--weight","True","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","crystalWeights","--weight","True","-f","crystal"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","gaussExpWeights","--weight","True","-f","gaussExp"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","gaussWeights","--weight","True","-f","gaus"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","cruijffWeights","--weight","True"]
subprocess.call(command)
#~ command = ["python","makeMassRes.py","-i","2017MassBinned","-o","default","-f","doubleCB"]
#~ subprocess.call(command)
#~ command = ["python","makeMassRes.py","-i","2017MassBinned","-o","cruijff"]
#~ subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","Rebin2Weights","--weight","True","--rebin","2","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","Rebin2CruijffWeights","--weight","True","--rebin","2"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","Rebin2CrystalWeights","--weight","True","--rebin","2","-f","crystal"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","Rebin8Weights","--weight","True","--rebin","8","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","Rebin8CruijffWeights","--weight","True","--rebin","8"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","Rebin8CrystalWeights","--weight","True","--rebin","8","-f","crystal"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","WindowSmallWeights","--weight","True","--xMinFac","-1","--xMaxFac","1","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","WindowSmallCruijffWeights","--weight","True","--xMinFac","-1","--xMaxFac","1"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","WindowSmallCrystalWeights","--weight","True","--xMinFac","-1","--xMaxFac","1","-f","crystal"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","WindowLargeWeights","--weight","True","--xMinFac","-3","--xMaxFac","3","-f","doubleCB"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","WindowLargeCruijffWeights","--weight","True","--xMinFac","-3","--xMaxFac","3"]
subprocess.call(command)
command = ["python","makeMassRes.py","-i","2017MassBinned","-o","WindowLargeCrystalWeights","--weight","True","--xMinFac","-3","--xMaxFac","3","-f","crystal"]
subprocess.call(command)
