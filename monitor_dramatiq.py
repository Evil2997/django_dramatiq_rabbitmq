import subprocess
import time


def get_dramatiq_processes():
    """Возвращает список PID процессов dramatiq"""
    try:
        # Выполняем команду `ps aux` и фильтруем по процессам dramatiq
        result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.splitlines()

        dramatiq_processes = []
        for line in lines:
            if 'dramatiq' in line:
                parts = line.split()
                pid = parts[1]
                dramatiq_processes.append(pid)

        return dramatiq_processes
    except Exception as e:
        print(f"Ошибка при получении процессов dramatiq: {e}")
        return []


def monitor_processes(interval=5):
    """Мониторит использование ресурсов процессами dramatiq"""
    try:
        while True:
            processes = get_dramatiq_processes()
            if not processes:
                print("Процессы dramatiq не найдены.")
            else:
                print(f"{'PID':<10} {'CPU %':<10} {'Memory %':<10} {'RSS Memory (MB)':<15} {'Command'}")
                print("=" * 150)

                for pid in processes:
                    try:
                        # Получаем информацию о процессе с помощью команды `ps`
                        ps_command = f"ps -p {pid} -o %cpu,%mem,rss,cmd"
                        result = subprocess.run(ps_command, shell=True, stdout=subprocess.PIPE, text=True)
                        lines = result.stdout.splitlines()

                        if len(lines) > 1:
                            cpu_mem_info = lines[1].split()
                            cpu_usage = cpu_mem_info[0]
                            memory_usage = cpu_mem_info[1]
                            memory_rss = int(cpu_mem_info[2]) / 1024  # Перевод из KB в MB
                            command = ' '.join(cpu_mem_info[3:])

                            print(f"{pid:<10} {cpu_usage:<10} {memory_usage:<10} {memory_rss:<15.2f} {command}")
                    except Exception as e:
                        print(f"Ошибка при получении информации о процессе {pid}: {e}")

            print("\n" + "=" * 150 + "\n")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("Мониторинг остановлен.")


if __name__ == "__main__":
    monitor_processes()
