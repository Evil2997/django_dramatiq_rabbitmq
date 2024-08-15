import subprocess
import json
import argparse
import time
import re


def run_command(command, use_sudo=False):
    """Выполняет команду в оболочке и возвращает результат."""
    if use_sudo:
        command = f"echo {sudo_password} | sudo -S {command}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"[X] ERROR: {result.stderr.decode().strip()}")
    return result.stdout.decode().strip()


def create_docker_network(network_name):
    """Создает Docker-сеть, если она не существует."""
    existing_networks = run_command("docker network ls")
    if network_name in existing_networks:
        print(f"\nСеть Docker {network_name} уже существует.")
    else:
        run_command(f"docker network create {network_name}")
        print(f"\nСеть Docker {network_name} создана.")


def container_exists(container_name):
    """Проверяет, существует ли контейнер по его имени."""
    existing_containers = run_command("docker ps -a --format '{{.Names}}'")
    return container_name in existing_containers


def remove_container(container_name):
    """Удаляет контейнер."""
    run_command(f"docker rm -f {container_name}")
    print(f"\nКонтейнер Docker {container_name} удален.")


def restart_container(container_name):
    """Перезапускает контейнер."""
    run_command(f"docker restart {container_name}")
    print(f"\nКонтейнер Docker {container_name} перезапущен.")


def run_docker_container(container_name, network_name, image_name):
    """Запускает Docker-контейнер в указанной сети."""
    run_command(f"docker build -t {image_name} .")
    run_command(f"docker run -d --name {container_name} --network {network_name} {image_name}")
    print(f"\nКонтейнер Docker {container_name} запущен в сети {network_name}.")


def get_docker_network_interface(network_name):
    """Получает сетевой интерфейс Docker для указанной сети."""
    inspect_output = run_command(f"docker network inspect {network_name}")
    network_info = json.loads(inspect_output)
    network_id = network_info[0]['Id']
    interface = f"br-{network_id[:12]}"
    return interface


def set_upload_limit(interface, upload_speed, sudo_password):
    """Устанавливает ограничение на исходящий трафик."""
    run_command(f"tc qdisc del dev {interface} root", use_sudo=True)
    run_command(f"tc qdisc add dev {interface} root handle 1: htb default 30", use_sudo=True)
    run_command(f"tc class add dev {interface} parent 1: classid 1:1 htb rate {upload_speed}mbit", use_sudo=True)
    run_command(f"tc filter add dev {interface} protocol ip parent 1:0 prio 1 u32 match ip src 0.0.0.0/0 flowid 1:1",
                use_sudo=True)


def set_download_limit(interface, download_speed, sudo_password):
    """Устанавливает ограничение на входящий трафик."""
    run_command(f"tc qdisc del dev {interface} ingress", use_sudo=True)
    run_command(f"tc qdisc add dev {interface} handle ffff: ingress", use_sudo=True)
    run_command(
        f"tc filter add dev {interface} parent ffff: protocol ip prio 50 u32 match ip dst 0.0.0.0/0 police rate {download_speed}mbit burst 10k drop flowid :1",
        use_sudo=True)


def get_container_logs(container_name):
    """Получает логи контейнера."""
    return run_command(f"docker logs {container_name}")


def main():
    print("\n")
    parser = argparse.ArgumentParser(description='Automate Docker network creation and traffic control.')
    parser.add_argument('--network_name', required=True, help='Name of the Docker network')
    parser.add_argument('--container_name', required=True, help='Name of the Docker container')
    parser.add_argument('--image_name', required=True, help='Docker image to use for the container')
    parser.add_argument('--upload_speed', required=True, type=int, help='Upload speed limit in Mbit')
    parser.add_argument('--download_speed', required=True, type=int, help='Download speed limit in Mbit')
    parser.add_argument('--sudo_password', required=True, help='Sudo password for executing commands')
    parser.add_argument('--action', required=True, choices=['restart', 'recreate', 'leave'],
                        help='Action to take if the container already exists')

    args = parser.parse_args()
    # --network_name mynetwork --container_name db --upload_speed 10 --download_speed 5 --action recreate
    # --network_name mynetwork --container_name rabbitmq --upload_speed 10 --download_speed 5 --action recreate
    # --network_name mynetwork --container_name web --upload_speed 10 --download_speed 5 --action recreate
    # --network_name mynetwork --container_name worker --upload_speed 10 --download_speed 5 --action recreate

    global sudo_password
    sudo_password = args.sudo_password

    network_name = args.network_name
    container_name = args.container_name
    image_name = args.image_name
    upload_speed = args.upload_speed
    download_speed = args.download_speed
    action = args.action

    # Создание сети Docker
    create_docker_network(network_name)

    # Проверка существования контейнера
    if container_exists(container_name):
        if action == 'restart':
            # Перезапуск контейнера
            restart_container(container_name)
        elif action == 'recreate':
            # Удаление и пересоздание контейнера
            remove_container(container_name)
            run_docker_container(container_name, network_name, image_name)
        else:   # action == 'leave':
            print(f"\nКонтейнер {container_name} уже существует и останется без изменений.")
    else:
        # Запуск контейнера, если он не существует
        run_docker_container(container_name, network_name, image_name)

    # Получение сетевого интерфейса Docker
    interface = get_docker_network_interface(network_name)
    print(f"\nСетевой интерфейс Docker для сети {network_name}: {interface}")

    # Установка ограничений на трафик
    set_upload_limit(interface, upload_speed, sudo_password)
    set_download_limit(interface, download_speed, sudo_password)
    print("Ограничения установлены")

    time.sleep(90)

    # Получение логов контейнера и вывод результатов
    logs = get_container_logs(container_name)
    print(f"\n\n{logs}")

    # print("Результаты теста скорости до внесения изменений:")
    # before_speedtest = re.search(
    #     r"Результаты теста скорости до внесения изменений:(.*?)Выполнение теста скорости после внесения изменений:",
    #     logs, re.DOTALL)
    # if before_speedtest:
    #     print(before_speedtest.group(1).strip())
    #
    # print("Результаты теста скорости после внесения изменений:")
    # after_speedtest = re.search(r"Результаты теста скорости после внесения изменений:(.*?)$", logs, re.DOTALL)
    # if after_speedtest:
    #     print(after_speedtest.group(1).strip())


if __name__ == "__main__":
    main()
