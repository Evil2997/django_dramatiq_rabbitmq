import logging
import time

import dramatiq

logger = logging.getLogger("app3")


@dramatiq.actor(queue_name="high_priority_queue")
def high_priority_task(x, y):
    logger.info(f"\n{'=' * 40}\nЗАПУСК ЗАДАЧИ HIGH PRIORITY\nАргументы: x={x}, y={y}\n{'-' * 40}")
    print(f"\n{'=' * 40}\nЗАПУСК ЗАДАЧИ HIGH PRIORITY\nАргументы: x={x}, y={y}\n{'-' * 40}")
    result = (x + y) * (x - y)
    logger.info(f"RESULT HIGH PRIORITY: {result}\n{'=' * 40}")
    print(f"RESULT HIGH PRIORITY: {result}\n{'=' * 40}")
    return result


@dramatiq.actor(queue_name="medium_priority_queue")
def medium_priority_task(x, y):
    logger.info(f"\n{'=' * 40}\nЗАПУСК ЗАДАЧИ MEDIUM PRIORITY\nАргументы: x={x}, y={y}\n{'-' * 40}")
    print(f"\n{'=' * 40}\nЗАПУСК ЗАДАЧИ MEDIUM PRIORITY\nАргументы: x={x}, y={y}\n{'-' * 40}")
    result = (x + y) * (x - y)
    logger.info(f"RESULT MEDIUM PRIORITY: {result}\n{'=' * 40}")
    print(f"RESULT MEDIUM PRIORITY: {result}\n{'=' * 40}")
    return result


@dramatiq.actor(queue_name="low_priority_queue")
def low_priority_task(x, y):
    logger.info(f"\n{'=' * 40}\nЗАПУСК ЗАДАЧИ LOW PRIORITY\nАргументы: x={x}, y={y}\n{'-' * 40}")
    print(f"\n{'=' * 40}\nЗАПУСК ЗАДАЧИ LOW PRIORITY\nАргументы: x={x}, y={y}\n{'-' * 40}")
    result = (x + y) * (x - y)
    logger.info(f"RESULT LOW PRIORITY: {result}\n{'=' * 40}")
    print(f"RESULT LOW PRIORITY: {result}\n{'=' * 40}")
    return result
