import boto3
import os

import subprocess
from multiprocessing import Process, Queue
from urllib.request import urlretrieve

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


tasks_queue = Queue()
app = FastAPI()


class Task(BaseModel):
    client_id: str
    url: str
    avatar_id: int


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def process_client(task: Task):
    # Save task for processing
    tasks_queue.put(task)

    # Create url for result
    client_id = task.client_id

    return {
        "url": f"https://storage.yandexcloud.net/3d-avatar/{client_id}.mp4",
        "order": tasks_queue.qsize()
    }


session = boto3.session.Session()

ENDPOINT = "https://storage.yandexcloud.net"
BACKET = "3d-avatar"

session = boto3.Session(
    aws_access_key_id=(os.environ['TOKEN']),
    aws_secret_access_key=(os.environ['KEY']),
    region_name="ru-central1",
)

s3 = session.client(
    service_name='s3',
    endpoint_url=ENDPOINT
)


def upload_to_storage(path, client_id):
    s3.upload_file(path, BACKET, f'{client_id}.mp4', ExtraArgs={'ACL': 'public-read', 'ContentType': 'audio/mp4'})


AUDIO_PATH_OGG = "/home/ubuntu/work/audio.ogg"
AUDIO_PATH_WAV = "/home/ubuntu/work/audio.wav"
RESULTS_DIR_PATH = "/home/ubuntu/work/results"
RESULT_FILENAME = "result.mp4"


def animate():
    while True:
        task = tasks_queue.get()
        audio_url = task.url
        avatar_id = task.avatar_id
        client_id = task.client_id

        # Get avatar image path
        avatar_img_path = f"/home/ubuntu/work/avatars/{avatar_id}.png"

        # Load audio from url
        urlretrieve(audio_url, AUDIO_PATH_OGG)

        # Convert to WAV and animate
        subprocess.run([f"ffmpeg -y -i {AUDIO_PATH_OGG} {AUDIO_PATH_WAV} | python3.8 /home/ubuntu/work/SadTalker/inference.py --driven_audio {AUDIO_PATH_WAV} --source_image {avatar_img_path} --result_dir {RESULTS_DIR_PATH} --still --preprocess full --enhancer gfpgan"], shell=True, text=True)

        # Upload to url
        upload_to_storage(f"{RESULTS_DIR_PATH}/{RESULT_FILENAME}", client_id)


p = Process(target=animate)


if __name__ == "__main__":
    p.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    p.join()
