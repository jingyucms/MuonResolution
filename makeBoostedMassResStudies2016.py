import subprocess

tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]
#~ tracks = ["TunePNew"]

for track in tracks:

	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2016.root","--iMC","2016PtBinned","-o","2016Boosteddefault","--weight","True","-f","doubleCB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2016.root","--iMC","2016PtBinned","-o","2016Boostedcrystal","--weight","True","-f","CB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2016.root","--iMC","2016PtBinned","-o","2016Boostedcruijff","--weight","True","-f","cruijff","-t","%s"%track]
	subprocess.call(command)
	#~ command = ["python","makeMassRes.py","-i","2016MassBinned","-o","default","-f","doubleCB"]
	#~ subprocess.call(command)
	#~ command = ["python","makeMassRes.py","-i","2016MassBinned","-o","cruijff"]
	#~ subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2016.root","--iMC","2016PtBinned","-o","2016BoostedRebin2","--weight","True","--rebin","2","-f","doubleCB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2016.root","--iMC","2016PtBinned","-o","2016BoostedRebin2Cruijff","--weight","True","--rebin","2","-f","cruijff","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2016.root","--iMC","2016PtBinned","-o","2016BoostedRebin2Crystal","--weight","True","--rebin","2","-f","CB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2016.root","--iMC","2016PtBinned","-o","2016BoostedRebin4","--weight","True","--rebin","4","-f","doubleCB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2016.root","--iMC","2016PtBinned","-o","2016BoostedRebin4Cruijff","--weight","True","--rebin","4","-f","cruijff","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2016.root","--iMC","2016PtBinned","-o","2016BoostedRebin4Crystal","--weight","True","--rebin","4","-f","CB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2016.root","--iMC","2016PtBinned","-o","2016BoostedWindowSmall","--weight","True","--xMin","80","--xMax","100","-f","doubleCB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2016.root","--iMC","2016PtBinned","-o","2016BoostedWindowSmallCruijff","--weight","True","--xMin","80","--xMax","100","-f","cruijff","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2016.root","--iMC","2016PtBinned","-o","2016BoostedWindowSmallCrystal","--weight","True","--xMin","800","--xMax","100","-f","CB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2016.root","--iMC","2016PtBinned","-o","2016BoostedWindowLarge","--weight","True","--xMin","60","--xMax","120","-f","doubleCB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2016.root","--iMC","2016PtBinned","-o","2016BoostedWindowLargeCruijff","--weight","True","--xMin","60","--xMax","120","-f","cruijff","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","data_2016.root","--iMC","2016PtBinned","-o","2016BoostedWindowLargeCrystal","--weight","True","--xMin","60","--xMax","120","-f","CB","-t","%s"%track]
	subprocess.call(command)
