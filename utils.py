import time
import json
from Scraper import RedditCrawler
from random import randrange
from pydub import AudioSegment
import moviepy.editor as mp

lorem_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce interdum mi tincidunt, blandit eros in, viverra purus. Nulla non diam dignissim, tempus libero mollis, ullamcorper nunc. Aliquam turpis tellus, semper a sagittis et, tristique sed lectus. Pellentesque tincidunt ante ut lacinia fringilla. Duis elementum quis lectus non lobortis. In finibus turpis et augue vestibulum, vitae viverra urna pellentesque. Ut dolor arcu, dictum sed aliquam ut, elementum mattis velit. Proin vel sapien eget leo finibus viverra a eget lorem. Phasellus sed interdum leo, sed porttitor eros. Nam eu quam et ex mollis aliquet. Nunc lacinia, odio sit amet posuere malesuada, massa sapien sagittis nisi, ut maximus eros ante at est. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Donec nec tempor dui. Nunc congue viverra quam at dapibus. Donec et nibh euismod, mollis nunc ac, porttitor magna. Aenean hendrerit urna rhoncus, posuere tellus dictum, imperdiet sem.

Nunc fringilla sapien eu diam consectetur laoreet. Sed condimentum finibus imperdiet. Etiam non sem nec enim semper volutpat sed sed libero. Aliquam nisi lacus, iaculis et orci id, varius aliquam erat. Morbi porttitor fringilla risus vitae commodo. Aliquam purus ante, ornare ullamcorper est sit amet, egestas malesuada sem. Phasellus quis laoreet dolor. Etiam facilisis diam fermentum euismod consequat. Vestibulum tempor condimentum sapien nec pellentesque. In mollis mi nec urna eleifend, eget facilisis est rutrum. Nullam iaculis venenatis enim. Praesent molestie nibh ligula, ut dignissim ipsum ornare ac.

Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aliquam tempor, erat in suscipit euismod, diam neque tempus odio, ut elementum nibh massa vel ante. Sed quis tristique ipsum, et semper nisi. Phasellus finibus nunc quis maximus bibendum. Aenean rutrum nisl non purus blandit condimentum. Etiam tempor, urna eu facilisis egestas, mi nibh suscipit est, sed sagittis augue ante vitae turpis. Praesent vestibulum augue felis, blandit elementum justo varius eget. Integer sagittis in lorem vitae tempor. Proin bibendum ultrices risus eu vulputate. Sed scelerisque sapien nec dapibus bibendum. Phasellus lobortis urna neque, a vehicula urna tincidunt quis. Quisque dictum varius sagittis. Nullam a mauris consectetur, auctor mauris id, hendrerit odio. Suspendisse potenti. Fusce placerat vulputate eros eget lobortis. Suspendisse vestibulum maximus enim, vel pharetra dolor suscipit consequat.

Sed aliquet sapien mauris. In interdum, nunc et viverra mollis, mauris urna tincidunt nisl, a condimentum nibh tellus accumsan lectus. Vivamus egestas neque a vestibulum aliquet. Maecenas id ex vulputate, volutpat orci nec, volutpat tellus. Aenean justo purus, porttitor quis quam varius, iaculis imperdiet nisi. Mauris rutrum quis arcu id cursus. Sed nec tortor varius, consectetur est a, feugiat sapien. Fusce vitae felis urna. Integer eget suscipit metus. Aenean et lectus vitae nibh tristique finibus vel non quam. In vitae efficitur diam. Phasellus sodales id dui in lacinia.

Nam sodales velit velit, eu placerat ex malesuada non. Vivamus in augue ante. Donec venenatis ligula sed odio tincidunt rutrum. Nam pharetra enim in interdum maximus. Etiam quis viverra orci, a facilisis velit. Ut mi mauris, congue non lorem et, suscipit venenatis purus. Duis in orci laoreet lorem sagittis dictum nec nec diam. Vestibulum sapien sem, mollis sed pulvinar non, volutpat a justo. Integer tristique tortor nunc, nec dignissim diam condimentum a. Vestibulum vel metus at mi maximus hendrerit. Nam ut magna vel dui gravida ultrices. Donec pulvinar sapien eget mauris pharetra, a pharetra mi porta. Nullam euismod lorem ex, sit amet congue felis feugiat ut."""


class timer:
    def __init__(self):
        self.time = 0

    def start(self):
        self.time = time.time()

    def end(self, rnd=True):
        if rnd:
            print(time.time() - self.time)


def random(iterable, n, remove_after_selection: bool = True):
    _iterable = iterable.copy()
    length_of_iterable = len(_iterable)
    selections = []
    for i in range(n):
        selection = _iterable[randrange(0, length_of_iterable)]
        selections.append(selection)
        if remove_after_selection:
            _iterable.remove(selection)

    return selections


def chop_audio(start, end, audio, new=None):
    _audio = AudioSegment.from_file(audio)[start * 1000:end * 1000]
    if new:
        path = new
    else:
        path = audio
    _audio.export(path)


def chop_video(start, end, video, new=None):
    _video = mp.VideoFileClip(video)
    _video = _video.subclip(start, end)
    if new:
        path = new
    else:
        path = video
    _video.write_videofile(path)


if __name__ == '__main__':
    print(random(['a', 'b', 'c', 'd', 'e', 'f', 'g'], 3))
