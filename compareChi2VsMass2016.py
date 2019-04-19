from ROOT import *
import pickle
import math
from setTDRStyle import setTDRStyle

#~ ptbins = [52, 72, 100, 152, 200, 300, 452, 800.]


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
	chi2 = result["chi2"]
	masses2 = result2["mass"]
	massErr2 = result2["massErr"]
	chi22 = result2["chi2"]
	
	
	ratio  = TGraphErrors(len(masses))
	ratio.SetName(label)
	for i,mass in enumerate(masses):    
		ratio   .SetPoint(i,mass,chi2[i]/chi22[i])
		ratio   .SetPointError(i,massErr[i],0)
	
	return ratio
	

def getGraph(result,label,Data=False):
	
	masses = result["mass"]
	massErr = result["massErr"]
	chi2 = result["chi2"]
	
	res  = TGraphAsymmErrors(len(masses))
	res.SetName(label)
	for i,mass in enumerate(masses):        
		res.SetPoint(i,mass,chi2[i])
		res.SetPointError(i,massErr[i],massErr[i],0,0)
	
	return res
	


def compareMassRes(trackType):
	
	file2016BB = open("default2016/MassResolutionVsMass_%s_BB.pkl"%trackType)
	file2016BE = open("default2016/MassResolutionVsMass_%s_BE.pkl"%trackType)
	file2017BB = open("cruijff2016/MassResolutionVsMass_%s_BB.pkl"%trackType)
	file2017BE = open("cruijff2016/MassResolutionVsMass_%s_BE.pkl"%trackType)
	fileCBB = open("crystal2016/MassResolutionVsMass_%s_BB.pkl"%trackType)
	fileCBE = open("crystal2016/MassResolutionVsMass_%s_BE.pkl"%trackType)

	results2016BB = pickle.load(file2016BB)
	results2016BE = pickle.load(file2016BE)
	results2017BB = pickle.load(file2017BB)
	results2017BE = pickle.load(file2017BE)
	resultsCBB = pickle.load(fileCBB)
	resultsCBE = pickle.load(fileCBE)

	graph2016BB = getGraph(results2016BB,"2016BB")
	graph2016BE = getGraph(results2016BE,"2016BE")
	graph2017BB = getGraph(results2017BB,"2017BB")
	graph2017BE = getGraph(results2017BE,"2017BE")
	graphCBB = getGraph(resultsCBB,"CBB")
	graphCBE = getGraph(resultsCBE,"CBE")
		
	
	ratioBB = 	getRatio(results2016BB,results2017BB,"ratioBB")
	ratioBE = 	getRatio(results2016BE,results2017BE,"ratioBE")
	ratioCBB = 	getRatio(results2016BB,resultsCBB,"ratioCBB")
	ratioCBE = 	getRatio(results2016BE,resultsCBE,"ratioCBE")



	canv = TCanvas("c1","c1",800,800)

	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	#~ ratioPad = TPad("ratioPad","ratioPad",0,0.,1,0.3)
	style = setTDRStyle()
	gStyle.SetOptStat(0)
	plotPad.UseCurrentStyle()
	#~ ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	#~ ratioPad.Draw()	
	plotPad.cd()
	plotPad.cd()
	plotPad.SetGrid()
	gStyle.SetTitleXOffset(1.45)

	xMax = 10
	if trackType == "Inner":
		xMax = 10
	if trackType == "Outer":
		xMax = 20

	plotPad.DrawFrame(0,0,6000,xMax,";mass [GeV]; #chi^{2}/N_{dof}")

	graph2016BB.Draw("samepl")
	graph2017BB.Draw("samepl")
	graph2017BB.SetLineColor(kRed)
	graph2017BB.SetMarkerColor(kRed)
	graphCBB.Draw("samepl")
	graphCBB.SetLineColor(kBlue)
	graphCBB.SetMarkerColor(kBlue)

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
	leg.AddEntry(graph2016BB,"Double-Sided CB","l")
	leg.AddEntry(graph2017BB,"Cruijff","l")
	leg.AddEntry(graphCBB,"Crystal Ball","l")

	leg.Draw()

	plotPad.RedrawAxis()


	#~ ratioPad.cd()

	#~ ratioBB.SetLineColor(kRed)

	#~ ratioPad.DrawFrame(0,0.5,6000,1.5,";;ratio")

	#~ ratioBB.Draw("samepe")


	canv.Print("chi2CompareVsMass2016_%s_BB.pdf"%trackType)
	
	
	canv = TCanvas("c1","c1",800,800)

	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	#~ ratioPad = TPad("ratioPad","ratioPad",0,0.,1,0.3)
	style = setTDRStyle()
	gStyle.SetOptStat(0)
	plotPad.UseCurrentStyle()
	#~ ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	#~ ratioPad.Draw()	
	plotPad.cd()
	plotPad.cd()
	plotPad.SetGrid()
	gStyle.SetTitleXOffset(1.45)

	xMax = 10
	if trackType == "Inner":
		xMax = 10
	if trackType == "Outer":
		xMax = 10

	plotPad.DrawFrame(0,0,6000,xMax,";mass [GeV]; #chi^{2}/N_{dof}")

	graph2016BE.Draw("samepl")
	graph2017BE.Draw("samepl")
	graph2017BE.SetLineColor(kRed)
	graph2017BE.SetMarkerColor(kRed)
	graphCBE.Draw("samepl")
	graphCBE.SetLineColor(kBlue)
	graphCBE.SetMarkerColor(kBlue)

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
	leg.AddEntry(graph2016BE,"Double-Sided CB","l")
	leg.AddEntry(graph2017BE,"Cruiff","l")
	leg.AddEntry(graphCBE,"Crystal Ball","l")

	leg.Draw()

	plotPad.RedrawAxis()



	canv.Print("chi2CompareVsMass2016_%s_BE.pdf"%trackType)


#~ tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]
tracks = ["TunePNew"]
for trackType in tracks:
	compareMassRes(trackType)
