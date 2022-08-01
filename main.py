# !pip install psaw
import psaw
from psaw import PushshiftAPI
import numpy as np

api = psaw.PushshiftAPI()

from PIL import Image, UnidentifiedImageError

# Image might be too big, causing an exception from PIL
# Image.MAX_IMAGE_PIXELS = None

import requests
from io import BytesIO

def GetImages(subreddit = "aww", number = 9, sort = "created_utc"):
    
    """sort types: score, created_utc"""
    
    global api
    
    posts = api.search_submissions(subreddit = subreddit, filter = ["url", "permalink"], sort_type = sort)
    
    count = 0
    
    for post in posts:
        url = str(post.url)
        
        if "png" in url or "jpg" in url or "jpeg" in url:
            try:
                response = requests.get(url)
            except:
                # print("RequestError")
                # print(post.permalink)
                continue
        else:
            continue

        status = response.status_code
        if status == 404 or status == 406 or status == 504:
            continue

        try:
            tmp = Image.open(BytesIO(response.content))
        except UnidentifiedImageError:
            # print(post.permalink)
            continue
        # not sure if possible to check size before loading as image
        except Image.DecompressionBombError:
            continue
        except OSError:
            continue

        # avoids having alpha channel
        yield tmp.convert("RGB")
        count += 1
        if count >= number:
            break
