import matplotlib
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn')
labels = ['chloesaddiction', 'fitnessblender', 'bgfilms', 'bonappetitdotcom']
average_2019 = [2.0029281199965454, 2.003630384005495, 2.0326563631171086, 2.0244468737637833]
average_2020 = [2.0050131609842725, 2.0003333350400148, 2.000908357388021, 2.0]
x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, average_2019, width, color='#00203fff', label='2019')
rects2 = ax.bar(x + width/2, average_2020, width, color="#adefd1ff", label='2020')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Average Growth Rate for a Month in a Year')
ax.set_xlabel('Channel Name')
ax.set_title('Comparison of average growth rate of subscribers in a specific month of a year')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.ylim(1.9, 2.1)


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


# autolabel(rects1)
# autolabel(rects2)

fig.tight_layout()

plt.show()