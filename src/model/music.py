import asyncio
import json
import os
import shutil
import re
import typing

import youtube_dl
from discord import FFmpegPCMAudio, PCMVolumeTransformer, Embed, File
from discord.ext import commands
from discord.utils import get

import custom_errors
import utils
import youtube_query


class Music(commands.Cog):
    """Plays music based on mp3"""
    YOUTUBE_URL_BASE = 'https://www.youtube.com/watch?v='
    DATA_DIR = utils.DATA_DIR
    CACHED_DIR = os.path.join(DATA_DIR, 'cached_music')
    MUSIC_DICT_DIR = os.path.join(CACHED_DIR, 'cached_music_dict.json')
    CACHED_MUSIC_DIR = os.path.join(CACHED_DIR, 'music')
    CACHED_SONG_QUOTA = 50

    MELODY_IMG = os.path.join(utils.DATA_DIR, 'melody.jpg')

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.name = None
        self.url = None
        self.queues = []
        self.playing = None
        self.is_playing = asyncio.Event()
        self.is_waiting = asyncio.Event()

    @commands.command()
    async def play(self, ctx: commands.Context, *, args: typing.Optional[str] = '') -> None:
        """plays song in voice client"""
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        # check if command can be called
        if len(args) == 0 and len(self.queues) == 0:
            await ctx.send('No song to play')
            return
        elif len(args) == 0 and voice.is_playing():
            await ctx.send("A song is already playing")
            return
        elif len(args) == 0 and voice.is_paused():
            await ctx.send(f'There is currently a song paused, type `{utils.PREFIX}resume` '
                           f'to resume or `{utils.PREFIX}skip` to skip')
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

    async def loop(self, ctx, voice) -> None:
        """play until queue is empty, latch system to make sure current song is done before playing next"""
        while len(self.queues) > 0:
            self.is_playing.clear()
            await self.is_waiting.wait()
            self.play_audio(voice)
            await ctx.send('playing song')
            await self.is_playing.wait()

    def _delete(self, e) -> None:
        """remove finished song from queue"""
        self.queues.pop(0)
        self.is_playing.set()
        if len(self.queues) == 0:
            self.is_waiting.clear()

    async def is_song_cached(self) -> bool:
        """return true if song is cached, otherwise false"""
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

    def play_audio(self, voice) -> None:
        """play mp3 of song in voice channel"""
        voice.play(FFmpegPCMAudio(os.path.join(self.CACHED_MUSIC_DIR, self.queues[0])), after=self._delete)
        voice.source = PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

    async def check_cache_size(self) -> None:
        """ensure cache size limit is not exceeded
        remove oldest cached song when quota is reached"""
        song_paths = self.CACHED_MUSIC_DIR
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

    async def delete_song_data(self, file_name) -> None:
        """removes the specified song data from cached_music_dict.json"""
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

    async def move_to_cache(self) -> None:
        """move file to cached_music folder"""
        for file in os.listdir(utils.MAIN_DIR):
            if file.endswith('.mp3'):
                self.name = file
                break
        shutil.move(self.name, self.CACHED_MUSIC_DIR)

        # update song data
        await self.add_song_data(file=self.name, url=self.url)

    async def add_song_data(self, file, url) -> None:
        """adds song data to file"""
        # check if there is a file, if not create one
        if not os.path.isfile(self.MUSIC_DICT_DIR):
            cached_music_file = open(self.MUSIC_DICT_DIR, 'w')
            json.dump({}, cached_music_file)
            cached_music_file.close()

        json_file_read = open(self.MUSIC_DICT_DIR, 'r')
        data = json.load(json_file_read)
        json_file_read.close()

        def check_data() -> bool:
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

    async def download_music(self) -> None:
        """downloads music from url"""
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

    async def get_url(self, args) -> None:
        """gets url of youtube video"""
        if self.YOUTUBE_URL_BASE in args:
            self.url = args
        else:
            youtube_search = youtube_query.YoutubeQuery()
            self.url = youtube_search.search_youtube(args)

    @commands.command()
    async def pause(self, ctx: commands.Context) -> None:
        """pauses current playing song"""
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print('Music paused')
            voice.pause()
            await ctx.send('Music paused')
        else:
            print('Music not playing, failed pause')
            await ctx.send('Music not playing, failed pause')

    @commands.command()
    async def resume(self, ctx: commands.Context) -> None:
        """resumes current paused song"""
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print('Music resumed')
            voice.resume()
            await ctx.send('Music resumed')
        else:
            print('Music is not paused, failed resume')
            await ctx.send('Music is not paused, failed resume')

    @commands.command()
    async def skip(self, ctx: commands.Context) -> None:
        """skips to next song in queue"""
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

    @commands.command()
    async def queue(self, ctx: commands.Context, *args) -> None:
        """add a song to the queue"""
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

    @commands.command()
    async def clear(self, ctx: commands.Context) -> None:
        """removes all songs from queue"""
        self.queues = []
        await ctx.send("Queues cleared!")

    def song_embed(self) -> tuple:
        """returns an embed of the songs currently in queue"""

        def get_song_name(name) -> list:
            bracket_regex = r'\(.*\)'
            parenth_regex = r'\[.*\]'
            ft_regex = r'ft.*'
            removed_code = name.split('-')[:2]
            author = removed_code[0]
            first_clean = re.sub(bracket_regex, "", removed_code[1])
            second_clean = re.sub(parenth_regex, "", first_clean)
            final_name = re.sub(ft_regex, '', second_clean)
            ft = re.findall(ft_regex, first_clean)
            if ft:
                ft = ft[0]
            else:
                ft = ''
            final_author = (author + ft).strip(" ")
            return [final_name, final_author]

        image = File(fp=self.MELODY_IMG, filename='melody.jpg')
        msg = Embed(title='Songs', description="Melody has found the following songs", color=0xFFB6C1)
        msg.set_thumbnail(url='attachment://melody.jpg')
        if len(self.queues) == 0:
            msg.add_field(name='NONE', value='Give me a song to play', inline=False)
        else:
            for song in enumerate(self.queues):
                song_details = get_song_name(song[1])
                if song[0] == 0:
                    message = "(Current)"
                else:
                    message = f"(Queued {song[0]}) "
                msg.add_field(name=message + song_details[0], value=song_details[1], inline=False)
        return msg, image

    @commands.command()
    async def songs(self, ctx: commands.Context) -> None:
        """shows all songs in queue"""
        file = self.song_embed()[1]
        embed = self.song_embed()[0]
        await ctx.send(file=file, embed=embed)
