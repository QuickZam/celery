from flask import Flask, request
from celery import Celery
import requests, os,  base64
from io import BytesIO

app = Flask(__name__)
simple_app = Celery(
    'simple_worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

url = "https://chitramai.com/version-test/api/1.1/obj/Data"
headers = {'Authorization': 'Bearer e1a9185d16055bac44068c8ac1f0893a'}


@app.route('/simple_start_task')
def call_method():
    app.logger.info("Invoking Method ")
    #                        queue name in task folder.function name
    link = request.args.get('link')
    r = simple_app.send_task('tasks.predict', kwargs={'link': link})
    global link_yt 
    link_yt = link 
    app.logger.info(r.backend)
    global id_ 
    id = r.id 
    id_ = id 
    return id 

@app.route('/simple_task_status')
def get_status():
    task_id = request.args.get('task_id') 
    status = simple_app.AsyncResult(task_id, app=simple_app)
    while True: 
        if str(status.state) == 'SUCCESS':
            result = simple_app.AsyncResult(task_id).result 

            with open("result.txt", 'w') as f:
                f.write(str(result))
            with open("result.txt", 'rb') as file:
                 mp3bytes = BytesIO(file.read())

            mp3 = base64.b64encode(mp3bytes.getvalue()).decode("ISO-8859-1")

            payload={'youtube_link': link_yt, 'file': mp3, 'id' :id_}  
            files = [(file, mp3bytes)]
            response = requests.request("POST", url, headers=headers, data=payload)#, files=files)
            os.remove("result.txt")
            return response.text 


@app.route('/simple_task_result')
def task_result():
    task_id = request.args.get('task_id')
    result = simple_app.AsyncResult(task_id).result
    return str(result)

