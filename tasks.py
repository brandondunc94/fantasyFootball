from celery import Celery

app = Celery('tasks', broker='redis://localhost')

@app.task
def add():
    print("Hello World!")
    result = 2
    return result

