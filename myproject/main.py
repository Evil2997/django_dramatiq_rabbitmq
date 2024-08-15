import logging
import subprocess
import json
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_command(command, use_sudo=False, password=None):
    """Выполняет команду в оболочке и возвращает результат."""
    if use_sudo and password:
        command = f"echo {password} | sudo -S {command}"
    logging.info(f"Выполняется команда: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        logging.error(f"Ошибка при выполнении команды: {command}")
        logging.error(result.stderr)
    else:
        logging.info(f"Команда выполнена успешно: {command}")
    return result.stdout.strip()


def execute_docker_compose_up():
    """Запускает Docker Compose с командой 'up'."""
    command = "docker-compose up -d"
    run_command(command)


def execute_docker_compose_down():
    """Запускает Docker Compose с командой 'down'."""
    command = "docker-compose down"
    run_command(command)


def remove_network(network_name, password):
    """Удаляет Docker-сеть."""
    command = f"docker network rm {network_name}"
    run_command(command, use_sudo=True, password=password)


def create_network(network_name, password):
    """Создает Docker-сеть."""
    command = f"docker network create {network_name}"
    run_command(command, use_sudo=True, password=password)


def connect_containers_to_network(network_name, containers, password):
    """Подключает указанные контейнеры к сети."""
    for container in containers:
        command = f"docker network connect {network_name} {container}"
        run_command(command, use_sudo=True, password=password)


def get_docker_network_interface(network_name):
    """Получает сетевой интерфейс Docker для указанной сети."""
    inspect_output = run_command(f"docker network inspect {network_name}")
    network_info = json.loads(inspect_output)
    network_id = network_info[0]['Id']
    interface = f"br-{network_id[:12]}"
    return interface


def set_upload_limit(interface, upload_speed, password):
    """Устанавливает ограничение на исходящий трафик."""
    run_command(f"tc qdisc del dev {interface} root", use_sudo=True, password=password)
    run_command(f"tc qdisc add dev {interface} root handle 1: htb default 30", use_sudo=True, password=password)
    run_command(f"tc class add dev {interface} parent 1: classid 1:1 htb rate {upload_speed}mbit", use_sudo=True,
                password=password)
    run_command(f"tc filter add dev {interface} protocol ip parent 1:0 prio 1 u32 match ip src 0.0.0.0/0 flowid 1:1",
                use_sudo=True, password=password)


def set_download_limit(interface, download_speed, password):
    """Устанавливает ограничение на входящий трафик."""
    run_command(f"tc qdisc del dev {interface} ingress", use_sudo=True, password=password)
    run_command(f"tc qdisc add dev {interface} handle ffff: ingress", use_sudo=True, password=password)
    run_command(
        f"tc filter add dev {interface} parent ffff: protocol ip prio 50 u32 match ip dst 0.0.0.0/0 police rate {download_speed}mbit burst 10k drop flowid :1",
        use_sudo=True, password=password)


def execute_close_commands(password, network_name):
    """Выполнение команд завершения и очистки Docker, включая удаление сети."""
    commands = [
        "docker-compose down --rmi all --volumes --remove-orphans",
        "docker system prune --all --volumes -f"
    ]
    for command in commands:
        run_command(command, use_sudo=True, password=password)

    # Удаляем сеть после очистки Docker
    remove_network(network_name, password)


def main():
    sudo_password = "12345678"
    network_name = "mynetwork"
    upload_speed = 10  # Mbit
    download_speed = 5  # Mbit
    containers = ["db", "rabbitmq", "web", "worker"]
    delay = 1

    # 1. Выполнение команд очистки и завершения работы Docker
    execute_close_commands(sudo_password, network_name)

    # 2. Задержка перед перезапуском Docker Compose
    logging.info(f"Задержка {delay} секунд перед перезапуском Docker Compose...")
    time.sleep(delay)

    # 3. Выполнение команды Docker Compose 'up'
    execute_docker_compose_up()

    # 4. Задержка перед созданием сети и подключением контейнеров
    logging.info(f"Задержка {delay} секунд перед созданием сети и подключением контейнеров...")
    time.sleep(delay)

    # 5. Создание новой сети
    create_network(network_name, sudo_password)

    # 6. Подключение всех контейнеров к сети
    connect_containers_to_network(network_name, containers, sudo_password)

    # 7. Задержка перед установкой ограничений на трафик
    logging.info(f"Задержка {delay} секунд перед созданием сети и подключением контейнеров...")
    time.sleep(delay)

    # 8. Установка ограничений на трафик
    interface = get_docker_network_interface(network_name)
    set_upload_limit(interface, upload_speed, sudo_password)
    set_download_limit(interface, download_speed, sudo_password)
    logging.info("Ограничения на трафик установлены")


if __name__ == "__main__":
    main()
