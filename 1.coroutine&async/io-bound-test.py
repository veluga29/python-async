import requests


def io_bound_function(url: str):
    res = requests.get(url)
    return res


if __name__ == "__main__":
    result = io_bound_function("https://www.google.com")
    print(result)
