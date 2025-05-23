from datetime import datetime


def log(filename=None):
    """Декоратор для логирования вызовов функций.
    Логирует начало и конец выполнения функции, а также возможные ошибки.
    Логи могут записываться в файл или выводиться в консоль."""

    def decorator(func):
        """Внутренний декоратор, который добавляет логирование к функции `func`."""

        def wrapper(*args, **kwargs):
            """Обёртка вокруг функции. Выполняет логирование перед и после вызова `func`."""

            start_msg = f"{datetime.now()} - {func.__name__} started with args: {args}, kwargs: {kwargs}\n"

            if filename:
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(start_msg)
            else:
                print(start_msg.strip())

            try:
                result = func(*args, **kwargs)  # Вызываем исходную функцию
                end_msg = f"{datetime.now()} - {func.__name__} finished. Result: {result}\n"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(end_msg)
                else:
                    print(end_msg.strip())

                return result

            except Exception as e:
                error_msg = f"{datetime.now()} - {func.__name__} ERROR: {type(e).__name__} - {e}\n"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_msg)
                else:
                    print(error_msg.strip())
                raise

        return wrapper

    return decorator


@log(filename="mylog.txt")
def my_function(x, y):
    return x + y


my_function(1, 2)
