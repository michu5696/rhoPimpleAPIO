import matplotlib
import matplotlib.pyplot as plt
import numpy as np

apio_Hawk_16M_HT =  [26.7782, 21.3555, 18.9113, 18.3298, 18.5421, 15.1125, 18.3367, 19.9450, 19.7480, 17.9285]
error_Hawk_16M_HT = [8.01163, 4.49086, 2.43774, 1.47235, 2.54602, 1.36065, 8.9733, 4.05702, 0.837467, 3.89477]

apio_Hawk_16M_noHT=[17.2605, 15.5989, 14.5322, 14,0060, 13.9478]
error_Hawk_16M_noHT=[32.5485, 36.8373]

apio_Hawk_47M_HT = [23.6104,12.1889,18.0841,17.9769, 17.5496, 16.5607, 35.8565, 18.5137, 17.6161, 17.7134]
error_Hawk_47M_HT = [8.3636,5.74458, 6.29083, 5.25135, 1.96414, 6.05777, 5.09818, 6.0155,2.31729, 5.36715]



apio_MN_16M_HT = [5.2879, 4.8460, 4.7543, 5.2388]
error_MN_16M_HT = [0.291889, 0.388085, 1.93841, 1.59021]

apio_MN_16M_noHT = [1.9340, 1.7466, 2.1990, 1.3819, 0.9530]
error_MN_16M_noHT = [1.42236, 3.91184, 3.28432, 3.17905, 4.7972]


apio=apio_Hawk_16M_HT
error=error_Hawk_16M_HT

x = np.arange(len(apio))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(8,12))
rects1 = ax.bar(x,apio, width,yerr=error)
#rects2 = ax.bar(x + width/2, original, width, label='ORIGINAL')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Speedup (%) [averaged over 12 hour run]')
ax.set_xlabel('Runs (Different nodes)')
ax.set_title('Speedup for APIO on single node Hawk (128 cores, HT) - 16M cells (1\u0394t)')
ax.set_xticks(x)
#ax.set_xticklabels(apio)
#ax.legend()


def autolabel(rects1):
    """Attach a text label above each bar in *rects*, displaying its height."""
    i=0
    for rect in rects1:
        height = rect.get_height() 
        err = error[i]
        ax.annotate('{} %\n \u00B1 {}%'.format(round(height,2),round(err,2)),
                    xy=(rect.get_x() + rect.get_width() , height),
                    xytext=(5, 18*err),  # 5 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
        i+=1


autolabel(rects1)

fig.tight_layout()

plt.show()
