import subprocess

ResStudy = {

# comparison between fit functions
"compareChi2VsMass.py" : "compare chi2 of three fit functions vs mass for 2017",
"compareChi2VsMass2016.py": "2016",
"compareChi2VsMass2018.py": "2018",

"compareChi2VsPt2017.py": "compare chi2 of three fit function vs pt for 2017",
"compareChi2VsPt2016.py": "2016",
"compareChi2VsPt2018.py": "2018",

"compareResolutionFunc.py": "compare res of three fit functions vs mass for 2017",
"compareResolutionFunc2016.py": "2016",
"compareResolutionFunc2018.py": "2018",

"compareResolutionFuncMean.py": "compare mean of three fit functions vs mass for 2017",
"compareResolutionFuncMean2016.py": "2016",
"compareResolutionFuncMean2018.py": "2018",

# comparison between years, 2016-2018 (res vs mass)
"compareMassBias.py": "compare mass scale vs mass for 2016, 2017, 2018",

"compareResolution.py": "compare res vs mass for 2016, 2017, 2018",

# calculate systematic uncertainties for 2016-2018 (res vs mass)
"compareResolutionBinning.py": "compare res vs mass with binning 1, 2, 8 for 2017",
"compareResolutionBinning2016.py": "2016",
"compareResolutionBinning2018.py": "2018",

"compareResolutionWindow.py": "compare res vs mass with diff fit windows for 2017",
"compareResolutionWindow2016.py": "2016",
"compareResolutionWindow2018.py": "2018",

# comparison between years, 2016-2018 (res vs pt)
"comparePtResolutionBoosted.py": "compare DATA res vs pt for 2016, 2017, 2018",
"comparePtResolutionBoostedMC.py": "compare MC res vs pt for 2016, 2017, 2018",

# calculate systematic uncertainties for 2016-2018 (res vs pt)
"comparePtResolutionWindow.py": "compare res vs pt with diff fit windows for 2017",
"comparePtResolutionWindow2016.py": "2016",
"comparePtResolutionWindow2018.py": "2018",

"comparePtResolutionBinning.py": "compare res vs pt with binning for 2017",
"comparePtResolutionBinning2016.py": "2016",
"comparePtResolutionBinning2018.py": "2018",

}


for fn in ResStudy.keys():
	subprocess.call(["python", fn])
