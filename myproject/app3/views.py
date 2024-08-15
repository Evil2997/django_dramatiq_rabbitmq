import logging

from django.conf import settings
from django.http import JsonResponse

from django.shortcuts import render
from .tasks import *
import random

logger = logging.getLogger("django")


# def start_all_tasks(request):
#     if request.method == "POST":
#         logger.info("Запуск всех задач...")
#
#         for _ in range(3):
#             high_priority_task.send(random.randint(1, 10), random.randint(1, 10))
#
#         for _ in range(4):
#             medium_priority_task.send(random.randint(1, 10), random.randint(1, 10))
#
#         for _ in range(3):
#             low_priority_task.send(random.randint(1, 10), random.randint(1, 10))
#
#         return JsonResponse({'status': 'All tasks started'})
#
#     return render(request, 'app3/start_all_tasks.html')


def start_all_tasks(request):
    if request.method == "POST":
        logger.info("Запуск всех задач...")

        # Отправка задачи
        message = high_priority_task.send(random.randint(1, 10), random.randint(1, 10))

        return JsonResponse({'status': 'Task enqueued', 'task_id': message.message_id})

    return render(request, 'app3/start_all_tasks.html')


