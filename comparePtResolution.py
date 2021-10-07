from ROOT import TGraphAsymmErrors, TGraphErrors, TCanvas, TLegend, TPad, gStyle, kRed, kGreen, kBlue, TLatex
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


def comparePtRes(trackType):
	
	file2016B = open("default2016Pt/PtResolutionVsPt_%s_B.pkl"%trackType,'rb')
	file2016O = open("default2016Pt/PtResolutionVsPt_%s_O.pkl"%trackType,'rb')
	file2016E = open("default2016Pt/PtResolutionVsPt_%s_E.pkl"%trackType,'rb')
	file2017B = open("defaultPtSplit/PtResolutionVsPt_%s_B.pkl"%trackType,'rb')
	file2017O = open("defaultPtSplit/PtResolutionVsPt_%s_O.pkl"%trackType,'rb')
	file2017E = open("defaultPtSplit/PtResolutionVsPt_%s_E.pkl"%trackType,'rb')
	file2018B = open("default2018Pt/PtResolutionVsPt_%s_B.pkl"%trackType,'rb')
	file2018O = open("default2018Pt/PtResolutionVsPt_%s_O.pkl"%trackType,'rb')
	file2018E = open("default2018Pt/PtResolutionVsPt_%s_E.pkl"%trackType,'rb')

	results2016B = pickle.load(file2016B)
	results2016O = pickle.load(file2016O)
	results2016E = pickle.load(file2016E)

	results2017B = pickle.load(file2017B)
	results2017O = pickle.load(file2017O)
	results2017E = pickle.load(file2017E)

	results2018B = pickle.load(file2018B)
	results2018O = pickle.load(file2018O)
	results2018E = pickle.load(file2018E)

	graph2016B = getGraph(results2016B,"2016B")
	graph2016O = getGraph(results2016O,"2016O")
	graph2016E = getGraph(results2016E,"2016E")

	graph2017B = getGraph(results2017B,"2017B")
	graph2017O = getGraph(results2017O,"2017O")
	graph2017E = getGraph(results2017E,"2017E")
		
	graph2018B = getGraph(results2018B,"2018B")
	graph2018O = getGraph(results2018O,"2018O")
	graph2018E = getGraph(results2018E,"2018E")
		


	canv = TCanvas("c1","c1",800,1200)

	plotPad = TPad("plotPad","plotPad",0,0.,1,1)
	# ~ ratioPad = TPad("ratioPad","ratioPad",0,0.,1,0.3)
	style = setTDRStyle()
	gStyle.SetOptStat(0)
	plotPad.UseCurrentStyle()
	# ~ ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	# ~ ratioPad.Draw()	
	plotPad.cd()
	plotPad.cd()
	plotPad.SetGrid()
	gStyle.SetTitleXOffset(1.45)
	gStyle.SetTitleYOffset(1.55)

	xMax = 0.15
	if trackType == "Inner":
		xMax = 0.3
	if trackType == "Outer":
		xMax = 0.5

	plotPad.DrawFrame(0,0,2000,xMax,";p_{T} [GeV]; p_{T} resolution [%]")

	graph2016B.Draw("samepe")
	# ~ graph2016O.Draw("samepe")
	graph2016E.Draw("samepe")
	graph2016B.SetLineColor(kRed)
	graph2016B.SetMarkerColor(kRed)
	graph2016O.SetLineColor(kGreen)
	graph2016O.SetMarkerColor(kGreen)
	graph2016E.SetLineColor(kBlue)
	graph2016E.SetMarkerColor(kBlue)

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


	leg = TLegend(0.52, 0.76, 0.95, 0.91,"%s 2016"%trackType,"brNDC")
	leg.SetFillColor(10)
	leg.SetFillStyle(0)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)		
	leg.AddEntry(graph2016B,"Barrel","l")
	# ~ leg.AddEntry(graph2016O,"Overlap","l")
	leg.AddEntry(graph2016E,"Endcap","l")

	leg.Draw()

	plotPad.RedrawAxis()


	canv.Print("PtResolutionCompare_%s_2016.pdf"%trackType)
	canv.Print("PtResolutionCompare_%s_2016.root"%trackType)

	canv = TCanvas("c1","c1",800,1200)

	plotPad = TPad("plotPad","plotPad",0,0.,1,1)
	# ~ ratioPad = TPad("ratioPad","ratioPad",0,0.,1,0.3)
	style = setTDRStyle()
	gStyle.SetOptStat(0)
	plotPad.UseCurrentStyle()
	# ~ ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	# ~ ratioPad.Draw()	
	plotPad.cd()
	plotPad.cd()
	plotPad.SetGrid()
	gStyle.SetTitleXOffset(1.45)
	gStyle.SetTitleYOffset(1.55)

	xMax = 0.15
	if trackType == "Inner":
		xMax = 0.3
	if trackType == "Outer":
		xMax = 0.5

	plotPad.DrawFrame(0,0,2000,xMax,";p_{T} [GeV]; p_{T} resolution [%]")

	graph2017B.Draw("samepe")
	# ~ graph2017O.Draw("samepe")
	graph2017E.Draw("samepe")
	graph2017B.SetLineColor(kRed)
	graph2017B.SetMarkerColor(kRed)
	graph2017O.SetLineColor(kGreen)
	graph2017O.SetMarkerColor(kGreen)
	graph2017E.SetLineColor(kBlue)
	graph2017E.SetMarkerColor(kBlue)

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


	leg = TLegend(0.52, 0.76, 0.95, 0.91,"%s 2017"%trackType,"brNDC")
	leg.SetFillColor(10)
	leg.SetFillStyle(0)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)		
	leg.AddEntry(graph2017B,"Barrel","l")
	# ~ leg.AddEntry(graph2017O,"Overlap","l")
	leg.AddEntry(graph2017E,"Endcap","l")

	leg.Draw()

	plotPad.RedrawAxis()


	canv.Print("PtResolutionCompare_%s_2017.pdf"%trackType)
	canv.Print("PtResolutionCompare_%s_2017.root"%trackType)

	canv = TCanvas("c1","c1",800,1200)

	plotPad = TPad("plotPad","plotPad",0,0.,1,1)
	# ~ ratioPad = TPad("ratioPad","ratioPad",0,0.,1,0.3)
	style = setTDRStyle()
	gStyle.SetOptStat(0)
	plotPad.UseCurrentStyle()
	# ~ ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	# ~ ratioPad.Draw()	
	plotPad.cd()
	plotPad.cd()
	plotPad.SetGrid()
	gStyle.SetTitleXOffset(1.45)
	gStyle.SetTitleYOffset(1.55)

	xMax = 0.15
	if trackType == "Inner":
		xMax = 0.3
	if trackType == "Outer":
		xMax = 0.5

	plotPad.DrawFrame(0,0,2000,xMax,";p_{T} [GeV]; p_{T} resolution [%]")

	graph2018B.Draw("samepe")
	# ~ graph2018O.Draw("samepe")
	graph2018E.Draw("samepe")
	graph2018B.SetLineColor(kRed)
	graph2018B.SetMarkerColor(kRed)
	graph2018O.SetLineColor(kGreen)
	graph2018O.SetMarkerColor(kGreen)
	graph2018E.SetLineColor(kBlue)
	graph2018E.SetMarkerColor(kBlue)

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


	leg = TLegend(0.52, 0.76, 0.95, 0.91,"%s 2018"%trackType,"brNDC")
	leg.SetFillColor(10)
	leg.SetFillStyle(0)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)		
	leg.AddEntry(graph2018B,"Barrel","l")
	# ~ leg.AddEntry(graph2018O,"Overlap","l")
	leg.AddEntry(graph2018E,"Endcap","l")

	leg.Draw()

	plotPad.RedrawAxis()


	canv.Print("PtResolutionCompare_%s_2018.pdf"%trackType)
	canv.Print("PtResolutionCompare_%s_2018.root"%trackType)
	


tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]
for trackType in tracks:
	comparePtRes(trackType)
