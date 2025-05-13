import os
import pytest
from src.decorators import log


# Тест для записи в файл
def test_file_logging(tmp_path):
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def add(a, b):
        return a + b

    # Успешное выполнение
    assert add(2, 3) == 5
    assert os.path.exists(log_file)
    with open(log_file) as f:
        assert "add ok" in f.read()

    # Очистка файла
    log_file.write_text("")

    # Ошибочное выполнение
    @log(filename=str(log_file))
    def div(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(1, 0)

    with open(log_file) as f:
        content = f.read()
        assert "div error: ZeroDivisionError" in content
        assert "Inputs: (1, 0), {}" in content


# Тест для вывода в консоль (с использованием capsys)
def test_console_logging(capsys):
    @log()
    def multiply(a, b):
        return a * b

    # Успешное выполнение
    assert multiply(3, 4) == 12
    captured = capsys.readouterr()
    assert "multiply ok" in captured.out

    # Ошибочное выполнение
    @log()
    def fail_func():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        fail_func()

    captured = capsys.readouterr()
    assert "fail_func error: ValueError" in captured.out
    assert "Inputs: (), {}" in captured.out


# Тест с именованными аргументами
def test_kwargs_logging(tmp_path):
    log_file = tmp_path / "kwargs.log"

    @log(filename=str(log_file))
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}"

    # Успешное выполнение
    assert greet("Alice", greeting="Hi") == "Hi, Alice"
    with open(log_file) as f:
        assert "greet ok" in f.read()

    # Очистка файла
    log_file.write_text("")

    # Ошибочное выполнение с kwargs
    @log(filename=str(log_file))
    def kwargs_error(**kwargs):
        raise TypeError("Test error")

    with pytest.raises(TypeError):
        kwargs_error(param1=1, param2=2)

    with open(log_file) as f:
        content = f.read()
        assert "kwargs_error error: TypeError" in content
        assert "'param1': 1" in content
        assert "'param2': 2" in content


# Тест сохранения метаданных функции
def test_function_metadata():
    @log()
    def sample(a: int, b: int) -> int:
        """Test function"""
        return a + b

    assert sample.__name__ == "sample"
    assert sample.__doc__ == "Test function"
    assert sample.__annotations__ == {"a": int, "b": int, "return": int}


# Тест без аргументов
def test_no_args_logging(capsys):
    @log()
    def no_args():
        return 42

    assert no_args() == 42
    captured = capsys.readouterr()
    assert "no_args ok" in captured.out
