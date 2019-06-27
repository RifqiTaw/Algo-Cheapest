import numpy as np
import random
# def nest_empty(self,nest):
#     nests = []
#     if self.cur_tsp
#     for i in range(self.numNest):
#         nests.append(self.initialSolution(nest))
#     return nests
#
# def get_cuckoo(self,candidate):
#     if self.cur_tsp:
#         for i in range(self.numNest):
#             cuckooNest = self.nest_empty()
#             cuckoo  = list(cuckooNest)
#             pjgCuckoo = len(cuckoo)
#             interval = [1/pjgCuckoo* i for i in range(pjgCuckoo+1)]
#             stepsize = abs(self.levy_flight())
#
#             # len_cuckoo = len(cuckoo)
#             # inipath = list(range(0,len_cuckoo))
#
#             x = random.randint(0, len(cuckoo)-1)
#             y = random.randint(0, len(cuckoo)-1)
#             z = random.randint(0, len(cuckoo)-1)
#
#             if (x>y) and (y<z):
#                 x,y = y,x
#             elif (y>x) and (z<y):
#                 y,z = z,y
#             elif (x<y) and (z<x):
#                  x,z = z,y
#
#             candidate = cuckoo[random.randint(0,self.pc)]
#             if(self.levy_flight()>4):
#                 cuckooNest = self.doubleBridgeMove(cuckoo,x,y,z)
#                 cuckooNest = list(cuckooNest)
#                 candidate_tsp,candidate_tour = self.hitungWaktu(cuckooNest)
#                 fcuckoo = self.utility(candidate_tsp)
#                 if fcuckoo > self.currentFitness:
#                     self.currentFitness = fcuckoo
#                     self.cur_solution()
#             else:
#                 cuckooNest= self.twoOptMove(cuckoo,x,y)
#             randomNextIndex= random.randint(0,self.numNest-1)
#             if(cuckoo[randomNextIndex]>cuckooNest[1]):
#                 cuckoo

# twoopt_move(self,candidate,i,j):
#     candidate[j:(j+i)] = reversed(candidate[j:(j+i)])
#
# doublebridge_move(self,candidate,i,j,k,l):
#     arr1 = []
#     arr2 = []
#     arry3 = []
#     arry4 = []

    # pengecekan i harus lebih kecil dari j,k,l
# pengecekan(self,a,b,c,d):

def doubleBridgeMove(self,candidate):
    pjg = len(candidate)
    best_arr = candidate
    acak = np.random.randint(pjg)
    indek = [acak%pjg,(acak+2)%pjg,(acak+4)%pjg,(acak+6)%pjg]
    q = np.array(indek)
    q.sort()

    a = candidate[0:q[0]+1]
    b = candidate[q[2]+1:q[3]+1]
    c = candidate[q[1]+1:q[2]+1]
    d = candidate[q[0]+1:q[1]+1]
    e = candidate[q[3]+1]

    a1 = a.tolist()
    b1 = b.tolist()
    c1 = c.tolist()
    d1 = d.tolist()
    e1 = e.tolist()

    hasil = np.array(a1+b1+c1+d1+e1)

    return print(hasil)
    # l = len(hasil)
    # total = 0
    #
    # for i in range(l-1):
    #     h = np.linalg.norm(hasil[i+1]-hasil[i])
    #     total = total + h
    # a = random.randint()
    # b = random.randint(a,20)
    # c = random.randint(b,20)
    # d = random.randint(c,20)
    # for i in range(0,20):
    #     if a == b:
    #         b = random.randint(a,20)
    #     if b == c:
    #         c = random.randint(b,20)
    #     if c == d:
    #         d = random.randint(c,20)


print( a,b,c,d)
