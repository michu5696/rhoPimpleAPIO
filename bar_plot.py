import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# SPEEDUPS -------------------------------------------

# HAWK

# 16M HT
apio_speedup_Hawk_16M_HT =  [21.3886,19.0262,18.3298,18.5421,15.1125,18.3367,19.9450,19.7679,17.9285]
error_speedup_Hawk_16M_HT = [3.82958,3.4382,1.47235,2.54602,1.36065,8.9733,4.05702,2.06128,3.89477]

# 16M noHT

apio_speedup_Hawk_16M_noHT=[17.1106, 15.5989, 14.5322, 14.0060, 13.9478]
error_speedup_Hawk_16M_noHT=[32.453, 36.8373, 35.137, 37.7762, 34.6483]

# 47M HT

apio_speedup_Hawk_47M_HT = [23.7807,12.2818,18.0643,17.9534,17.5948,16.7104,35.8595,18.5144,17.7205,17.6904]
error_speedup_Hawk_47M_HT = [8.37082,5.76567,6.53229,5.57937,1.9587,6.02509,5.21197,6.08994,2.22459,5.10513]

# MARENOSTRUM

# 16M 
apio_speedup_MN_16M_HT = [5.2879, 4.8460, 4.7543, 5.2388]
error_speedup_MN_16M_HT = [0.291889, 0.388085, 1.93841, 1.59021]

apio_speedup_MN_16M_noHT = [1.9340, 1.7466, 2.1990, 1.3819, 0.9530]
error_speedup_MN_16M_noHT = [1.42236, 3.91184, 3.28432, 3.17905, 4.7972]

# 131M 

apio_speedup_MN_131M_HT = [3.8854]
error_speedup_MN_131M_HT = [12.7247]


# TIMES ------------------------------------------------------
# HAWK 

# 16M HT

apio_times_Hawk_16M_HT = [199.19,197.588,196.045,198.108,198.522,194.072,
195.692,197.269,198.882]
orig_times_Hawk_16M_HT = [253.279,243.669,240.045,243.203,233.865,237.649,244.447,245.812,242.328]

error_apio_Hawk_16M_HT = [10.7528,13.1683,12.3626,11.7871,12.2447,10.2818,9.81996,9.8694,12.4873]
error_orig_Hawk_16M_HT = [24.2802,18.4654,19.5737,21.4159,19.1869,31.4297,22.6134,18.0574,19.7288]

# 16M noHT

apio_times_Hawk_16M_noHT =[263.073,235.066,247.154,231.054,239.848]
orig_times_Hawk_16M_noHT =[323.753,281.832,292.844,272.696,278.038]

error_apio_Hawk_16M_noHT =[30.6525,32.2238,32.4496,30.3121,37.595]
error_orig_Hawk_16M_noHT =[27.6698,30.9056,29.7344,35.3025,27.7122]  

# 47M

apio_times_Hawk_47M_HT=[469.817,444.967,447.847,447.696,452.023,445.628,545.594,449.031,450.893,454.896]
orig_times_Hawk_47M_HT=[616.402,507.269,546.584,545.661,548.537,535.035,850.624 ,551.056 ,548.002 ,552.665]

error_apio_Hawk_47M_HT =[10.4484,7.23065,7.48686,7.69396,20.7064,9.18887,17.4506,10.1179,17.7322,32.7097]
error_orig_Hawk_47M_HT =[72.7191,36.5873,45.8855,43.4139,38.4934,40.7786,79.839,46.0439,40.8846,27.3239]

# MARENOSTRUM

# 16M HT

apio_times_MN_16M_HT =[304.84,307.768,305.866,305.943]
orig_times_MN_16M_HT =[321.349,323.136,320.722,323.03]

error_apio_MN_16M_HT =[8.93421,7.66825,8.56885,4.80733]
error_orig_MN_16M_HT =[7.14703,7.35964,5.29224,7.96996]

# 16M noHT

apio_times_MN_16M_noHT =[169.132,168.202,169.075,170.363,169.283]
orig_times_MN_16M_noHT =[172.529,171.288,172.621,173.016,171.364]

error_apio_MN_16M_noHT =[3.99261,7.6534,4.74202,7.86461,7.83668]
error_orig_MN_16M_noHT =[6.32892,5.38505,6.94575,7.11445,3.82727]

# 131M HT 

apio_times_MN_131M_HT =[660.452]
orig_times_MN_131M_HT =[687.151]

error_apio_MN_131M_HT =[7.20755]
error_orig_MN_131M_HT =[6.8851]

# -------------------------

apio=apio_times_MN_131M_HT
orig= orig_times_MN_131M_HT

error_apio=error_apio_MN_131M_HT
error_orig=error_orig_MN_131M_HT

speedup=apio_speedup_MN_131M_HT
error_speedup=error_speedup_MN_131M_HT


x = np.arange(len(apio))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(12,10))
rects1 = ax.bar(x-width/2,apio, width,yerr=error_apio,label="APIO")
rects2 = ax.bar(x + width/2, orig, width, yerr=error_orig,label="ORIGINAL")

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Time (s) [averaged over 12 hour run]')
ax.set_xlabel('Runs (Different nodes)')
ax.set_title('Speedup for APIO on 4 nodes MN (192 cores,  HT) - 131M cells (1\u0394t)')
ax.set_xticks(x)
#ax.set_xticklabels(apio)
ax.legend()


def autolabel(rects1,rect2):
    i=0
    for rect1,rect2 in zip(rects1,rects2):
        h1 = rect1.get_height() 
        h2 = rect2.get_height()
        ax.annotate('{} %\n \u00B1 {}%'.format(round(speedup[i],2),round(error_speedup[i],2)),
                    xy=(rect1.get_x() + rect1.get_width() , max(h1,h2)),
                    xytext=(-15, 10),  # 5 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
        i+=1


autolabel(rects1,rects2)

fig.tight_layout()

plt.show()
