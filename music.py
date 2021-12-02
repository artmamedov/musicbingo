import vlc
import time
import random

#random.seed(0)

class SongPlayer:
    def __init__(self,path,num_songs):
        self.path = path
        self.song_list = [i for i in range(1,num_songs+1)]
        self.queue = self.song_list.copy()
        #random.shuffle(self.queue)
        self.played = []
        self.playing = False
        self.autoplay = True

    def play_next_song(self):
        if self.autoplay:
            while self.autoplay:
                song = self.queue[0]
                self.played.append(self.queue[0])
                self.queue = self.queue[1:]
                player = vlc.MediaPlayer(f'{self.path}/{song}.mp3')
                self.playing = True
                player.play()
                time.sleep(1)
                duration = player.get_length()/1000
                print(f"Playing {song}.mp3, duration is: {duration}")
                #Can make into while playing to allow pause feature
                time.sleep(duration)
        else:
            song = self.queue[0]
            self.played.append(self.queue[0])
            self.queue = self.queue[1:]
            player = vlc.MediaPlayer(f'{self.path}/{song}.mp3')
            self.playing = True
            player.play()
            time.sleep(1)
            duration = player.get_length()/1000
            print(f"Playing {song}.mp3, duration is: {duration}")
            #Can make into while playing to allow pause feature
            time.sleep(duration)
        self.playing = False

    def shuffle(self):
        random.shuffle(self.queue)

    def set_autoplay(self,autoplay_checked):
        self.autoplay = autoplay_checked

    def back(self):
        if len(self.played)>0:
            self.queue = [self.played[-1]] + self.queue
            self.played = self.played[:-1]
