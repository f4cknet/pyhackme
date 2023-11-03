import argon2

def argon2hasher(password):
    salt = b"123456789"
    time_cost = 16
    memory_cost = 2**15
    parallelism = 2
    hash_len = 32

    hasher = argon2.PasswordHasher(
        time_cost=time_cost,
        memory_cost=memory_cost,
        parallelism = parallelism,
        hash_len = hash_len
    )

    password_hash = hasher.hash(password.encode(),salt=salt)
    return password_hash