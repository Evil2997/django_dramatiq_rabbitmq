import logging
from django.conf import settings
import time

import dramatiq

# Используем логгер "django"
logger = logging.getLogger("django")


@dramatiq.actor
def high_priority_task(param1, param2):
    logger.info(f"Воркер запущен с параметрами: {param1}, {param2}")

    result = param1 + param2  # Пример простой логики

    logger.info(f"Результат задачи: {result}")
    return result


@dramatiq.actor(queue_name="medium_priority_queue")
def medium_priority_task(x, y):
    logger.info(f"\n{'=' * 40}\nЗАПУСК ЗАДАЧИ MEDIUM PRIORITY\nАргументы: x={x}, y={y}\n{'-' * 40}")
    print(f"\n{'=' * 40}\nЗАПУСК ЗАДАЧИ MEDIUM PRIORITY\nАргументы: x={x}, y={y}\n{'-' * 40}")
    result = (x + y) * (x - y)
    time.sleep(5)
    logger.info(f"RESULT MEDIUM PRIORITY: {result}\n{'=' * 40}")
    print(f"RESULT MEDIUM PRIORITY: {result}\n{'=' * 40}")
    return result


@dramatiq.actor(queue_name="low_priority_queue")
def low_priority_task(x, y):
    logger.info(f"\n{'=' * 40}\nЗАПУСК ЗАДАЧИ LOW PRIORITY\nАргументы: x={x}, y={y}\n{'-' * 40}")
    print(f"\n{'=' * 40}\nЗАПУСК ЗАДАЧИ LOW PRIORITY\nАргументы: x={x}, y={y}\n{'-' * 40}")
    result = (x + y) * (x - y)
    time.sleep(5)
    logger.info(f"RESULT LOW PRIORITY: {result}\n{'=' * 40}")
    print(f"RESULT LOW PRIORITY: {result}\n{'=' * 40}")
    return result
