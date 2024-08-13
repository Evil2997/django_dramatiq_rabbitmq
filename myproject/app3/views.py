import logging
import random

from django.http import JsonResponse
from django.shortcuts import render

from .tasks import high_priority_task, medium_priority_task, low_priority_task

logger = logging.getLogger(__name__)


def start_all_tasks(request):
    if request.method == "POST":
        logger.info("Запуск всех задач...")
        for _ in range(3):
            high_priority_task.send(random.randint(1, 10), random.randint(1, 10))

        for _ in range(4):
            medium_priority_task.send(random.randint(1, 10), random.randint(1, 10))

        for _ in range(3):
            low_priority_task.send(random.randint(1, 10), random.randint(1, 10))

        return JsonResponse({'status': 'All tasks started'})

    return render(request, 'app3/start_all_tasks.html')


# def list_queues(request):
#     # Пример использования Management API для получения списка очередей
#     response = requests.get('http://localhost:15672/api/queues',
#                             auth=HTTPBasicAuth('guest', 'guest'))
#     queues = response.json()
#     queue_list = "\n".join([f"Queue: {queue['name']}, Messages: {queue['messages']}" for queue in queues])
#     return HttpResponse(f"<pre>{queue_list}</pre>")
#
#
# def publish_message(request):
#     # Пример использования pika для отправки сообщения в очередь
#     connection = pika.BlockingConnection(
#         pika.ConnectionParameters('rabbitmq', 5672, '/', pika.PlainCredentials('guest', 'guest')))
#     channel = connection.channel()
#
#     queue_name = 'high_priority_queue'
#     message = 'Hello, high priority task!'
#     channel.basic_publish(exchange='', routing_key=queue_name, body=message)
#     connection.close()
#
#     return HttpResponse(f"Message sent to queue '{queue_name}': {message}")
#
#
# def consume_message(request):
#     # Пример использования pika для получения сообщения из очереди
#     connection = pika.BlockingConnection(
#         pika.ConnectionParameters('rabbitmq', 5672, '/', pika.PlainCredentials('guest', 'guest')))
#     channel = connection.channel()
#
#     queue_name = 'high_priority_queue'
#     method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
#
#     if method_frame:
#         message = f"Received message from queue '{queue_name}': {body}"
#     else:
#         message = f"Queue '{queue_name}' is empty."
#
#     connection.close()
#     return HttpResponse(message)
