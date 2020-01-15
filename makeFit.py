import ROOT
ROOT.gROOT.LoadMacro("cruijff.C+")
ROOT.gROOT.LoadMacro("doubleCB.C+")


from setTDRStyle import setTDRStyle
style = setTDRStyle()

inputfiles = ["dileptonAna_resolution_dy50to120_2017.root","dileptonAna_resolution_dy120to200_2017.root","dileptonAna_resolution_dy200to400_2017.root","dileptonAna_resolution_dy400to800_2017.root","dileptonAna_resolution_dy800to1400_2017.root","dileptonAna_resolution_dy1400to2300_2017.root","dileptonAna_resolution_dy2300to3500_2017.root","dileptonAna_resolution_dy3500to4500_2017.root","dileptonAna_resolution_dy4500to6000_2017.root","dileptonAna_resolution_dy6000toInf_2017.root"]

weights =  [1975,19.32,2.731,0.241,1.678e-2,1.39e-3,0.8948e-4,0.4135e-5,4.56e-7,2.06e-8]
_file = []
for mc in inputfiles:
	_file.append(ROOT.TFile(mc))
ROOT.TH1.AddDirectory(ROOT.kFALSE)    
histoname = "Our2017MuonsPlusMuonsMinusTunePNewResolutionMC"

region = "BB"

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

histo = ROOT.TH1D() 
histo.SetDirectory(0)
ROOT.TH1.AddDirectory(ROOT.kFALSE)    
	
c1 = ROOT.TCanvas("c1","c1",700,700)
c1.cd()
xmin = 50
xmax = 14000
histo = hmc.ProjectionY("res" , xmin, xmax)
histo.Rebin(2)

plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
#~ style = setTDRStyle()
ROOT.gStyle.SetOptStat(0)
plotPad.UseCurrentStyle()
plotPad.Draw()	
plotPad.cd()
#~ plotPad.cd()	

xMinFactor = -2.0
xMaxFactor = 1.7

	
fit_min = histo.GetMean()+xMinFactor*histo.GetRMS() 
fit_max = histo.GetMean()+xMaxFactor*histo.GetRMS()

# fit with a gaussian to use parameters of the fit for the CB...
funct = ROOT.TF1("gaus","gaus",fit_min,fit_max)
funct.SetParameters(0,histo.GetMean(),histo.GetRMS())
histo.Fit("gaus","M0R+")

	

funct.SetLineColor(ROOT.kBlue)
funct.SetLineWidth(2)




histo.SetTitle("Mass resolution")
histo.GetXaxis().SetTitle("m_{ll}^{RECO} / m_{ll}^{GEN} - 1")
histo.SetLineColor(ROOT.kBlack)
histo.SetMarkerStyle(20)
histo.SetMarkerSize(0.8)
histo.GetXaxis().SetRangeUser(fit_min,fit_max)

histo.Draw("E")
funct.Draw("SAME")
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


latexFit = ROOT.TLatex()
latexFit.SetTextFont(42)
latexFit.SetTextSize(0.030)
latexFit.SetNDC(True)        
for par in range(funct.GetNpar()-1):
	yPos = 0.74-0.04*(float(par))
	latexFit.DrawLatex(0.19, yPos,"%s = %5.3g #pm %5.3g"%(funct.GetParName(par+1),funct.GetParameter(par+1),funct.GetParError(par+1)))
if funct.GetNDF() > 0:
	latexFit.DrawLatex(0.19, 0.50, "#chi^{2}/ndf = %5.1f / %2.0f = %4.2f" %(funct.GetChisquare(),funct.GetNDF(),funct.GetChisquare()/funct.GetNDF()))


c1.Print("resolutionFit.pdf")
