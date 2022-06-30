import praw
from psaw import PushshiftAPI

api = psaw.PushshiftAPI()

from PIL import Image
import requests
from io import BytesIO

def GetImages(sub = "aww", number = 9, sort = "score"):
    
    """sort types: score, created_utc"""
    
    global api
    
    submissions = api.search_submissions(subreddit = sub, filter = ['url'], sort_type=sort)
    
    count = 0
    for post in submissions:
        url = str(post.url).strip("\|/")
        
        # check if a post is an image
        
        if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):
            
            # pull an image
            response = requests.get(url)
            yield Image.open(BytesIO(response.content))
            count += 1
            # end generator when required number of images reached
            if count > number - 1:
                break
