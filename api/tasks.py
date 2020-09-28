from api.models import Message
from api_messagies.celery import app


@app.task()
def send_message(message_id):
    message = Message.objects.get(id=message_id)
    message.sending()
