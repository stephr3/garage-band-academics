import pandas as pd
import praw
from praw.models import MoreComments
from dotenv import load_dotenv
import os

load_dotenv()

reddit = praw.Reddit(client_id = os.getenv('CLIENT_ID'),
                     client_secret = os.getenv('CLIENT_SECRET'),
                     user_agent = os.getenv('USER_AGENT'),
                     username = os.getenv('USERNAME'),
                     password = os.getenv('PASSWORD'))

submission_url = 'https://www.reddit.com/r/AskMen/comments/165rp8z/what_blunt_advice_would_you_offer_women_if_you'
submission = reddit.submission(url=submission_url)
csv_name = 'blunt_advice'

all_comments = []

submission.comments.replace_more(limit=None)
for comment in submission.comments.list():
    all_comments.append(comment)

comment_authors = []
comment_is_submitters = []
comment_times = []
comment_parent_ids = []
comment_bodies = []
comment_scores = []
comment_urls = []

for comment in all_comments:
    comment_authors.append(comment.author.name if comment.author else 'Deleted')
    comment_is_submitters.append(comment.is_submitter)
    comment_times.append(comment.created_utc)
    comment_parent_ids.append(comment.parent_id)
    comment_bodies.append(comment.body)
    comment_scores.append(comment.score)
    comment_urls.append(comment.permalink)

data  = {
  'Author': comment_authors,
  'Is Original Poster?': comment_is_submitters,
  'Time': comment_times,
  'Parent Comment ID': comment_parent_ids,
  'Body': comment_bodies,
  'Score': comment_scores,
  'URL': comment_urls
}

df=pd.DataFrame(data)
df.to_csv('{}.csv'.format(csv_name))
print(f"csv {csv_name} has been created with {len(all_comments)} comments completed")
