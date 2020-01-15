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
	fun = TF1("fun", "pol4")
	for i in range(fun.GetNpar()):
		fun.ReleaseParameter(i)
		fun.SetParameter(i, 0.)
	fun.SetParameters(0., 1E-5, -1.E-8, 2E-12,-2E-16)
	fun.SetParLimits(1, 1.0E-6, 1.0E-4)
        fun.SetParLimits(2,-1.0E-7,-1.0E-9)
        fun.SetParLimits(4,-1.0E-16,1.0E-16)
	res.Fit(fun, "MBFE+")

	return res


def compareMassRes(trackType):
	
	file2016BB = open("ResVsMass2016final/MassResolutionVsMass_%s_BB.pkl"%trackType)
	file2016BE = open("ResVsMass2016final/MassResolutionVsMass_%s_BE.pkl"%trackType)
	file2017BB = open("ResVsMass2017final/MassResolutionVsMass_%s_BB.pkl"%trackType)
	file2017BE = open("ResVsMass2017final/MassResolutionVsMass_%s_BE.pkl"%trackType)
	file2018BB = open("ResVsMass2018final/MassResolutionVsMass_%s_BB.pkl"%trackType)
	file2018BE = open("ResVsMass2018final/MassResolutionVsMass_%s_BE.pkl"%trackType)

	results2016BB = pickle.load(file2016BB)
	results2016BE = pickle.load(file2016BE)
	results2017BB = pickle.load(file2017BB)
	results2017BE = pickle.load(file2017BE)
	results2018BB = pickle.load(file2018BB)
	results2018BE = pickle.load(file2018BE)
	'''
	BB2016 = getGraph(results2016BB,"2016BB")
	BE2016 = getGraph(results2016BE,"2016BE")
	BB2017 = getGraph(results2017BB,"2017BB")
	BE2017 = getGraph(results2017BE,"2017BE")
	BB2018 = getGraph(results2018BB,"2018BB")
	BE2018 = getGraph(results2018BE,"2018BE")
	
	graph2016BB = BB2016.GetFunction("fun")
	graph2016BE = BE2016.GetFunction("fun")	
        graph2017BB = BB2017.GetFunction("fun")
        graph2017BE = BE2017.GetFunction("fun")
        graph2018BB = BB2018.GetFunction("fun")
        graph2018BE = BE2017.GetFunction("fun")
	'''
	graph2016BB = TF1("graph2016BB", "pol4", 0, 6000)
        for i in range(graph2016BB.GetNpar()):
                graph2016BB.ReleaseParameter(i)
	graph2016BB.SetParameters(0.0076, 3.19E-5, -1.05E-8, 1.8E-12, -1E-16)
	graph2016BB.SetParError(0, 0.00147)
        graph2016BB.SetParError(1, 4.26E-6)
        graph2016BB.SetParError(2, 2.58E-9)
        graph2016BB.SetParError(3, 4.04E-13)
        graph2016BB.SetParError(4, 1.85E-16)
	
	graph2016BE = TF1("graph2016BE", "pol4", 0, 6000)
	for i in range(graph2016BE.GetNpar()):
                graph2016BE.ReleaseParameter(i)
	graph2016BE.SetParameters(0.0132, 3.08E-5, -9.81E-9, 1.67E-12, -1E-16)
        graph2016BE.SetParError(0, 0.00169)
        graph2016BE.SetParError(1, 4.84E-6)
        graph2016BE.SetParError(2, 2.89E-9)
        graph2016BE.SetParError(3, 4.41E-13)
        graph2016BE.SetParError(4, 1.76E-16)
	
	graph2017BB = TF1("graph2017BB", "pol4", 0, 6000)
        for i in range(graph2017BB.GetNpar()):
                graph2017BB.ReleaseParameter(i)
        graph2017BB.SetParameters(0.00595, 3.43E-5, -1.3E-8, 2.11E-12, -1E-16)
        graph2017BB.SetParError(0, 0.0014)
        graph2017BB.SetParError(1, 4.3E-6)
        graph2017BB.SetParError(2, 2.9E-9)
        graph2017BB.SetParError(3, 5.01E-13)
        graph2017BB.SetParError(4, 1.41E-16)
	
	#print graph2017BB.Eval(6000)
        graph2017BE = TF1("graph2017BE", "pol4", 0, 6000)
        for i in range(graph2017BE.GetNpar()):
                graph2017BE.ReleaseParameter(i)
        graph2017BE.SetParameters(0.0113, 3.09E-5, -1.03E-8, 1.7E-12, -1E-16)
        graph2017BE.SetParError(0, 0.00134)
        graph2017BE.SetParError(1, 3.56E-6)
        graph2017BE.SetParError(2, 2.06E-9)
        graph2017BE.SetParError(3, 3.08E-13)
        graph2017BE.SetParError(4, 1.44E-16)
	
	graph2018BB = TF1("graph2018BB", "pol4", 0, 6000)
        for i in range(graph2018BB.GetNpar()):
                graph2018BB.ReleaseParameter(i)
	graph2018BB.SetParameters(0.00798, 2.97E-5, -1.04E-8, 1.72E-12, -1E-16)
        graph2018BB.SetParError(0, 0.0012)
        graph2018BB.SetParError(1, 3.17E-6)
        graph2018BB.SetParError(2, 1.82E-9)
        graph2018BB.SetParError(3, 2.73E-13)
        graph2018BB.SetParError(4, 1.41E-16)
	
        graph2018BE = TF1("graph2018BE", "pol4", 0, 6000)
	for i in range(graph2018BE.GetNpar()):
		graph2018BE.ReleaseParameter(i)
        graph2018BE.SetParameters(0.0138, 2.73E-5, -8.97E-9, 1.54E-12, -1E-16)
        graph2018BE.SetParError(0, 0.00131)
        graph2018BE.SetParError(1, 3.38E-6)
        graph2018BE.SetParError(2, 1.86E-9)
        graph2018BE.SetParError(3, 2.65E-13)
        graph2018BE.SetParError(4, 1.72E-16)
	
	#ratioBB = 	getRatio(results2016BB,results2017BB,"ratioBB")
	#ratioBE = 	getRatio(results2016BE,results2017BE,"ratioBE")
	#ratioBB18 = getRatio(results2016BB,results2018BB,"ratioBB18")
	#ratioBE18 = getRatio(results2016BE,results2018BE,"ratioBE18")


	canv = TCanvas("c1","c1",800,800)

	plotPad = TPad("plotPad","plotPad",0,0.,1,1)
	#ratioPad = TPad("ratioPad","ratioPad",0,0.,1,0.3)
	style = setTDRStyle()
	gStyle.SetOptStat(0)
	plotPad.UseCurrentStyle()
	#ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	#ratioPad.Draw()	
	plotPad.cd()
	plotPad.cd()
	plotPad.SetGrid()
	gStyle.SetTitleXOffset(1.45)
	gStyle.SetTitleYOffset(1.55)

	xMax = 0.12
	if trackType == "Inner":
		xMax = 0.2
	if trackType == "Outer":
		xMax = 0.4

	plotPad.DrawFrame(0,0,6000,xMax,";M [GeV]; mass resolution")

	'''graph2016BB.DrawCopy("same")
	graph2017BB.DrawCopy("same")
	graph2018BB.DrawCopy("same")'''
	graph2016BB.SetLineColor(kBlack)
	#graph2016BB.SetMarkerColor(kBlack)
	graph2017BB.SetLineColor(kRed)
	#graph2017BB.SetMarkerColor(kRed)
	graph2018BB.SetLineColor(kBlue)
	#graph2018BB.SetMarkerColor(kBlue)
	graph2016BB.DrawCopy("cesame")
        graph2017BB.DrawCopy("cesame")
        graph2018BB.DrawCopy("cesame")
	
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
	leg.AddEntry(graph2016BB,"2016","l")
	leg.AddEntry(graph2017BB,"2017","l")
	leg.AddEntry(graph2018BB,"2018","l")

	leg.Draw()

	plotPad.RedrawAxis()


	'''ratioPad.cd()

	ratioBB.SetLineColor(kRed)
	ratioBB18.SetLineColor(kBlue)
	ratioBB.SetMarkerColor(kRed)
	ratioBB18.SetMarkerColor(kBlue)

	ratioPad.DrawFrame(0,0.5,6000,1.5,";;ratio")

	ratioBB.Draw("samepe")
	ratioBB18.Draw("samepe")

	l = TLine(0,1,6000,1)
	l.SetLineStyle(kDashed)
	l.Draw()'''
	
	canv.Print("massResolutionCompareFit_%s_BB.pdf"%trackType)
	
	
	canv = TCanvas("c1","c1",800,800)

	plotPad = TPad("plotPad","plotPad",0,0.,1,1)
	#ratioPad = TPad("ratioPad","ratioPad",0,0.,1,0.3)
	style = setTDRStyle()
	gStyle.SetOptStat(0)
	plotPad.UseCurrentStyle()
	#ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	#ratioPad.Draw()	
	plotPad.cd()
	plotPad.cd()
	plotPad.SetGrid()
	gStyle.SetTitleXOffset(1.45)
	gStyle.SetTitleYOffset(1.55)

	xMax = 0.12
	if trackType == "Inner":
		xMax = 0.2
	if trackType == "Outer":
		xMax = 0.4

	plotPad.DrawFrame(0,0,6000,xMax,";M [GeV]; mass resolution")

	'''graph2016BE.Draw("same")
	graph2017BE.Draw("same")
	graph2018BE.Draw("same")'''
	graph2016BE.SetLineColor(kBlack)
	#graph2016BE.SetMarkerColor(kBlack)
	graph2017BE.SetLineColor(kRed)
	#graph2017BE.SetMarkerColor(kRed)
	graph2018BE.SetLineColor(kBlue)
	#graph2018BE.SetMarkerColor(kBlue)
        graph2016BE.Draw("ce same")
        graph2017BE.Draw("ce same")
        graph2018BE.Draw("ce same")

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
	leg.AddEntry(graph2016BE,"2016","l")
	leg.AddEntry(graph2017BE,"2017","l")
	leg.AddEntry(graph2018BE,"2018","l")

	leg.Draw()

	plotPad.RedrawAxis()

	'''
	ratioPad.cd()

	ratioBE.SetLineColor(kRed)
	ratioBE18.SetLineColor(kBlue)
	ratioBE.SetMarkerColor(kRed)
	ratioBE18.SetMarkerColor(kBlue)

	ratioPad.DrawFrame(0,0.5,6000,1.5,";;ratio")

	l = TLine(0,1,6000,1)
	l.SetLineStyle(kDashed)
	l.Draw()

	ratioBE.Draw("samepe")
	ratioBE18.Draw("samepe")

	'''
	canv.Print("massResolutionCompareFit_%s_BE.pdf"%trackType)


#tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]
tracks = ["TunePNew"]
for trackType in tracks:
	compareMassRes(trackType)
