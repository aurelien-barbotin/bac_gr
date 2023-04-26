#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 11:06:33 2022

@author: aurelienb
"""

import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
import glob
import tifffile
import os
import sys

import pandas as pd

def main():
    folder_in = "to_process/"
    folder_out = "results/"
    
    if not os.path.isdir(folder_in):
        os.mkdir(folder_in)
        
    if not os.path.isdir(folder_out):
        os.mkdir(folder_out)
        
    files = glob.glob(folder_in+"*.tif*")
    
    def expf(t,tau):
        return np.exp(t/tau)
    
    dt = 1 # frames
    
    all_out = {"filename":[],
               "doubling time (exp. fit)":[],
               "doubling time (ratio)":[]}
    
    subfolder=input("Please enter output folder name:\n")
    
    if os.path.isdir(subfolder):
        print("The filename already exists, please specify another one")
        sys.exit(0)
    os.mkdir(folder_out+subfolder+"/")
    
    for j in range(len(files)):
        name = files[j].split(os.sep)[-1].split('.')[0]
        out_name = folder_out+subfolder+"/"+name
        stack = tifffile.imread(files[j])
        
        counts = []
        for t in range(stack.shape[0]):
            im = stack[t]
            count = np.count_nonzero(im>im.min())
            counts.append(count)
        counts = np.asarray(counts).astype(float)
        counts/=stack[0].size
        
        try:
            t_double_ratio = stack.shape[0]*np.log(2)/np.log(counts[-1]/counts[0])
        except:
            t_double_ratio = 1
        all_out["doubling time (ratio)"].append(t_double_ratio)
        
        xt = np.arange(len(counts))*dt
        try:
            popt, _ = curve_fit(expf,xt,counts/counts[0],p0 = (t_double_ratio))
        except:
            popt = [1]
            
        yh = expf(xt,*popt)
        t_double = popt[0]*np.log(2)
        
        all_out["doubling time (exp. fit)"].append(t_double)
        all_out['filename'].append(name)
        
        
        plt.figure(figsize=(8,3))
        plt.subplot(131)
        plt.imshow(stack[0])
        plt.title('Mask, first frame')
        plt.subplot(132)
        plt.imshow(stack[-1])
        plt.title('Mask, last frame')
        plt.subplot(133)
        plt.plot(xt, counts/counts[0],'-o',label='fit')
        plt.plot(xt,yh,'k--',label='data')
        plt.legend()
        plt.xlabel('time (frames)')
        plt.ylabel('Relative growth')
        plt.suptitle('Doubling time {:.2f} frames'.format(t_double))
        plt.tight_layout()
        plt.savefig(out_name+'_summary.png')
        plt.close()
        
        
        out_dict={"frame": xt,
                  "cell fraction": counts,
                  "relative growth": counts/counts[0],
                  "exponential fit": yh
                  }
        
        df = pd.DataFrame(data=out_dict)
        df.to_excel(out_name+"_results.xlsx")
        print('Doubling time {}: {:.2f}'.format(name, t_double))
    
    all_out_df = pd.DataFrame(all_out)
    all_out_df.to_excel(folder_out+subfolder+"/"'doubling_times.xlsx')
    print('Done')
    
if __name__=='__main__':
    main()
