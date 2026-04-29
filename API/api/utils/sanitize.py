import nh3

def sanitize(value: str) -> str:
    return nh3.clean(value, tags=set())