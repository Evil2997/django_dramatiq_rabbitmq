import logging

import pexpect
import psutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def execute_commands_with_sudo(commands, password):
    results = []
    for command in commands:
        try:
            if command.startswith("python") or command.startswith("python3"):
                full_command = command
            else:
                full_command = f"sudo {command}"

            child = pexpect.spawn(full_command)

            if full_command.startswith("sudo"):
                child.expect("password")
                child.sendline(password)

            child.expect(pexpect.EOF)
            output = child.before.decode('utf-8')
            return_code = child.exitstatus

            results.append({
                "command": full_command,
                "output": output,
                "return_code": return_code
            })
        except pexpect.exceptions.ExceptionPexpect as e:
            results.append({
                "command": full_command,
                "output": "",
                "error": str(e),
                "return_code": -1
            })
    return results


def find_and_kill_ports(ports):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port in ports:
            try:
                proc = psutil.Process(conn.pid)
                logging.info(
                    f"Процесс {proc.name()} (PID: {proc.pid}) использует порт {conn.laddr.port}. Завершаем процесс.")
                proc.terminate()
                proc.wait(timeout=3)  # Ждём до 3 секунд
                if proc.is_running():
                    logging.warning(
                        f"Процесс {proc.name()} (PID: {proc.pid}) не завершился. Принудительно завершаем процесс.")
                    proc.kill()
                    proc.wait()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                logging.warning(f"Не удалось завершить процесс, использующий порт {conn.laddr.port}: {e}")


def main():
    # Команды для выполнения, связанные с сервисами из вашего docker-compose.yml
    commands = [
        # "docker-compose stop db",
        # "docker-compose stop rabbitmq",
        # "docker-compose stop web",
        # "docker-compose stop worker",
        # "docker-compose rm -f db",
        # "docker-compose rm -f rabbitmq",
        # "docker-compose rm -f web",
        # "docker-compose rm -f worker",
        "docker-compose down",
    ]
    password = "12345678"  # Замените на ваш пароль

    # Выполнение команд с использованием sudo
    results = execute_commands_with_sudo(commands, password)

    for result in results:
        if "No stopped containers" not in result['output']:
            if result['output'].split(" for user-q: ")[1] != "\r\n":
                print(f"КОМАНДА:\n {result['command']}")
                print(f"РЕЗУЛЬТАТ:\n {result['output']}")
                print(f"КОД ВОЗВРАТА:\n {result['return_code']}")
                if 'error' in result:
                    print(f"ОШИБКА:\n {result['error']}")
                print("=" * 44)

    ports_to_free = [8001, 5672, 5673, 15673]
    find_and_kill_ports(ports_to_free)


if __name__ == "__main__":
    main()
