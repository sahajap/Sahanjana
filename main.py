from youtube import Stats

API_KEY = 'AIzaSyDcg05zH6fsV5z4dqeLs6Pb3tNsx6K9GtM'
channel_id = "UCpQ34afVgk8cRQBjSJ1xuJQ"

yt = Stats(API_KEY, channel_id)
yt.get_channel_statistics()


