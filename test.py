def wrapper(*args, **kwargs):
    print("до вызова")
    result = target(args, kwargs)
    print("после вызова")
    return result

def target(method, url, timeout=30):
    print(f"{method} {url} (timeout={timeout})")

wrapper("GET", "/users", timeout=5)
# до вызова
# GET /users (timeout=5)
# после вызова