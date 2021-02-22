import random

def generate_random(gerados, max=4):
    r_num = random.randint(1, max)
    while r_num in gerados:
        r_num = random.randint(1, max)
    return r_num