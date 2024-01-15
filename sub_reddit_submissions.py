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

subreddit = reddit.subreddit('AskMen')
top_submissions = subreddit.top(time_filter='all', limit=None)
csv_name = 'ask_men_top_submissions'

titles = []
dates = []
authors = []
scores = []
saves = []
stickies = []
nums_comments = []
urls = []

for submission in top_submissions:
  titles.append(submission.title)
  dates.append(submission.created_utc)
  if submission.author:
    authors.append(submission.author.name)
  else:
    authors.append("Deleted User")
  scores.append(submission.score)
  saves.append(submission.saved)
  stickies.append(submission.stickied)
  nums_comments.append(submission.num_comments)
  urls.append(submission.url)

data  = {
  'Title': titles,
  'Date': dates,
  'Author': authors,
  'Upvotes Score': scores,
  'Saved': saves,
  'Stickied': stickies,
  'Number of Comments': nums_comments,
  'URL': urls
}

df=pd.DataFrame(data)
df.to_csv('{}.csv'.format(csv_name))
print(f"csv {csv_name} has been created with {len(titles)} submissions completed")
