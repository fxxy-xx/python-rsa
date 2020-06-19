import random
import math
from math import sqrt

#获取1000以内的素数
def is_prime(n): 

    if n == 1: 
        return False 
    for i in range(2, int(sqrt(n))+1): 
        if n % i == 0: 
            return False 
    return True 
#用1000以内的素数进行初步判断
def primes_check(n):
    primes = []
    for i in range(1,1000):
        if is_prime(i):
            primes.append(i)

    for i in primes:
        print('现在是 %d 除以 %d  , 余数为：%d'%(n,i,n%i))
        if n%i==0:
            print("第一步就排除了%d"%n)
            return False
    #print('成功通过100以内的素数')
    return True
#验证费马定理
def pow_mod(p, q, n):
    '''
    幂模运算，快速计算(p^q) mod (n)
    这里采用了蒙哥马利算法
    '''
    res = 1
    while q :
        if q & 1:
            res = (res * p) % n
        q >>= 1
        p = (p * p) % n
    return res
#求d
def mod_1(x, n):
    '''
    扩展欧几里得算法求模逆
    取模负1的算法:计算x2= x^-1 (mod n)的值
    '''
    x0 = x
    y0 = n
    x1 = 0
    y1 = 1
    x2 = 1
    y2 = 0
    while n != 0:
            q = x // n
            (x, n) = (n, x % n)
            #print('%d = %d * %d + %d'%(n,x,y1,y2))
            (x1, x2) = ((x2 - (q * x1)), x1)
            (y1, y2) = ((y2 - (q * y1)), y1)
            #print('x1 x2 y1 y2 q n x :%d %d %d %d  %d  %d  %d'%(x1,x2,y1,y2,q,n,x))
    if x2 < 0:
            x2 += y0
    if y2 < 0:
            y2 += x0
    return x2

#用miller_rabin算法对n进行检测
def prime_miller_rabin(a, n): # 检测n是否为素数
    
    if pow_mod(a, n-1, n) == 1: # 费马定理
        d = n-1 # d=2^q*m, 求q和m
        q = 0
        while not(d & 1):  # 末尾是0
            q = q+1
            d >>= 1
        m = d

        #二次探测
        for i in range(q):  # 0~q-1, 我们先找到的最小的a^u，再逐步扩大到a^((n-1)/2)
            u = m * (2**i)  # u = 2^i * m
            tmp = pow_mod(a, u, n)
            if tmp == 1 or tmp == n-1:
                # 满足条件 
                return True
        return False
    else:
        return False


#对素数调用1000以内的检测方法以及miller-rabin算法进行检测
def prime_test(n, k):
    #第一步：用1000以内的数检测
        if primes_check(n):
            print("数字%d通过了1000以内的素数检测"%n)
            #第二步：用Miller-rabin检测
            while k > 0:
                a = random.randint(2, n-1)
                if not prime_miller_rabin(a, n):
                    return False
                print('%d通过了第%d次检测'%(n,6-k))
                k = k - 1
                while k == 0:
                    return True

def rsa_jiami(e,n):
    M = input('输入需要加密的明文：')
    print('\n----------------加密---------------')

    M = bin(int.from_bytes(M.encode(), 'big'))
    print('字符串转换为二进制后：', M)

    M = int(M,2)
    print('二进制转换为十进制后：', M)
    
    C = pow_mod(M,e,n)
    
    return C

def rsa_jiemi(d,n,C):

    print('\n-----------------解密----------------')

    M = pow_mod(C,d,n)
    

    print('密文转换为十进制：',M)
    _M2 = M.to_bytes((M.bit_length() + 7) // 8, 'big').decode()
    return _M2


if __name__=='__main__':
    p = gmpy2.next_prime(int(urandom(k / 8).encode('hex'),16))
    q = gmpy2.next_prime(int(urandom(k / 8).encode('hex'),16))
    
    n = p * q   # 公开n
    OrLa = (p-1)*(q-1)  # 欧拉函数
    e = 37

    d = mod_1(e, OrLa)

    print('私钥p,q,d分别为:\n')
    print('p: %d\n' % p)
    print('q: %d\n' % q)
    # print('d: %d\n\n' % d)
    print('OrLa:%d'%OrLa)

    print('\n---------------------------------')
    print('公钥n,e分别为:\n')
    print('n: %d\n' % n)
    print('e: %d\n\n' % e)

    print('\n---------------------------------')
    print('私钥n,d为:\n')
    print('n: %d\n' % n)
    print('d: %d\n\n' % d)


    #M = int(input("请输入待加密的明文："))
    
    C = []
    C = rsa_jiami( e, n) # 加密

    print('\n---------------------------------')
    print('\n加密完成，得到的密文：%d\n'%C)

    M = rsa_jiemi(d, n,C) # 解密
    print('\n解密完成，得到的明文为：%s\n'%M)
