import logging
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_command(command):
    """Функция для выполнения bash-команд."""
    logging.info(f"Выполняется команда: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        logging.error(f"Ошибка при выполнении команды: {command}")
        logging.error(result.stderr)
    else:
        logging.info(f"Команда выполнена успешно: {command}")
    return result.stdout.strip()


def check_network_exists(network_name):
    """Проверка, существует ли сеть в Docker."""
    command = f"docker network ls --filter name=^{network_name}$ --format '{{{{.Name}}}}'"
    result = run_command(command)
    return result == network_name


def create_network(network_name):
    """Создание сети в Docker, если она не существует."""
    if not check_network_exists(network_name):
        logging.info(f"Сеть {network_name} не существует. Создаем...")
        command = f"docker network create {network_name}"
        output = run_command(command)
        logging.info(f"Результат создания сети: {output}")
    else:
        logging.info(f"Сеть {network_name} уже существует.")


def connect_container_to_network(container_name, network_name):
    """Подключение контейнера к сети Docker."""
    logging.info(f"Подключение контейнера {container_name} к сети {network_name}...")
    command = f"docker network connect {network_name} {container_name}"
    result = run_command(command)
    if not result:
        logging.info(f"Контейнер {container_name} подключен к сети {network_name}.")
    else:
        logging.error(f"Не удалось подключить контейнер {container_name} к сети {network_name}.")


def remove_network(network_name):
    """Удаление сети Docker, если она существует."""
    if check_network_exists(network_name):
        logging.info(f"Удаляем сеть {network_name}...")
        command = f"docker network rm {network_name}"
        run_command(command)
    else:
        logging.info(f"Сеть {network_name} не существует, удалять нечего.")


def main():
    try:
        create_network(network_name)
        for container in containers:
            connect_container_to_network(container, network_name)
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
        logging.info("Выполняется откат изменений...")
        remove_network(network_name)
        logging.info("Откат выполнен.")


if __name__ == "__main__":
    network_name = "mynetwork"
    containers = ["db", "rabbitmq", "web", "worker"]

    main()
