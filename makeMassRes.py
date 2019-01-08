#!/usr/bin/python

# import ROOT in batch mode
import sys,os
import argparse
import math
from setTDRStyle import setTDRStyle
import pickle
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv
	
mrange = [120, 200, 300, 400, 600, 800, 1000, 1300, 1600, 2000, 2500, 3100, 3800, 4500, 5500]
#mrange = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500]

ROOT.gROOT.LoadMacro("cruijff.C+")
ROOT.gROOT.LoadMacro("doubleCB.C+")
ROOT.gROOT.LoadMacro("gaussExp.C+")

FITMIN = -1.
FITMAX =  1. 
rebin = 5


def makeRatioGraph(f1,f2,xMin,xMax):
	graph = ROOT.TGraph()
	
	for i in range(0,100):
		x = xMin + i*(xMax-xMin)/100
		if f2.Eval(x) > 0:
			graph.SetPoint(i,x,f1.Eval(x)/f2.Eval(x))
		else:	
			graph.SetPoint(i,x,0)
		
	return graph	
	
	

sampleLists  = {

	"2016Inclusive":["ana_datamc_DYInclusive2016.root"],
	"2017Inclusive":["ana_datamc_DYInclusive2017.root"],
	"2016MassBinned":["dileptonAna_resolution_2016_dy50to120.root","dileptonAna_resolution_2016_dy120to200.root","dileptonAna_resolution_2016_dy200to400.root","dileptonAna_resolution_2016_dy400to800.root","dileptonAna_resolution_2016_dy800to1400.root","dileptonAna_resolution_2016_dy1400to2300.root","dileptonAna_resolution_2016_dy2300to3500.root","dileptonAna_resolution_2016_dy3500to4500.root","dileptonAna_resolution_2016_dy4500to6000.root","dileptonAna_resolution_2016_dy6000toInf.root"],
	"2017MassBinned":["dileptonAna_resolution_dy50to120_2017.root","dileptonAna_resolution_dy120to200_2017.root","dileptonAna_resolution_dy200to400_2017.root","dileptonAna_resolution_dy400to800_2017.root","dileptonAna_resolution_dy800to1400_2017.root","dileptonAna_resolution_dy1400to2300_2017.root","dileptonAna_resolution_dy2300to3500_2017.root","dileptonAna_resolution_dy3500to4500_2017.root","dileptonAna_resolution_dy4500to6000_2017.root","dileptonAna_resolution_dy6000toInf_2017.root"],
	"2018MassBinned":["dileptonAna_resolution_2018_dy50to120.root","dileptonAna_resolution_2018_dy120to200.root","dileptonAna_resolution_2018_dy200to400.root","dileptonAna_resolution_2018_dy400to800.root","dileptonAna_resolution_2018_dy800to1400.root","dileptonAna_resolution_2018_dy1400to2300.root","dileptonAna_resolution_2018_dy2300to3500.root","dileptonAna_resolution_2018_dy3500to4500.root","dileptonAna_resolution_2018_dy4500to6000.root","dileptonAna_resolution_2018_dy6000toInf.root"],
	"2016PtBinned":["dileptonAna_resolution_2016_dyInclusive50.root","dileptonAna_resolution_2016_dyPt50To100.root","dileptonAna_resolution_2016_dyPt100To250.root","dileptonAna_resolution_2016_dyPt250To400.root","dileptonAna_resolution_2016_dyPt400To600.root","dileptonAna_resolution_2016_dyPt650ToInf.root"],
	"2017PtBinned":["dileptonAna_resolution_2016_dyInclusive50.root","dileptonAna_resolution_dyPt50To150_1Jet_2017.root","dileptonAna_resolution_dyPt50To150_2Jets_2017.root","dileptonAna_resolution_dyPt150To250_1Jet_2017.root","dileptonAna_resolution_dyPt150To250_2Jets_2017.root","dileptonAna_resolution_dyPt250To400_1Jet_2017.root","dileptonAna_resolution_dyPt250To400_2Jets_2017.root","dileptonAna_resolution_dyPt400ToInf_1Jet_2017.root","dileptonAna_resolution_dyPt400ToInf_2Jets_2017.root","dileptonAna_resolution_dy_3Jets_2017.root","dileptonAna_resolution_dy_4Jets_2017.root"]

}

xSecs = {

	"2016Inclusive": [ 1921.8 ],
	"2017Inclusive": [ 1921.8 ],
	"2016MassBinned": [1975,19.32,2.731,0.241,1.678e-2,1.39e-3,0.8948e-4,0.4135e-5,4.56e-7,2.06e-8],
	"2017MassBinned": [1975,19.32,2.731,0.241,1.678e-2,1.39e-3,0.8948e-4,0.4135e-5,4.56e-7,2.06e-8],
	"2018MassBinned": [1975,19.32,2.731,0.241,1.678e-2,1.39e-3,0.8948e-4,0.4135e-5,4.56e-7,2.06e-8],
	"2016PtBinned": [1921.8,363.81428,84.014804,3.228256512,0.436041144,0.040981055],
	"2017PtBinned": [1921.8,491.5,587.8599,27.31,10.99,6.068,5.917,2.536,2.536,119.6,40.44]	
}

def getBinRange(histo,mlow,mhigh):
	xmin =  0
	xmax = -1
	nbins = histo.GetNbinsX()
	for bin in range(nbins):
		if mlow==histo.GetXaxis().GetBinLowEdge(bin): 
			xmin = bin
		if mhigh==histo.GetXaxis().GetBinLowEdge(bin):
			xmax = bin
	return xmin,xmax
	
def loadHistos(inputfiles,region,rebin,trackType,weights):
	_file = []
	for mc in inputfiles:
		_file.append(ROOT.TFile(mc))
	ROOT.TH1.AddDirectory(ROOT.kFALSE)    
	histoname = "Our2017MuonsPlusMuonsMinus%sResolutionMC"%trackType
	
	for k,mc in enumerate(_file):
		if ("BB" in region):
			tmp   = _file[k].Get("%s/DileptonMassResVMass_2d_BB" %(histoname)).Clone()
		elif ("BE" in region):
			tmp   = _file[k].Get("%s/DileptonMassResVMass_2d_BE" %(histoname)).Clone()
		tmp.Sumw2()
		if k==0 and not weights: 
			hmc = tmp
		elif k==0 and weights:
			nEvents = _file[k].Get("EventCounter/Events").GetBinContent(1)
			print ("Weighting with %s " %(40000*weights[k]/nEvents))
			tmp.Scale(40000*weights[k]/nEvents)
			hmc = tmp
		elif not weights:
			hmc.Add(tmp)
		else: 
			nEvents = _file[k].Get("EventCounter/Events").GetBinContent(1)			
			print ("Weighting with %s " %(40000*weights[k]/nEvents))
			tmp.Scale(40000*weights[k]/nEvents)
			hmc.Add(tmp)
		
	for f in _file:
		f.Close()
	
	histos = [ROOT.TH1D() for x in range(len(mrange)-1)]
	for h in histos:
		h.SetDirectory(0)
		ROOT.TH1.AddDirectory(ROOT.kFALSE)    
		
	c1 = ROOT.TCanvas("c1","c1",700,700)
	c1.cd()
	for i,h in enumerate(histos): 
		xmin,xmax = getBinRange(hmc,mrange[i],mrange[i+1])
		histos[i] = hmc.ProjectionY("res%s%s" %(mrange[i],region), xmin, xmax)
		histos[i].Rebin(rebin)


		
	return histos

xMinFactor = -2.0
xMaxFactor = 1.7

def doFitGeneric(hist,output,rap="BB",fit="cruijff",syst=False):
	c1 = ROOT.TCanvas("c1","c1",700,700)
	c1.cd()

	pars = []
	errs = []
	chi2 = []
	for i,h in enumerate(hist):
		
		plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
		ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
		#~ style = setTDRStyle()
		ROOT.gStyle.SetOptStat(0)
		plotPad.UseCurrentStyle()
		ratioPad.UseCurrentStyle()
		plotPad.Draw()	
		ratioPad.Draw()	
		plotPad.cd()
		#~ plotPad.cd()		
		
		if ("cruijff" in fit or "doubleCB" in fit or "gaussExp" in fit or "crystal" in fit):
			fit_min = h.GetMean()+xMinFactor*h.GetRMS() 
			fit_max = h.GetMean()+xMaxFactor*h.GetRMS()
		#~ elif ("crystal" in fit):
			#~ fit_min = h.GetMean() - 2.3*h.GetRMS() 
			#~ fit_max = h.GetMean() + 2.0*h.GetRMS()
		elif ("gaus" in fit):
			fit_min = h.GetMean() - 0.5*h.GetRMS() 
			fit_max = h.GetMean() + 1.0*h.GetRMS()
		else: 
			fit_min = FITMIN
			fit_max = FITMAX

		print ("+++++++++++++++++++++++++++++++++++++++++")
		print ("Fitting histogram for %d < m_{ll} <%d, with Range=[%3.2f, %3.2f]" %(mrange[i],mrange[i+1],fit_min,fit_max))
		print ("+++++++++++++++++++++++++++++++++++++++++\n")

 
		# fit with a gaussian to use parameters of the fit for the CB...
		gaus = ROOT.TF1("gaus","gaus",fit_min,fit_max)
		gaus.SetParameters(0,h.GetMean(),h.GetRMS())
		h.Fit("gaus","M0R+")
		
		funct = ROOT.TF1()
		if "cruijff" in fit: 
			print (">>>>>> Using Cruijff >>>>>>>>")
			funct = ROOT.TF1(fit,ROOT.cruijff,fit_min,fit_max,5)
			funct.SetParameters(gaus.GetParameter(0), gaus.GetParameter(1), gaus.GetParameter(2), 0., 0.) #15, 0.001)             
			funct.SetParNames("Constant","Mean","Sigma","AlphaL","AlphaR")      
		elif "gaus" in fit:	  
			print (">>>>>> Using Gauss >>>>>>>>")
			funct = ROOT.TF1(fit,"gaus",fit_min,fit_max)
			funct.SetParameters(gaus.GetParameter(0), gaus.GetParameter(1), gaus.GetParameter(2)) #15, 0.001)             
			funct.SetParNames("Constant","Mean","Sigma")        

		elif "crystal" in fit: 
			print (">>>>>>>>  Using CRYSTAL BALL >>>>>>>>")
			funct = ROOT.TF1(fit,"crystalball",fit_min,fit_max)
			funct.SetParameters(gaus.GetParameter(0), gaus.GetParameter(1), gaus.GetParameter(2), 1.4, 1.5)
#            funct.SetParLimits(1, gaus.GetParameter(1)*0.5, gaus.GetParameter(1)*1.5)
			funct.SetParLimits(2, 0., 2.5*h.GetRMS())
			funct.SetParLimits(3, 0.5, 2.)
			funct.SetParLimits(4, 0., 3.)

		elif "doubleCB" in fit:
			print (">>>>>>> Using Double Crystal Ball >>>>>>>")
			funct = ROOT.TF1(fit, ROOT.doubleCB, fit_min, fit_max, 7)
			funct.SetParameters(gaus.GetParameter(0), gaus.GetParameter(1), gaus.GetParameter(2), 1.4, 1.4, 1.5, 1.5)
			funct.SetParLimits(2, 0, 2.5*h.GetRMS())
			funct.SetParLimits(3, 0., 3.)
			funct.SetParLimits(4, 0., 4.)
			funct.SetParLimits(5, 0., 20.)
			funct.SetParLimits(6, 0., 20.)
			funct.SetParNames("Constant","Mean","Sigma","AlphaL","AlphaR","nL","nR")
		elif "gaussExp" in fit:
			print (">>>>>>> Using GaussExp >>>>>>>")
			funct = ROOT.TF1(fit, ROOT.gaussExp, fit_min, fit_max, 5)
			funct.SetParameters(gaus.GetParameter(0), gaus.GetParameter(1), gaus.GetParameter(2), 0, 0)
			funct.SetParLimits(2, 0, 2.5*h.GetRMS())
			funct.SetParLimits(3, 0.5, 3.)
			funct.SetParLimits(4, 0.5, 4.)
			funct.SetParNames("Constant","Mean","Sigma","AlphaL","AlphaR")
			
			
		funct.SetLineColor(ROOT.kBlue)
		funct.SetLineWidth(2)
		h.Fit(fit,"M0R+")

		if syst: 
			if ("cruijff" in fit): 
				print (">>>>>>>>  Using DCB for systematics >>>>>>>>")
				systfunc = ROOT.TF1("systfunc",ROOT.doubleCB, fit_min, fit_max, 7)
				#~ systfunc.SetParameters(funct.GetParameter(0), funct.GetParameter(1), funct.GetParameter(2), 1.4, 2.)
				systfunc.SetParameters(gaus.GetParameter(0), gaus.GetParameter(1), gaus.GetParameter(2), 1.4, 1.4, 1.5, 1.5)
				systfunc.SetParLimits(2, 0, 2.5*h.GetRMS())
				systfunc.SetParLimits(3, 0.5, 3.)
				systfunc.SetParLimits(4, 0.5, 4.)
				systfunc.SetParLimits(5, 0., 3.)
				systfunc.SetParLimits(6, 0., 20.)	
				systfunc.SetParNames("Constant","Mean","Sigma","AlphaL","AlphaR","nL","nR")
			
			elif ("crystal" in fit or "doubleCB" in fit or "gaussExp" in fit or "gaus" in fit): 
				print (">>>>>>>>  Using CRUIJFF for systematics >>>>>>>>")
				systfunc = ROOT.TF1("systfunc",ROOT.cruijff, h.GetMean() +xMinFactor*h.GetRMS(),  h.GetMean() +xMaxFactor*h.GetRMS(),5)
				systfunc.SetParameters(funct.GetParameter(0), funct.GetParameter(1), funct.GetParameter(2), 0., 0.) #15, 0.001)             
				systfunc.SetParNames("Constant","Mean","Sigma","AlphaL","AlphaR")        
			systfunc.SetLineColor(ROOT.kRed)
			h.Fit("systfunc","M0R+")
			
		if "doubleCB" in fit: 
			print (">>>>>>>>  Using CB for additional systematics >>>>>>>>")
			systfunc2 = ROOT.TF1("systfunc2","crystalball", h.GetMean() - 2.3*h.GetRMS() , h.GetMean() + 2.0*h.GetRMS() )
			systfunc2.SetParameters(gaus.GetParameter(0), gaus.GetParameter(1), gaus.GetParameter(2), 1.4, 1.5)
#            funct.SetParLimits(1, gaus.GetParameter(1)*0.5, gaus.GetParameter(1)*1.5)
			systfunc2.SetParLimits(2, 0., 2.5*h.GetRMS())
			systfunc2.SetParLimits(3, 0.5, 2.)
			systfunc2.SetParLimits(4, 0., 3.)
		
			h.Fit("systfunc2","M0R+")

		for par in range(funct.GetNpar()-1):
			pars.append(funct.GetParameter(par+1))
			#~ if syst and ("Mean" in funct.GetParName(par+1) or "Sigma" in funct.GetParName(par+1)) and funct.GetParameter(par+1) > 0: 
				#~ sys =1-systfunc.GetParameter(par+1)/funct.GetParameter(par+1)
				#~ sys = sys*funct.GetParameter(par+1)
			#~ else:
			sys = 0.
			errs.append(math.sqrt(sys*sys+funct.GetParError(par+1)*funct.GetParError(par+1)))
		if funct.GetNDF() > 0:
			chi2.append(funct.GetChisquare()/funct.GetNDF())
		else:
			chi2.append(0)

		h.SetTitle("Mass resolution for %d < m_{ll} <%d" %(mrange[i],mrange[i+1]))
		h.GetXaxis().SetTitle("m_{ll}^{RECO} / m_{ll}^{GEN} - 1")
		h.SetLineColor(ROOT.kBlack)
		h.SetMarkerStyle(20)
		h.SetMarkerSize(0.8)
		h.GetXaxis().SetRangeUser(fit_min,fit_max)

		h.Draw("E")
		funct.Draw("SAME")
		systfunc.Draw("SAME")
		systfunc.SetLineColor(ROOT.kRed)
		if "doubleCB" in fit:
			systfunc2.Draw("SAME")
			systfunc2.SetLineColor(ROOT.kGreen+1)
		
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.04)
		latex.SetNDC(True)
		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		latexCMS.SetTextSize(0.055)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		latexCMSExtra.SetTextSize(0.03)
		latexCMSExtra.SetNDC(True)

		latex.DrawLatex(0.95, 0.96, "(13 TeV)")

		cmsExtra = "Simulation" 
		latexCMS.DrawLatex(0.78,0.88,"CMS")
		yLabelPos = 0.84
		latexCMSExtra.DrawLatex(0.78,yLabelPos,"%s"%(cmsExtra))

		latexFit1 = ROOT.TLatex()
		latexFit1.SetTextFont(61)
		latexFit1.SetTextSize(0.035)
		latexFit1.SetNDC(True)
		latexFit1.DrawLatex(0.19, 0.84, "%d < m <%d" %(mrange[i],mrange[i+1]))
		
		latexFit = ROOT.TLatex()
		latexFit.SetTextFont(42)
		latexFit.SetTextSize(0.030)
		latexFit.SetNDC(True)        
		for par in range(funct.GetNpar()-1):
			yPos = 0.74-0.04*(float(par))
			latexFit.DrawLatex(0.19, yPos,"%s = %5.3g #pm %5.3g"%(funct.GetParName(par+1),funct.GetParameter(par+1),funct.GetParError(par+1)))
		if funct.GetNDF() > 0:
			if "doubleCB" in fit:
				latexFit.DrawLatex(0.19, 0.50, "#chi^{2}/ndf = %5.1f / %2.0f = %4.2f" %(funct.GetChisquare(),funct.GetNDF(),funct.GetChisquare()/funct.GetNDF()))
			else:	
				latexFit.DrawLatex(0.19, 0.58, "#chi^{2}/ndf = %5.1f / %2.0f = %4.2f" %(funct.GetChisquare(),funct.GetNDF(),funct.GetChisquare()/funct.GetNDF()))
	
		if "doubleCB" in fit:
			line1 = ROOT.TLine(-funct.GetParameter(3)*funct.GetParameter(2)+funct.GetParameter(1),0,-funct.GetParameter(3)*funct.GetParameter(2)+funct.GetParameter(1),0.8*h.GetBinContent(h.GetMaximumBin()))
			line1.Draw("same")
			line2 = ROOT.TLine(funct.GetParameter(4)*funct.GetParameter(2)+funct.GetParameter(1),0,funct.GetParameter(4)*funct.GetParameter(2)+funct.GetParameter(1),0.8*h.GetBinContent(h.GetMaximumBin()))
			line2.Draw("same")

		ratioPad.cd()
		#~ ratio = ROOT.TF1("ratio","%s/systfunc"%fit,fit_min,fit_max)
		ratio = makeRatioGraph(funct,systfunc,fit_min,fit_max)
		
		ratioPad.DrawFrame(fit_min,0.8,fit_max,1.2,";;Double CB / Variant")
		
		ratio.Draw("sameL")
		ratio.SetLineColor(ROOT.kRed)
		if "doubleCB" in fit:
			ratio2 = makeRatioGraph(funct,systfunc2,fit_min,fit_max)		
			ratio2.Draw("sameL")
			ratio2.SetLineColor(ROOT.kGreen+1)
				
				
		saveas = "/MassRes_M%d_%d_%s_%s" %(mrange[i],mrange[i+1],rap,fit)
		c1.Print(output+saveas+".root")
		c1.Print(output+saveas+".C")
		c1.Print(output+saveas+".png")
		c1.Print(output+saveas+".pdf")
		
	print ("DONE Fitting...")
	return pars,errs,chi2

def doFitWithSyst(hist,output,nrms,rapidity):
	print ("######################################################")
	print ("### FITTING HISTOS AND COMPUTING SYST  ERRORS      ###")
	print ("######################################################")
	(sig     ,err,alp     ,aer,n     ,nerr) = doFit(hist,output,nrms,rapidity)
	(sig_down,_  ,alp_down,_  ,n_down,_   ) = doFit(hist,output,nrms*0.75,rapidity)
	(sig_up  ,_  ,alp_up  ,_  ,n_up  ,_   ) = doFit(hist,output,nrms*1.25,rapidity)
	
	for i in range(0,len(sig)):
		sys    = max(abs(1-sig_up[i]/sig[i]),abs(1-sig_down[i]/sig[i]))
		sys    = sys*sig[i]
		err[i] = math.sqrt(sys*sys+err[i]*err[i])

		sys    = max(abs(1-alp_up[i]/alp[i]),abs(1-alp_down[i]/alp[i]))
		sys    = sys*alp[i]
		aer[i] = math.sqrt(sys*sys+aer[i]*aer[i])

		sys     = max(abs(1-n_up[i]/n[i]),abs(1-n_up[i]/n[i]))
		sys     = sys*n[i]
		nerr[i] = math.sqrt(sys*sys+aer[i]*aer[i])

	print ("############")
	print ("### DONE ###")
	print ("############")
	return sig,err,alp,aer,n,nerr
	

def drawMassResGeneric(hist,output,rapidity,funct="cruijff",trackType="TunePNew"):
	mass = []
	merr = []
	for i in range(len(mrange)-1):
		mass.append(mrange[i]+(mrange[i+1]-mrange[i])/2)
		merr.append((mrange[i+1]-mrange[i])/2)
	

	(pars,errs,chi2) = doFitGeneric(hist,output,rapidity,funct,True)
#    if "crystal" in funct: 
#        (pars2,_,_) = doFitGeneric(hist,output,rapidity,"cruijff")
#    else:
#        (pars2,_,_) = doFitGeneric(hist,output,rapidity,"crystal")
	
	c2 = ROOT.TCanvas("c2","c2",700,700)
	c2.cd()

	fun  = ROOT.TF1("fun","pol4")
	fun.SetParNames("A","B","C","D","E")            
	for i in range(fun.GetNpar()): 
		fun.ReleaseParameter(i)
		fun.SetParameter(i,0.)

	param = [ROOT.TGraphErrors(len(mass)) for x in range(int(len(pars)/len(mass))+1)] 
	res = ROOT.TGraphErrors(len(mass))
	
	result = {}
	result["sigma"] = []
	result["sigmaErr"] = []
	result["mean"] = []
	result["meanErr"] = []
	result["mass"] = []
	result["massErr"] = []
	result["chi2"] = []


	nPar = 4
	if funct == "doubleCB":
		nPar = 6
	elif funct == "crystal":
		nPar = 4
	elif funct == "gaus":
		nPar = 2
	
	for k,f in enumerate(param): 
		if k==nPar: 
			f.SetName("chi2")
		else : 
			f.SetName(hist[0].GetFunction(funct).GetParName(k+1))            

		for i in range(0,len(mass)):
			if k==nPar: 
				f.SetName("chi2")
				result["chi2"].append(chi2[i])
				f.SetPoint(i,mass[i],chi2[i])
				f.SetPointError(i,merr[i],0)
			else: 
				f.SetPoint(i,mass[i],pars[i*nPar+k])
				f.SetPointError(i,merr[i],errs[i*nPar+k])
				if "Sigma" in f.GetName():
					result["sigma"].append(pars[i*nPar+k])
					result["sigmaErr"].append(errs[i*nPar+k])
					result["mass"].append(mass[i])
					result["massErr"].append(merr[i])
				elif "Mean" in f.GetName():
					result["mean"].append(pars[i*nPar+k])
					result["meanErr"].append(errs[i*nPar+k])
		if ("Sigma" in f.GetName()):
			res = param[k]

		f.SetMarkerStyle(20)
		f.SetMarkerSize(1.0)
		f.SetMarkerColor(ROOT.kBlue)
		f.SetLineColor(ROOT.kBlue)
		f.SetFillColor(0)
		f.GetXaxis().SetTitle("m(#mu^{+}#mu^{-}) [GeV]")
		f.GetXaxis().SetRangeUser(mrange[0],mrange[len(mrange)-1])
		if ("chi2" in f.GetName()): 
			f.GetYaxis().SetRangeUser(0,20)            

		if "Sigma" in f.GetName():
			f.GetYaxis().SetRangeUser(0,0.15)

		if "AlphaR" in f.GetName():
			f.GetYaxis().SetRangeUser(0,.4)

		if "AlphaL" in f.GetName():
			f.GetYaxis().SetRangeUser(0.1,.6)

		if "Mean" in f.GetName():
			f.GetYaxis().SetRangeUser(-0.035,0.05)
						
		f.Draw("AP E0")
		
		## FIT PARAMETERS 
		for i in range(fun.GetNpar()): 
			fun.ReleaseParameter(i)
			fun.SetParameter(i,0.)
		
		if ("chi2" not in f.GetName()): 
			if ("Sigma" in f.GetName()):  
				print ("Fitting Sigma")
				fun.SetParameters(0.,1E-5,-1.E-8,2E-12,-2E-16)
				fun.SetParLimits(1, 1.0E-6, 1.0E-4)
				fun.SetParLimits(2,-1.0E-7,-1.0E-9)
#                fun.SetParLimits(4,-3.0E-16,-1E-16)
				#                fun.FixParameter(3,0.)
#                fun.FixParameter(3,0.)
#                fun.FixParameter(4,0.)
			elif "AlphaR" in f.GetName(): 
				fun.SetParameters(0.25, 1E-6, -1.E-9, 1.E-12, -1.E-16)
				fun.SetParLimits(1, 1E-7, 1E-5)
				fun.SetParLimits(2, -1E-8 ,-1E-10)                
				fun.SetParLimits(3, 1E-14 ,1E-11)                
				fun.FixParameter(4,0.)
				fun.FixParameter(3,0.)
#                fun.FixParameter(2,0.)
#                fun.FixParameter(1,0.)
			elif "AlphaL" in f.GetName(): 
				fun.SetParameters(0.1,-1E-6, 1E-9, -1.E-13, 1E-16)
				fun.SetParLimits(1, -5E-5, -5E-7)
				fun.SetParLimits(2, 1E-10, 1E-8)                
				fun.SetParLimits(3, -1E-12, -1E-15)
#                fun.SetParLimits(4, 1E-18, 1E-10)
				fun.FixParameter(4,0.)
				fun.FixParameter(3,0.)
#                fun.FixParameter(2,0.)
			elif "Mean" in f.GetName():
				fun.SetParameters(0.004,-3E-5,1E-10,-1E-12,1.E-16)
				fun.SetParLimits(1,-1E-4,-1E-6)
				fun.SetParLimits(2, 1E-12,1E-8)
				fun.SetParLimits(3,-1E-12,-5E-14)
				fun.FixParameter(4,0.)
				
			f.Fit(fun,"MBFE+")            
			fun.Draw("SAME")

		
			latexFit = ROOT.TLatex()
			latexFit.SetTextFont(42)
			latexFit.SetTextSize(0.030)
			latexFit.SetNDC(True)        
			for par in range(fun.GetNpar()):
				yPos = 0.74-0.04*(float(par))
				latexFit.DrawLatex(0.19, yPos,"%s = %5.3g #pm %5.3g"%(fun.GetParName(par),fun.GetParameter(par),fun.GetParError(par)))
			latexFit.DrawLatex(0.19, 0.54, "#chi^{2}/ndf = %5.1f / %2.0f = %4.2f" %(fun.GetChisquare(),fun.GetNDF(),fun.GetChisquare()/fun.GetNDF()))
			
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.04)
		latex.SetNDC(True)
		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		latexCMS.SetTextSize(0.055)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		latexCMSExtra.SetTextSize(0.03)
		latexCMSExtra.SetNDC(True)
		
		latex.DrawLatex(0.95, 0.96, "(13 TeV)")
		
		cmsExtra = "Simulation" #splitline{Simulation}{Preliminary}"
		latexCMS.DrawLatex(0.19,0.88,"CMS")
		yLabelPos = 0.84
		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))


		c2.SetGrid()
		saveas = "/%sVsMass_%s_%s" %(f.GetName(),trackType,rapidity)
		c2.SaveAs(output+saveas+".png")
		c2.SaveAs(output+saveas+".pdf")
		c2.SaveAs(output+saveas+".root")
		c2.SaveAs(output+saveas+".C")
	
		ROOT.gPad.Update()
		c2.Clear()
	pklFile = open(output+"/MassResolutionVsMass_%s_%s.pkl" %(trackType,rapidity),"wb")
	pickle.dump(result,pklFile)
	pklFile.close()	

	# PRINT FIT RESULTS!!!
	return res
	
	
def makeMassRes(inputfile,output,funct,trackType,weights):
	style = setTDRStyle()
	ROOT.gStyle.SetTitleYOffset(1.45)
	ROOT.gStyle.SetTitleXOffset(1.45)
	ROOT.gStyle.SetOptFit(0)
	ROOT.gStyle.SetStatX(.9)
	ROOT.gStyle.SetStatY(.9)
	
	hist_barrel = loadHistos(inputfile,"BB",rebin,trackType,weights)
	hist_other  = loadHistos(inputfile,"BE",rebin,trackType,weights)
	resBB  = drawMassResGeneric(hist_barrel,output,"BB",funct,trackType)
	resBE  = drawMassResGeneric(hist_other,output,"BE",funct,trackType)
	
	res = ROOT.TCanvas("res","res",700,700)
	res.cd()
	res.SetTickx()
	res.SetTicky()
	
	resBB.SetMarkerStyle(20)
	resBB.SetMarkerSize(1)
	resBB.SetMarkerColor(ROOT.kRed)
	resBB.SetLineColor(ROOT.kRed)
	resBB.SetFillColor(0)
	resBB.SetTitle("Dimuon mass resolution vs mass")
	resBB.GetYaxis().SetTitle("Dimuon Mass Resolution")
#    resBB.GetYaxis().SetTitleOffset(1.5)
	resBB.GetXaxis().SetTitle("m(#mu^{+}#mu^{-}) [GeV]")
	resBB.GetYaxis().SetRangeUser(0,.15)
	resBB.GetXaxis().SetRangeUser(mrange[0],mrange[len(mrange)-1])
	resBB.GetFunction("fun").SetLineColor(ROOT.kRed+1)
	resBB.Draw("AP E0")
	
	resBE.SetMarkerStyle(20)
	resBE.SetMarkerSize(1.0)
	resBE.SetMarkerColor(ROOT.kGreen+1)
	resBE.SetLineColor(ROOT.kGreen+1)
	resBE.SetFillColor(0)
	resBE.SetTitle("Dimuon mass resolution vs mass")
	resBE.GetYaxis().SetTitle("Dimuon Mass Resolution")
	resBE.GetYaxis().SetTitleOffset(1.5)
 #   resBE.GetXaxis().SetTitle("m(#mu^{+}#mu^{-}) [GeV]")
	resBE.GetYaxis().SetRangeUser(0,.15)
	resBE.GetXaxis().SetRangeUser(mrange[0],mrange[len(mrange)-1])
	resBE.GetFunction("fun").SetLineColor(ROOT.kGreen+2)
	resBE.Draw("PE0 SAME")

	latexFitBB = ROOT.TLatex()
	latexFitBB.SetTextFont(42)
	latexFitBB.SetTextSize(0.030)
	latexFitBB.SetNDC(True)        
	latexFitBB.SetTextColor(ROOT.kRed)

	latexFitBE = ROOT.TLatex()
	latexFitBE.SetTextFont(42)
	latexFitBE.SetTextSize(0.030)
	latexFitBE.SetNDC(True)        
	latexFitBE.SetTextColor(ROOT.kGreen+2)
	latexFitBB.DrawLatex(0.19, 0.78,"BB Category")
	latexFitBE.DrawLatex(0.60, 0.78,"BE+EE Category")
	for par in range(resBB.GetFunction("fun").GetNpar()):
		yPos = 0.74-0.04*(float(par))
		latexFitBB.DrawLatex(0.19, yPos,"%s = %5.3g #pm %5.3g"%(resBB.GetFunction("fun").GetParName(par),resBB.GetFunction("fun").GetParameter(par),resBB.GetFunction("fun").GetParError(par)))
		latexFitBE.DrawLatex(0.60, yPos,"%s = %5.3g #pm %5.3g"%(resBE.GetFunction("fun").GetParName(par),resBE.GetFunction("fun").GetParameter(par),resBE.GetFunction("fun").GetParError(par)))
	latexFitBB.DrawLatex(0.19, 0.54, "#chi^{2}/ndf = %5.1f / %2.0f = %4.2f" %(resBB.GetFunction("fun").GetChisquare(),resBB.GetFunction("fun").GetNDF(),resBB.GetFunction("fun").GetChisquare()/resBB.GetFunction("fun").GetNDF()))
	latexFitBE.DrawLatex(0.60, 0.54, "#chi^{2}/ndf = %5.1f / %2.0f = %4.2f" %(resBE.GetFunction("fun").GetChisquare(),resBE.GetFunction("fun").GetNDF(),resBE.GetFunction("fun").GetChisquare()/resBE.GetFunction("fun").GetNDF()))
		
#    leg = ROOT.TLegend(.35,.7,.50,.80,"","brNDC")
#    leg.AddEntry(resBB,"BB")
#    leg.AddEntry(resBE,"BE+EE")
#    leg.SetTextFont(42)
#    leg.SetBorderSize(0)
#    leg.SetTextSize(.04)
#    leg.Draw("SAME")

	latex = ROOT.TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexCMS = ROOT.TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.055)
	latexCMS.SetNDC(True)
	latexCMSExtra = ROOT.TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.03)
	latexCMSExtra.SetNDC(True)
	
	latex.DrawLatex(0.95, 0.96, "(13 TeV)")
	
	cmsExtra = "Simulation" #splitline{Simulation}{Preliminary}"
	latexCMS.DrawLatex(0.19,0.88,"CMS")
	yLabelPos = 0.84
	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
	
	res.SetGrid()
	saveas = "/MassResolutionVsMass_%s"%trackType 
	res.SaveAs(output+saveas+".png")
	res.SaveAs(output+saveas+".pdf")
	res.SaveAs(output+saveas+".root")
	res.SaveAs(output+saveas+".C")
			 
#### ========= MAIN =======================
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(usage="makeMassRes.py [options]",description="Compute mass resolution",
									 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument("-i","--ifile", dest="inputfile",default="files/res_ZToMuMu_M_120_6000.root", help='Input filename')
	parser.add_argument("-o","--ofolder",dest="output", default="plots/", help='folder name to store results')
	parser.add_argument("-f","--funct",dest="funct", default="cruijff", help='function used')
	parser.add_argument("-x","--xrange", type=str, help='lower and upper x limit', nargs=1)
	parser.add_argument("--xMinFac", dest ="xMinFac", type=float, help='lower x limit', default = -2.0)
	parser.add_argument("--xMaxFac",dest = "xMaxFac", type=float, help='lower x limit', default = 1.7)
	parser.add_argument("--rebin",dest = "rebin", type=int, help='rebin factor', default = 5)
	parser.add_argument("--weight",type=bool, help='Reweight MC samples to xsec',default=False)
					
#    parser.add_argument("-ncat","--ncategories", dest="ncat", type=int, default=3, help='number of categories')
	args = parser.parse_args()
	
	inputfiles = sampleLists[args.inputfile]
	output=args.output
#    ncat=args.ncat

	if args.xrange is not None:
		ranges = args.xrange[0].split(",")
		FITMIN = float(ranges[0])
		FITMAX = float(ranges[1])

	xMinFactor = args.xMinFac
	xMaxFactor = args.xMaxFac
	rebin = args.rebin

	if not os.path.exists(args.output):
		os.makedirs(args.output);
		if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+args.output)
	weights = []
	if args.weight:
		weights = xSecs[args.inputfile]

	print ("Running on: %s " %(inputfiles))
	print ("Saving result in: %s" %(output))
	# ~ tracks = ["Inner","Outer","Global","TPFMS","Picky","DYT","TunePNew"]
	tracks = ["TunePNew"]
	for trackType in tracks:
		makeMassRes(inputfiles,output,args.funct,trackType,weights)
	print ("DONE")
