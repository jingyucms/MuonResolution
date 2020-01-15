#!/usr/bin/python

# import ROOT in batch mode
import sys,os
import argparse
import math
import pickle
import subprocess
from setTDRStyle import setTDRStyle

oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
#~ import ROOT
from ROOT import TF1, TCanvas, gROOT, gStyle, TFile, TH2F, TH1, kFALSE, TH1D, gSystem, RooWorkspace, RooRealVar, RooCmdArg, RooDataHist, RooArgList, TPad, TLegend, TLatex, TGraphAsymmErrors, TGraph, TGraphErrors, kBlack, kRed, kBlue, TLine
from ROOT import RooDataHist, RooBreitWigner, RooFFTConvPdf, RooFit
import ROOT
from ROOT import *
gROOT.SetBatch(True)
sys.argv = oldargv

ptbins = [52, 72, 100, 152, 200, 300, 452, 800]

gROOT.LoadMacro("cruijff.C+")
gROOT.LoadMacro("doubleCB.C+")

rebinFactor = 1
xLow = 75
xHigh = 105


sampleLists  = {

	"2016Inclusive":["ana_datamc_DYInclusive2016.root"],
	"2017Inclusive":["ana_datamc_DYInclusive2017.root"],
	"2016MassBinned":["dileptonAna_resolution_2016_dy50to120.root","dileptonAna_resolution_2016_dy120to200.root","dileptonAna_resolution_2016_dy200to400.root","dileptonAna_resolution_2016_dy400to800.root","dileptonAna_resolution_2016_dy800to1400.root","dileptonAna_resolution_2016_dy1400to2300.root","dileptonAna_resolution_2016_dy2300to3500.root","dileptonAna_resolution_2016_dy3500to4500.root","dileptonAna_resolution_2016_dy4500to6000.root","dileptonAna_resolution_2016_dy6000toInf.root"],
	"2017MassBinned":["dileptonAna_resolution_dy50to120_2017.root","dileptonAna_resolution_dy120to200_2017.root","dileptonAna_resolution_dy200to400_2017.root","dileptonAna_resolution_dy400to800_2017.root","dileptonAna_resolution_dy800to1400_2017.root","dileptonAna_resolution_dy1400to2300_2017.root","dileptonAna_resolution_dy2300to3500_2017.root","dileptonAna_resolution_dy3500to4500_2017.root","dileptonAna_resolution_dy4500to6000_2017.root","dileptonAna_resolution_dy6000toInf_2017.root"],
	"2018MassBinned":["dileptonAna_resolution_2018_dy50to120.root","dileptonAna_resolution_2018_dy120to200.root","dileptonAna_resolution_2018_dy200to400.root","dileptonAna_resolution_2018_dy400to800.root","dileptonAna_resolution_2018_dy800to1400.root","dileptonAna_resolution_2017_dy1400to2300.root","dileptonAna_resolution_2018_dy2300to3500.root","dileptonAna_resolution_2017_dy3500to4500.root","dileptonAna_resolution_2018_dy4500to6000.root","dileptonAna_resolution_2017_dy6000toInf.root"],
	"2016PtBinned":["dileptonAna_resolution_2016_dyInclusive50.root","dileptonAna_resolution_2016_dyPt50To100.root","dileptonAna_resolution_2016_dyPt100To250.root","dileptonAna_resolution_2016_dyPt250To400.root","dileptonAna_resolution_2016_dyPt400To600.root","dileptonAna_resolution_2016_dyPt650ToInf.root"],
	"2017PtBinned":[#"dileptonAna_resolution_2016_dyInclusive50.root",
"dileptonAna_resolution_dyPt50To150_1Jet_2017.root","dileptonAna_resolution_dyPt50To150_2Jets_2017.root","dileptonAna_resolution_dyPt150To250_1Jet_2017.root","dileptonAna_resolution_dyPt150To250_2Jets_2017.root","dileptonAna_resolution_dyPt250To400_1Jet_2017.root","dileptonAna_resolution_dyPt250To400_2Jets_2017.root","dileptonAna_resolution_dyPt400ToInf_1Jet_2017.root","dileptonAna_resolution_dyPt400ToInf_2Jets_2017.root","dileptonAna_resolution_dy_3Jets_2017.root","dileptonAna_resolution_dy_4Jets_2017.root"],
#	"2017PtBinned":["dileptonAna_resolution_dyPt400ToInf_1Jet_2017.root","dileptonAna_resolution_dyPt400ToInf_2Jets_2017.root"]
	"2018PtBinned":["dyPt150to250_1Jets_2018.root", "dyPt250to400_1Jets_2018.root", "dyPt400toInf_1Jets_2018.root", "dyPt50to150_1Jets_2018.root", "dyPt_3Jets_2018.root", "dyPt150to250_2Jets_2018.root", "dyPt250to400_2Jets_2018.root", "dyPt400toInf_2Jets_2018.root", "dyPt50to150_2Jets_2018.root", "dyPt_4Jets_2018.root"],

}

xSecs = {

	"2016Inclusive": [ 1921.8 ],
	"2017Inclusive": [ 1921.8 ],
	"2016MassBinned": [1975,19.32,2.731,0.241,1.678e-2,1.39e-3,0.8948e-4,0.4135e-5,4.56e-7,2.06e-8],
	"2017MassBinned": [1975,19.32,2.731,0.241,1.678e-2,1.39e-3,0.8948e-4,0.4135e-5,4.56e-7,2.06e-8],
	"2016PtBinned": [1921.8,363.81428,84.014804,3.228256512,0.436041144,0.040981055],
	"2017PtBinned": [1921.8,316.6,169.6,9.543,15.65,1.098,2.737,0.1193,0.4477,111.5,44.03],
#	"2017PtBinned": [2.536,2.536]	
	"2018PtBinned": [9.543, 1.098, 0.1193, 316.6, 111.5, 15.65, 2.737, 0.4477, 169.6, 44.03],
}#    
#    resBB.SetMarkerStyle(22)
#    resBB.SetMarkerColor(kRed)
#    resBB.SetLineColor(kRed)
#    resBB.SetFillColor(0)
#    resBB.SetTitle("Dimuon mass resolution vs pT")
#    resBB.GetYaxis().SetTitle("Dimuon Mass Resolution")
#    resBB.GetYaxis().SetTitleOffset(1.5)
#    resBB.GetXaxis().SetTitle("p_T (#mu^{#pm}) [GeV]")
#    resBB.GetYaxis().SetRangeUser(0,.2)
#    resBB.GetXaxis().SetRangeUser(0,5000)
#    resBB.GetFunction("fun").SetLineColor(kRed+1)
#    resBB.Draw("AP E0")
#    
#    resBE.SetMarkerStyle(22)
#    resBE.SetMarkerColor(kBlue+1)
#    resBE.SetLineColor(kBlue+1)
#    resBE.SetFillColor(0)
#    resBE.SetTitle("Dimuon mass resolution vs mass")
#    resBE.GetYaxis().SetTitle("Dimuon Mass Resolution")
#    resBE.GetYaxis().SetTitleOffset(1.5)
#    resBE.GetXaxis().SetTitle("p_T (#mu^{#pm}) [GeV]")
#    resBE.GetYaxis().SetRangeUser(0,.2)
#    resBE.GetXaxis().SetRangeUser(0,5000)
#    resBE.GetFunction("fun").SetLineColor(kBlue+2)
#    resBE.Draw("PE0 SAME")
#        
#    leg = TLegend(.35,.7,.50,.80,"","brNDC")
#    leg.AddEntry(resBB,"BB")
#    leg.AddEntry(resBE,"BE")
#    leg.SetTextFont(42)
#    leg.SetBorderSize(0)
#    leg.SetTextSize(.02)
#    leg.Draw("SAME")
#    
#    res.SetGrid()
#    saveas = "/MassResolutionVsPt_2CAT"
#    res.SaveAs(output+saveas+".png")
#    res.SaveAs(output+saveas+".pdf")
#    res.SaveAs(output+saveas+".root")
#    res.SaveAs(output+saveas+".C")



def getBinRange(histo,mlow,mhigh,reg="BB"):
	ymin =  0
	ymax = -1
	nbins = histo.GetNbinsY()
	for bin in range(nbins):
		if mlow==histo.GetYaxis().GetBinLowEdge(bin): 
			ymin = bin
		if mhigh==histo.GetYaxis().GetBinLowEdge(bin):
			ymax = bin

	if mhigh==ptbins[len(ptbins)-1]: ymax=-1
	if mhigh==ptbins[len(ptbins)-2] and "BE" in reg: ymax=-1
	return ymin,ymax

def loadHistos(inputdata,inputMC,region,weights,weights2,trackType,mcIsData,dataIsMC):
	_fileDATA = []
	if not dataIsMC:
		_fileDATA.append(TFile(inputdata))
	else:
		for data in inputdata:
			_fileDATA.append(TFile(data))
	_fileMC   = []
	if mcIsData:
		_fileMC.append(TFile(inputMC))
	else: 
		for mc in inputMC:
			_fileMC.append(TFile(mc))
	
	hdata = TH2F()
	hmc   = TH2F()
	
	hdata.SetDirectory(0)
	hmc  .SetDirectory(0)
	TH1.AddDirectory(kFALSE)
	
	reg = ""
	if   ("BB" in region or "barrel" in region):  reg = "_BB"
	elif ("BE" in region or "endcap" in region):  reg = "_BE"
	
	if not dataIsMC:
		hdata = _fileDATA[0].Get("Our2017MuonsPlusMuonsMinus%sResolution/DileptonMass_2d_vsPt%s" %(trackType,reg)).Clone()
	else:	
		for k,data in enumerate(inputdata):
			tmp   = _fileDATA[k].Get("Our2017MuonsPlusMuonsMinus%sResolution/DileptonMass_2d_vsPt%s" %(trackType,reg)).Clone()
			if k==0 and not weights2: 
				hdata = tmp
			elif k==0 and weights2:
				nEvents = _fileDATA[k].Get("EventCounter/Events").GetBinContent(1)
				print ("Weighting with %s " %(40000*weights2[k]/nEvents))
				tmp.Scale(40000*weights2[k]/nEvents)
				hdata = tmp
			elif not weights2:
				hdata.Add(tmp)
			else: 
				nEvents = _fileDATA[k].Get("EventCounter/Events").GetBinContent(1)			
				print ("Weighting with %s " %(40000*weights2[k]/nEvents))
				tmp.Scale(40000*weights2[k]/nEvents)
				hdata.Add(tmp)

	if mcIsData:
		hmc = _fileMC[0].Get("Our2017MuonsPlusMuonsMinus%sResolution/DileptonMass_2d_vsPt%s" %(trackType,reg)).Clone()
	else:	
		for k,mc in enumerate(inputMC):
			#print mc
			tmp   = _fileMC[k].Get("Our2017MuonsPlusMuonsMinus%sResolution/DileptonMass_2d_vsPt%s" %(trackType,reg)).Clone()
			
			if k==0 and not weights: 
				hmc = tmp
			elif k==0 and weights:
				nEvents = _fileMC[k].Get("EventCounter/Events").GetBinContent(1)
				print ("Weighting with %s " %(40000*weights[k]/nEvents))
				tmp.Scale(40000*weights[k]/nEvents)
				hmc = tmp
			elif not weights:
				hmc.Add(tmp)
			else: 
				nEvents = _fileMC[k].Get("EventCounter/Events").GetBinContent(1)			
				print ("Weighting with %s " %(40000*weights[k]/nEvents))
				tmp.Scale(40000*weights[k]/nEvents)
				hmc.Add(tmp)
		
	for f in _fileDATA:
		f.Close()
	for f in _fileMC:
		f.Close()

	if "BB" in reg: 
		data = [TH1D() for x in range(len(ptbins)-1)]
		mc   = [TH1D() for x in range(len(ptbins)-1)]
		ptda = [0 for x in range(len(ptbins)-1)]
		ptmc = [0 for x in range(len(ptbins)-1)]
	else:
		data = [TH1D() for x in range(len(ptbins)-2)]
		mc   = [TH1D() for x in range(len(ptbins)-2)]
		ptda = [0 for x in range(len(ptbins)-2)]
		ptmc = [0 for x in range(len(ptbins)-2)]

	for h in data:
		h.SetDirectory(0)
		TH1.AddDirectory(kFALSE)
	for h in mc:
		h.SetDirectory(0)
		TH1.AddDirectory(kFALSE)
	
	for i,h in enumerate(data):        
		ymin,ymax=getBinRange(hdata,ptbins[i],ptbins[i+1],reg)
		hdata.GetYaxis().SetRangeUser(ptbins[i],ptbins[i+1])
		hmc.GetYaxis().SetRangeUser(ptbins[i],ptbins[i+1])
		ptda[i] = hdata.GetMean(2)
		ptmc[i] = hmc.GetMean(2)
		hdata.GetYaxis().SetRange()
		hmc  .GetYaxis().SetRange()

		data[i] = hdata.ProjectionX("datapy%s%s" %(ptbins[i],region),ymin,ymax)
		mc  [i] = hmc  .ProjectionX("mcpy%s%s" %(ptbins[i],region)  ,ymin,ymax)
		
		#~ data[i].Rebin(1)
		#~ mc  [i].Rebin(1)
		
		if (data[i].Integral() < 1500): 
			data[i].Rebin(6)
		elif (data[i].Integral() < 2500): 
			data[i].Rebin(4)
		else:
			data[i].Rebin(rebinFactor)


		if (mc[i].Integral() < 1500): 
			mc[i].Rebin(6)
		elif (mc[i].Integral() < 2500): 
			mc[i].Rebin(4)
		else:
			mc  [i].Rebin(rebinFactor)

		#~ if mcIsData:
			#~ mc[i].Rebin(2)
		#~ else:	
			#~ mc[i].Rebin(2)
		
#        if (ptbins[i]==200 or ptbins[i]==152) and "BE" in region:
#            mc[i].Rebin(2)

	return data,mc,ptda,ptmc

def doFit(hist,output,rap="BB",flavour="DATA",trackType="TunePNew",funct="doubleCB"):

	
	sig    = []
	sige   = []
	meanList   = []
	meanListe  = []
	nChi2  = []
	gSystem.Load("./RooCruijff_cxx.so")
	gSystem.Load("./RooDCBShape_cxx.so")
	for i,h in enumerate(hist):
		ws = RooWorkspace("tempWS")

		mass = RooRealVar('mass','mass',91, xLow, xHigh )
		getattr(ws,'import')(mass,RooCmdArg())			
		dataHist = RooDataHist("hist","hist",RooArgList(ws.var("mass")),h)
		getattr(ws,'import')(dataHist,RooCmdArg())

		ws.writeToFile("tmpWorkspace.root")
		
		subprocess.call(["python","fitCapsule.py",output,rap,flavour,trackType,funct,"%d"%xLow,"%d"%xHigh,"%d"%rebinFactor,"%d"%i])
		
		returnFile = TFile("tmpWorkspaceReturn.root","OPEN")
		wsReturn = returnFile.Get("tempWS")
		
		sig.append(wsReturn.var("Sig").getVal())
		sige.append(wsReturn.var("Sige").getVal())
		meanList.append(wsReturn.var("Mean").getVal())
		meanListe.append(wsReturn.var("Meane").getVal())
		nChi2.append(wsReturn.var("chi2").getVal()/wsReturn.var("nDOF").getVal())


	return meanList,meanListe,sig,sige, nChi2	
	
def drawMassRes(data,mc,output,rapidity,ptda,ptmc,trackType,funct,mcIsData,dataIsMC):
	style = setTDRStyle()
	
	pt_e = [0 for x in range(len(data))]
	pt_x = [0 for x in range(len(data))]
	for i,pt in enumerate(pt_x):
		pt_x[i] = ptbins[i]+(ptbins[i+1]-ptbins[i])/2.
		pt_e[i] = (ptbins[i+1]-ptbins[i])/2.
	if dataIsMC:
		(da_mean,da_meane,da_sig,da_sige, da_nChi2) = doFit(data,output,rapidity,"MC2",trackType,funct)
	else:	
		(da_mean,da_meane,da_sig,da_sige, da_nChi2) = doFit(data,output,rapidity,"DATA",trackType,funct)
	if mcIsData:	
		(mc_mean,mc_meane,mc_sig,mc_sige, mc_nChi2) = doFit(mc  ,output,rapidity,"DATA2",trackType,funct)
	else:
		(mc_mean,mc_meane,mc_sig,mc_sige, mc_nChi2) = doFit(mc  ,output,rapidity,"MC",trackType,funct)
	result = {}
	result["data_mean"] = da_mean
	result["data_meane"] = da_meane
	result["data_sig"] = da_sig
	result["data_sige"] = da_sige
	result["mc_mean"] = mc_mean
	result["mc_meane"] = mc_meane
	result["mc_sig"] = mc_sig
	result["mc_sige"] = mc_sige
	result["ptda"] = ptda
	result["ptmc"] = ptmc
	result["da_nChi2"] = da_nChi2
	result["mc_nChi2"] = mc_nChi2



	pklFile = open(output+"/MassResolutionVsPt_%s_%s.pkl" %(trackType,rapidity),"wb")
	pickle.dump(result,pklFile)
	pklFile.close()
	
	
	c2 = TCanvas("c2","c2",700,700)
	c2.cd()

	# Upper plot will be in pad1
	pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
	pad1.SetGrid()        # Vertical grid
	pad1.SetBottomMargin(0.1)
	pad1.Draw()             # Draw the upper pad: pad1
	pad1.cd()               # pad1 becomes the current pad
	pad1.SetTicks()
	
	res_data  = TGraphAsymmErrors()
	res_data.SetName("res_data")
	res_mc    = TGraphAsymmErrors()
	res_mc  .SetName("res_mc")
	ratio     = TGraphErrors()
	ratio   .SetName("ratio")
	#~ print len(pt_x)
	for i,pt in enumerate(pt_x):        
		res_data.SetPoint(i,ptda[i],da_sig[i])
		res_data.SetPointError(i,ptda[i]-ptbins[i],ptbins[i+1]-ptda[i],da_sige[i],da_sige[i])
		res_mc  .SetPoint(i,ptmc[i],mc_sig[i])
		res_mc  .SetPointError(i,ptmc[i]-ptbins[i],ptbins[i+1]-ptmc[i],mc_sige[i],mc_sige[i])
		if mc_sig[i] > 0:
			ratio   .SetPoint(i,pt,da_sig[i]/mc_sig[i])
			ratio   .SetPointError(i,pt_e[i],(da_sig[i]/mc_sig[i])*math.sqrt((da_sige[i]/da_sig[i])**2+(mc_sige[i]/mc_sig[i])**2))
	res_data.SetMarkerStyle(22)
	res_data.SetMarkerColor(kBlack)
	res_data.SetLineColor(kBlack)
	res_data.SetFillColor(0)
	res_data.SetTitle("Dimuon mass resolution vs pT for %s tracks"%trackType)
	res_data.GetYaxis().SetTitle("Mass resolution at Z peak [GeV]")
	res_data.GetXaxis().SetTitle("p_{T} (#mu^{#pm}) [GeV]")
	res_data.GetYaxis().SetTitleOffset(1.2)
	res_data.GetYaxis().SetRangeUser(0.,6.)
	if trackType == "Outer":
		res_data.GetYaxis().SetRangeUser(1.,20.)
	res_data.GetXaxis().SetRangeUser(ptbins[0],ptbins[len(ptda)])
	res_data.Draw("AP E0")
	res_mc.SetMarkerStyle(22)
	res_mc.SetMarkerColor(kRed)
	res_mc.SetLineColor(kRed)
	res_mc.SetFillColor(0)
	res_mc.SetTitle("Dimuon mass resolution vs pT for %s tracks"%trackType)
	res_mc.GetYaxis().SetTitle("Mass resolution at Z peak [GeV]")
	res_mc.GetXaxis().SetTitle("p_{T} (#mu^{#pm}) [GeV]")
	res_mc.GetYaxis().SetTitleOffset(1.5)
	res_mc.Draw("P E0 SAME")
	if rapidity == "BB": leg = TLegend(0.25,0.6,0.50,0.80,"both muons |#eta| < 1.2","brNDC")
	else: leg = TLegend(0.25,0.6,0.5,0.8,"at least one muon |#eta| > 1.2","brNDC")
	if mcIsData:
		leg.AddEntry(res_data,"DATA 2017")
		leg.AddEntry(res_mc,"DATA 2016")
	elif dataIsMC:
		leg.AddEntry(res_data,"MC 2017")
		leg.AddEntry(res_mc,"MC 2016")		
	else:
		leg.AddEntry(res_data,"DATA","p")
		leg.AddEntry(res_mc,"Simulation")
	
	leg.SetTextFont(42)
	leg.SetBorderSize(0)
	leg.SetTextSize(.04)
	leg.Draw("SAME")
	latex = TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexCMS = TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.055/0.7)
	latexCMS.SetNDC(True)
	latexCMSExtra = TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.03/0.7)
	latexCMSExtra.SetNDC(True)
	
	latex.DrawLatex(0.95, 0.96, "(13 TeV)")
	
	cmsExtra = "Preliminary" 
	latexCMS.DrawLatex(0.78,0.88,"CMS")
	yLabelPos = 0.84
	latexCMSExtra.DrawLatex(0.78,yLabelPos,"%s"%(cmsExtra))
	c2.cd()          # Go back to the main canvas before defining pad2
	pad2 = TPad("pad2", "pad2",0, 0.1, 1, 0.30)    
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	pad2.SetGrid()
	pad2.Draw()
	pad2.cd()
	pad2.SetTicks()
	ratio.SetMarkerColor(kBlue-4)
	ratio.SetFillColor(kBlue-4 )
	ratio.SetTitle("")
	ratio.GetYaxis().SetTitle("Data/MC")
	if mcIsData:
		ratio.GetYaxis().SetTitle("Data 2017 / Data 2016")
	elif dataIsMC:
		ratio.GetYaxis().SetTitle("MC 2017 / MC 2016")
	ratio.GetXaxis().SetTitle("p_{T} (#mu^{#pm}) [GeV]")
	ratio.GetYaxis().SetRangeUser(0.5,1.5)
	ratio.GetXaxis().SetRangeUser(ptbins[0],ptbins[len(ptda)])
	ratio.GetYaxis().SetTitleOffset(0.50)
	ratio.GetYaxis().SetTitleSize(0.14)
	ratio.GetYaxis().SetLabelSize(0.14)    
	ratio.GetYaxis().SetNdivisions(506)    
	ratio.GetXaxis().SetTitleSize(0.12)
	ratio.GetXaxis().SetTitleOffset(1.2)
	ratio.GetXaxis().SetLabelSize(0.20)
	ratio.Draw("A P E2")
	pad2.Update()
	line = TLine(ptbins[0],1,ptbins[len(ptda)],1)

	line.SetLineColor(kBlue+1)
	line.SetLineWidth(2)
	line.Draw()
	saveas = "/MassResolutionVsPt_%s_%s" %(trackType,rapidity)
	c2.SaveAs(output+saveas+".png")
	c2.SaveAs(output+saveas+".pdf")
	c2.SaveAs(output+saveas+".root")
	c2.SaveAs(output+saveas+".C")
	

	
def makeMassRes(inputDATA,inputMC,output,weights,weights2,trackType,funct,mcIsData,dataIsMC):
	style = setTDRStyle()
	gStyle.SetTitleYOffset(1.45)
	gStyle.SetTitleXOffset(1.45)
	gStyle.SetOptFit(0)
	gStyle.SetStatX(.9)
	gStyle.SetStatY(.9)
	
	(data_B,mc_B,ptdaB,ptmcB) = loadHistos(inputDATA,inputMC,"BB",weights,weights2,trackType,mcIsData,dataIsMC)
	(data_E,mc_E,ptdaE,ptmcE) = loadHistos(inputDATA,inputMC,"BE",weights,weights2,trackType,mcIsData,dataIsMC)

	drawMassRes(data_B,mc_B,output,"BB",ptdaB,ptmcB,trackType,funct,mcIsData,dataIsMC)
	drawMassRes(data_E,mc_E,output,"BE",ptdaE,ptmcE,trackType,funct,mcIsData,dataIsMC)
	
	
		 
#### ========= MAIN =======================
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(usage="makeMassRes.py [options]",description="Compute mass resolution",
									 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument("--iDATA", dest="inputDATA",default="", help='Input filename')
	parser.add_argument("--iDATA2", dest="inputDATA2",default="", help='Input filename 2')
#    parser.add_argument("--iMC", dest="inputMC",default="", help='Input filename')
	parser.add_argument("--iMC", dest="inputMC", type=str, help='input MC name',default = "")
	parser.add_argument("--iMC2", dest="inputMC2", type=str, help='input MC name 2',default = "")
	parser.add_argument("--weight",type=bool, help='Reweight MC samples to xsec',default=False)
	parser.add_argument("-f","--funct",dest="funct", default="cruijff", help='function used')	
	#~ parser.add_argument("--weight",type=bool, help='Reweight MC samples to xsec',default=False)
	parser.add_argument("-o","--ofolder",dest="output", default="plots/", help='folder name to store results')
	parser.add_argument("-t","--track",dest="track", default="TunePNew", help='which track to use')
	parser.add_argument("--xMin", dest ="xMin", type=float, help='lower x limit', default = 75)
	parser.add_argument("--xMax",dest = "xMax", type=float, help='lower x limit', default = 105)
	parser.add_argument("--rebin",dest = "rebin", type=int, help='rebin factor', default = 1)	
	args = parser.parse_args()
	
	if not os.path.exists(args.output):
		os.makedirs(args.output);
		if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+args.output)
	
	inputDATA = args.inputDATA
	inputDATA2 = args.inputDATA2
	mcIsData = False
	dataIsMC = False
	if args.inputMC == "":
		inputMC = inputDATA2
		mcIsData = True
	else:
		inputMC   = sampleLists[args.inputMC]
	if inputDATA == "":
		inputDATA = sampleLists[args.inputMC2]
		dataIsMC = True
		
	
	output=args.output

	rebinFactor = args.rebin
	xLow = args.xMin
	xHigh = args.xMax

		
	print ("Running on: %s %s with 2 categories" %(inputDATA,inputMC))
	print ("Saving result in: %s" %(output))

	tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]
	#~ tracks = ["TunePNew"]
	#~ tracks = ["Global"]
	#tracks = ["Outer","Global","TPFMS","Picky","DYT","TunePNew"]
	#~ tracks = [""]
	weights = []
	weights2 = []
	if args.weight:
		weights = xSecs[args.inputMC]
		if dataIsMC:
			weights2 = xSecs[args.inputMC2]
	
	#~ for trackType in tracks:	
	makeMassRes(inputDATA,inputMC,output,weights,weights2,args.track,args.funct,mcIsData,dataIsMC)
	print ("DONE")
