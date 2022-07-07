import praw
from psaw import PushshiftAPI

api = psaw.PushshiftAPI()

from PIL import Image
import requests
from io import BytesIO

def GetImages(subreddit = "aww", number = 9, sort = "created_utc", alpha = False):
    
    """
    subreddit: the subreddit you want to pull images from
    
    sort types: score, created_utc. Basically sorting by "top all time" or "new". I highly suggest using new instead of top, as I could pull 40,000 images in one go using new, while top broke at thousand. 
    
    number: limit on the number of images you want to pull. For constant stream you can try float("inf")
    
    alpha: keeps alpha channel if there is one. For working with numpy you probably want to keep it at false
    
    """
    
    global api
    
    posts = api.search_submissions(subreddit = subreddit, filter = ["url", "permalink"], sort_type = sort)
    
    count = 0
    
    for post in posts:
        url = str(post.url)
        
        # sadly nothing I can do about this try-except.
        
        if "png" in url or "jpg" in url or "jpeg" in url:
            try:
                response = requests.get(url)
            except:
                continue
        else:
            continue

        status = response.status_code
        # was getting UnidentifiedImageError but removing these codes should eliminate the error
        # also filters out "this image was deleted" image from stream
        if status == 404 or status == 406 or status == 504:
            continue

        tmp = Image.open(BytesIO(response.content))


        if alpha:
            yield tmp
        else:
            yield tmp.convert("RGB")
        count += 1
        if count >= number:
            break
