import matplotlib
import matplotlib.pyplot as plt
import numpy as np


x = np.arange(len(apio))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x-width/2,apio, width,yerr=error_apio,label="APIO")
rects2 = ax.bar(x + width/2, orig, width, yerr=error_orig,label="ORIGINAL")

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Time (s) [averaged over 12 hour run]')
ax.set_xlabel('Runs (Different nodes)')
ax.set_title('Speedup for APIO on 4 nodes MN (192 cores,  HT) - 131M cells (1\u0394t)')
ax.set_xticks(x)
ax.set_yticklabels(labels)
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
