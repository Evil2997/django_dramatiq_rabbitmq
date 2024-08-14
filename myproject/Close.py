import logging
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def execute_command_with_sudo(command, password):
    try:
        full_command = f"echo {password} | sudo -S {command}"
        logging.info(f"Выполнение команды: {command}")
        result = subprocess.run(full_command, shell=True, text=True, capture_output=True)
        if result.returncode != 0:
            logging.error(f"Ошибка при выполнении команды {command}: {result.stderr}")
        else:
            logging.info(f"Команда {command} выполнена успешно.")
        return result.returncode
    except Exception as e:
        logging.error(f"Произошла ошибка при выполнении команды {command}: {e}")
        return -1


def main():
    commands = [
        "docker-compose down",
        "docker-compose down --rmi all --volumes --remove-orphans",
        "docker system prune --all --volumes -f"
    ]

    password = "12345678"

    for command in commands:
        return_code = execute_command_with_sudo(command, password)
        if return_code != 0:
            logging.error(f"Команда '{command}' завершилась с кодом {return_code}. Останавливаем выполнение.")
            break


if __name__ == "__main__":
    logging.info("Запуск Close.py...")
    try:
        main()
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    logging.info("Close.py завершен успешно.")
