from ROOT import *
import pickle
import math
from setTDRStyle import setTDRStyle

ptbins = [52, 72, 100, 152, 200, 300, 452, 800.]

def efficiencyRatio(eff1,eff2):
	newEff = TGraphAsymmErrors(eff1.GetN())
	for i in range(0,eff1.GetN()):
		pointX1 = Double(0.)
		pointX2 = Double(0.)
		pointY1 = Double(0.)
		pointY2 = Double(0.)
		
		isSuccesful1 = eff1.GetPoint(i,pointX1,pointY1)
		isSuccesful2 = eff2.GetPoint(i,pointX2,pointY2)
		errY1Up = eff1.GetErrorYhigh(i)
		errY1Low = eff1.GetErrorYlow(i)
		errY2Up = eff2.GetErrorYhigh(i)
		errY2Low = eff2.GetErrorYlow(i)
		
		errX = eff1.GetErrorX(i)
		
		
		if pointY2!=0:
			yValue = pointY1/pointY2
			xValue = pointX1
			xError = errX
			#~ yErrorUp = math.sqrt(((1/pointY2)*errY1Up)**2+((pointY1/pointY2**2)*errY2Up)**2)
			yErrorUp = math.sqrt(((1/pointY2)*errY1Up)**2+((pointY1/pointY2**2)*errY2Up)**2)
			yErrorDown = math.sqrt(((1/pointY2)*errY1Low)**2+((pointY1/pointY2**2)*errY2Low)**2)				
		else:
			yValue = 0
			xValue = pointX1
			xError = errX
			yErrorUp =0
			yErrorDown = 0
			
		#~ print i
		newEff.SetPoint(i,xValue,yValue)
		newEff.SetPointError(i,xError,xError,yErrorDown,yErrorUp)
		
	return newEff
	
def getRatio(result,result2,label):
	
	
	masses = result["mass"]
	massErr = result["massErr"]
	sigma = result["sigma"]
	sigmaErr = result["sigmaErr"]	
	masses2 = result2["mass"]
	massErr2 = result2["massErr"]
	sigma2 = result2["sigma"]
	sigmaErr2 = result2["sigmaErr"]	
	
	
	ratio  = TGraphErrors(len(masses))
	ratio.SetName(label)
	for i,mass in enumerate(masses):     
		ratio   .SetPoint(i,mass,sigma[i]/sigma2[i])
		ratio   .SetPointError(i,massErr[i],(sigma[i]/sigma2[i])*math.sqrt((sigmaErr[i]/sigma[i])**2+(sigmaErr2[i]/sigma2[i])**2))
	
	return ratio
	

def getGraph(result,label):
	
	masses = result["mass"]
	massErr = result["massErr"]
	sigma = result["sigma"]
	sigmaErr = result["sigmaErr"]
	
	res  = TGraphAsymmErrors(len(masses))
	res.SetName(label)
	for i,mass in enumerate(masses):        
		res.SetPoint(i,mass,sigma[i])
		res.SetPointError(i,massErr[i],massErr[i],sigmaErr[i],sigmaErr[i])
	
	return res



def compareMassRes(trackType):
	
	fileDefaultBB = open("default2018/MassResolutionVsMass_%s_BB.pkl"%trackType)
	fileORBB = open("WindowSmall2018/MassResolutionVsMass_%s_BB.pkl"%trackType)
	fileNoBB = open("WindowLarge2018/MassResolutionVsMass_%s_BB.pkl"%trackType)
	fileDefaultBE = open("default2018/MassResolutionVsMass_%s_BE.pkl"%trackType)
	fileORBE = open("WindowSmall2018/MassResolutionVsMass_%s_BE.pkl"%trackType)
	fileNoBE = open("WindowLarge2018/MassResolutionVsMass_%s_BE.pkl"%trackType)

	resultsDefaultBB = pickle.load(fileDefaultBB)
	resultsORBB = pickle.load(fileORBB)
	resultsNoBB = pickle.load(fileNoBB)
	resultsDefaultBE = pickle.load(fileDefaultBE)
	resultsORBE = pickle.load(fileORBE)
	resultsNoBE = pickle.load(fileNoBE)


	graphDefaultBB = getGraph(resultsDefaultBB,"DefaultBB")
	graphORBB = getGraph(resultsORBB,"ORBB")
	graphNoBB = getGraph(resultsNoBB,"NoBB")
	graphDefaultBE = getGraph(resultsDefaultBE,"DefaultBE")
	graphORBE = getGraph(resultsORBE,"ORBE")
	graphNoBE = getGraph(resultsNoBE,"NoBE")
		
	
	ratioORBB = 	getRatio(resultsORBB,resultsDefaultBB,"ratioBBOR")
	ratioNoBB = 	getRatio(resultsNoBB,resultsDefaultBB,"ratioBBNo")
	ratioORBE = 	getRatio(resultsORBE,resultsDefaultBE,"ratioBEOR")
	ratioNoBE = 	getRatio(resultsNoBE,resultsDefaultBE,"ratioBENo")



	canv = TCanvas("c1","c1",800,1200)

	plotPad = TPad("plotPad","plotPad",0,0.3,1,1)
	ratioPad = TPad("ratioPad","ratioPad",0,0.,1,0.3)
	style = setTDRStyle()
	gStyle.SetOptStat(0)
	plotPad.UseCurrentStyle()
	ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	ratioPad.Draw()	
	plotPad.cd()
	plotPad.cd()
	plotPad.SetGrid()
	gStyle.SetTitleXOffset(1.45)

	xMax = 0.08
	if trackType == "Inner":
		xMax = 0.2
	if trackType == "Outer":
		xMax = 0.4

	plotPad.DrawFrame(0,0,6000,xMax,";M [GeV]; mass resolution")

	graphDefaultBB.Draw("samepe")
	graphORBB.Draw("samepe")
	graphNoBB.Draw("samepe")
	graphORBB.SetLineColor(kRed)
	graphORBB.SetMarkerColor(kRed)
	graphNoBB.SetLineColor(kBlue)
	graphNoBB.SetMarkerColor(kBlue)

	latex = TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexCMS = TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.055)
	latexCMS.SetNDC(True)
	latexCMSExtra = TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.03)
	latexCMSExtra.SetNDC(True) 

	latex.DrawLatex(0.95, 0.96, "(13 TeV)")

	cmsExtra = "#splitline{Preliminary}{}"
	latexCMS.DrawLatex(0.19,0.88,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))			


	leg = TLegend(0.52, 0.76, 0.95, 0.91,"%s BB"%trackType,"brNDC")
	leg.SetFillColor(10)
	leg.SetFillStyle(0)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)		
	leg.AddEntry(graphDefaultBB,"Default Window","l")
	leg.AddEntry(graphORBB,"Small Window","l")
	leg.AddEntry(graphNoBB,"Large Window","l")

	leg.Draw()

	plotPad.RedrawAxis()


	ratioPad.cd()

	ratioORBB.SetLineColor(kRed)
	ratioNoBB.SetLineColor(kBlue)

	ratioPad.DrawFrame(0,0.9,6000,1.1,";;ratio")

	ratioORBB.Draw("samepe")
	ratioNoBB.Draw("samepe")

	canv.Print("massResolutionWindow2018_%s_BB.pdf"%trackType)
	
	canv = TCanvas("c1","c1",800,1200)

	plotPad = TPad("plotPad","plotPad",0,0.3,1,1)
	ratioPad = TPad("ratioPad","ratioPad",0,0.,1,0.3)
	style = setTDRStyle()
	gStyle.SetOptStat(0)
	plotPad.UseCurrentStyle()
	ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	ratioPad.Draw()	
	plotPad.cd()
	plotPad.cd()
	plotPad.SetGrid()
	gStyle.SetTitleXOffset(1.45)

	xMax = 0.08
	if trackType == "Inner":
		xMax = 0.2
	if trackType == "Outer":
		xMax = 0.4

	plotPad.DrawFrame(0,0,6000,xMax,";M [GeV]; mass resolution")


	graphDefaultBE.Draw("samepe")
	graphORBE.Draw("samepe")
	graphNoBE.Draw("samepe")
	graphORBE.SetLineColor(kRed)
	graphORBE.SetMarkerColor(kRed)
	graphNoBE.SetLineColor(kBlue)
	graphNoBE.SetMarkerColor(kBlue)

	latex = TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexCMS = TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.055)
	latexCMS.SetNDC(True)
	latexCMSExtra = TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.03)
	latexCMSExtra.SetNDC(True) 

	latex.DrawLatex(0.95, 0.96, "(13 TeV)")

	cmsExtra = "#splitline{Preliminary}{}"
	latexCMS.DrawLatex(0.19,0.88,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))			


	leg = TLegend(0.52, 0.76, 0.95, 0.91,"%s BE"%trackType,"brNDC")
	leg.SetFillColor(10)
	leg.SetFillStyle(0)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)		
	leg.AddEntry(graphDefaultBE,"Default Window","l")
	leg.AddEntry(graphORBE,"Small Window","l")
	leg.AddEntry(graphNoBE,"Large Window","l")

	leg.Draw()

	plotPad.RedrawAxis()


	ratioPad.cd()

	ratioORBE.SetLineColor(kRed)
	ratioNoBE.SetLineColor(kBlue)

	ratioPad.DrawFrame(0,0.9,6000,1.1,";;ratio")

	ratioORBE.Draw("samepe")
	ratioNoBE.Draw("samepe")


	canv.Print("massResolutionWindow2018_%s_BE.pdf"%trackType)
	
	



#~ tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]
tracks = ["TunePNew"]
for trackType in tracks:
	compareMassRes(trackType)
