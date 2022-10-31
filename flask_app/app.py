from flask import Flask, request
from celery import Celery

app = Flask(__name__)
simple_app = Celery(
    'simple_worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


@app.route('/simple_start_task')
def call_method():
    app.logger.info("Invoking Method ")
    #                        queue name in task folder.function name
    link = request.args.get('link')
    r = simple_app.send_task('tasks.predict', kwargs={'link': link})
    app.logger.info(r.backend)
    return r.id

@app.route('/simple_task_status')
def get_status():
    task_id = request.args.get('task_id') 
    status = simple_app.AsyncResult(task_id, app=simple_app)
    print("Invoking Method ")
    return str(status.state)


@app.route('/simple_task_result')
def task_result():
    task_id = request.args.get('task_id')
    result = simple_app.AsyncResult(task_id).result
    return str(result)

