from functools import wraps


def log(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__

            try:
                result = func(*args, **kwargs)
                message = f"{func_name} ok"

                if filename:
                    with open(filename, "a") as f:
                        f.write(message + "\n")
                else:
                    print(message)

                return result

            except Exception as e:
                error_message = f"{func_name} error: {type(e).__name__}. Inputs: {args}, {kwargs}"

                if filename:
                    with open(filename, "a") as f:
                        f.write(error_message + "\n")
                else:
                    print(error_message)

                raise

        return wrapper

    return decorator


@log(filename="mylog.txt")
def my_function(x, y):
    return x + y


my_function(1, 2)
