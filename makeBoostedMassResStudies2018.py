import subprocess

tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]
#tracks = ["TunePNew"]

for track in tracks:

	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2018.root","--iMC","2018PtBinned","-o","2018Boosteddefault","--weight","True","-f","doubleCB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2018.root","--iMC","2018PtBinned","-o","2018Boostedcrystal","--weight","True","-f","CB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2018.root","--iMC","2018PtBinned","-o","2018Boostedcruijff","--weight","True","-f","cruijff","-t","%s"%track]
	subprocess.call(command)
	#~ command = ["python","makeMassRes.py","-i","2017MassBinned","-o","default","-f","doubleCB"]
	#~ subprocess.call(command)
	#~ command = ["python","makeMassRes.py","-i","2017MassBinned","-o","cruijff"]
	#~ subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2018.root","--iMC","2018PtBinned","-o","2018BoostedRebin2","--weight","True","--rebin","2","-f","doubleCB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2018.root","--iMC","2018PtBinned","-o","2018BoostedRebin2Cruijff","--weight","True","--rebin","2","-f","cruijff","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2018.root","--iMC","2018PtBinned","-o","2018BoostedRebin2Crystal","--weight","True","--rebin","2","-f","CB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2018.root","--iMC","2018PtBinned","-o","2018BoostedRebin4","--weight","True","--rebin","4","-f","doubleCB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2018.root","--iMC","2018PtBinned","-o","2018BoostedRebin4Cruijff","--weight","True","--rebin","4","-f","cruijff","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2018.root","--iMC","2018PtBinned","-o","2018BoostedRebin4Crystal","--weight","True","--rebin","4","-f","CB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2018.root","--iMC","2018PtBinned","-o","2018BoostedWindowSmall","--weight","True","--xMin","80","--xMax","100","-f","doubleCB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2018.root","--iMC","2018PtBinned","-o","2018BoostedWindowSmallCruijff","--weight","True","--xMin","80","--xMax","100","-f","cruijff","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2018.root","--iMC","2018PtBinned","-o","2018BoostedWindowSmallCrystal","--weight","True","--xMin","800","--xMax","100","-f","CB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2018.root","--iMC","2018PtBinned","-o","2018BoostedWindowLarge","--weight","True","--xMin","60","--xMax","120","-f","doubleCB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2018.root","--iMC","2018PtBinned","-o","2018BoostedWindowLargeCruijff","--weight","True","--xMin","60","--xMax","120","-f","cruijff","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2018.root","--iMC","2018PtBinned","-o","2018BoostedWindowLargeCrystal","--weight","True","--xMin","60","--xMax","120","-f","CB","-t","%s"%track]
	subprocess.call(command)
