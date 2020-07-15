import matplotlib
import matplotlib.pyplot as plt
import numpy as np


apio =  [12.8363, 20.1325, 19.1207, 22.4712, 20.3637, 19.1664, 19.6664, 18.3873, 20.3834, 19.2077, 23.3460]

error= [0.540572, 1.53785, 7.21405, 5.5195, 5.31839, 2.08903, 5.93908, 2.16524, 1.91775, 2.5841, 3.11317]


x = np.arange(len(apio))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(8,8))
rects1 = ax.bar(x,apio, width,yerr=error)
#rects2 = ax.bar(x + width/2, original, width, label='ORIGINAL')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Speedup (%) [averaged over 12 hour run]')
ax.set_xlabel('Runs')
ax.set_title('Speedup for APIO on one node (128 cores) - 16M cells (1\u0394t)')
ax.set_xticks(x)
#ax.set_xticklabels(apio)
#ax.legend()


def autolabel(rects1):
    """Attach a text label above each bar in *rects*, displaying its height."""
    i=0
    for rect in rects1:
        height = rect.get_height() 
        err = error[i]
        ax.annotate('{} %'.format(height),
                    xy=(rect.get_x() + rect.get_width() , height),
                    xytext=(0, 18*err),  # 5 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
        i+=1


autolabel(rects1)

fig.tight_layout()

plt.show()
