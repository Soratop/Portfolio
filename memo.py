#leverage US 
L=2.4
L_d=L-1
US_d=0.7 #SBI 0.7 DMM 0.6
JP_d=0.8
JP_DMM_d=0.6 #DMM US 0.6
if L<1:
    print("Error")
else:
    print("US_TLoan amount"+" "+str(100*L))
    print("US_Total amount" +" "+ str(100*L))
    print("US_Margin call"+" "+str((100-((100*US_d)/(100*L)*100))))

    print("US_Double stock") 
    print("US_TLoan amount"+" "+str(L_d*100*US_d))
    print("US_Total amount" +" "+ str(L_d*100*US_d+100))     
    print("US_Margin call"+" "+str(100-((100*(US_d**3))/(L_d*100+100)*100)))

#leverage JP
    print("JP_TLoan amount"+" "+str(100*L))
    print("JP_Total amount" +" "+ str(100*L))
    print("JP_Margin call"+" "+str((100-((100*JP_d)/(100*L)*100))))

    print("JP_Double stock") 
    print("JP_TLoan amount"+" "+str(L_d*100*JP_d))
    print("JP_Total amount" +" "+ str(L_d*100*JP_d+100))     
    print("JP_Margin call"+" "+str(100-((100*(JP_d**3))/(L_d*100+100)*100)))
    
    #DMM
    print("DMM_Double stock") 
    print("DMM_TLoan amount"+" "+str(L_d*100*JP_DMM_d))
    print("DMM_Total amount" +" "+ "US 100 "+"JP "+str(L_d*100*JP_DMM_d))     
    print("DMM_Margin call"+" "+str(100-((100*(JP_DMM_d*JP_DMM_d*JP_d))/(L_d*100+100)*100))) # maybe
    # DMM maybe
    
    
    # JP (L4.3:L1 =10:23)= L2  50% (L4.3) 15.15%  (L1)  34.85%
    # US (L3:L1= 1:1) = L2     50% (L3)   25%    (NISA L1)  25%
    
    # JP (L4.3) 15.15%
    # JP (L1)  34.85%
    # JP (コムストックローン・SBI証券 interest rate ４．１７５％) 34.85% * 0.6= 20.91%   
    # JP (コムストックローン・SBI証券 interest rate ４．１７５％) 34.85% * 0.4= 13.94% 13.94%+34.85%=48.79%   Margin call 0.612    (7/10*0.6/stock)
    # US (NISA) 34.85% * 0.2= 6.97%
    
    
    # JP (L4.3) 15.15%     
    # JP (L1) 48.79%       #Total JP 113.935
    # US (L3) 25%          
    # US (NISA L1) 31.97   #Total US 106.97
    
    # Total 127.88% (JP 51.57%  (L) 1.78)  *  -(0.04175 *20.91%)= -0.87%
    #               (US 48.42%  (L) 1.877) 
    
    
    # or
    
    # US (L3) 50%          
    # US (NISA L1)  50%
    #Total 100 (US 100%  (L) 2)
    
    # or
    
    #DMM 
     
    