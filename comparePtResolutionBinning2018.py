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
	
def getGraph(result,label):
	
	ptda = result["ptda"]
	da_sig = result["data_sig"]
	da_sige = result["data_sige"]
	
	res_data  = TGraphAsymmErrors(len(ptda))
	res_data.SetName(label)
	for i,pt in enumerate(ptda):        
		print da_sig[i]
		res_data.SetPoint(i,ptda[i],da_sig[i])
		#~ print ptda[i],ptda[i]-ptbins[i],ptbins[i+1]-ptda[i]
		res_data.SetPointError(i,ptda[i]-ptbins[i],ptbins[i+1]-ptda[i],da_sige[i],da_sige[i])
	
	return res_data

def getRatio(result,result2,label):
	
	ptda = result["ptda"]
	da_sig = result["data_sig"]
	da_sige = result["data_sige"]
	ptmc = result2["ptda"]
	mc_sig = result2["data_sig"]
	mc_sige = result2["data_sige"]
	
	ratio  = TGraphAsymmErrors(len(ptda))
	ratio.SetName(label)
	for i,pt in enumerate(ptda):     
		#~ pt_e = (ptbins[i+1]-ptbins[i])/2   
		sig_e = (da_sig[i]/mc_sig[i])*math.sqrt((da_sige[i]/da_sig[i])**2+(mc_sige[i]/mc_sig[i])**2)
		ratio   .SetPoint(i,pt,da_sig[i]/mc_sig[i])
		ratio   .SetPointError(i,ptda[i]-ptbins[i],ptbins[i+1]-ptda[i],sig_e,sig_e)
	
	return ratio


def compareMassRes(trackType):
	
	fileDefaultBB = open("2018Boosteddefault/MassResolutionVsPt_%s_BB.pkl"%trackType)
	fileORBB = open("2018BoostedRebin2/MassResolutionVsPt_%s_BB.pkl"%trackType)
	fileNoBB = open("2018BoostedRebin4/MassResolutionVsPt_%s_BB.pkl"%trackType)
	fileDefaultBE = open("2018Boosteddefault/MassResolutionVsPt_%s_BE.pkl"%trackType)
	fileORBE = open("2018BoostedRebin2/MassResolutionVsPt_%s_BE.pkl"%trackType)
	fileNoBE = open("2018BoostedRebin4/MassResolutionVsPt_%s_BE.pkl"%trackType)

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

	xMax = 6
	if trackType == "Inner":
		xMax = 8
	if trackType == "Outer":
		xMax = 20

	plotPad.DrawFrame(52,0,800,xMax,";p_{T} [GeV]; Z peak resolution [GeV]")

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
	leg.AddEntry(graphDefaultBB,"0.5 GeV Binning","l")
	leg.AddEntry(graphORBB,"1 GeV Binning","l")
	leg.AddEntry(graphNoBB,"2 GeV Binning","l")

	leg.Draw()

	plotPad.RedrawAxis()


	ratioPad.cd()

	ratioORBB.SetLineColor(kRed)
	ratioNoBB.SetLineColor(kBlue)

	ratioPad.DrawFrame(52,0.5,800,1.5,";;ratio")

	ratioORBB.Draw("samepe")
	ratioNoBB.Draw("samepe")

	canv.Print("massResolutionVsPtBinning2018_%s_BB.pdf"%trackType)
	
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

	xMax = 6
	if trackType == "Inner":
		xMax = 8
	if trackType == "Outer":
		xMax = 20

	plotPad.DrawFrame(52,0,452,xMax,";p_{T} [GeV]; Z peak resolution [GeV]")

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
	leg.AddEntry(graphDefaultBE,"0.5 GeV Binning","l")
	leg.AddEntry(graphORBE,"1 GeV Binning","l")
	leg.AddEntry(graphNoBE,"2 GeV Binning","l")

	leg.Draw()

	plotPad.RedrawAxis()


	ratioPad.cd()

	ratioORBE.SetLineColor(kRed)
	ratioNoBE.SetLineColor(kBlue)

	ratioPad.DrawFrame(52,0.5,452,1.5,";;ratio")

	ratioORBE.Draw("samepe")
	ratioNoBE.Draw("samepe")


	canv.Print("massResolutionVsPtBinning2018_%s_BE.pdf"%trackType)
	
	



#~ tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]
tracks = ["TunePNew"]
for trackType in tracks:
	compareMassRes(trackType)
