from Crypto.Random import get_random_bytes

# 產生 256 位元隨機金鑰（32 位元組 = 256 位元）
key = get_random_bytes(32)
print(f"key:{key}")

# 產生 salt
print(f"get_random_bytes : {get_random_bytes(32)}")