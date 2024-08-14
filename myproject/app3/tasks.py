import logging
import time
from django.conf import settings

import dramatiq

logger = logging.getLogger("django")


@dramatiq.actor(queue_name="high_priority_queue")
def high_priority_task(x, y):
    logger.info(f"\n{'=' * 40}\nЗАПУСК ЗАДАЧИ HIGH PRIORITY\nАргументы: x={x}, y={y}\n{'-' * 40}")
    result = (x + y) * (x - y)
    time.sleep(5)
    logger.info(f"RESULT HIGH PRIORITY: {result}\n{'=' * 40}")
    return result


@dramatiq.actor(queue_name="medium_priority_queue")
def medium_priority_task(x, y):
    logger.info(f"\n{'=' * 40}\nЗАПУСК ЗАДАЧИ MEDIUM PRIORITY\nАргументы: x={x}, y={y}\n{'-' * 40}")
    result = (x + y) * (x - y)
    time.sleep(5)
    logger.info(f"RESULT MEDIUM PRIORITY: {result}\n{'=' * 40}")
    return result


@dramatiq.actor(queue_name="low_priority_queue")
def low_priority_task(x, y):
    logger.info(f"\n{'=' * 40}\nЗАПУСК ЗАДАЧИ LOW PRIORITY\nАргументы: x={x}, y={y}\n{'-' * 40}")
    result = (x + y) * (x - y)
    time.sleep(5)
    logger.info(f"RESULT LOW PRIORITY: {result}\n{'=' * 40}")
    return result
