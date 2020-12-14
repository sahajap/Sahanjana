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

import matplotlib.pyplot as plt
from datetime import datetime, timedelta
#chloeting
dates = [
   datetime(2019, 4, 25),
   datetime(2019, 5, 6),
   datetime(2019, 5, 16),
   datetime(2020, 6, 26),
   datetime(2019, 7, 6),
   datetime(2019, 7, 18)
]
#bgfilms
dates2 = [
   datetime(2019, 4, 25),
   datetime(2019, 5, 6),
   datetime(2019, 5, 16),
   datetime(2020, 8, 31),
   datetime(2020, 9, 10),
   datetime(2020, 9, 22)
]
 
#fitnessblender
dates3 = [
   datetime(2019, 6, 3),
   datetime(2019, 6, 18),
   datetime(2019, 6, 27),
   datetime(2020, 5, 15),
   datetime(2020, 5, 22),
   datetime(2020, 6, 6)
]
 
#fitnessblender
dates4= [
   datetime(2019, 4, 26),
   datetime(2019, 5, 7),
   datetime(2019, 5, 20),
   datetime(2020, 9, 12),
   datetime(2020, 9, 23),
   datetime(2020, 10, 4)
]
 
#chloeting
y1 = [2.0, 2.008, 2.007, 2.009, 2.0, 2.008]
#bgfilms
y2 = [2.0, 2.002, 2.002, 2.001, 2.0, 2.004]
#fitnessblender
y3 = [2.0 , 2.002, 2.0, 2.0, 2.0016, 2.0]
#bonappetitdotcom
y4 = [2.003 , 2.0, 2.003, 2.0, 2.0, 2.0]
 
plt.plot(dates, y1)
#, label = "chloesaddiction", color = 'red')
plt.plot(dates2, y2)
#, label = "bgfilms", color = 'purple')
plt.plot(dates3, y3)
#, label = "fitnessblender",  color = 'green')
plt.plot(dates3, y4)
#, label = "bonappetitdotcom", color = 'blue')
 
 
plt.xlabel('Date')
# Set the y axis label of the current axis.
plt.ylabel('Daily Growth Rate (%)')
# Set a title of the current axes.
plt.grid(True)
plt.ylim((1,3.0))
 
plt.title('YouTube Channel Growth Rates')
# show a legend on the plot
plt.legend()
# Display a figure.
plt.show()

import matplotlib.pyplot as plt
from datetime import datetime, timedelta
 
#chloeting
dates = [
   datetime(2019, 4, 25),
   datetime(2019, 5, 6),
   datetime(2019, 5, 19),
   datetime(2020, 6, 26),
   datetime(2020, 7, 6),
   datetime(2020, 7, 18)
]
#bgfilms
dates2 = [
   datetime(2019, 4, 25),
   datetime(2019, 5, 6),
   datetime(2019, 5, 16),
   datetime(2020, 8, 31),
   datetime(2020, 9, 10),
   datetime(2020, 9, 22)
]
 
#fitnessblender
dates3 = [
   datetime(2019, 6, 3),
   datetime(2019, 6, 18),
   datetime(2019, 6, 27),
   datetime(2020, 5, 15),
   datetime(2020, 5, 22),
   datetime(2020, 6, 6)
]
 
#bonappetitdotcom
dates4= [
   datetime(2019, 4, 26),
   datetime(2019, 5, 7),
   datetime(2019, 5, 20),
   datetime(2020, 9, 12),
   datetime(2020, 9, 23),
   datetime(2020, 10, 4)
]
 
#chloeting
y1 = [1.19, 1.24, 1.27, 11.0, 11.6, 12.3]
#bgfilms
y2 = [4.18, 4.23, 4.23, 7.72, 7.78, 7.86]
#fitnessblender
y3 = [5.71 , 5.72, 5.73, 6.23, 6.24, 6.27]
#bonappetitdotcom
y4 = [3.67, 3.72, 3.8, 5.99, 5.99, 5.99]
 
 
plt.plot_date(dates, y1, color = 'blue', label = 'bgfilms')
plt.plot_date(dates2, y2, color = 'red' , label = 'chloesaddiction')
plt.plot_date(dates3, y3, color = 'purple' , label = 'fitnessblender')
plt.plot_date(dates4, y4, color = 'green' , label = 'bonappetitdotcom')
plt.grid(True)
plt.ylim((1 , 15))
plt.xlabel('Date')
# Set the y axis label of the current axis.
plt.ylabel('Number of Subscribers (in millions)')
# Set a title of the current axes.
plt.title('Change in Number of Subscribers Over Time')
# show a legend on the plot
plt.legend()
# Display a figure.
plt.show()
