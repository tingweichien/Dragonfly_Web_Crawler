from passlib.context import CryptContext

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        deprecated=["pbkdf2_sha256"],
        pbkdf2_sha256__default_rounds=30
)

decrypt_content = CryptContext(schemes=["md5_crypt"],
                         deprecated=["md5_crypt"])

def encrypt_password(password):
    return pwd_context.encrypt(password)


def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)




print("Enter password : ", end="")
PW = input()

Encrypt_PW = encrypt_password(PW)
print(f"Encrypt_PW : {Encrypt_PW}")

print(f"Verify : {check_encrypted_password(PW,Encrypt_PW)}")
