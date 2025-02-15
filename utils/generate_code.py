import random

def generate_code(length=10):
    data = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''.join(random.choice(data) for _ in range(length))
    return code