'''
python实现
AES 128位CBC加密模式，填充模式采用PKCs5Padding/PKCs7Padding
'''
import json

import numpy as np
from functools import reduce
import base64

# def multiply(a,b):
#     if b==0x01:
#         c=a
#     elif b==0x02:
#         c=a<<1;
#     elif b==0x03:
#         c=(a<<1)^a
#     elif b==0x09:
#         c=(a<<3)^a
#     elif b==0x0b:
#         c=(a<<3)^(a<<1)^a
#     elif b==0x0d:
#         c=(a<<3)^(a<<2)^a
#     elif b==0x0e:
#         c=(a<<3)^(a<<2)^(a<<1)
#     else:
#         print('error')
#     if c&0x0400:
#         c=(c&0x03ff)^0b01101100
#     if c&0x0200:
#         c=(c&0x01ff)^0b00110110
#     if c&0x0100:
#         c=(c&0xff)^0b00011011
#     return c
# def ByteSubstitution(A,Sbox):
#     B=np.zeros(A.shape,dtype=int)
#     for i in range(A.shape[0]):
#         for j in range(A.shape[1]):
#             B[i,j]=Sbox[A[i,j]]
#     return B
# def T(W_col,Rcon,Sbox,j):
#     v=W_col.copy()
#     temp=v[0]
#     for i in range(len(v)-1):
#         v[i]=v[i+1]
#     v[len(v)-1]=temp
#     for i in range(len(v)):
#         v[i]=Sbox[v[i]]
#     v[0]=v[0]^((Rcon[j]&0xFF000000)>>24)
#     v[1]=v[1]^((Rcon[j]&0x00FF0000)>>16)
#     v[2]=v[2]^((Rcon[j]&0x0000FF00)>>8)
#     v[3]=v[3]^((Rcon[j]&0x000000FF))
#     return v
# def ExtendKey(key,lens,rnd):
#     W=np.zeros([4,lens*(rnd+1)//32],dtype=int)
#     for i in range(4):
#         W[:,i]=key[:,i]
#     for i in range(4,lens*(rnd+1)//32):
#         if i%4!=0:
#             W[:,i]=W[:,i-4]^W[:,i-1]
#         else:
#             W[:,i]=W[:,i-4]^T(W[:,i-1],Rcon,Sbox,i//4-1)
#     return W
# def ByteRotation(A):
#     B=np.zeros(A.shape,dtype=int)
#     for i in range(A.shape[0]):
#         for j in range(A.shape[1]):
#             B[i,j]=A[i,(j+i)%A.shape[1]]
#     return B
# def MixColumn(A,cx):
#     B=np.zeros(A.shape,dtype=int)
#     temp=np.zeros(4,dtype=int)
#     for i in range(cx.shape[0]):
#         for j in range(cx.shape[0]):
#             for k in range(cx.shape[1]):
#                 temp[k]=multiply(A[k,i],cx[j,k])
#             B[j,i]=reduce(lambda x,y:x^y,temp)
#     return B
# def EN_AES(Sbox,cx,key,plain,iv):
#     iv=list(iv.encode())
#     plain=list(plain.encode())+[16-len(plain.encode())%16]*(16-len(plain.encode())%16)
#     # plain=list(plain.encode())+[8-len(plain.encode())%8]*(8-len(plain.encode())%8)
#     key=np.array(list(key.encode())).reshape(4,4).T
#     W=ExtendKey(key,128,10)
#     temp=np.array([np.array(plain[i:i+16]).reshape(4,4).T for i in range(0,len(plain),16)])
#     P=np.concatenate(temp,axis=1)
#     C=np.zeros(P.shape,dtype=int)
#     last=np.array(iv).reshape(4,4).T
#     for i in range(0,P.shape[1],4):
#         P[:,i:i+4]=last^P[:,i:i+4]
#         C[:,i:i+4]=P[:,i:i+4]^W[:,0:4]
#         for j in range(10):
#             C[:,i:i+4]=ByteSubstitution(C[:,i:i+4],Sbox)
#             C[:,i:i+4]=ByteRotation(C[:,i:i+4])
#             if j!=9:
#                 C[:,i:i+4]=MixColumn(C[:,i:i+4],cx)
#             C[:,i:i+4]=C[:,i:i+4]^W[:,4*j+4:4*j+8]
#         last=C[:,i:i+4]
#     cipher=base64.b64encode(bytes(list(C.flatten('F')))).decode()
#     return str(cipher)
#
# def InvMixColumn(A,Invcx):
#     return MixColumn(A,Invcx)
#
# def InvByteRotation(A):
#     B=np.zeros(A.shape,dtype=int)
#     for i in range(A.shape[0]):
#         for j in range(A.shape[1]):
#             B[i,j]=A[i,(j-i)%A.shape[1]]
#     return B
#
# def InvByteSubstitution(A,InvSbox):
#     return ByteSubstitution(A,InvSbox)
#
# def DE_AES(InvSbox, Invcx, key, cipher, iv):
#     # iv=list('123'.encode())+[0]*13
#     iv = list(iv.encode())
#     # cipher=list(base64.b64decode(c))
#     cipher=list(base64.b64decode(cipher))
#     # key=np.array(list(key.encode())+[0]*(16-len(key.encode())%16)).reshape(4,4).T
#     key=np.array(list(key.encode())).reshape(4,4).T
#     W=ExtendKey(key,128,10)
#     temp=np.array([np.array(cipher[i:i+16]).reshape(4,4).T for i in range(0,len(cipher),16)])
#     # temp=np.array([np.array(cipher[i:i+8]).reshape(4,4).T for i in range(0,len(cipher),8)])
#     C=np.concatenate(temp,axis=1)
#     P=np.zeros(C.shape,dtype=int)
#     last=np.array(iv).reshape(4,4).T
#     for i in range(0,C.shape[1],4):
#         P[:,i:i+4]=C[:,i:i+4]^W[:,W.shape[1]-4:W.shape[1]]
#         for j in range(10):
#             P[:,i:i+4]=InvByteRotation(P[:,i:i+4])
#             P[:,i:i+4]=InvByteSubstitution(P[:,i:i+4],InvSbox)
#             P[:,i:i+4]=P[:,i:i+4]^W[:,W.shape[1]-4*j-8:W.shape[1]-4*j-4]
#             if j!=9:
#                 P[:,i:i+4]=InvMixColumn(P[:,i:i+4],Invcx)
#         P[:,i:i+4]=P[:,i:i+4]^last
#         last=C[:,i:i+4]
#     plain=''.join(chr(x) for x in P.flatten('F'))
#     pad=plain[len(plain)-1]*ord(plain[len(plain)-1])
#     plain=plain.replace(pad,'')
#     return plain
# Sbox=[0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
#     0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
#     0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
#     0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
#     0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
#     0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
#     0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
#     0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
#     0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
#     0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
#     0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
#     0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
#     0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
#     0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
#     0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
#     0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16]
# InvSbox=[0x52,0x09,0x6a,0xd5,0x30,0x36,0xa5,0x38,0xbf,0x40,0xa3,0x9e,0x81,0xf3,0xd7,0xfb,
#     0x7c,0xe3,0x39,0x82,0x9b,0x2f,0xff,0x87,0x34,0x8e,0x43,0x44,0xc4,0xde,0xe9,0xcb,
#     0x54,0x7b,0x94,0x32,0xa6,0xc2,0x23,0x3d,0xee,0x4c,0x95,0x0b,0x42,0xfa,0xc3,0x4e,
#     0x08,0x2e,0xa1,0x66,0x28,0xd9,0x24,0xb2,0x76,0x5b,0xa2,0x49,0x6d,0x8b,0xd1,0x25,
#     0x72,0xf8,0xf6,0x64,0x86,0x68,0x98,0x16,0xd4,0xa4,0x5c,0xcc,0x5d,0x65,0xb6,0x92,
#     0x6c,0x70,0x48,0x50,0xfd,0xed,0xb9,0xda,0x5e,0x15,0x46,0x57,0xa7,0x8d,0x9d,0x84,
#     0x90,0xd8,0xab,0x00,0x8c,0xbc,0xd3,0x0a,0xf7,0xe4,0x58,0x05,0xb8,0xb3,0x45,0x06,
#     0xd0,0x2c,0x1e,0x8f,0xca,0x3f,0x0f,0x02,0xc1,0xaf,0xbd,0x03,0x01,0x13,0x8a,0x6b,
#     0x3a,0x91,0x11,0x41,0x4f,0x67,0xdc,0xea,0x97,0xf2,0xcf,0xce,0xf0,0xb4,0xe6,0x73,
#     0x96,0xac,0x74,0x22,0xe7,0xad,0x35,0x85,0xe2,0xf9,0x37,0xe8,0x1c,0x75,0xdf,0x6e,
#     0x47,0xf1,0x1a,0x71,0x1d,0x29,0xc5,0x89,0x6f,0xb7,0x62,0x0e,0xaa,0x18,0xbe,0x1b,
#     0xfc,0x56,0x3e,0x4b,0xc6,0xd2,0x79,0x20,0x9a,0xdb,0xc0,0xfe,0x78,0xcd,0x5a,0xf4,
#     0x1f,0xdd,0xa8,0x33,0x88,0x07,0xc7,0x31,0xb1,0x12,0x10,0x59,0x27,0x80,0xec,0x5f,
#     0x60,0x51,0x7f,0xa9,0x19,0xb5,0x4a,0x0d,0x2d,0xe5,0x7a,0x9f,0x93,0xc9,0x9c,0xef,
#     0xa0,0xe0,0x3b,0x4d,0xae,0x2a,0xf5,0xb0,0xc8,0xeb,0xbb,0x3c,0x83,0x53,0x99,0x61,
#     0x17,0x2b,0x04,0x7e,0xba,0x77,0xd6,0x26,0xe1,0x69,0x14,0x63,0x55,0x21,0x0c,0x7d]
#
# Rcon=[0x01000000,0x02000000,0x04000000,0x08000000,0x10000000,0x20000000,0x40000000,0x80000000,0x1B000000,0x36000000]
# cx=np.array([[2,3,1,1], [1,2,3,1],[1,1,2,3],[3,1,1,2]])
# Invcx=np.array([[0x0e,0x0b,0x0d,0x09],[0x09,0x0e,0x0b,0x0d],[0x0d,0x09,0x0e,0x0b],[0x0b,0x0d,0x09,0x0e]])


# key = 'yTwsk9MvRJhc5wRN'
# iv = 'rEIZ5M4JcAL4Tz8F'
# plain = 'nQvY8cL0eQiaoMuK/tFpQL9yknxgL9Zb1snvST8/t+s='
# key = 'nHwsk9MvRJhc5wRN'
# iv = 'wjIZ5M4JcAL4Tz8F'
#
# data = {"quota":20,"id":64,"userId":1}
#
#
# plain = json.dumps(data).replace(' ','')
#
# c = EN_AES(Sbox, cx, key, plain, iv)
# p = DE_AES(InvSbox, Invcx, key, c, iv)
#
# print(c)
# print(p)


class AESCBC:

    Sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
            0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
            0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
            0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
            0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
            0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
            0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
            0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
            0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
            0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
            0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
            0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
            0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
            0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
            0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]

    InvSbox = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
               0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
               0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
               0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
               0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
               0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
               0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
               0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
               0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
               0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
               0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
               0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
               0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
               0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
               0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
               0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]

    Rcon = [0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000, 0x20000000, 0x40000000, 0x80000000, 0x1B000000,
            0x36000000]
    cx = np.array([[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]])
    Invcx = np.array(
        [[0x0e, 0x0b, 0x0d, 0x09], [0x09, 0x0e, 0x0b, 0x0d], [0x0d, 0x09, 0x0e, 0x0b], [0x0b, 0x0d, 0x09, 0x0e]])

    def __init__(self, key=None, iv=None):
        if not key:
            key = 'nHwsk9MvRJhc5wRN'
        if not iv:
            iv = 'wjIZ5M4JcAL4Tz8F'
        self.key = key
        self.iv = iv

    def multiply(self, a, b):
        if b == 0x01:
            c = a
        elif b == 0x02:
            c = a << 1
        elif b == 0x03:
            c = (a << 1) ^ a
        elif b == 0x09:
            c = (a << 3) ^ a
        elif b == 0x0b:
            c = (a << 3) ^ (a << 1) ^ a
        elif b == 0x0d:
            c = (a << 3) ^ (a << 2) ^ a
        elif b == 0x0e:
            c = (a << 3) ^ (a << 2) ^ (a << 1)
        else:
            print('error')
        if c & 0x0400:
            c = (c & 0x03ff) ^ 0b01101100
        if c & 0x0200:
            c = (c & 0x01ff) ^ 0b00110110
        if c & 0x0100:
            c = (c & 0xff) ^ 0b00011011
        return c

    def ByteSubstitution(self, A, Sbox):
        B = np.zeros(A.shape, dtype=int)
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                B[i, j] = Sbox[A[i, j]]
        return B

    def T(self, W_col, Rcon, Sbox, j):
        v = W_col.copy()
        temp = v[0]
        for i in range(len(v) - 1):
            v[i] = v[i + 1]
        v[len(v) - 1] = temp
        for i in range(len(v)):
            v[i] = Sbox[v[i]]
        v[0] = v[0] ^ ((Rcon[j] & 0xFF000000) >> 24)
        v[1] = v[1] ^ ((Rcon[j] & 0x00FF0000) >> 16)
        v[2] = v[2] ^ ((Rcon[j] & 0x0000FF00) >> 8)
        v[3] = v[3] ^ ((Rcon[j] & 0x000000FF))
        return v

    def ExtendKey(self, key, lens, rnd):
        W = np.zeros([4, lens * (rnd + 1) // 32], dtype=int)
        for i in range(4):
            W[:, i] = key[:, i]
        for i in range(4, lens * (rnd + 1) // 32):
            if i % 4 != 0:
                W[:, i] = W[:, i - 4] ^ W[:, i - 1]
            else:
                W[:, i] = W[:, i - 4] ^ self.T(W[:, i - 1], self.Rcon, self.Sbox, i // 4 - 1)
        return W

    def ByteRotation(self, A):
        B = np.zeros(A.shape, dtype=int)
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                B[i, j] = A[i, (j + i) % A.shape[1]]
        return B

    def MixColumn(self, A, cx):
        B = np.zeros(A.shape, dtype=int)
        temp = np.zeros(4, dtype=int)
        for i in range(cx.shape[0]):
            for j in range(cx.shape[0]):
                for k in range(cx.shape[1]):
                    temp[k] = self.multiply(A[k, i], cx[j, k])
                B[j, i] = reduce(lambda x, y: x ^ y, temp)
        return B

    def EN_AES(self, plain):

        key = self.key
        iv = self.iv
        cx = self.cx
        Sbox = self.Sbox


        iv = list(iv.encode())
        plain = list(plain.encode()) + [16 - len(plain.encode()) % 16] * (16 - len(plain.encode()) % 16)
        key = np.array(list(key.encode())).reshape(4, 4).T
        W = self.ExtendKey(key, 128, 10)
        temp = np.array([np.array(plain[i:i + 16]).reshape(4, 4).T for i in range(0, len(plain), 16)])
        P = np.concatenate(temp, axis=1)
        C = np.zeros(P.shape, dtype=int)
        last = np.array(iv).reshape(4, 4).T
        for i in range(0, P.shape[1], 4):
            P[:, i:i + 4] = last ^ P[:, i:i + 4]
            C[:, i:i + 4] = P[:, i:i + 4] ^ W[:, 0:4]
            for j in range(10):
                C[:, i:i + 4] = self.ByteSubstitution(C[:, i:i + 4], Sbox)
                C[:, i:i + 4] = self.ByteRotation(C[:, i:i + 4])
                if j != 9:
                    C[:, i:i + 4] = self.MixColumn(C[:, i:i + 4], cx)
                C[:, i:i + 4] = C[:, i:i + 4] ^ W[:, 4 * j + 4:4 * j + 8]
            last = C[:, i:i + 4]
        cipher = base64.b64encode(bytes(list(C.flatten('F')))).decode()
        return str(cipher)

    def InvMixColumn(self, A, Invcx):
        return self.MixColumn(A, Invcx)

    def InvByteRotation(self, A):
        B = np.zeros(A.shape, dtype=int)
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                B[i, j] = A[i, (j - i) % A.shape[1]]
        return B

    def InvByteSubstitution(self, A, InvSbox):
        return self.ByteSubstitution(A, InvSbox)

    def DE_AES(self, cipher):

        if type(cipher) == type('string'):
            cipher = cipher.encode()

        InvSbox = self.InvSbox
        Invcx = self.Invcx
        key = self.key
        iv = self.iv

        # iv=list('123'.encode())+[0]*13
        iv = list(iv.encode())
        cipher = list(base64.b64decode(cipher))
        key = np.array(list(key.encode())).reshape(4, 4).T
        W = self.ExtendKey(key, 128, 10)
        temp = np.array([np.array(cipher[i:i + 16]).reshape(4, 4).T for i in range(0, len(cipher), 16)])
        C = np.concatenate(temp, axis=1)
        P = np.zeros(C.shape, dtype=int)
        last = np.array(iv).reshape(4, 4).T
        for i in range(0, C.shape[1], 4):
            P[:, i:i + 4] = C[:, i:i + 4] ^ W[:, W.shape[1] - 4:W.shape[1]]
            for j in range(10):
                P[:, i:i + 4] = self.InvByteRotation(P[:, i:i + 4])
                P[:, i:i + 4] = self.InvByteSubstitution(P[:, i:i + 4], InvSbox)
                P[:, i:i + 4] = P[:, i:i + 4] ^ W[:, W.shape[1] - 4 * j - 8:W.shape[1] - 4 * j - 4]
                if j != 9:
                    P[:, i:i + 4] = self.InvMixColumn(P[:, i:i + 4], Invcx)
            P[:, i:i + 4] = P[:, i:i + 4] ^ last
            last = C[:, i:i + 4]
        plain = ''.join(chr(x) for x in P.flatten('F'))
        pad = plain[len(plain) - 1] * ord(plain[len(plain) - 1])
        plain = plain.replace(pad, '')
        return plain

aes = AESCBC()

plain = 'nQvY8cL0eQiaoMuK/tFpQL9yknxgL9Zb1snvST8/t+s='

print(aes.DE_AES(plain.encode()))

raw = "{'a':1,'b':2}"

print(aes.EN_AES(raw))
print(aes.DE_AES(aes.EN_AES(raw)))