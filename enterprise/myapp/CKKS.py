import requests
import json

def CKKS_kengen():
    url = 'http://39.102.39.63:9000/seal/CKKS_kengen'
    data = requests.get(url)
    result = data.json()
    return  result['public_key'], result['relin_keys'], result['secret_key']


def CKKS_Encrypt(x,public_key):
    url = 'http://39.102.39.63:9000/seal/CKKS_Encrypt'
    x_encrypted = json.loads(requests.post(url, data={'x': int(x), 'public_key': public_key}).text)[
        'x_encrypted']
    return x_encrypted

def CKKS_Decrypt(x_encrypted,secret_key):
    url = 'http://39.102.39.63:9000/seal/CKKS_Decrypt'
    x = (json.loads(requests.post(url, data={'x_encrypted': x_encrypted, 'secret_key': secret_key}).text)[
                'x_decrypted'])
    return x


def CKKS_add(x_encrypted, y_encrypted, relin_keys):  # x_encrypted,y_encrypted是明文x，y对应的密文类，返回x+y对应的密文类
    url = 'http://39.102.39.63:9000/seal/CKKS_add'
    add_encrypted = json.loads(requests.post(url, data={'x_encrypted': x_encrypted, 'y_encrypted': y_encrypted, 'relin_keys':relin_keys}).text)[
                'add_encrypted']
    return add_encrypted

def CKKS_sub(x_encrypted, y_encrypted, relin_keys):  # x_encrypted,y_encrypted是明文x，y对应的密文类，返回x+y对应的密文类
    url = 'http://39.102.39.63:9000/seal/CKKS_sub'
    sub_encrypted = json.loads(requests.post(url, data={'x_encrypted': x_encrypted, 'y_encrypted': y_encrypted, 'relin_keys':relin_keys}).text)[
                'sub_encrypted']
    return sub_encrypted


def CKKS_mul1(lis, relin_keys):
    lis = str(lis)
    lis = eval(lis)
    if len(lis) == 1:
        return lis[0]
    lis = str(lis)
    url = 'http://39.102.39.63:9000/seal/CKKS_mul1'
    mul_encrypted = json.loads(requests.post(url, data={'lis': lis, 'relin_keys': relin_keys}).text)[
                'mul_encrypted']
    return mul_encrypted


def CKKS_mul(x_encrypted, y_encrypted, relin_keys):
    url = 'http://39.102.39.63:9000/seal/CKKS_mul'
    mul_encrypted = json.loads(requests.post(url, data={'x_encrypted': x_encrypted, 'y_encrypted' : y_encrypted, 'relin_keys': relin_keys}).text)[
                'mul_encrypted']
    return mul_encrypted


def CKKS_squr(x_encrypted, relin_keys):
    url = 'http://39.102.39.63:9000/seal/CKKS_squr'
    squr_encrypted = json.loads(requests.post(url, data={'x_encrypted': x_encrypted, 'relin_keys': relin_keys}).text)[
                'squr_encrypted']
    return squr_encrypted
'''
def CKKS_pow(x_encrypted, x, relin_keys, public_key):
    if int(x) == 0:
        return CKKS_Encrypt(1,public_key)
    url = 'http://39.102.39.63:9000/seal/CKKS_pow'
    pow_encrypted = json.loads(requests.post(url, data={'x_encrypted': x_encrypted,'x': x, 'relin_keys': relin_keys}).text)[
        'pow_encrypted']
    return pow_encrypted
'''