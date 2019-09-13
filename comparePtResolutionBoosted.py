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



def comparePtRes(trackType):
	
	file2016BB = open("2016Boosteddefault/MassResolutionVsPt_%s_BB.pkl"%trackType)
	file2016BE = open("2016Boosteddefault/MassResolutionVsPt_%s_BE.pkl"%trackType)
	file2017BB = open("Boosteddefault/MassResolutionVsPt_%s_BB.pkl"%trackType)
	file2017BE = open("Boosteddefault/MassResolutionVsPt_%s_BE.pkl"%trackType)
	file2018BB = open("2018Boosteddefault/MassResolutionVsPt_%s_BB.pkl"%trackType)
	file2018BE = open("2018Boosteddefault/MassResolutionVsPt_%s_BE.pkl"%trackType)

	results2016BB = pickle.load(file2016BB)
	results2016BE = pickle.load(file2016BE)
	results2017BB = pickle.load(file2017BB)
	results2017BE = pickle.load(file2017BE)
	results2018BB = pickle.load(file2018BB)
	results2018BE = pickle.load(file2018BE)

	graph2016BB = getGraph(results2016BB,"2016BB")
	graph2016BE = getGraph(results2016BE,"2016BE")
	graph2017BB = getGraph(results2017BB,"2017BB")
	graph2017BE = getGraph(results2017BE,"2017BE")
	graph2018BB = getGraph(results2018BB,"2018BB")
	graph2018BE = getGraph(results2018BE,"2018BE")
		
	
	ratioBB = 	getRatio(results2016BB,results2017BB,"ratioBB")
	ratioBE = 	getRatio(results2016BE,results2017BE,"ratioBE")
	ratioBB18 = getRatio(results2016BB,results2018BB,"ratioBB18")
	ratioBE18 = getRatio(results2016BE,results2018BE,"ratioBE18")



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

	xMax = 6
	if trackType == "Inner":
		xMax = 8
	if trackType == "Outer":
		xMax = 20

	plotPad.DrawFrame(52,0,800,xMax,";p_{T} [GeV]; Z peak resolution [GeV]")

	graph2016BB.Draw("samepe")
	graph2017BB.Draw("samepe")
	graph2018BB.Draw("samepe")
	graph2017BB.SetLineColor(kRed)
	graph2017BB.SetMarkerColor(kRed)
	graph2018BB.SetLineColor(kBlue)
	graph2018BB.SetMarkerColor(kBlue)

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


	ratioPad.cd()

	ratioBB.SetLineColor(kRed)
	ratioBB18.SetLineColor(kBlue)
	ratioBB.SetMarkerColor(kRed)
	ratioBB18.SetMarkerColor(kBlue)

	ratioPad.DrawFrame(52,0.5,800,1.5,";;ratio")

	ratioBB.Draw("samepe")
	ratioBB18.Draw("samepe")

	l = TLine(52,1,800,1)
	l.SetLineStyle(kDashed)
	l.Draw()
	
	canv.Print("PtResolutionBoostedCompare_%s_BB.pdf"%trackType)
	
	
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

	xMax = 6
	if trackType == "Inner":
		xMax = 8
	if trackType == "Outer":
		xMax = 20

	plotPad.DrawFrame(52,0,452,xMax,";p_{T} [GeV]; Z peak resolution [GeV]")

	graph2016BE.Draw("samepe")
	graph2017BE.Draw("samepe")
	graph2018BE.Draw("samepe")
	graph2017BE.SetLineColor(kRed)
	graph2017BE.SetMarkerColor(kRed)
	graph2018BE.SetLineColor(kBlue)
	graph2018BE.SetMarkerColor(kBlue)

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


	ratioPad.cd()

	ratioBE.SetLineColor(kRed)
	ratioBE18.SetLineColor(kBlue)
	ratioBE.SetMarkerColor(kRed)
	ratioBE18.SetMarkerColor(kBlue)

	ratioPad.DrawFrame(52,0.5,452,1.5,";;ratio")

	l = TLine(52,1,452,1)
	l.SetLineStyle(kDashed)
	l.Draw()

	ratioBE.Draw("samepe")
	ratioBE18.Draw("samepe")


	canv.Print("PtResolutionBoostedCompare_%s_BE.pdf"%trackType)


#tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]
tracks = ["TunePNew"]
for trackType in tracks:
	comparePtRes(trackType)
