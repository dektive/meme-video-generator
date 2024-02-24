import praw
from praw import Reddit
import os


generated_media = "generated_media"
reddit = praw.Reddit(client_id='4K038f_UDGzRvv-aNTguQw',
                     client_secret='aBNKxPKSWamAxfz2KX0P-mtv_lAiMA',
                     username='ItWasWonderfulToSee',
                     password='hYr3875jHnhgoII',
                     user_agent='aredditscraperbot')
# reddit = praw.Reddit(client_id='',
#                      client_secret='',
#                      username='',
#                      password='',
#                      user_agent='')

class RedditCrawler:
    def __init__(self, Subreddit: str):
        self.subreddit = reddit.subreddit(Subreddit)

    def retrieve_posts_id(self, n):
        return [i.id for i in self.subreddit.hot(limit=n) if i.author is not None]

    def retrieve_single_post(self):
        return self.retrieve_posts_id(1)[0]

    def download_post_video(self):
        pass

    @staticmethod
    def retrieve_comments_id(post, n):
        return [comment.id for i, comment in enumerate(reddit.submission(id=post).comments) if i < n and comment.author is not None]

    @staticmethod
    def retrieve_comment(comment_id):
        return reddit.comment(id=comment_id)

    @staticmethod
    def retrieve_post(post_id):
        return reddit.submission(id=post_id)
