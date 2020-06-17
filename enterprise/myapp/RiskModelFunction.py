'''
在所有的风险模型中,系数都会从有限小数变成整数进行计算,从而大大地加快运算的效率,
注意:这里的风险计算模型都不带比大小操作,比大小操作在平台上,
是对这些操作的复合运算,需要用求逆差分进行局部同态承若的方式交互进行解密
'''
# from CC_getongtaiN import *
from . import CC_getongtaiN as HLP
from . import paillier
# from paillier import  *
# /**Paillier部分*/
def quick_paillier_pow_mod(a,b,c):#快速乘法,(a^b)%c
    a=a%c
    ans=1
    while b!=0:
        if b&1:
            ans=(ans*a)%c
        b>>=1
        b = int(b)
        a=(a*a)%c
    return ans
#Paillier二元一次多项式情况
def Paillier_HomAdd(x1,x2,a1,a2,c,n):#x1为变量1,x2为变量2,a1为系数1,a2为系数2,c为常数部分密文,n为mod数 result=a1*x1+a2*x2+c
    result = c#paillier_encryption(g,c,r,n)#否则传入的c是明文
    N = n*n
    result= result*quick_paillier_pow_mod(x1,a1,N)*quick_paillier_pow_mod(x2,a2,N)
    return result

# Paillier多元一次多项式情况
def Paillier_HomAdd_More(x,a,num,c,n):#x为变量密文数组,a为系数数组,num为变量的个数,c为常数部分密文,n为mod数,result=a1*x1+a2*x2+...+a_num*x_num+c
    result = c#paillier_encryption(g,c,r,n)#否则传入的c是明文
    M = n*n
    for i in range(0, num):  # 1~n
        result= result*quick_paillier_pow_mod(x[i],a[i],M)
    return result



# /**Hlp部分*/
def quick_hlp_pow_mod(a,b,col,p):#快速加法
    ans = [0 for i in range(col)]
    ans = [ans]
    while b!=0:
        if b&1:
            ans=HLP.MatrixAdd(ans,a,1,col,p)
        b>>=1
        b = int(b)
        a=HLP.MatrixAdd(a,a,1,col,p)
    return ans

#Hlp二元一次多项式情况
def HLP_HomAdd(x1, x2, a1, a2, c ,N,p):  #x1为变量1,x2为变量2,a1为系数1,a2为系数2,c为常数部分密文,N,p为HLP的参数,result=a1*x1+a2*x2+c
    result = c
    tmp1 = quick_hlp_pow_mod(x1,a1,2 * N,p)
    tmp2 = quick_hlp_pow_mod(x2,a2,2 * N,p)
    result = HLP.MatrixAdd(result, tmp1, 1, 2 * N, p)
    result = HLP.MatrixAdd(result, tmp2, 1, 2 * N, p)
    return result

# Hlp多元一次多项式情况
def HLP_HomAdd_More(x,a,c,num,N,p):#x为变量密文数组,a为系数数组,c为常数部分密文,num为变量的个数,N,p为HLP的参数,result=a1*x1+a2*x2+...+a_num*x_num+c
    result = c
    for i in range(0,num):
        result =HLP.MatrixAdd(result, quick_hlp_pow_mod(x[i],a[i],2 * N,p), 1, 2 * N, p)
    return result


# from BFV import *
from . import BFV
# /**BFV部分*/

def quick_bfv_add_pow_mod(a, b, relin, public_key):#快速加法,减法是加法的逆元
    encrypted_b = BFV.BFV_Encrypt(b, public_key)
    ans=BFV.BFV_mul(str([a, encrypted_b]), relin)
    return ans


#BFV形如特殊的二元二次多项式情况 result=a1*x1+a2*x2+a3*x1*x2+c
def BFV_Hom(x1, x2, a1, a2, a3, c, relin, public_key):  # x1为变量1,x2为变量2,a1为系数1,a2为系数2,c为常数 result=a1*x1+a2*x2+a3*x1*x2+c
    result = c
    tmp1 = quick_bfv_add_pow_mod(x1, a1, relin, public_key)
    result = BFV.BFV_add(result, tmp1, relin)   # result= result+(a1*x1)
    tmp2 = quick_bfv_add_pow_mod(x2, a2, relin, public_key)
    result = BFV.BFV_add(result, tmp2, relin)   # result= result+(a2*x2)
    tmp3 = BFV.BFV_mul(str([x1, x2]),relin)
    tmp4 = quick_bfv_add_pow_mod(tmp3, a3, relin, public_key)
    result = BFV.BFV_add(result, tmp4, relin)#result=result+a3*x1*x2
    return result


#BFV多元高次多项式情况
def BFV_Hom_More(x, a, cimi, c, num, relin, public_key):#x为1*num的一维数组,a为1*num的一维数组，cimi为num*num的二维数组,c为常数密文,多项式形如num元多次
    result = c
    one = BFV.BFV_Encrypt(1, public_key)
    for i in range(0,num):  # 1~n
        linshi = one
        for j in range(0, num):  # 1~n
            tmp1 = BFV.BFV_pow(x[j], cimi[i][j], relin,public_key)
            linshi = BFV.BFV_mul(str([linshi, tmp1]), relin)
        linshi = quick_bfv_add_pow_mod(linshi, a[i], relin, public_key)
        result = BFV.BFV_add(result, linshi, relin)
    return result



# /**CKKS部分*/
# from CKKS import *
from . import CKKS

def quick_ckks_mul_pow_mod(a, b, rel, pub):#快速乘法,除法是乘法的逆元
    ans = CKKS.CKKS_Encrypt(1, pub)
    while b != 0:
        if b & 1:
            ans = CKKS.CKKS_mul(a, ans, rel)
        b >>= 1
        b = int(b)
        a = CKKS.CKKS_mul(a, a, rel)
    return ans

def quick_ckks_add_pow_mod(a,b, relin, public_key):#减法是加法的逆元
    ans = CKKS.CKKS_Encrypt(0, public_key)
    while b!=0:
        if b&1:
            ans=CKKS.CKKS_add(ans, a, relin)
        b>>=1
        b = int(b)
        a=CKKS.CKKS_add(a, a, relin)
    return ans

#BFV形如特殊的二元二次多项式情况 result=a1*x1+a2*x2+a3*x1*x2+c
def CKKS_Hom(x1, x2, a1, a2, a3, c, relin, public_key):  # x1为变量1,x2为变量2,a1为系数1,a2为系数2,c为常数 result=a1*x1+a2*x2+a3*x1*x2+c
    result = c
    tmp1 = quick_ckks_add_pow_mod(x1, a1, relin, public_key)
    result = CKKS.CKKS_add(result, tmp1, relin)   # result= result+(a1*x1)
    tmp2 = quick_ckks_add_pow_mod(x2, a2, relin, public_key)
    result = CKKS.CKKS_add(result, tmp2, relin)   # result= result+(a2*x2)
    tmp3 = CKKS.CKKS_mul(x1, x2,relin)
    tmp4 = quick_ckks_add_pow_mod(tmp3, a3, relin, public_key)
    result = CKKS.CKKS_add(result, tmp4, relin)#result=result+a3*x1*x2
    return result

# CKKS多元高次多项式情况
def CKKS_Hom_More(x, a, cimi, c, num, relin, public_key):#x为1*num的一维数组,a为1*num的一维数组，cimi为num*num的二维数组,c为常数密文,多项式形如num元多次
    result = c
    one = CKKS.CKKS_Encrypt(1, public_key)
    for i in range(0,num):  # 1~n
        linshi = one
        tot = 0
        for j in range(0, num):  # 1~n
            tot = tot + cimi[i][j]
        print('tot:', tot)
        if tot <= 4:
            lis = []
            for j in range(0, num):
                while cimi[i][j] > 0:
                    lis.append(x[j])
                    cimi[i][j] = cimi[i][j] - 1
            linshi = CKKS.CKKS_mul1(lis, relin)
        linshi = quick_ckks_add_pow_mod(linshi, a[i], relin, public_key)
        result = CKKS.CKKS_add(result, linshi, relin)
    return result
'''
/***这只是一个Tips***/
def diaoyong_fuction():
    / ** *如下函数调用方法 ** * /
    Paillier_HomAdd(x1, x2, a1, a2, c, n)  # 二元一次result=a1*x1+a2*x2+c
    Paillier_HomAdd_More(x, a, num, c, n)  # 多元一次result=a1*x1+a2*x2+...+a_num*x_num+c

    HLP_HomAdd(x1, x2, a1, a2, c, N, p)  # 二元一次result=a1*x1+a2*x2+c
    HLP_HomAdd_More(x, a, c, num, N, p)  # 多元一次result=a1*x1+a2*x2+...+a_num*x_num+c

    BFV_Hom(x1, x2, a1, a2, a3, c)  # 特殊二元二次result=a1*x1+a2*x2+a3*x1*x2+c
    BFV_Hom_More(x, a, cimi, c, num)  # 多元高次

    CKKS_Hom(x1, x2, a1, a2, a3, c)  # 特殊二元二次result=a1*x1+a2*x2+a3*x1*x2+c
    CKKS_Hom_More(x, a, cimi, c, num)  # 多元高次

'''
def paillier_func():
    n, g, r, lamda, u = paillier.paillier_generation()  # 密钥生成 n,g公钥 lamda，v私钥
    m1 = 12011
    m2 = 3122
    a1 = 3
    a2 = 2
    x1 = paillier.paillier_encryption(g, m1, r, n)
    x2 = paillier.paillier_encryption(g, m2, r, n)
    c = paillier.paillier_encryption(g, 3, r, n)
    res = Paillier_HomAdd(x1, x2, a1, a2, c, n)
    ans = paillier.paillier_decryption(res, g, lamda, n, u)
    print(ans)
    x = [x1,x2]
    a = [a1,a2]
    num = 2
    res = Paillier_HomAdd_More(x, a, num, c, n)
    ans = paillier.paillier_decryption(res, g, lamda, n, u)
    print(ans)


def HLP_func():
    N, l, Mhard, Msoft, random_numbers, p, Deta, A, B, q, n, sigema_max, l_0, sigma, r = key_generartion()  # 密钥生成
    m1 = 12011
    m2 = 3122
    a1 = 3
    a2 = 2
    c = 3
    m1 = HLP.long_to_two(m1, N)
    m2 = HLP.long_to_two(m2, N)
    c = HLP.long_to_two(c, N)
    x1 = HLP.lattice_encryption(m1, Mhard, Msoft, random_numbers, N, n, p)
    x2 = HLP.lattice_encryption(m2, Mhard, Msoft, random_numbers, N, n, p)
    c = HLP.lattice_encryption(c, Mhard, Msoft, random_numbers, N, n, p)
    res = HLP_HomAdd(x1, x2, a1, a2, c, N, p)  # x1为变量1,x2为变量2,a1为系数1,a2为系数2,c为常数部分密文,N,p为HLP的参数,result=a1*x1+a2*x2+c
    ans = HLP.lattice_decryption(res, Deta, A, B, N, p, q)
    ans = HLP.two_to_long(ans, N)
    print(ans)
    x = [x1, x2]
    a = [a1, a2]
    num = 2
    res = HLP_HomAdd_More(x, a, c, num, N, p)
    ans = HLP.lattice_decryption(res, Deta, A, B, N, p, q)
    ans = HLP.two_to_long(ans, N)
    print(ans)


def BFV_func():
    pub, rel, sec = BFV.BFV_kengen()
    m1 = 102
    m2 = 32
    a1 = 3
    a2 = 2
    a3 = 1
    c = 3
    x1 = BFV.BFV_Encrypt(m1, pub)
    x2 = BFV.BFV_Encrypt(m2, pub)
    c = BFV.BFV_Encrypt(c, pub)
    res = BFV_Hom(x1, x2, a1, a2, a3, c, rel, pub)
    ans = BFV.BFV_Decrypt(res,sec)
    print(ans)
    x = [x1, x2, BFV.BFV_mul(str([x1, x2]), rel)]
    a = [a1, a2, a3]
    cimi = [[1,0,0], [0,1,0], [1,1,0]]
    res = BFV_Hom_More(x, a, cimi, c, 3, rel, pub)
    ans = BFV.BFV_Decrypt(res, sec)
    print(ans)


def CKKS_func():
    pub, rel, sec = CKKS.CKKS_kengen()
    m1 = 102
    m2 = 32
    a1 = 3
    a2 = 2
    a3 = 1
    c = 3
    x1 = CKKS.CKKS_Encrypt(m1, pub)
    x2 = CKKS.CKKS_Encrypt(m2, pub)
    c = CKKS.CKKS_Encrypt(c, pub)
    res = CKKS_Hom(x1, x2, a1, a2, a3, c, rel, pub)
    ans = CKKS.CKKS_Decrypt(res, sec)
    print(ans)
    x = [x1, x2, CKKS.CKKS_mul(x1, x2, rel)]
    a = [a1, a2, a3]
    cimi = [[1, 0, 0], [0, 1, 0], [1, 1, 0]]
    res = CKKS_Hom_More(x, a, cimi, c, 3, rel, pub)
    ans = CKKS.CKKS_Decrypt(res, sec)
    print(ans)

if __name__ == "__main__":
    # paillier_func()
    # HLP_func()
    #BFV_func()
    CKKS_func()
