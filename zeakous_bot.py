#!/usr/bin/python

import praw
import re
import os

reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("longboarding")

if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []
else:
    with open("comments_replied_to.txt", "r") as f:
       comments_replied_to = f.read()
       comments_replied_to = comments_replied_to.split("\n")
       comments_replied_to = list(filter(None, comments_replied_to))

for submission in subreddit.hot(limit=10):
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        if re.search("zealous", comment.body, re.IGNORECASE):
            print(comment.body)
            comments_replied_to.append(comment.id)

# Write our updated list back to the file
with open("comments_replied_to.txt", "w") as f:
    for comment_id in comments_replied_to:
        f.write(comment_id + "\n")
