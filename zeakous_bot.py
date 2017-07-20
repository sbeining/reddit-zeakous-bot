#!/usr/bin/python

import praw
import re
import os

def main():
    global comments_replied_to

    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit("longboarding")
    comments_replied_to = load_comments_replied_to()

    for submission in subreddit.hot(limit=10):
        process_submission(submission)

    save_comments_replied_to(comments_replied_to)


def process_submission(submission):
    # Expand all "load more comments" entries
    submission.comments.replace_more(limit=0)

    # Flatten top level comments an replies
    comments = submission.comments.list()

    for comment in comments:
        # Skip if already replied
        if comment.id in comments_replied_to:
            continue

        # Skip if the comment does not contain the magic word
        if not re.search("zealous", comment.body, re.IGNORECASE):
            continue

        process_comment(comment)
        comments_replied_to.append(comment.id)

def process_comment(comment):
    pattern = re.compile("zealous", re.IGNORECASE)

    # Handle lines individually to not quote too much
    for line in comment.body.split("\n"):
        if not re.search("zealous", line, re.IGNORECASE):
            continue

        replyBody = "> " + pattern.sub("**ZEAKOUS**", line)
        replyBody += "\n"
        replyBody += "\n"
        replyBody += "---"
        replyBody += "\n"
        replyBody += "^^\"I've&#32;been&#32;memed&#32;again!\"&#32;-/u/lbibass"

        comment.reply(replyBody)

def load_comments_replied_to():
    if not os.path.isfile("comments_replied_to.txt"):
        result = []
    else:
        with open("comments_replied_to.txt", "r") as f:
           result = f.read()
           result = result.split("\n")
           result = list(filter(None, result))

    return result

def save_comments_replied_to(comment_ids):
    with open("comments_replied_to.txt", "w") as f:
        for comment_id in comment_ids:
            f.write(comment_id + "\n")

if __name__ == '__main__':
    main()
