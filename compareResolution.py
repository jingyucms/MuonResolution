from ROOT import TGraphAsymmErrors, TCanvas, TPad, TGraphErrors, gStyle, kRed, kBlue, kBlack, TLatex, TLegend, TLine, kDashed
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
	
	fileEOYBB = open("MassResolutionVsMass_TunePNew_BB_EOY.pkl","rb")
	fileEOYBE = open("MassResolutionVsMass_TunePNew_BE_EOY.pkl","rb")
	fileULBB = open("default/MassResolutionVsMass_TunePNew_BB.pkl","rb")
	fileULBE = open("default/MassResolutionVsMass_TunePNew_BE.pkl","rb")

	resultsEOYBB = pickle.load(fileEOYBB)
	resultsEOYBE = pickle.load(fileEOYBE)
	resultsULBB = pickle.load(fileULBB)
	resultsULBE = pickle.load(fileULBE)


	graphEOYBB = getGraph(resultsEOYBB,"EOYBB")
	graphEOYBE = getGraph(resultsEOYBE,"EOYBE")
	graphULBB = getGraph(resultsULBB,"ULBB")
	graphULBE = getGraph(resultsULBE,"ULBE")

		
	
	ratioBB = 	getRatio(resultsEOYBB,resultsULBB,"ratioBB")
	ratioBE = 	getRatio(resultsEOYBE,resultsULBE,"ratioBE")




	canv = TCanvas("c1","c1",800,800)

	plotPad = TPad("plotPad","plotPad",0.01,0.01,0.99,0.99)

	ratioPad = TPad("ratioPad","ratioPad",0.01, 0.01, 0.99, 0.29)
	style = setTDRStyle()
	gStyle.SetOptStat(0)
	plotPad.UseCurrentStyle()
	ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	ratioPad.Draw()	
	plotPad.cd()
	plotPad.cd()
	# ~ plotPad.SetGrid()
	gStyle.SetTitleXOffset(1.45)
	gStyle.SetTitleYOffset(1.55)

	plotPad.SetTopMargin(0.05)
	plotPad.SetLeftMargin(0.13)
	plotPad.SetRightMargin(0.045)
	plotPad.SetBottomMargin(0.3)	
	
	ratioPad.SetTopMargin(0)
	ratioPad.SetTopMargin(0.05)
	ratioPad.SetLeftMargin(0.13)
	ratioPad.SetRightMargin(0.045)	
	ratioPad.SetBottomMargin(0.4)	

	#~ xMax = 0.08
	#~ if trackType == "Inner":
		#~ xMax = 0.2
	#~ if trackType == "Outer":
		#~ xMax = 0.4

	graphEOYBB.SetMarkerStyle(22)
	graphEOYBB.SetMarkerSize(2)
	graphEOYBB.SetMarkerColor(kBlack)
	graphEOYBB.SetLineColor(kBlack)
	graphEOYBB.SetLineWidth(2)
	graphEOYBB.SetFillColor(0)
	graphEOYBB.SetTitle("Dimuon mass resolution vs pT for %s tracks"%trackType)
	graphEOYBB.GetYaxis().SetTitle("Mass resolution")
	# ~ res_data.GetXaxis().SetTitle("p_{T} (#mu^{#pm}) [GeV]")
	graphEOYBB.GetYaxis().SetTitleFont(42)
	graphEOYBB.GetYaxis().SetTitleSize(0.05)
	graphEOYBB.GetYaxis().SetTitleOffset(1.35)
	graphEOYBB.GetYaxis().SetLabelFont(42)
	graphEOYBB.GetYaxis().SetLabelSize(0.038)
	graphEOYBB.GetYaxis().SetRangeUser(0,0.1)
	graphEOYBB.GetXaxis().SetTitleSize(0.0)
	graphEOYBB.GetXaxis().SetLabelSize(0.0)

	graphEOYBB.GetXaxis().SetRangeUser(0,6500)
	graphEOYBB.Draw("AP E0")

	graphULBB.Draw("samepe")
	graphEOYBB.SetMarkerSize(2)
	graphULBB.SetMarkerSize(2)
	graphEOYBB.SetLineWidth(2)
	graphULBB.SetLineWidth(2)
	graphEOYBB.SetMarkerStyle(20)
	graphULBB.SetMarkerStyle(21)
	graphULBB.SetLineColor(kRed)
	graphULBB.SetMarkerColor(kRed)

	latex = TLatex()
	# ~ latex.SetTextFont(42)
	# ~ latex.SetTextAlign(31)
	# ~ latex.SetTextSize(0.04)
	# ~ latex.SetNDC(True)
	latexCMS = TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.055)
	latexCMS.SetNDC(True)
	latexCMSExtra = TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(.03/0.7)
	latexCMSExtra.SetNDC(True) 

	latex.DrawLatexNDC(0.50, 0.96, "#scale[0.8]{#font[42]{       2017, 42.1 fb^{-1} (13 TeV)}}")

	cmsExtra = "Preliminary"
	latexCMS.DrawLatex(0.19,0.88,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))					


	leg = TLegend(0.5,0.65,0.95,0.90,"Both muons |#eta| < 1.2","brNDC")
	leg.SetFillColor(10)
	leg.SetFillStyle(0)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)		
	leg.AddEntry(graphEOYBB,"EOY ReReco","l")
	leg.AddEntry(graphULBB,"Legacy ReReco","l")


	leg.Draw()

	plotPad.RedrawAxis()


	ratioPad.cd()

	ratioBB.GetYaxis().SetTitle("#splitline{EOY ReReco/}{Legacy ReReco}")
	ratioBB.GetXaxis().SetNoExponent(0)
	ratioBB.GetXaxis().SetTitleFont(42)
	ratioBB.GetXaxis().SetTitleOffset(0.85)
	ratioBB.GetXaxis().SetTitleSize(0.2)
	ratioBB.GetXaxis().SetLabelColor(1)
	ratioBB.GetXaxis().SetLabelOffset(0.01)
	ratioBB.GetXaxis().SetLabelFont(42)
	ratioBB.GetXaxis().SetLabelSize(0.17)		
	ratioBB.GetXaxis().SetTitle("GEN dimuon mass (GeV)")
	ratioBB.GetYaxis().SetRangeUser(0.5,1.5)
	ratioBB.GetXaxis().SetRangeUser(0,6500)
	ratioBB.GetYaxis().SetTitleOffset(0.475)
	ratioBB.GetYaxis().SetTitleSize(0.12)
	ratioBB.GetYaxis().SetTitleFont(42)
	ratioBB.GetYaxis().SetLabelSize(0.14)    
	ratioBB.GetYaxis().SetLabelOffset(0.007)    
	ratioBB.GetYaxis().SetLabelFont(42)    
	ratioBB.GetYaxis().SetNdivisions(505)       
	
	ratioBB.SetMarkerColor(kRed)
	ratioBB.SetLineColor(kRed)
	ratioBB.SetLineWidth(2)
	ratioBB.SetMarkerStyle(20)
	ratioBB.SetMarkerSize(2)
	


	line = TLine(10,1,6500,1)

	line.SetLineColor(kBlack)
	line.SetLineStyle(kDashed)
	line.SetLineWidth(2)
	
	
	ratioBB.Draw("A P E")
	ratioBB.GetXaxis().SetRangeUser(0,6500)

	line.Draw()
	ratioBB.Draw("samePE")
	ratioPad.RedrawAxis()
	
	canv.Print("massResolutionCompareUL_%s_BB.pdf"%trackType)
	
	
	canv = TCanvas("c1","c1",800,800)

	plotPad = TPad("plotPad","plotPad",0.01,0.01,0.99,0.99)

	ratioPad = TPad("ratioPad","ratioPad",0.01, 0.01, 0.99, 0.29)
	style = setTDRStyle()
	gStyle.SetOptStat(0)
	plotPad.UseCurrentStyle()
	ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	ratioPad.Draw()	
	plotPad.cd()
	plotPad.cd()
	# ~ plotPad.SetGrid()
	gStyle.SetTitleXOffset(1.45)
	gStyle.SetTitleYOffset(1.55)

	plotPad.SetTopMargin(0.05)
	plotPad.SetLeftMargin(0.13)
	plotPad.SetRightMargin(0.045)
	plotPad.SetBottomMargin(0.3)	
	
	ratioPad.SetTopMargin(0)
	ratioPad.SetTopMargin(0.05)
	ratioPad.SetLeftMargin(0.13)
	ratioPad.SetRightMargin(0.045)	
	ratioPad.SetBottomMargin(0.4)	

	#~ xMax = 0.08
	#~ if trackType == "Inner":
		#~ xMax = 0.2
	#~ if trackType == "Outer":
		#~ xMax = 0.4

	graphEOYBE.SetMarkerStyle(22)
	graphEOYBE.SetMarkerSize(2)
	graphEOYBE.SetMarkerColor(kBlack)
	graphEOYBE.SetLineColor(kBlack)
	graphEOYBE.SetLineWidth(2)
	graphEOYBE.SetFillColor(0)
	graphEOYBE.SetTitle("Dimuon mass resolution vs pT for %s tracks"%trackType)
	graphEOYBE.GetYaxis().SetTitle("Mass resolution")
	# ~ res_data.GetXaxis().SetTitle("p_{T} (#mu^{#pm}) [GeV]")
	graphEOYBE.GetYaxis().SetTitleFont(42)
	graphEOYBE.GetYaxis().SetTitleSize(0.05)
	graphEOYBE.GetYaxis().SetTitleOffset(1.35)
	graphEOYBE.GetYaxis().SetLabelFont(42)
	graphEOYBE.GetYaxis().SetLabelSize(0.038)
	graphEOYBE.GetYaxis().SetRangeUser(0,.2)
	graphEOYBE.GetXaxis().SetTitleSize(0.0)
	graphEOYBE.GetXaxis().SetLabelSize(0.0)

	graphEOYBE.GetXaxis().SetRangeUser(0,6500)
	graphEOYBE.Draw("AP E0")

	graphULBE.Draw("samepe")
	graphEOYBE.SetMarkerSize(2)
	graphULBE.SetMarkerSize(2)
	graphEOYBE.SetLineWidth(2)
	graphULBE.SetLineWidth(2)
	graphEOYBE.SetMarkerStyle(20)
	graphULBE.SetMarkerStyle(21)
	graphULBE.SetLineColor(kRed)
	graphULBE.SetMarkerColor(kRed)



	latex = TLatex()
	# ~ latex.SetTextFont(42)
	# ~ latex.SetTextAlign(31)
	# ~ latex.SetTextSize(0.04)
	# ~ latex.SetNDC(True)
	latexCMS = TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.055)
	latexCMS.SetNDC(True)
	latexCMSExtra = TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(.03/0.7)
	latexCMSExtra.SetNDC(True) 

	latex.DrawLatexNDC(0.50, 0.96, "#scale[0.8]{#font[42]{       2017, 42.1 fb^{-1} (13 TeV)}}")

	cmsExtra = "Preliminary"
	latexCMS.DrawLatex(0.19,0.88,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))					


	leg = TLegend(0.5,0.65,0.95,0.90,"At least one muon |#eta| > 1.2","brNDC")
	leg.SetFillColor(10)
	leg.SetFillStyle(0)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)	
	leg.AddEntry(graphEOYBE,"EOY ReReco","lp")
	leg.AddEntry(graphULBE,"Legacy  ReReco","lp")

	leg.Draw()

	plotPad.RedrawAxis()


	ratioPad.cd()

	ratioBE.GetYaxis().SetTitle("#splitline{EOY ReReco/}{Legacy ReReco}")
	ratioBE.GetXaxis().SetNoExponent(0)
	ratioBE.GetXaxis().SetTitleFont(42)
	ratioBE.GetXaxis().SetTitleOffset(0.85)
	ratioBE.GetXaxis().SetTitleSize(0.2)
	ratioBE.GetXaxis().SetLabelColor(1)
	ratioBE.GetXaxis().SetLabelOffset(0.01)
	ratioBE.GetXaxis().SetLabelFont(42)
	ratioBE.GetXaxis().SetLabelSize(0.17)		
	ratioBE.GetXaxis().SetTitle("GEN dimuon mass (GeV)")
	ratioBE.GetYaxis().SetRangeUser(0.5,1.5)
	ratioBE.GetXaxis().SetRangeUser(0,6500)
	ratioBE.GetYaxis().SetTitleOffset(0.475)
	ratioBE.GetYaxis().SetTitleSize(0.12)
	ratioBE.GetYaxis().SetTitleFont(42)
	ratioBE.GetYaxis().SetLabelSize(0.14)    
	ratioBE.GetYaxis().SetLabelOffset(0.007)    
	ratioBE.GetYaxis().SetLabelFont(42)    
	ratioBE.GetYaxis().SetNdivisions(505)       
	
	ratioBE.SetMarkerColor(kRed)
	ratioBE.SetLineColor(kRed)
	ratioBE.SetLineWidth(2)
	ratioBE.SetMarkerStyle(20)
	ratioBE.SetMarkerSize(2)
	


	line = TLine(10,1,6500,1)

	line.SetLineColor(kBlack)
	line.SetLineStyle(kDashed)
	line.SetLineWidth(2)
	
	
	ratioBE.Draw("A P E")
	ratioBE.GetXaxis().SetRangeUser(0,6500)

	line.Draw()
	ratioBE.Draw("samePE")
	ratioPad.RedrawAxis()
	ratioBE.Draw("samepe")



	canv.Print("massResolutionCompareUL_%s_BE.pdf"%trackType)


#tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]
tracks = ["TunePNew"]
for trackType in tracks:
	compareMassRes(trackType)
