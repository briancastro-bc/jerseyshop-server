import string, random

def generate_code(length: int=15):
    random_code: str = ""
    for i in range(length):
        random_code += "".join(random.choice(string.ascii_letters + string.digits))
    return random_code