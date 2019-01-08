#include "TMath.h" 

Double_t doubleCB( Double_t *x, Double_t * par) {

 // par[0] = normalization
 // par[1] = mean
 // par[2] = sigma
 // par[3] = alphaL
 // par[4] = alphaR
 // par[5] = nL
 // par[6] = nR

  Double_t t = (x[0]-par[1])/par[2];

  Double_t absAlphaL = fabs((Double_t)par[3]);
  Double_t absAlphaR = fabs((Double_t)par[4]);
  Double_t nL = par[5];
  Double_t nR = par[6];
  if (t >= -absAlphaL && t <= absAlphaR) {
    return par[0]*exp(-0.5*t*t);
  }
  else if (t < -absAlphaL) {
    Double_t a = TMath::Power(nL/absAlphaL,nL)*exp(-0.5*absAlphaL*absAlphaL);
    Double_t b = nL/absAlphaL - absAlphaL;
    return par[0]*a/TMath::Power(b - t, nL);
  }
  else {
    Double_t a = TMath::Power(nR/absAlphaR,nR)*exp(-0.5*absAlphaR*absAlphaR);
    Double_t b = nR/absAlphaR - absAlphaR;
    return par[0]*a/TMath::Power(b + t, nR);
  }
}
