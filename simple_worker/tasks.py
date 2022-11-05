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
def predict(link, email, youtube_title, unique_id):

    url = f"https://chitramai.com/version-test/api/1.1/obj/metadata/{unique_id}"
    headers = {'Authorization': 'Bearer e1a9185d16055bac44068c8ac1f0893a'}
  
    logger.info('Got Request - Starting work ')
    logger.info(f"Got input paramters, link: {link}, yt_link: {yt_link}, youtube_title :{youtube_title}") 
    if 'amazonaws' in link: 
      link = shorten(f'https:{link}')
     
    
    model_payload = {'link':link}
    logger.info(f"Model Payload: {model_payload}") 
    logger.info("Sent the bytes file to Banana...")
    
    out = banana.run(api_key, model_key, model_payload)
    logger.info("Got the output from banan") 
    
    out = create_subtitle(out)

    logger.info("The output is created and it's preparing to send to bubble io!")

    mp3 = base64.b64encode(bytes(str(out), 'utf-8'))

    payload={'file': mp3, 'Email': email, 'youtube_title': youtube_title, 'status':'Success'}  

    logger.info("Payload is Ready! ")

    # response = requests.request("POST", url, headers=headers, data=payload) ## older payload 
    response = requests.request("PATCH", url, headers=headers, data=payload)

    logger.info("Succesfully sent the file to bubble! Check in bubble")




    logger.info('Work Finished ')
    return out 
    



"""
    # response = requests.get(
    #     f'http://quickzam.pythonanywhere.com/give_bytes?link=https://www.youtube.com/watch?v={link}') ## python anywhere

    # response = requests.get(
    #     f"https://lionfish-app-wynde.ondigitalocean.app/give_bytes?link={link}") # digital Ocean flask app









"""
