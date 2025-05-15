import os
import pytest
from src.decorators import log


def test_file_logging(tmp_path):
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def add(a, b):
        return a + b

    # Успешное выполнение
    assert add(2, 3) == 5
    assert os.path.exists(log_file)
    with open(log_file, encoding='utf-8') as f:
        content = f.read()
        assert "add started" in content
        assert "add finished" in content
        assert "Result: 5" in content

    # Очистка файла
    log_file.write_text("")

    # Ошибочное выполнение
    @log(filename=str(log_file))
    def div(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(1, 0)

    with open(log_file, encoding='utf-8') as f:
        content = f.read()
        assert "div started" in content
        assert "div ERROR: ZeroDivisionError" in content


def test_console_logging(capsys):
    @log()
    def multiply(a, b):
        return a * b

    # Успешное выполнение
    assert multiply(3, 4) == 12
    captured = capsys.readouterr()
    assert "multiply started" in captured.out
    assert "multiply finished" in captured.out
    assert "Result: 12" in captured.out

    # Ошибочное выполнение
    @log()
    def fail_func():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        fail_func()

    captured = capsys.readouterr()
    assert "fail_func started" in captured.out
    assert "fail_func ERROR: ValueError" in captured.out


def test_kwargs_logging(tmp_path):
    log_file = tmp_path / "kwargs.log"

    @log(filename=str(log_file))
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}"

    # Успешное выполнение
    assert greet("Alice", greeting="Hi") == "Hi, Alice"
    with open(log_file, encoding='utf-8') as f:
        content = f.read()
        assert "greet started" in content
        assert "greet finished" in content
        assert "Hi, Alice" in content

    # Очистка файла
    log_file.write_text("")

    # Ошибочное выполнение с kwargs
    @log(filename=str(log_file))
    def kwargs_error(**kwargs):
        raise TypeError("Test error")

    with pytest.raises(TypeError):
        kwargs_error(param1=1, param2=2)

    with open(log_file, encoding='utf-8') as f:
        content = f.read()
        assert "kwargs_error started" in content
        assert "kwargs_error ERROR: TypeError" in content


def test_function_metadata():
    @log()
    def sample(a: int, b: int) -> int:
        """Test function"""
        return a + b

    assert sample.__name__ == "sample"
    assert sample.__doc__ == "Test function"
    assert sample.__annotations__ == {"a": int, "b": int, "return": int}


def test_no_args_logging(capsys):
    @log()
    def no_args():
        return 42

    assert no_args() == 42
    captured = capsys.readouterr()
    assert "no_args started" in captured.out
    assert "no_args finished" in captured.out
    assert "Result: 42" in captured.out