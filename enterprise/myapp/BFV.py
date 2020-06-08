import requests
import json

def BFV_kengen():
    url = 'http://39.102.39.63:9000/seal/BFV_kengen'
    data = requests.get(url)
    result = data.json()
    return  result['public_key'], result['relin_keys'], result['secret_key']


def BFV_Encrypt(x,public_key):
    url = 'http://39.102.39.63:9000/seal/BFV_Encrypt'
    x_encrypted = json.loads(requests.post(url, data={'x': int(x), 'public_key': public_key}).text)[
        'x_encrypted']
    return x_encrypted

def BFV_Decrypt(x_encrypted,secret_key):
    url = 'http://39.102.39.63:9000/seal/BFV_Decrypt'
    x = (json.loads(requests.post(url, data={'x_encrypted': x_encrypted, 'secret_key': secret_key}).text)[
                'x_decrypted'])
    return x


def BFV_add(x_encrypted, y_encrypted, relin_keys):  # x_encrypted,y_encrypted是明文x，y对应的密文类，返回x+y对应的密文类
    url = 'http://39.102.39.63:9000/seal/BFV_add'
    add_encrypted = json.loads(requests.post(url, data={'x_encrypted': x_encrypted, 'y_encrypted': y_encrypted, 'relin_keys':relin_keys}).text)[
                'add_encrypted']
    return add_encrypted

def BFV_sub(x_encrypted, y_encrypted, relin_keys):  # x_encrypted,y_encrypted是明文x，y对应的密文类，返回x+y对应的密文类
    url = 'http://39.102.39.63:9000/seal/BFV_sub'
    sub_encrypted = json.loads(requests.post(url, data={'x_encrypted': x_encrypted, 'y_encrypted': y_encrypted, 'relin_keys':relin_keys}).text)[
                'sub_encrypted']
    return sub_encrypted

def BFV_mul(lis, relin_keys):
    lis = str(lis)
    url = 'http://39.102.39.63:9000/seal/BFV_mul'
    mul_encrypted = json.loads(requests.post(url, data={'lis': lis, 'relin_keys': relin_keys}).text)[
                'mul_encrypted']
    return mul_encrypted


def BFV_squr(x_encrypted, relin_keys):
    url = 'http://39.102.39.63:9000/seal/BFV_squr'
    squr_encrypted = json.loads(requests.post(url, data={'x_encrypted': x_encrypted, 'relin_keys': relin_keys}).text)[
                'squr_encrypted']
    return squr_encrypted

def BFV_pow(x_encrypted, x, relin_keys, public_key):
    if int(x) == 0:
        return BFV_Encrypt(1,public_key)
    url = 'http://39.102.39.63:9000/seal/BFV_pow'
    pow_encrypted = json.loads(requests.post(url, data={'x_encrypted': x_encrypted,'x': x, 'relin_keys': relin_keys}).text)[
        'pow_encrypted']
    return pow_encrypted
