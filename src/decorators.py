from functools import wraps


def logfile(func):
    """Ведет лог функции в консоль и файл"""
    @wraps(func)
    def decorator(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Function '{func.__name__}' called with args: {args}, kwargs: {kwargs}. Result: {result}")
        conets = f"Calling function {func.__name__} with args {args} and kwargs {kwargs}\n"

        # Define the file within a context manager
        with open("logfile.txt", "a") as file:
            file.write(conets)

        return result

    return decorator


def log(filename=None):
    """Ведет лог функции в консоль либо файл"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if filename != None:
                conets = f"Calling function {func.__name__} with args {args} and kwargs {kwargs}\n"
                with open(filename, "w") as file:
                    file.write(conets)
            else:
                conets = f"Calling function {func.__name__} with args {args} and kwargs {kwargs}"
                print(conets)

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                if filename:
                    with open(filename, "a") as file:
                        file.write(f"Error: {e}\n")
                        file.write(f"Input parameters: {args} {kwargs}\n")
                else:
                    print(f"Error: {e}\nInput parameters: {args} {kwargs}")
                raise e

        return wrapper

    return decorator
