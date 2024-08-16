import json
import logging
import pathlib
import subprocess
import time
from typing import Final

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_command(command, use_sudo=False, password=None):
    """Выполняет команду в оболочке и возвращает результат."""
    if use_sudo and password:
        command = f"echo {password} | sudo -S {command}"
    logging.info(f"Выполняется команда: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        logging.error(f"ОШИБКА при выполнении команды: {command}")
        logging.error(result.stderr.strip())
    else:
        logging.info(f"Команда выполнена успешно: {command}")
    return result.stdout.strip()


def execute_docker_compose_up(compose_file_path: pathlib.Path):
    """Запускает Docker Compose с командой 'up'."""
    command = f"docker-compose -f {compose_file_path}/docker-compose.yml up -d"
    run_command(command)


def execute_docker_compose_down(compose_file_path="."):
    """Запускает Docker Compose с командой 'down'."""
    command = f"docker-compose -f {compose_file_path}/docker-compose.yml down"
    run_command(command)


def remove_network(network_name, password):
    """Удаляет Docker-сеть."""
    if check_network_exists(network_name):
        command = f"docker network rm {network_name}"
        run_command(command, use_sudo=True, password=password)


def create_network(network_name, password):
    """Создает Docker-сеть, если она не существует."""
    if not check_network_exists(network_name):
        command = f"docker network create {network_name}"
        run_command(command, use_sudo=True, password=password)
    else:
        logging.info(f"Сеть {network_name} уже существует. Пропускаем создание сети.")


def check_network_exists(network_name):
    """Проверяет, существует ли сеть Docker."""
    command = f"docker network ls --filter name=^{network_name}$ --format '{{{{.Name}}}}'"
    result = run_command(command)
    return result == network_name


def connect_containers_to_network(network_name, containers, password):
    """Подключает указанные контейнеры к сети."""
    for container in containers:
        if not check_container_in_network(container, network_name):
            if check_container_exists(container):
                command = f"docker network connect {network_name} {container}"
                run_command(command, use_sudo=True, password=password)
            else:
                logging.error(f"Контейнер {container} не существует. Пропускаем подключение.")
        else:
            logging.info(f"Контейнер {container} уже подключен к сети {network_name}. Пропускаем.")


def check_container_in_network(container_name, network_name):
    """Проверяет, подключен ли контейнер к сети."""
    command = f"docker inspect -f '{{{{.HostConfig.NetworkMode}}}}' {container_name}"
    result = run_command(command)
    return result == network_name


def check_container_exists(container_name):
    """Проверяет, существует ли контейнер."""
    command = f"docker inspect {container_name}"
    result = run_command(command)
    return result != ""


def get_docker_network_interface(network_name):
    """Получает сетевой интерфейс Docker для указанной сети."""
    inspect_output = run_command(f"docker network inspect {network_name}")
    network_info = json.loads(inspect_output)
    network_id = network_info[0]['Id']
    interface = f"br-{network_id[:12]}"
    return interface


def delete_qdisc(interface, password, qdisc_type='root'):
    """Удаляет qdisc, если он существует."""
    command = f"tc qdisc show dev {interface}"
    output = run_command(command, use_sudo=True, password=password)
    if qdisc_type in output:
        delete_command = f"tc qdisc del dev {interface} {qdisc_type}"
        run_command(delete_command, use_sudo=True, password=password)
    else:
        logging.info(f"Qdisc {qdisc_type} не найден на интерфейсе {interface}, пропускаем удаление.")


def set_upload_limit(interface, upload_speed, password):
    """Устанавливает ограничение на исходящий трафик."""
    delete_qdisc(interface, password, 'root')
    run_command(f"tc qdisc add dev {interface} root handle 1: htb default 30", use_sudo=True, password=password)
    run_command(f"tc class add dev {interface} parent 1: classid 1:1 htb rate {upload_speed}mbit", use_sudo=True,
                password=password)
    run_command(f"tc filter add dev {interface} protocol ip parent 1:0 prio 1 u32 match ip src 0.0.0.0/0 flowid 1:1",
                use_sudo=True, password=password)


def set_download_limit(interface, download_speed, password):
    """Устанавливает ограничение на входящий трафик."""
    delete_qdisc(interface, password, 'ingress')
    run_command(f"tc qdisc add dev {interface} handle ffff: ingress", use_sudo=True, password=password)
    run_command(
        f"tc filter add dev {interface} parent ffff: protocol ip prio 50 u32 match ip dst 0.0.0.0/0 police rate {download_speed}mbit burst 10k drop flowid :1",
        use_sudo=True, password=password)


def execute_close_commands(password, network_name, compose_file_path: pathlib.Path):
    """Выполнение команд завершения и очистки Docker, включая удаление сети."""
    commands = [
        f"docker-compose -f {compose_file_path}/docker-compose.yml down --rmi all --volumes --remove-orphans",
        "docker system prune --all --volumes -f"
    ]
    for command in commands:
        run_command(command, use_sudo=True, password=password)

    # Удаляем сеть после очистки Docker
    remove_network(network_name, password)


def main():
    sudo_password = "12345678"
    network_name = "mynetwork"
    upload_speed = 0  # Mbit
    download_speed = 5  # Mbit
    containers = ["db", "rabbitmq", "web", "worker"]
    compose_file_path: Final[pathlib.Path] = pathlib.Path(__file__).parent / "myproject"

    # 1. Выполнение команд очистки и завершения работы Docker
    execute_close_commands(sudo_password, network_name, compose_file_path)

    # 2. Выполнение команды Docker Compose 'up'
    execute_docker_compose_up(compose_file_path)

    # 3. Создание новой сети
    create_network(network_name, sudo_password)

    # 4. Подключение всех контейнеров к сети
    connect_containers_to_network(network_name, containers, sudo_password)

    # 5. Установка ограничений на трафик
    if upload_speed != 0 and download_speed != 0:
        interface = get_docker_network_interface(network_name)
        set_upload_limit(interface, upload_speed, sudo_password)
        set_download_limit(interface, download_speed, sudo_password)
        logging.info("Ограничения на трафик установлены")
    else:
        logging.info("Ограничения не устанавливаются")


if __name__ == "__main__":
    main()
