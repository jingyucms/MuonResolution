from ROOT import *
import pickle
import math
from setTDRStyle import setTDRStyle
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
	
	file2016BB = open("massRes2016Split/MassResolutionVsMass_%s_BB.pkl"%trackType)
	file2016OO = open("massRes2016Split/MassResolutionVsMass_%s_OO.pkl"%trackType)
	file2016EE = open("massRes2016Split/MassResolutionVsMass_%s_EE.pkl"%trackType)
	file2017BB = open("massRes2017Split/MassResolutionVsMass_%s_BB.pkl"%trackType)
	file2017OO = open("massRes2017Split/MassResolutionVsMass_%s_OO.pkl"%trackType)
	file2017EE = open("massRes2017Split/MassResolutionVsMass_%s_EE.pkl"%trackType)

	results2016BB = pickle.load(file2016BB)
	results2016OO = pickle.load(file2016OO)
	results2016EE = pickle.load(file2016EE)
	results2017BB = pickle.load(file2017BB)
	results2017OO = pickle.load(file2017OO)
	results2017EE = pickle.load(file2017EE)

	graph2016BB = getGraph(results2016BB,"2016BB")
	graph2016OO = getGraph(results2016OO,"2016OO")
	graph2016EE = getGraph(results2016EE,"2016EE")
	graph2017BB = getGraph(results2017BB,"2017BB")
	graph2017OO = getGraph(results2017OO,"2017OO")
	graph2017EE = getGraph(results2017EE,"2017EE")
		
	
	ratioBB = 	getRatio(results2016BB,results2017BB,"ratioBB")
	ratioOO = 	getRatio(results2016OO,results2017OO,"ratioOO")
	ratioEE = 	getRatio(results2016EE,results2017EE,"ratioEE")



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

	graph2016BB.Draw("samepe")
	graph2017BB.Draw("samepe")
	graph2017BB.SetLineColor(kRed)
	graph2017BB.SetMarkerColor(kRed)

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


	leg = TLegend(0.52, 0.76, 0.95, 0.91,"%s Barrel-Barrel"%trackType,"brNDC")
	leg.SetFillColor(10)
	leg.SetFillStyle(0)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)		
	leg.AddEntry(graph2016BB,"2016","l")
	leg.AddEntry(graph2017BB,"2017","l")

	leg.Draw()

	plotPad.RedrawAxis()


	ratioPad.cd()

	ratioBB.SetLineColor(kRed)
	ratioBB.SetMarkerColor(kRed)

	ratioPad.DrawFrame(0,0.5,6000,1.5,";;ratio")

	ratioBB.Draw("samepe")


	canv.Print("massResolutionCompare_%s_BB.pdf"%trackType)
	
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

	graph2016OO.Draw("samepe")
	graph2017OO.Draw("samepe")
	graph2017OO.SetLineColor(kRed)
	graph2017OO.SetMarkerColor(kRed)

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


	leg = TLegend(0.52, 0.76, 0.95, 0.91,"%s Overlap-Overlap"%trackType,"brNDC")
	leg.SetFillColor(10)
	leg.SetFillStyle(0)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)		
	leg.AddEntry(graph2016OO,"2016","l")
	leg.AddEntry(graph2017OO,"2017","l")

	leg.Draw()

	plotPad.RedrawAxis()


	ratioPad.cd()

	ratioOO.SetLineColor(kRed)
	ratioOO.SetMarkerColor(kRed)

	ratioPad.DrawFrame(0,0.5,6000,1.5,";;ratio")

	ratioOO.Draw("samepe")


	canv.Print("massResolutionCompare_%s_OO.pdf"%trackType)
	
	
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

	graph2016EE.Draw("samepe")
	graph2017EE.Draw("samepe")
	graph2017EE.SetLineColor(kRed)
	graph2017EE.SetMarkerColor(kRed)

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


	leg = TLegend(0.52, 0.76, 0.95, 0.91,"%s Endcap-Endcap"%trackType,"brNDC")
	leg.SetFillColor(10)
	leg.SetFillStyle(0)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)		
	leg.AddEntry(graph2016EE,"2016","l")
	leg.AddEntry(graph2017EE,"2017","l")

	leg.Draw()

	plotPad.RedrawAxis()


	ratioPad.cd()

	ratioEE.SetLineColor(kRed)
	ratioEE.SetMarkerColor(kRed)

	ratioPad.DrawFrame(0,0.5,6000,1.5,";;ratio")

	ratioEE.Draw("samepe")


	canv.Print("massResolutionCompare_%s_EE.pdf"%trackType)


tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]
for trackType in tracks:
	compareMassRes(trackType)
