from Scraper import RedditCrawler
import requests
from pprint import pprint
import moviepy.editor as mp
from PIL import Image
from pathlib import Path
from utils import *
import os
from configparser import ConfigParser
from ast import literal_eval
import time, datetime
rc = RedditCrawler("animemes")


class VideoGenerator:
    def __init__(self, settings, videoconfig):
        self.config = ConfigParser()
        self.config.read(settings)

        self.stock = self.config.get("directories", "stock")
        self.generated_images = self.config.get("directories", "generated_images")
        self.generated_videos = self.config.get("directories", "generated_videos")
        self.stock_audios = self.config.get("directories", "stock_audios")
        self.stock_videos = self.config.get("directories", "stock_videos")

        self.accepted_media_formats = literal_eval(self.config.get("settings", "accepted_media_formats"))
        self.video_formats = literal_eval(self.config.get("settings", "video_formats"))
        self.image_formats = literal_eval(self.config.get("settings", "image_formats"))

        self.all_stock_audios = [os.path.join(self.stock_audios, path) for path in os.listdir(self.stock_audios)]
        self.all_stock_videos = [os.path.join(self.stock_videos, path) for path in os.listdir(self.stock_videos)]

        with open(videoconfig, "r") as f:
            self.video_and_audio_settings = json.loads(f.read())

    def check_is_media(self, url: str):
        for i in self.accepted_media_formats:
            if url.endswith(i):
                return True, i
        return False, None

    def check_is_video(self, fp):
        for i in self.video_formats:
            if fp.endswith(i):
                return True, i
        return False, None

    def check_is_image(self, fp):
        for i in self.image_formats:
            if fp.endswith(i):
                return True, i
        return False, None

    def resize_media(self, video_dimensions, media, x_padding: int, y_padding: int):
        is_video, video_extension = self.check_is_video(media)
        is_image, image_extension = self.check_is_image(media)
        if is_video:
            media_size = mp.VideoFileClip(media).size
        if is_image:
            _image = Image.open(media).convert('RGB')
            media_size = _image.size

        media_aspect_ratio = media_size[1] / media_size[0]
        video_aspect_ratio = video_dimensions[1] / video_dimensions[0]
        new_image_dimensions = (0, 0)

        if media_aspect_ratio > video_aspect_ratio:
            if media_size[1] != (maximum_image_size_y := video_dimensions[1] - y_padding):
                new_image_dimensions = round(maximum_image_size_y / media_aspect_ratio), maximum_image_size_y
        else:
            if media_size[0] != (maximum_image_size_x := video_dimensions[0] - x_padding):
                new_image_dimensions = maximum_image_size_x, round(maximum_image_size_x * media_aspect_ratio)

        if is_video:
            video = mp.VideoFileClip(media).resize(new_image_dimensions)
            if media.endswith(".gif"):
                video.write_gif(media, logger=None)
            else:
                video.write_videofile(media, threads=16, logger=None)

        if is_image:
            _image = _image.resize(new_image_dimensions)
            _image.save(media)

        return media

    def generate(self):
        video_length = self.video_and_audio_settings["video_length"]

        images = self.video_and_audio_settings["other_images"]
        if (number_of_reddit_images := self.video_and_audio_settings["reddit_images"]) != 0:
            images += self.get_reddit_images(number_of_reddit_images, self.generated_images, sfw=True)

        if self.video_and_audio_settings["randomise_video"]:
            all_video_bases = random(self.all_stock_videos, len(images), self.video_and_audio_settings["no_repeat_video"])
        else:
            all_video_bases = list(self.video_and_audio_settings["stock_video"]*len(images))

        if self.video_and_audio_settings["randomise_audio"]:
            all_audio_bases = random(self.all_stock_audios, len(images), self.video_and_audio_settings["no_repeat_audio"])
        else:
            all_audio_bases = list(self.video_and_audio_settings["stock_audio"]*len(images))

        for index, media in enumerate(images):
            try:
                current_base_video = mp.VideoFileClip(all_video_bases[index]).subclip(0, video_length)
                current_base_audio = mp.AudioFileClip(all_audio_bases[index]).subclip(0, video_length)

                if self.check_is_video(media)[0]:
                    overlay = mp.VideoFileClip(self.resize_media(current_base_audio.size, media, 20, 20))
                    overlay = overlay.loop(duration=video_length)

                if self.check_is_image(media)[0]:
                    overlay = mp.ImageClip(self.resize_media(current_base_video.size, media, 20, 20))

                overlay = overlay.set_duration(video_length)
                overlay = overlay.set_position('center', 'center')
                overlay = overlay.set_start(0)

                export = mp.CompositeVideoClip([current_base_video, overlay])
                export = export.set_audio(current_base_audio)
                export.write_videofile(f"{self.generated_videos}/video{index}-{datetime.datetime.now().strftime('%S_%M_%H-%d_%m_%Y')}.mp4", threads=16, logger=None)
                print(f"Finished writing to video {index + 1}...")
            except:
                print(f"Failed to write to video {index + 1}")

    def get_reddit_images(self, n, image_directory, sfw):
        start = time.time()
        paths = []

        while len(paths) != n:
            limit = n * 2
            post_ids = rc.retrieve_posts_id(limit)
            for i in post_ids:
                submissionObj = rc.retrieve_post(i)
                is_sfw = False if sfw and submissionObj.over_18 else True

                url = submissionObj.url
                accepted, extension = self.check_is_media(url)

                if accepted and is_sfw:
                    img_data = requests.get(url).content
                    path = f"{image_directory}\image{i}-{datetime.datetime.now().strftime('%S_%M_%H-%d_%m_%Y')}{extension}"
                    with open(path, 'wb') as handler:
                        handler.write(img_data)
                    paths.append(path)

                    if len(paths) == n:
                        return paths
                    if time.time() - start > 50:
                        exit(0)


if __name__ == '__main__':
    t = timer()
    t.start()
    vg = VideoGenerator("projectsettings.config", "videoconfig.json")
    vg.generate()
    t.end()

    