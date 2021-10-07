import subprocess

#tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]
tracks = ["TunePNew"]

for track in tracks:

	command = ["python","makeMassRes_atZ3.py","--iDATA","dileptonAna_resolution_data2017UL.root","--iMC","2017PtBinned","-o","Boosteddefault","--weight","True","-f","doubleCB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","dileptonAna_resolution_data2017UL.root","--iMC","2017PtBinned","-o","Boostedcrystal","--weight","True","-f","CB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","dileptonAna_resolution_data2017UL.root","--iMC","2017PtBinned","-o","Boostedcruijff","--weight","True","-f","cruijff","-t","%s"%track]
	subprocess.call(command)
	#~ command = ["python","makeMassRes.py","-i","2017MassBinned","-o","default","-f","doubleCB"]
	#~ subprocess.call(command)
	#~ command = ["python","makeMassRes.py","-i","2017MassBinned","-o","cruijff"]
	#~ subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","dileptonAna_resolution_data2017UL.root","--iMC","2017PtBinned","-o","BoostedRebin2","--weight","True","--rebin","2","-f","doubleCB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","dileptonAna_resolution_data2017UL.root","--iMC","2017PtBinned","-o","BoostedRebin2Cruijff","--weight","True","--rebin","2","-f","cruijff","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","dileptonAna_resolution_data2017UL.root","--iMC","2017PtBinned","-o","BoostedRebin2Crystal","--weight","True","--rebin","2","-f","CB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","dileptonAna_resolution_data2017UL.root","--iMC","2017PtBinned","-o","BoostedRebin4","--weight","True","--rebin","4","-f","doubleCB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","dileptonAna_resolution_data2017UL.root","--iMC","2017PtBinned","-o","BoostedRebin4Cruijff","--weight","True","--rebin","4","-f","cruijff","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","dileptonAna_resolution_data2017UL.root","--iMC","2017PtBinned","-o","BoostedRebin4Crystal","--weight","True","--rebin","4","-f","CB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","dileptonAna_resolution_data2017UL.root","--iMC","2017PtBinned","-o","BoostedWindowSmall","--weight","True","--xMin","80","--xMax","100","-f","doubleCB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","dileptonAna_resolution_data2017UL.root","--iMC","2017PtBinned","-o","BoostedWindowSmallCruijff","--weight","True","--xMin","80","--xMax","100","-f","cruijff","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","dileptonAna_resolution_data2017UL.root","--iMC","2017PtBinned","-o","BoostedWindowSmallCrystal","--weight","True","--xMin","800","--xMax","100","-f","CB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","dileptonAna_resolution_data2017UL.root","--iMC","2017PtBinned","-o","BoostedWindowLarge","--weight","True","--xMin","60","--xMax","120","-f","doubleCB","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","dileptonAna_resolution_data2017UL.root","--iMC","2017PtBinned","-o","BoostedWindowLargeCruijff","--weight","True","--xMin","60","--xMax","120","-f","cruijff","-t","%s"%track]
	subprocess.call(command)
	command = ["python","makeMassRes_atZ3.py","--iDATA","dileptonAna_resolution_data2017UL.root","--iMC","2017PtBinned","-o","BoostedWindowLargeCrystal","--weight","True","--xMin","60","--xMax","120","-f","CB","-t","%s"%track]
	subprocess.call(command)
