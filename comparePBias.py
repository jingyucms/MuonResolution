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
	mean = result["mean"]
	meanErr = result["meanErr"]	
	masses2 = result2["mass"]
	massErr2 = result2["massErr"]
	mean2 = result2["mean"]
	meanErr2 = result2["meanErr"]	
	
	
	ratio  = TGraphErrors(len(masses))
	ratio.SetName(label)
	for i,mass in enumerate(masses):     
		ratio   .SetPoint(i,mass,mean[i]/mean2[i])
		ratio   .SetPointError(i,massErr[i],(mean[i]/mean2[i])*math.sqrt((meanErr[i]/mean[i])**2+(meanErr2[i]/mean2[i])**2))
	
	return ratio
	

def getGraph(result,label):
	
	masses = result["mass"]
	massErr = result["massErr"]
	mean = result["mean"]
	meanErr = result["meanErr"]
	
	res  = TGraphAsymmErrors(len(masses))
	res.SetName(label)
	for i,mass in enumerate(masses):        
		res.SetPoint(i,mass,mean[i])
		res.SetPointError(i,massErr[i],massErr[i],meanErr[i],meanErr[i])
	
	return res


def compareMassRes(trackType):
	
	file2016B = open("default2016PSplit/PResolutionVsP_%s_B.pkl"%trackType)
	file2016O = open("default2016PSplit/PResolutionVsP_%s_O.pkl"%trackType)
	file2016E = open("default2016PSplit/PResolutionVsP_%s_E.pkl"%trackType)
	file2017B = open("defaultPSplit/PResolutionVsP_%s_B.pkl"%trackType)
	file2017O = open("defaultPSplit/PResolutionVsP_%s_O.pkl"%trackType)
	file2017E = open("defaultPSplit/PResolutionVsP_%s_E.pkl"%trackType)
	file2018B = open("default2018PSplit/PResolutionVsP_%s_B.pkl"%trackType)
	file2018O = open("default2018PSplit/PResolutionVsP_%s_O.pkl"%trackType)
	file2018E = open("default2018PSplit/PResolutionVsP_%s_E.pkl"%trackType)

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
		
	
	ratioB = 	getRatio(results2016B,results2017B,"ratioB")
	ratioO = 	getRatio(results2016O,results2017O,"ratioO")
	ratioE = 	getRatio(results2016E,results2017E,"ratioE")
	ratioB18 = getRatio(results2016B,results2018B,"ratioB18")
	ratioO18 = getRatio(results2016O,results2018O,"ratioO18")
	ratioE18 = getRatio(results2016E,results2018E,"ratioE18")



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
	gStyle.SetTitleYOffset(1.55)

	#~ xMax = 0.08
	#~ if trackType == "Inner":
		#~ xMax = 0.2
	#~ if trackType == "Outer":
		#~ xMax = 0.4

	plotPad.DrawFrame(0,-0.025,3100,0.025,";p^{#mu} [GeV]; fitted p bias")

	graph2016B.Draw("samepe")
	graph2017B.Draw("samepe")
	graph2018B.Draw("samepe")
	graph2017B.SetLineColor(kRed)
	graph2017B.SetMarkerColor(kRed)
	graph2018B.SetLineColor(kBlue)
	graph2018B.SetMarkerColor(kBlue)

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


	leg = TLegend(0.52, 0.76, 0.95, 0.91,"%s Barrel"%trackType,"brNDC")
	leg.SetFillColor(10)
	leg.SetFillStyle(0)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)		
	leg.AddEntry(graph2016B,"2016","l")
	leg.AddEntry(graph2017B,"2017","l")
	leg.AddEntry(graph2018B,"2018","l")

	leg.Draw()

	plotPad.RedrawAxis()


	ratioPad.cd()

	ratioB.SetLineColor(kRed)
	ratioB18.SetLineColor(kBlue)
	ratioB.SetMarkerColor(kRed)
	ratioB18.SetMarkerColor(kBlue)

	ratioPad.DrawFrame(0,0,3100,2,";;ratio")

	ratioB.Draw("samepe")
	ratioB18.Draw("samepe")

	l = TLine(0,1,3100,1)
	l.SetLineStyle(kDashed)
	l.Draw()
	
	canv.Print("pBiasCompare_%s_B.pdf"%trackType)


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
	gStyle.SetTitleYOffset(1.55)

	#~ xMax = 0.08
	#~ if trackType == "Inner":
		#~ xMax = 0.2
	#~ if trackType == "Outer":
		#~ xMax = 0.4

	plotPad.DrawFrame(0,-0.025,3100,0.025,";p^{#mu} [GeV]; fitted p bias")

	graph2016O.Draw("samepe")
	graph2017O.Draw("samepe")
	graph2018O.Draw("samepe")
	graph2017O.SetLineColor(kRed)
	graph2017O.SetMarkerColor(kRed)
	graph2018O.SetLineColor(kBlue)
	graph2018O.SetMarkerColor(kBlue)

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


	leg = TLegend(0.52, 0.76, 0.95, 0.91,"%s Barrel"%trackType,"brNDC")
	leg.SetFillColor(10)
	leg.SetFillStyle(0)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)		
	leg.AddEntry(graph2016O,"2016","l")
	leg.AddEntry(graph2017O,"2017","l")
	leg.AddEntry(graph2018O,"2018","l")

	leg.Draw()

	plotPad.RedrawAxis()


	ratioPad.cd()

	ratioO.SetLineColor(kRed)
	ratioO18.SetLineColor(kBlue)
	ratioO.SetMarkerColor(kRed)
	ratioO18.SetMarkerColor(kBlue)

	ratioPad.DrawFrame(0,0,3100,2,";;ratio")

	ratioO.Draw("samepe")
	ratioO18.Draw("samepe")

	l = TLine(0,1,3100,1)
	l.SetLineStyle(kDashed)
	l.Draw()
	
	canv.Print("pBiasCompare_%s_O.pdf"%trackType)
	
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
	gStyle.SetTitleYOffset(1.55)

	#~ xMax = 0.08
	#~ if trackType == "Inner":
		#~ xMax = 0.2
	#~ if trackType == "Outer":
		#~ xMax = 0.4

	plotPad.DrawFrame(0,-0.025,3100,0.025,";p^{#mu} [GeV]; fitted p bias")

	graph2016E.Draw("samepe")
	graph2017E.Draw("samepe")
	graph2018E.Draw("samepe")
	graph2017E.SetLineColor(kRed)
	graph2017E.SetMarkerColor(kRed)
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


	leg = TLegend(0.52, 0.76, 0.95, 0.91,"%s Barrel"%trackType,"brNDC")
	leg.SetFillColor(10)
	leg.SetFillStyle(0)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)		
	leg.AddEntry(graph2016E,"2016","l")
	leg.AddEntry(graph2017E,"2017","l")
	leg.AddEntry(graph2018E,"2018","l")

	leg.Draw()

	plotPad.RedrawAxis()


	ratioPad.cd()

	ratioE.SetLineColor(kRed)
	ratioE18.SetLineColor(kBlue)
	ratioE.SetMarkerColor(kRed)
	ratioE18.SetMarkerColor(kBlue)

	ratioPad.DrawFrame(0,0,3100,2,";;ratio")

	ratioE.Draw("samepe")
	ratioE18.Draw("samepe")

	l = TLine(0,1,3100,1)
	l.SetLineStyle(kDashed)
	l.Draw()
	
	canv.Print("pBiasCompare_%s_E.pdf"%trackType)
	
	



tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]
for trackType in tracks:
	compareMassRes(trackType)
