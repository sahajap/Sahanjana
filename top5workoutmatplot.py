import matplotlib.pyplot as plt

# plt.style.use('ggplot')

# x = ['MadFit', 'Pamela Reif', 'Chloe Ting', 'Vicky Justiz', 'Mady Morrison']
# energy = [2.74, 1.37, 1.67, 3.69, 1.34]

# x_pos = [i for i, _ in enumerate(x)]

# plt.bar(x_pos, energy, color='pink')
# plt.xlabel("Top 5 Workout Youtubers from List of Top50Videos")
# plt.ylabel("Percentage of Likes")
# plt.title("Percentage of Likes for Videos in Top 50 workout videos")

# plt.xticks(x_pos, x)

# plt.show()

# plt.style.use('ggplot')


# x = ['SAM THE COOKING GUY', 'You Suck At Cooking', 'HidaMari Cooking', 'Kdeb Cooking', 'Village Cooking Channel']
# energy = [3.4, 6.9, 2.2, 1.2, 3.3]

# x_pos = [i for i, _ in enumerate(x)]
# plt.figure(figsize=(12,6))
# plt.bar(x_pos, energy, color='#3bffe8')
# wspace = 1
# plt.xlabel("Top 5 Cooking Youtubers from List of Top50Videos")
# plt.ylabel("Percentage of Likes")
# plt.title("Percentage of Likes for Videos in Top 50 cooking videos")
# plt.xticks(x_pos, x)

# plt.show()

plt.style.use('seaborn-pastel')


x = ['chloesaddiction', 'fitnessblender', 'bgfilms', 'bonappetitdotcom']
energy = [24743.8, 1530, 7131, 4402]

x_pos = [i for i, _ in enumerate(x)]
plt.figure(figsize=(12,6))
plt.bar(x_pos, energy, color='#ffba7a')
wspace = 1
plt.xlabel("Channel Name")
plt.ylabel("Number of new subscribers per day on average")
plt.title("Number of new subscribers per day on average for 4 Youtube Channels")
plt.xticks(x_pos, x)

plt.show()
