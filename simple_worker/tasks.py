import creds 
import requests, base64, urllib
from datetime import timedelta
from celery import Celery
import banana_dev as banana
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

app = Celery('tasks', broker='redis://redis:6379/0',
             backend='redis://redis:6379/0')

api_key = creds.api_key
model_key = creds.model_key

url = "https://chitramai.com/api/1.1/obj/Data"
headers = {'Authorization': 'Bearer e1a9185d16055bac44068c8ac1f0893a'}


def create_subtitle(data):
    data = data['modelOutputs'][0]

    all = ""
    for idx in range(len(data['segments'])):
        start = str(timedelta(seconds=data['segments'][idx]['start']))
        end = str(timedelta(seconds=data['segments'][idx]['end']))
        text = data['segments'][idx]['text']
        final =str(idx+1)+'\n'+start+' --> '+end+'\n'+text+'\n\n'
        all += final

    return all

def shorten(url_long):
    URL = "http://tinyurl.com/api-create.php"

    url = URL + "?" + urllib.parse.urlencode({"url": url_long})
    res = requests.get(url) 
    return res.text

@app.task()
def predict(link, yt_link, email, youtube_title):
    logger.info('Got Request - Starting work ')
    
    if 'amazonaws' in link: 
      link = shorten(link)
     
    
    

    model_payload = {'link':link}
    out = banana.run(api_key, model_key, model_payload)
    logger.info("Sent the bytes file to Banana...")
    out = create_subtitle(out)

    logger.info("The output is created and it's preparing to send to bubble io!")

    mp3 = base64.b64encode(bytes(str(out), 'utf-8'))
    payload={'youtube_link': yt_link, 'file': mp3, 'email': email, 'youtube_title': youtube_title}  

    logger.info("Payload is Ready! ")

    response = requests.request("POST", url, headers=headers, data=payload)

    logger.info("Succesfully sent the file to bubble! Check in bubble")




    logger.info('Work Finished ')
    return out 
    



"""
    # response = requests.get(
    #     f'http://quickzam.pythonanywhere.com/give_bytes?link=https://www.youtube.com/watch?v={link}') ## python anywhere

    # response = requests.get(
    #     f"https://lionfish-app-wynde.ondigitalocean.app/give_bytes?link={link}") # digital Ocean flask app









"""
