import random
import string


def generate_random_sender_id(length=10):
    sender_id = "".join(random.choices(string.ascii_letters + string.digits, k=length))
    return sender_id
