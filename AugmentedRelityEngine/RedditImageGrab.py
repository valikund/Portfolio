import praw
import requests
from PIL import Image
import StringIO

#Connect to reddit api, and go to RoastMe subreddit
reddit = praw.Reddit(user_agent='Comment Extraction (by /u/USERNAME)',
                     client_id='E0zsvd3mYANn1A', client_secret="UFbU61TvUq19v_KCWBECd3j9X-k",
                     username='', password='')
subreddit = reddit.subreddit('RoastMe')
image_number = 1

#Go trough submissions one-by-one, download .png and .jpg images
for submission in subreddit.hot(limit=None):
        image_url = submission.url
        if (image_url[-3:] == 'png') or (image_url[-3:] == 'jpg'):
            img_data = requests.get(image_url).content
            if (image_url[-3:] == 'jpg'):
                file_path = 'OriginalPhotos/image{}.jpg'.format(image_number)
                with open(file_path, 'wb') as handler:
                    handler.write(img_data)
                    image_number += 1
            else:
                file_path = 'OriginalPhotos/image{}.jpg'.format(image_number)
                tempBuff = StringIO.StringIO()
                tempBuff.write(img_data)
                tempBuff.seek(0)  # need to jump back to the beginning before handing it off to PIL
                im = Image.open(tempBuff)
                im.save(file_path)
                image_number += 1
