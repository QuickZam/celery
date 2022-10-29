import time, os, creds 
import requests
from datetime import timedelta
from celery import Celery
import banana_dev as banana
from flask import jsonify
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

app = Celery('tasks', broker='redis://redis:6379/0',
             backend='redis://redis:6379/0')

   
# api_key =  os.environ['API_KEY']
# model_key = os.environ['MODEL_KEY']
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


@app.task()
def predict(link):
    logger.info('Got Request - Starting work ')
    # response = requests.get(
    #     f'http://quickzam.pythonanywhere.com/give_bytes?link=https://www.youtube.com/watch?v={link}') ## python anywhere

    response = requests.get(
        f"https://lionfish-app-wynde.ondigitalocean.app/give_bytes?link={link}")

    logger.info("Got the output from python anywher")

    out = banana.run(api_key, model_key, response.json())
    out = create_subtitle(out)
    logger.info('Work Finished ')
    return out 
    
