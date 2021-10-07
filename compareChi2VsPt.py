from ROOT import TGraphAsymmErrors, TCanvas, TPad, TGraphErrors, gStyle, kRed, kBlue, kBlack, TLatex, TLegend, TLine, kDashed
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
	
def getRatio(result,result2,label,Data=False):
	
	
	ptda = result["ptda"]
	ptda2   = result2["ptda"]

	if Data:
		sigma = result["da_nChi2"]
		sigma2 = result2["da_nChi2"]
	else:	
		sigma = result["mc_nChi2"]
		sigma2 = result2["mc_nChi2"]
	
	print (sigma)
	print (sigma2)

	ratio  = TGraphAsymmErrors(len(ptda))
	ratio.SetName(label)
	for i,pt in enumerate(ptda):     
		ratio   .SetPoint(i,pt,sigma[i]/sigma2[i])
		ratio   .SetPointError(i,ptda[i]-ptbins[i],ptbins[i+1]-ptda[i],0,0)
	
	return ratio
	

def getGraph(result,label,Data=False):
	
	ptda = result["ptda"]

	if Data:
		sigma = result["da_nChi2"]
	else:	
		sigma = result["mc_nChi2"]
	sigmaErr = 0
	
	res  = TGraphAsymmErrors(len(ptda))
	res.SetName(label)
	for i,pt in enumerate(ptda):     
		res.SetPoint(i,pt,sigma[i])
		res.SetPointError(i,ptda[i]-ptbins[i],ptbins[i+1]-ptda[i],0,0)
	
	return res


def compareMassRes(trackType):
	
	fileCB = open("BoosteddefaultLeadingCB/MassResolutionVsPt_%s_BE16.pkl"%trackType,"rb")
	fileDCB = open("BoosteddefaultLeading/MassResolutionVsPt_%s_BE16.pkl"%trackType,"rb")
	fileCruijff = open("BoosteddefaultLeadingCruijff/MassResolutionVsPt_%s_BE16.pkl"%trackType,"rb")

	resultsCB = pickle.load(fileCB)
	resultsDCB = pickle.load(fileDCB)
	resultsCruijff = pickle.load(fileCruijff)

	graphCB = getGraph(resultsCB,"CB",Data=True)
	graphDCB = getGraph(resultsDCB,"DCB",Data=True)
	graphCruijff = getGraph(resultsCruijff,"Cruijff",Data=True)
		
	
	ratioCB = 	getRatio(resultsCB,resultsDCB,"ratioCB",Data=True)
	ratioCruijff = 	getRatio(resultsCruijff,resultsDCB,"ratioCruijff",Data=True)



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

	xMax = 20
	if trackType == "Inner":
		xMax = 10
	if trackType == "Outer":
		xMax = 20

	plotPad.DrawFrame(0,0,452,xMax,";p_{T} [GeV]; #chi^{2}/N_{dof}")

	graphCB.Draw("samepe")
	graphDCB.Draw("samepe")
	graphCruijff.Draw("samepe")
	graphDCB.SetLineColor(kRed)
	graphDCB.SetMarkerColor(kRed)
	graphCruijff.SetLineColor(kBlue)
	graphCruijff.SetMarkerColor(kBlue)

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
	leg.AddEntry(graphCB,"Single-Sided CB","l")
	leg.AddEntry(graphDCB,"Double-Sided CB","l")
	leg.AddEntry(graphCruijff,"Cruijff","l")

	leg.Draw()

	plotPad.RedrawAxis()


	#~ ratioPad.cd()

	#~ ratioBB.SetLineColor(kRed)

	#~ ratioPad.DrawFrame(0,0.5,6000,1.5,";;ratio")

	#~ ratioBB.Draw("samepe")


	canv.Print("chi2CompareVsPt_%s_BE16.pdf"%trackType)
	


#~ tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]
tracks = ["TunePNew"]
for trackType in tracks:
	compareMassRes(trackType)
