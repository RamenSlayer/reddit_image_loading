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

def GetImages(subreddit = "aww", number = 1, sort = "created_utc", alpha=False, before = None, after=None):
    
    """
    subreddit: the subreddit you want to pull images from
    
    sort types: score, created_utc. Basically sorting by "top all time" or "new"
    I highly suggest using new instead of top, as I could pull 40,000 images in one go using new, while top broke at thousand. 
    
    number: limit on the number of images you want to pull. For constant stream you can try float("inf")
    
    alpha: keeps alpha channel if there is one. For working with numpy you probably want to keep it at false
    
    before: date in format "yyyy-mm-dd" (example: "2020-01-01")
            or date time in format "yyyy-mm-dd hh:mm:ss" (example: "2020-01-01 22:22:22")
    
    after: date in format "yyyy-mm-dd" (example: "2020-01-01")
           or date time in format "yyyy-mm-dd hh:mm:ss" (example: "2020-01-01 22:22:22")
    """
    
    global api
    
    posts = api.search_submissions(subreddit = subreddit,
                                   filter = ["url", "permalink"],
                                   sort_type = sort,
                                   before = before,
                                   after = after)
    
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
        
        # print(post.permalink)
        
        # avoids having alpha channel
        if alpha:
            yield tmp.convert("RGBA")
        else:
            yield tmp.convert("RGB")
        count += 1
        if count >= number:
            break
