import time
import requests
import base64
import os
from io import BytesIO
from celery import Celery
import banana_dev as banana
from pytube import YouTube, extract
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

app = Celery('tasks', broker='redis://redis:6379/0',
             backend='redis://redis:6379/0')

api_key = "ec49909f-3d2f-4044-8882-535e3ce8a383"
model_key = "7734639e-bcae-41f6-b7b9-47a9cbba26e1"


@app.task()
def predict(link):
    logger.info('Got Request - Starting work ')
    # response = requests.get(
    #     f'http://quickzam.pythonanywhere.com/give_bytes?link=https://www.youtube.com/watch?v={link}') ## python anywhere

    response = requests.get(
        f"https://lionfish-app-wynde.ondigitalocean.app/give_bytes?link=https://www.youtube.com/watch?v={link}")

    logger.info("Got the output from python anywher")

    out = banana.run(api_key, model_key, response.json())
    logger.info('Work Finished ')
    return out
