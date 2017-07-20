#!/usr/bin/python

import praw
import re

reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("longboarding")

for submission in subreddit.hot(limit=10):
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        if re.search("zealous", comment.body, re.IGNORECASE):
            print(comment.body)
