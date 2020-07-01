import matplotlib
import matplotlib.pyplot as plt
import numpy as np



nprocs = ['24', '48', '96', '192', '384','768']

apio_1T =     [118.8, 72.5, 48.9, 59.5, 76.2, 0]
original_1T = [161.9, 79.7, 51.7, 56.5, 75.2, 0]

apio_2T =     [100.3, 56.8, 35.0, 27.8, 0, 0]
original_2T = [143.5, 59.4, 37.3, 29.2, 0, 0]

apio_4T =     [92.7, 46.1, 27.8, 19.6, 0, 0]
original_4T = [136.1, 47.3, 27.9, 19.7, 0, 0]

apio_10T =     [88.1, 41.8, 22.5, 12.2, 0, 0]
original_10T = [129.7, 42.3, 22.7, 12.7, 0, 0]


apio = apio_10T
original = original_10T


x = np.arange(len(nprocs))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(8,8))
rects1 = ax.bar(x - width/2, apio, width, label='APIO')
rects2 = ax.bar(x + width/2, original, width, label='ORIGINAL')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Time (s) [averaged over 10 runs]')
ax.set_xlabel('ntasks [MPI procs]')
ax.set_title('Runtime savings for the APIO asynchronous pipeline (10\u0394t)')
ax.set_xticks(x)
ax.set_xticklabels(nprocs)
ax.legend()


def autolabel(rects1,rects2):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect1,rect2 in zip(rects1,rects2):
        height = max(rect1.get_height(),rect2.get_height())
        gain = (rect2.get_height() - rect1.get_height())*100/rect2.get_height()
        ax.annotate('{}%'.format(round(gain,3)),
                    xy=(rect1.get_x() + rect1.get_width() , height),
                    xytext=(0, 5),  # 5 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1,rects2)

fig.tight_layout()

plt.show()
