import bcrypt

def to_enco(password):
    encoded=password.encode('utf-8')
    return encoded

def hashlize(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(to_enco(password), salt)
    return hashed

def check(password, hashed):
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')

    return bcrypt.checkpw(to_enco(password), hashed)

# s=input('输入要存的密码:')
# hashed1=hashlize(s)
# print('哈希之后的字节串:',hashed1)
#
# str=input('输入要验证的密码:')
# hashed2=hashlize(str)
# print('哈希后的验证密码:',hashed2,'\n')
# print('验证中...')
# if check(str,hashed1):
#     print('验证成功!')
# else:
#     print('验证失败')
