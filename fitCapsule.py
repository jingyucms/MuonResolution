from ROOT import TFile, gROOT, gSystem, RooFFTConvPdf, RooCmdArg, RooFit, kFALSE, RooChi2Var, RooRealVar, TCanvas, TLatex, TPad, TLegend, gStyle, RooAbsData, TF1, kRed
gROOT.SetBatch(True)

from sys import argv

ptbins = [52, 72, 100, 152, 200, 275, 452, 800]
# ~ ptbins = [300, 452, 800]

from setTDRStyle import setTDRStyle


def main():
	
		output = argv[1]
		rap = argv[2]
		flavour = argv[3]
		trackType = argv[4]
		f = argv[5] 
		fit_min = int(argv[6])
		fit_max = int(argv[7])
		rebinFactor = int(argv[8])
		i = int(argv[9])

		if f == "CB":
			DOCRYSTALBALL = True
			DOCRUIJFF = False
			DODOUBLECB = False
			
		elif f == "cruijff":		
			DOCRUIJFF = True
			DOCRYSTALBALL = False
			DODOUBLECB = False
			
		elif f == "doubleCB":
			DODOUBLECB = True
			DOCRYSTALBALL = False
			DOCRUIJFF = False

	
		print ("+++++++++++++++++++++++++++++++++++++++++")
		print ("Fitting histogram for %d < pt_{l} <%d" %(ptbins[i],ptbins[i+1]))
		print ("+++++++++++++++++++++++++++++++++++++++++\n")

		wsFile = TFile("tmpWorkspace.root")
		ws = wsFile.Get("tempWS")
		# fit with a gaussian 

		

		
		if DOCRYSTALBALL:
			funct = TF1("crystal","crystalball",fit_min,fit_max)
			funct.SetLineColor(kRed)
			if ws.data("hist").sum(False) < 1500:
				nDOF = (fit_max-fit_min)*2/(rebinFactor)-3
			else:	
				nDOF = (fit_max-fit_min)*2/rebinFactor-3

			ws.factory("RooCBShape::cb(mass, mean[0.0,-1.5,1.5], sigma[2,0,10], alphaL[3,-25,25], nL[5,-25,25])")
			ws.factory("BreitWigner::bw(mass,meanZ[91.187], width[2.495])")
			bw = ws.pdf("bw")
			cb = ws.pdf("cb")
			ws.var("mass").setBins(2000,"cache")
			ws.var("mass").setMin("cache",0)
			ws.var("mass").setMax("cache",1000); ## need to be adjusted to be higher than limit setting

			sigpdf = RooFFTConvPdf("sig","sig",ws.var("mass"),bw,cb)
			getattr(ws,'import')(sigpdf,RooCmdArg())

			fitResult = ws.pdf("sig").fitTo(ws.data("hist"),RooFit.Save(), RooFit.SumW2Error(kFALSE), RooFit.Minos(kFALSE))

		
		elif DOCRUIJFF:


			gSystem.Load("./RooCruijff_cxx.so")
			ws.factory("RooCruijff::cb(mass, mean[0.0,-1.5,1.5], sigma[2,0,20], sigma, alphaL[1,0,25], alphaR[1,0,25])")

			if ws.data("hist").sum(False) < 1500:
				nDOF = (fit_max-fit_min)*2/(1)-3
			elif ws.data("hist").sum(False) < 2500:
				nDOF = (fit_max-fit_min)*2/(1)-3
			else:	
				nDOF = (fit_max-fit_min)*2/rebinFactor-3

			ws.factory("BreitWigner::bw(mass,meanZ[91.187], width[2.495])")
			bw = ws.pdf("bw")
			cb = ws.pdf("cb")
			ws.var("mass").setBins(2000,"cache")
			ws.var("mass").setMin("cache",0)
			ws.var("mass").setMax("cache",1000); ## need to be adjusted to be higher than limit setting

			sigpdf = RooFFTConvPdf("sig","sig",ws.var("mass"),bw,cb)
			getattr(ws,'import')(sigpdf,RooCmdArg())

			fitResult = ws.pdf("sig").fitTo(ws.data("hist"),RooFit.Save(), RooFit.SumW2Error(kFALSE), RooFit.Minos(kFALSE))

		elif DODOUBLECB:


			gSystem.Load("./RooDCBShape_cxx.so")
			if i > 2:
				ws.factory("RooDCBShape::cb(mass, mean[0.0,-1.5,1.5], sigma[2,0,20], alphaL[2,0,25] , alphaR[2,0,25], nL[2.5,0,25], nR[0])")

			else:
				ws.factory("RooDCBShape::cb(mass, mean[0.0,-1.5,1.5], sigma[2,0,20], alphaL[2,0,25] , alphaR[2,0,25], nL[2.5,0,25], nR[2.5,0,25])")

			if i == 0:

				ws.var("nL").setVal(1)
				ws.var("nR").setVal(1)
			ws.factory("BreitWigner::bw(mass,meanZ[91.187], width[2.495])")
			bw = ws.pdf("bw")
			cb = ws.pdf("cb")
			ws.var("mass").setBins(2000,"cache")
			ws.var("mass").setMin("cache",0)
			ws.var("mass").setMax("cache",1000); ## need to be adjusted to be higher than limit setting

			sigpdf = RooFFTConvPdf("sig","sig",ws.var("mass"),bw,cb)
			getattr(ws,'import')(sigpdf,RooCmdArg())

			fitResult = ws.pdf("sig").fitTo(ws.data("hist"),RooFit.Save(), RooFit.SumW2Error(kFALSE), RooFit.Minos(kFALSE))

			chi2 = RooChi2Var("bla","blubb",ws.pdf("sig"),ws.data("hist")).getVal()


			if ws.data("hist").sum(False) < 1500:
				nDOF = (fit_max-fit_min)*2/(1)-5
			elif ws.data("hist").sum(False) < 2500:
				nDOF = (fit_max-fit_min)*2/(1)-5
			else:	
				nDOF = (fit_max-fit_min)*2/rebinFactor-5




		chi2 = RooChi2Var("bla","blubb",ws.pdf("sig"),ws.data("hist")).getVal()


		


		mean = RooRealVar('Mean','Mean',ws.var("meanZ").getVal() )
		getattr(ws,'import')(mean,RooCmdArg())	
		meane = RooRealVar('Meane','Meane',ws.var("meanZ").getError() )
		getattr(ws,'import')(meane,RooCmdArg())	
		sig = RooRealVar('Sig','Sig',ws.var("sigma").getVal() )
		getattr(ws,'import')(sig,RooCmdArg())	
		sige = RooRealVar('Sige','Sige',ws.var("sigma").getError() )
		getattr(ws,'import')(sige,RooCmdArg())	

		c1 = TCanvas("c1","c1",700,700)
		c1.cd()	
		plotPad = TPad("plotPad","plotPad",0,0,1,1)
		style = setTDRStyle()
		gStyle.SetOptStat(0)
		gStyle.SetTitleXOffset(1.45)
		gStyle.SetPadLeftMargin(0.2)	
		gStyle.SetTitleYOffset(2)			
		plotPad.UseCurrentStyle()
		plotPad.Draw()	
		plotPad.cd()

		if DODOUBLECB or DOCRYSTALBALL or DOCRUIJFF:
			ws.var("mass").setBins(30)
			frame = ws.var('mass').frame(RooFit.Title('Invariant mass of dimuon pairs'))
			frame.GetXaxis().SetTitle('m_{#mu#mu} [GeV]')
			frame.GetYaxis().SetTitle("Events / 2 GeV")
			RooAbsData.plotOn(ws.data('hist'), frame,RooFit.Name("hist"))
			ws.pdf('sig').plotOn(frame,RooFit.Name("sig"))
			frame.Draw()
			
			chi2 = frame.chiSquare("sig","hist") 
		else:

			h.GetXaxis().SetTitle("m_{ll} [GeV]")
			h.SetLineColor(kBlack)
			h.GetXaxis().SetRangeUser(fit_min,fit_max)
			h.SetMarkerStyle(20)
			h.SetMarkerSize(0.7)
				
			h.Draw("E")
			if DOCRYSTALBALL or DOCRUIJFF or DODOUBLECB:
				funct.Draw("SAME")
			else:
				gaus.Draw("SAME")


		nDOFforWS = RooRealVar('nDOF','nDOF',nDOF )
		getattr(ws,'import')(nDOFforWS,RooCmdArg())	
		chi2forWS = RooRealVar('chi2','chi2',chi2*nDOF )
		getattr(ws,'import')(chi2forWS,RooCmdArg())	

			
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

		cmsExtra = "Preliminary" 
		latexCMS.DrawLatex(0.78,0.88,"CMS")
		yLabelPos = 0.84
		latexCMSExtra.DrawLatex(0.78,yLabelPos,"%s"%(cmsExtra))

		latexFit1 = TLatex()
		latexFit1.SetTextFont(42)
		latexFit1.SetTextSize(0.035)
		latexFit1.SetNDC(True)
		latexFit1.DrawLatex(0.25, 0.84, "%d GeV < p_{T} < %d GeV" %(ptbins[i],ptbins[i+1]))
		
		latexFit = TLatex()
		latexFit.SetTextFont(42)
		latexFit.SetTextSize(0.030)
		latexFit.SetNDC(True)        
		latexFit.DrawLatex(0.25, 0.74,"%s = %5.3g #pm %5.3g GeV"%("mean bias",ws.var("mean").getVal(),ws.var("mean").getError()))
		if f == "CB":
				latexFit.DrawLatex(0.25, 0.7,"%s = %5.3g #pm %5.3g GeV"%("#sigma",ws.var("sigma").getVal(),ws.var("sigma").getError()))
				latexFit.DrawLatex(0.25, 0.66,"%s = %5.3g #pm %5.3g"%("alphaL",ws.var("alphaL").getVal(),ws.var("alphaL").getError()))
				latexFit.DrawLatex(0.25, 0.62,"%s = %5.3g #pm %5.3g"%("nL",ws.var("nL").getVal(),ws.var("nL").getError()))
		elif f == "cruijff":
				latexFit.DrawLatex(0.25, 0.7,"%s = %5.3g #pm %5.3g GeV"%("#sigma",ws.var("sigma").getVal(),ws.var("sigma").getError()))
				latexFit.DrawLatex(0.25, 0.66,"%s = %5.3g #pm %5.3g"%("alphaL",ws.var("alphaL").getVal(),ws.var("alphaL").getError()))
				latexFit.DrawLatex(0.25, 0.62,"%s = %5.3g #pm %5.3g"%("alphaR",ws.var("alphaR").getVal(),ws.var("alphaR").getError()))

		elif f == "doubleCB":
				latexFit.DrawLatex(0.25, 0.7,"%s = %5.3g #pm %5.3g GeV"%("#sigma",ws.var("sigma").getVal(),ws.var("sigma").getError()))
				latexFit.DrawLatex(0.25, 0.66,"%s = %5.3g #pm %5.3g"%("alphaL",ws.var("alphaL").getVal(),ws.var("alphaL").getError()))
				latexFit.DrawLatex(0.25, 0.62,"%s = %5.3g #pm %5.3g"%("alphaR",ws.var("alphaR").getVal(),ws.var("alphaR").getError()))
				latexFit.DrawLatex(0.25, 0.58,"%s = %5.3g #pm %5.3g"%("nL",ws.var("nL").getVal(),ws.var("nL").getError()))
				latexFit.DrawLatex(0.25, 0.54,"%s = %5.3g #pm %5.3g"%("nR",ws.var("nR").getVal(),ws.var("nR").getError()))
				
		latexFit.DrawLatex(0.25, 0.5, "#chi^{2}/ndf = %5.3f / %2.0f = %4.2f" %(chi2*nDOF,nDOF,chi2))

		saveas = "/MassRes_%s_%s_Pt%d_%d_%s" %(trackType,flavour,ptbins[i],ptbins[i+1],rap)
		c1.SaveAs(output+saveas+".root")
		c1.SaveAs(output+saveas+".C")
		c1.SaveAs(output+saveas+".png")
		c1.SaveAs(output+saveas+".pdf")

		print ("DONE Fitting...")
		ws.writeToFile("tmpWorkspaceReturn.root")
main()
