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


def graph(src,name):
	
	f = open("%s/%s"%(src,name))


	results = pickle.load(f)

	graph = getGraph(results,name)
		
	return graph



tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]

sources = {"2016":"default2016PSplit","2017":"defaultPSplit","2018":"default2018PSplit"}
	
for src, path in sources.iteritems():
	
	for rap in ["B","O","E"]:

		graphInner    = graph(path,"PResolutionVsP_%s_%s.pkl"%("Inner",rap))
		graphOuter    = graph(path,"PResolutionVsP_%s_%s.pkl"%("Outer",rap))
		graphGlobal   = graph(path,"PResolutionVsP_%s_%s.pkl"%("Global",rap))
		graphTPFMS    = graph(path,"PResolutionVsP_%s_%s.pkl"%("TPFMS",rap))
		graphPicky    = graph(path,"PResolutionVsP_%s_%s.pkl"%("Picky",rap))
		graphDYT      = graph(path,"PResolutionVsP_%s_%s.pkl"%("DYT",rap))
		graphTunePNew = graph(path,"PResolutionVsP_%s_%s.pkl"%("TunePNew",rap))
		
		

		canv = TCanvas("c1","c1",800,800)

		plotPad = TPad("plotPad","plotPad",0,0,1,1)
		style = setTDRStyle()
		gStyle.SetOptStat(0)
		plotPad.UseCurrentStyle()
		plotPad.Draw()	
		plotPad.cd()
		plotPad.SetGrid()
		gStyle.SetTitleXOffset(1.45)
		gStyle.SetTitleYOffset(1.55)

		#~ xMax = 0.08
		#~ if trackType == "Inner":
			#~ xMax = 0.2
		#~ if trackType == "Outer":
		xMax = 0.125

		plotPad.DrawFrame(0,0,3100,xMax,";p^{#mu} [GeV]; p^{#mu} resolution")

		graphTunePNew.SetLineColor(kRed)
		graphGlobal.SetLineColor(kGreen+2)
		graphOuter.SetLineColor(kYellow+2)
		graphInner.SetLineColor(kOrange)
		graphPicky.SetLineColor(kBlue)
		graphTPFMS.SetLineColor(kOrange)
		graphDYT.SetLineColor(kMagenta)

		graphTunePNew.SetMarkerColor(kRed)
		graphGlobal.SetMarkerColor(kGreen+2)
		graphOuter.SetMarkerColor(kYellow+2)
		graphInner.SetMarkerColor(kOrange)
		graphPicky.SetMarkerColor(kBlue)
		graphTPFMS.SetMarkerColor(kOrange)
		graphDYT.SetMarkerColor(kMagenta)
		graphTunePNew.SetMarkerStyle(20)
		graphGlobal.SetMarkerStyle(20)
		graphOuter.SetMarkerStyle(20)
		graphInner.SetMarkerStyle(20)
		graphPicky.SetMarkerStyle(20)
		graphTPFMS.SetMarkerStyle(20)
		graphDYT.SetMarkerStyle(20)

		graphDYT.Draw("samepe")
		graphTPFMS.Draw("samepe")
		graphGlobal.Draw("samepe")
		graphPicky.Draw("samepe")
		graphTunePNew.Draw("samepe")
		
		#~ graphInner.Draw("samepe")
		#~ graphOuter.Draw("samepe")

		

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

		cmsExtra = "#splitline{Simulation}{Preliminary}"
		latexCMS.DrawLatex(0.19,0.88,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.83	
		else:
			yLabelPos = 0.84	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))			


		leg = TLegend(0.42, 0.7, 0.95, 0.91,"%s %s"%(src,rap),"brNDC")
		leg.SetNColumns(2)
		leg.SetFillColor(10)
		leg.SetFillStyle(0)
		leg.SetLineColor(10)
		leg.SetShadowColor(0)
		leg.SetBorderSize(1)		
		#~ leg.AddEntry(graphOuter,"Standalone","l")
		#~ leg.AddEntry(graphInner,"Inner Track","l")
		leg.AddEntry(graphGlobal,"Global","l")
		leg.AddEntry(graphTPFMS,"TPFMS","l")
		leg.AddEntry(graphPicky,"Picky","l")
		leg.AddEntry(graphDYT,"DYT","l")
		leg.AddEntry(graphTunePNew,"Tune P","l")

		leg.Draw()

		plotPad.RedrawAxis()

		canv.Print("pResolutionCompare_%s_%s.pdf"%(src,rap))
	
	




