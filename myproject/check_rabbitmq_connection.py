import subprocess
import sys


def run_command(command):
    """
    Функция для выполнения команды в bash и возврата результата.
    """
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"


def check_dns_resolution(hostname):
    """
    Проверка разрешения имени хоста.
    """
    print(f"Checking DNS resolution for {hostname}...")
    result = run_command(f"nslookup {hostname}")
    print(result)


def check_ping(hostname):
    """
    Проверка доступности хоста через ping.
    """
    print(f"Pinging {hostname}...")
    result = run_command(f"ping -c 4 {hostname}")
    print(result)


def check_port(hostname, port):
    """
    Проверка доступности порта.
    """
    print(f"Checking if port {port} is open on {hostname}...")
    result = run_command(f"nc -zv {hostname} {port}")
    print(result)


def check_python_rabbitmq_connection(hostname):
    """
    Проверка подключения к RabbitMQ с помощью Python.
    """
    print(f"Attempting to connect to RabbitMQ on {hostname} using Python...")
    try:
        import pika
        connection = pika.BlockingConnection(pika.ConnectionParameters(hostname))
        channel = connection.channel()
        print("Connected to RabbitMQ")
        connection.close()
    except Exception as e:
        print(f"Error connecting to RabbitMQ: {e}")


def main():
    # Определите здесь хостнейм RabbitMQ, который используется вашим приложением.
    rabbitmq_hostname = "rabbitmq"  # Замените на ваше значение
    rabbitmq_port = 5672  # Стандартный порт RabbitMQ

    # Проверка разрешения имени хоста
    check_dns_resolution(rabbitmq_hostname)

    # Проверка доступности хоста через ping
    check_ping(rabbitmq_hostname)

    # Проверка доступности порта
    check_port(rabbitmq_hostname, rabbitmq_port)

    # Проверка подключения к RabbitMQ через Python
    check_python_rabbitmq_connection(rabbitmq_hostname)


if __name__ == "__main__":
    main()
