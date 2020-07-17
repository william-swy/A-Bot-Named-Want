import asyncio
import json
import os
import shutil

import youtube_dl
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands
from discord.utils import get

import custom_errors
import utils
import youtube_query


class Music(commands.Cog):
    YOUTUBE_URL_BASE = 'https://www.youtube.com/watch?v='
    DATA_DIR = utils.DATA_DIR
    CACHED_DIR = f'{DATA_DIR}//cached_music'
    MUSIC_DICT_DIR = f'{CACHED_DIR}//cached_music_dict.json'
    CACHED_MUSIC_DIR = f'{CACHED_DIR}//music'
    CACHED_SONG_QUOTA = 50

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.name = None
        self.url = None
        self.queues = []
        self.playing = None
        self.is_playing = asyncio.Event()
        self.is_waiting = asyncio.Event()

    # plays song in voice client
    @commands.command()
    async def play(self, ctx: commands.Context, *args):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        # check if command can be called
        if len(args) == 0 and len(self.queues) == 0:
            await ctx.send('No song to play')
            return
        elif len(args) == 0 and voice.is_playing():
            await ctx.send("A song is already playing")
            return
        elif len(args) == 0 and voice.is_paused():
            await ctx.send('There is currently a song paused, type `?resume` to resume or `?skip` to skip')
            return
        elif len(args) != 0:
            await self.get_url(args)

            # see if the song is cached
            is_cached = await self.is_song_cached()

            await ctx.send('Getting everything ready now')

            if not is_cached:
                await self.download_music()
                await self.check_cache_size()
                await self.move_to_cache()

            if len(self.queues) != 0:
                await ctx.send(f'There are currently {len(self.queues)} songs queued, '
                               f'your song has been added to the queue')
                self.queues.append(self.name)
                return

            self.queues.append(self.name)

        # create task to play queue
        self.playing = asyncio.create_task(self.loop(ctx, voice))
        self.is_waiting.set()  # awaken task to start playing queue

    # play until queue is empty, latch system to make sure current song is done before playing next
    async def loop(self, ctx, voice):
        while len(self.queues) > 0:
            self.is_playing.clear()
            await self.is_waiting.wait()
            self.play_audio(voice)
            song_name = self.queues[0].rsplit('-', 2)
            await ctx.send(f'Playing {song_name[0]}')
            print('Playing\n')
            await self.is_playing.wait()

    # remove finished song from queue
    def _delete(self, e):
        self.queues.pop(0)
        self.is_playing.set()
        if len(self.queues) == 0:
            self.is_waiting.clear()

    # return true if song is cached, otherwise false
    async def is_song_cached(self):
        if os.path.isfile(self.MUSIC_DICT_DIR):
            json_file = open(self.MUSIC_DICT_DIR, 'r')
            data = json.load(json_file)

            for key, value in data.items():
                if key == self.url:
                    self.name = value
                    return True
            json_file.close()
        else:
            json_file = open(self.MUSIC_DICT_DIR, 'w')
            json.dump({}, json_file)
            json_file.close()
        return False

    # play mp3 of song in voice channel
    def play_audio(self, voice):
        voice.play(FFmpegPCMAudio(self.CACHED_MUSIC_DIR + '\\' + self.queues[0]), after=self._delete)
        voice.source = PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

    # ensure cache size limit is not exceeded
    # remove oldest cached song when quota is reached
    async def check_cache_size(self):
        song_paths = self.CACHED_DIR + '\\music'
        list_of_song_paths = os.listdir(song_paths)
        num_song_cached = len(list_of_song_paths)

        if num_song_cached >= self.CACHED_SONG_QUOTA:
            full_path = [(song_paths + '/{0}').format(x) for x in list_of_song_paths]
            oldest_file = min(full_path, key=os.path.getctime)

            # prevent a currently queued song from being deleted
            for song in self.queues:
                if song in oldest_file:
                    raise custom_errors.TooManySongs()

            os.remove(oldest_file)
            await self.delete_song_data(oldest_file)

    # removes the specified song data from cached_music_dict.json
    async def delete_song_data(self, file_name):
        json_file_read = open(self.MUSIC_DICT_DIR, 'r')
        data = json.load(json_file_read)
        json_file_read.close()

        def find_key():
            for key, value in data.items():
                if value == file_name:
                    return key
            return None

        key_value = find_key()
        if key_value is not None:
            del data[key_value]
            json_file_write = open(self.MUSIC_DICT_DIR, 'w')
            json.dump(data, json_file_write)
            json_file_write.close()

    async def move_to_cache(self):
        # move file to cached_music folder
        for file in os.listdir(utils.MAIN_DIR):
            if file.endswith('.mp3'):
                self.name = file
                break
        shutil.move(self.name, self.CACHED_MUSIC_DIR)

        # update song data
        await self.add_song_data(file=self.name, url=self.url)

    # adds song data to file
    async def add_song_data(self, file, url):
        # check if there is a file, if not create one
        if not os.path.isfile(self.MUSIC_DICT_DIR):
            cached_music_file = open(self.MUSIC_DICT_DIR, 'w')
            json.dump({}, cached_music_file)
            cached_music_file.close()

        json_file_read = open(self.MUSIC_DICT_DIR, 'r')
        data = json.load(json_file_read)
        json_file_read.close()

        def check_data():
            for key in data:
                if key == url:
                    return False
            return True

        update_data = check_data()

        if update_data:
            data[url] = file
            json_file_write = open(self.MUSIC_DICT_DIR, 'w')
            json.dump(data, json_file_write)
            json_file_write.close()

    # downloads music from url
    async def download_music(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Downloading audio now\n')
            ydl.download([self.url])

    # gets url of youtube video
    async def get_url(self, args):
        if len(args) == 1 and self.YOUTUBE_URL_BASE in args[0]:
            self.url = args[0]
        else:
            keywords = ' '.join(args)
            youtube_search = youtube_query.YoutubeQuery()
            self.url = youtube_search.search_youtube(keywords)

    # pauses current playing song
    @commands.command()
    async def pause(self, ctx: commands.Context):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print('Music paused')
            voice.pause()
            await ctx.send('Music paused')
        else:
            print('Music not playing, failed pause')
            await ctx.send('Music not playing, failed pause')

    # resumes current paused song
    @commands.command()
    async def resume(self, ctx: commands.Context):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print('Music resumed')
            voice.resume()
            await ctx.send('Music resumed')
        else:
            print('Music is not paused, failed resume')
            await ctx.send('Music is not paused, failed resume')

    # skips to next song in queue
    @commands.command()
    async def skip(self, ctx: commands.Context):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print('Music skipped')
            voice.stop()
            self.playing.cancel()
            self.is_waiting.clear()  # reset latch
            await ctx.send('Music skipped')

            # create task to play queue
            self.playing = asyncio.create_task(self.loop(ctx, voice))
            self.is_waiting.set()  # awaken task to start playing queue
        else:
            print('No music playing, failed to skip')
            await ctx.send('No music playing, failed to skip')

    # add a song to the queue
    @commands.command()
    async def queue(self, ctx: commands.Context, *args):
        if len(args) == 0:
            await ctx.send('Give me a song to play')
            return

        await self.get_url(args)

        # see if the song is cached
        is_cached = await self.is_song_cached()

        if not is_cached:
            await self.download_music()
            await self.check_cache_size()
            await self.move_to_cache()

        self.queues.append(self.name)

        await ctx.send('Song added to queue')
