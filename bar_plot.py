import matplotlib
import matplotlib.pyplot as plt
import numpy as np


apio =  [12.8363, 20.2974, 19.1207, 22.1956, 19.6449, 18.6978, 19.5532, 18.5487, 20.4491, 19.2938]

error= [0.540572, 3.20905, 7.21405, 8.20477, 5.76353, 1.77947, 5.6149, 4.08073, 3.01729, 2.65221]


x = np.arange(len(apio))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(8,12))
rects1 = ax.bar(x,apio, width,yerr=error)
#rects2 = ax.bar(x + width/2, original, width, label='ORIGINAL')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Speedup (%) [averaged over 12 hour run]')
ax.set_xlabel('Runs')
ax.set_title('Speedup for APIO on single node (128 cores) - 16M cells (1\u0394t)')
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
                    xytext=(0, 21*err),  # 5 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
        i+=1


autolabel(rects1)

fig.tight_layout()

plt.show()
