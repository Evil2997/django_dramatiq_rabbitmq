import subprocess
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_script(script_name):
    """Функция для выполнения Python-скриптов."""
    try:
        logging.info(f"Запуск {script_name}...")
        subprocess.run(["python3", script_name], check=True)
        logging.info(f"{script_name} выполнен успешно.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при выполнении {script_name}: {e}")
        raise


# def run_docker_compose():
#     """Функция для выполнения команды docker-compose up --build в фоновом режиме с логированием."""
#     try:
#         logging.info("Запуск docker-compose up --build...")
#         process = subprocess.Popen(["docker-compose", "up", "--build"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#
#         # Логирование вывода docker-compose в реальном времени
#         for line in iter(process.stdout.readline, b''):
#             logging.info(line.decode().strip())
#         for line in iter(process.stderr.readline, b''):
#             logging.error(line.decode().strip())
#
#         process.stdout.close()
#         process.stderr.close()
#         return process
#     except Exception as e:
#         logging.error(f"Ошибка при выполнении docker-compose: {e}")
#         raise


# def wait_for_containers(container_names, timeout=60):
#     """Ожидание запуска контейнеров перед подключением к сети."""
#     start_time = time.time()
#     while time.time() - start_time < timeout:
#         all_running = True
#         for container in container_names:
#             result = subprocess.run(f"docker inspect -f '{{{{.State.Running}}}}' {container}", shell=True, text=True,
#                                     capture_output=True)
#             if "true" not in result.stdout:
#                 logging.info(f"Ожидание запуска контейнера {container}...")
#                 all_running = False
#                 break
#         if all_running:
#             logging.info("Все контейнеры запущены и готовы.")
#             return True
#         time.sleep(5)  # Ждем 5 секунд перед следующей проверкой
#     logging.error("Истекло время ожидания запуска контейнеров.")
#     return False


def main():
    try:
        run_script("Close.py")
        # process = run_docker_compose()
        time.sleep(300)
        # container_names = ["db", "rabbitmq", "web", "worker"]
        # if wait_for_containers(container_names):
        run_script("setup_network.py")
        # else:
        #     logging.error("Контейнеры не запущены вовремя. Прекращение работы.")

        # stdout, stderr = process.communicate()
        # logging.info(stdout.decode())
        # if stderr:
        #     logging.error(stderr.decode())

    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
        logging.error("Процесс завершен с ошибкой.")


if __name__ == "__main__":
    main()
