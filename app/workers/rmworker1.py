import pika 
from fastapi import Depends, status, APIRouter, HTTPException
from database.database import get_session
from services import user
from models import Model
from models.User import User, Prediction
import sys, os, json, time
import datetime

session = Depends(get_session)

def make_connection():
    conn = pika.BlockingConnection(pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST'),
            port=(os.getenv('RABBITMQ_PORT')),
            credentials=pika.PlainCredentials(
                username=os.getenv('RABBITMQ_USER'),
                password=os.getenv('RABBITMQ_PASS')
            )
            )
    )

    return conn

def callback(ch, method, properties, body):
    data = json.loads(body)
    
    model = Model("1.2")

    if user.get_balance(data["user_id"]) > 0 and model.validate():

        predictions = model.predict(data["input"])

        custumer = get_session().get(User, data["user_id"])

        user.modify_balance(data["user_id"],5,"user model",get_session())

        user.add_prediction(Prediction(user_id = data["user_id"], input = data["input"], output = predictions, modelVersion = model.get_version(), cost = 5, date_time = datetime.now()), session = get_session())


if __name__ == '__main__':
    connection = make_connection()
    channel = connection.channel()

    channel.queue_declare(queue='run_ml_tasks')
    channel.basic_consume(queue='run_ml_tasks', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

