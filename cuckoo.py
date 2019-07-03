from koneksi import ConDB
from random import uniform
import numpy as np
import time
import math
import random
import matplotlib.pyplot as plt
import datetime
import copy
class CuckooSearch(object):
    def __init__(self, tour= -1, pa = -1, sarang = -1,maxgenerasi = -1, timematrix=-1, tmhotelfrom=-1, tmhotelto=-1, hotel=-1, drating=-1, dtarif=-1, dtime=-1):
        self.db = ConDB()
        self.tour = self.db.getWisata() if tour == -1 else tour
        self.hotel = hotel
        self.hotels = self.db.HotelbyID(32)

        self.generasi = 0
        self.sarang = 20 if sarang == -1 else sarang
        self.maxGen = 100 if maxgenerasi == -1 else maxgenerasi

        self.dtime = 1 if dtime == -1 else dtime
        self.drating = 1 if drating == -1 else drating
        self.dtarif = 1 if dtarif == -1 else dtarif

        self.timematrix = self.db.getTimeMatrix() if timematrix == -1 else timematrix
        self.tmhotelfrom = self.db.TMHfrom() if tmhotelfrom == -1 else tmhotelfrom
        self.tmhotelto = self.db.TMHto() if tmhotelto == -1 else tmhotelto

        self.cur_solution = self.initialSolution()
        print(pa)
        self.pa = 0.6  if pa == -1 else pa

        self.hotel = self.hotels[0] if hotel == -1 else hotel
        self.hotel.dttime = datetime.time(8,0,0)
        self.endNode = copy.copy(self.hotel)

        self.cur_tsp,self.tour = self.hitungWaktu(self.cur_solution)
        if self.cur_tsp:
            self.currentFitness = self.utility(self.cur_tsp)
            self.cur_fitness = self.utility(self.cur_solution)
            self.best_fitness = self.currentFitness


#    get waktu dari db timematrix
    def tmatrix(self,wisata1,wisata2):
        if wisata1.jenisWisata == 'Hotel':
            for tm in self.tmhotelfrom:
                if(tm.titik_a == wisata1._id and tm.titik_b == wisata2._id):
                    time = tm.waktu
                    break
        elif wisata2.jenisWisata == 'Hotel':
            for tm in self.tmhotelto:
                if(tm.titik_a == wisata2._id and tm.titik_b == wisata1._id):
                    time = tm.waktu
                    break
        else:
            for tm in self.timematrix:
                if(tm.titik_a == wisata1._id and tm.titik_b == wisata2._id):
                    time = tm.waktu
                    break

        return time

    def getNodeMatrix(self,wisata,waktu,tour):
        for tm in self.timematrix:
            if(wisata._id == tm.titik_a and waktu == tm.waktu):
                node = self.getNodebyId(tm.titik_b)
                if node in tour:
                    wisata = node
                    break
        return wisata

    def getNodebyId(self,idnode):
        wisata = None
        for node in self.tour:
            if(node._id == idnode and node.jenisWisata != 'Hotel'):
                wisata = node
                break
        return wisata

#   random tour untuk solusi awal
    def initialSolution(self):
        solution = list(self.tour)
        random.shuffle(solution)
        start = solution[0]
        return solution
#   fungsi normalisasi
    def normalisasi(self,x,ub,lb):
       normalisasi = (x-lb)/(ub-lb)
       return normalisasi

#   Menghitung waktu berdasarkan durasi
    def fitness(self, sol):
        # ubf = 596
        # lbf = 22084
        # ubt = 597
        # lbt = 22752
        # ub = 77
        # lb = 29534
        ubf = 596
        lbf = 5814
        ubt = 597
        lbt = 6093
        ub = 77
        lb = 9432
        x = sum( [ self.normalisasi(self.tmatrix(sol[i-1],sol[i]),ub,lb) for i in range(1,len(sol)) ] )
        y = len(sol)-1
        try:
            z = x / y
        except ZeroDivisionError:
            z = 0
        return ((self.normalisasi(self.tmatrix(self.hotel,sol[0]),ubf,lbf)+z+self.normalisasi(self.tmatrix(sol[len(sol)-1],self.hotel),ubt,lbt)))/3

#   Fitness berdasarkan rating
    def fitnessRating(self, sol):
        ub = 5.0
        lb = 0
        return self.normalisasi(sum([sol[i-1].rating for i in range(1,len(sol))])/len(sol),ub,lb)

#   Fitness berdasarkan tarif
    def fitnessTarif(self, sol):
        lb = 50000
        ub = 0
        return self.normalisasi(sum([sol[i-1].tarif for i in range(1,len(sol))])/len(sol),ub,lb)

#   Fitness dengan DOI
    def utility(self,sol):
        # x = self.dtime*self.fitness(sol)
        # y = self.drating*self.fitnessRating(sol)
        # z = self.dtarif*self.fitnessTarif(sol)
        # tot = (x+y+z)/3
        return ((self.dtime*self.fitness(sol)) + (self.drating*self.fitnessRating(sol)) + (self.dtarif*self.fitnessTarif(sol)))/3

#   cek konstrain jam buka dan tutup
    def checkjam(self,node):
        accept = False
        if node.buka == node.tutup:
            accept = True
        elif node.timedatang > node.buka and node.dttime < node.tutup:
            accept = True
        return accept

#   Menghitung rentang waktu tiap destinasi wisata
    def jammenit(self,node1,node2):
        datang = self.tmatrix(node1,node2)
        jamd = (node1.dttime.hour) + int(datang // 3600)
        menitd = (node1.dttime.minute) + int((datang // 60) % 60 )
        detikd = (node1.dttime.second) + int(datang % 60)
        if detikd > 59:
            menitd += int(detikd / 60)
            detikd = int(detikd % 60)
        if menitd > 59:
            jamd += int(menitd / 60)
            menitd = int(menitd % 60)
        waktu = datang + node2.time
        jam = (node1.dttime.hour) + int(waktu // 3600)
        menit = (node1.dttime.minute) + int((waktu // 60) % 60 )
        detik = (node1.dttime.second) + int(waktu % 60)
        if detik > 59:
            menit += int(detik / 60)
            detik = int(detik % 60)
        if menit > 59:
            jam += int(menit / 60)
            menit = int(menit % 60)
        jdatang = [jamd,menitd,detikd]
        jselesai = [jam,menit,detik]
        return jdatang,jselesai

#   Menghitung waktu perjalanan dalam 1 hari
    def hitungWaktu(self,tour):
        sol = list(tour)
        tsp = []
        cur_node = self.hotel
        for i in range(0,len(sol)):
            jamd,jams = self.jammenit(cur_node,sol[i])
            if jams[0] < 20 :
                node = copy.copy(sol[i])
                node.timedatang = datetime.time(jamd[0],jamd[1],jamd[2])
                node.dttime = datetime.time(jams[0],jams[1],jams[2])
                accept = self.checkjam(node)
                if accept == True:
                    cur_node = node
                    tsp.append(cur_node)
            else :
                break


        return tsp,sol


# membangkitkan cukoo
    def sarang(self,candidate,a,b):
        for i in range(self.numNest-self.pa,self.numNest):
            nilaifitness[i] = self.fitness(candidate[i])
            candidate = twoOptMove(candidate,a,b)
        return candidate


### twoOptMove

    def swap(self,x,i,j):
        temp = x[i]
        x[i] = x[j]
        x[j] = temp

    def twoOptMove(self,nest,a,c):
    	lul = nest
    	self.swap(lul,a,c)
    	return (lul)

    def doubleBridgeMove(self,nest,a,b,c,d):
    	node = nest
    	self.swap(node,a,b)
    	self.swap(node,c,d)
    	return (node)

    def cek_fitness(self,candidate):
        candidate_tsp,candidate_tour = self.hitungWaktu(candidate)
        fitness_baru = self.utility(candidate_tsp)
        if fitness_baru < self.currentFitness:
            self.currentFitness = fitness_baru
            self.cur_solution = candidate
            self.cur_tsp = list(candidate_tsp)
            self.tour = candidate_tour

    def levy_flight(self):
        Lambda = 1.5
        sigma1 = np.power((math.gamma(1 + Lambda) * np.sin((np.pi * Lambda) / 2)) \
                          / math.gamma((1 + Lambda) / 2) * np.power(2, (Lambda - 1) / 2), 1 / Lambda)
        sigma2 = 1

        u = np.random.randn()*sigma1
        v = np.random.randn()*sigma2
        step = u / np.power(np.fabs(v), 1 / Lambda)

        return step



    def mainCuckoo(self):
        nest = []
        fitness = []
        for i in range(self.sarang):

            self.cur_solution = self.initialSolution()
            # print("initialSolution : ",self.cur_solution)
            # print("solution: ",self.cur_solution)
            # nest.append(self.cur_solution)
            # print("nest : ",nest)
            self.cur_tsp,self.tour = self.hitungWaktu(self.cur_solution)
            if self.cur_tsp:
                self.currentFitness = self.utility(self.cur_tsp)
                self.cur_fitness = self.utility(self.cur_solution)

        #     # nest = list(self.cur_solution)
            # n = len(nest)
            # dimension = len(self.cur_solution[0])
            # k = np.array([np.random.random([len(self.cur_solution)])<self.pa],dtype=int)
            # stepsize = np.multiply(np.subtract(self))



        if self.cur_tsp:
        #### algoritma  cuckoo ####
            while self.generasi <= self.maxGen:
                # x = 0
                # while (x <= self.sarang):
                candidate = list(self.cur_solution)
                candidate_tsp,candidate_tour = self.hitungWaktu(candidate)
                candidate_fitness = self.utility(candidate_tsp)
                # if (self.currentFitness < self.pa):
                #     self.cur_solution = self.initialSolution()
                # else:
                cuckoofit = self.levy_flight() * candidate_fitness + candidate_fitness
                a = random.randint(0,len(candidate)-1)
                b = random.randint(0,len(candidate)-1)
                c = random.randint(0,len(candidate)-1)
                d = random.randint(0,len(candidate)-1)
                for i in range(len(candidate)-1):
                    if a > b:
                        a,b = b,a
                    if b > c:
                        b,c = c,b
                    if c > d:
                        c,d = d,c


                #m#masuk ke dalam pengecekan cucko

                if  (len(candidate)<11) and (cuckoofit > candidate_fitness):
                        # candidate = self.twoOptMove(candidate,a,b)
                    # candidate[b:(b+a)] = reversed(candidate[b:(b+a)])
                    cuckoofit = self.twoOptMove(candidate,a,b)
                        # print("candidate two opt move: ",candidate)
                    self.cek_fitness(cuckoofit)
                    if (self.currentFitness < self.pa):
                        self.cur_solution =  self.initialSolution()

                elif (len(candidate)>= 11) and (cuckoofit > candidate_fitness):
                    # candidate[b:(b+a)] = reversed(candidate[b:(b+a)])
                    # print("candidate a:",candidate[b:(b+a)])
                    # candidate[d:(d+c)] = reversed(candidate[d:(d+c)])
                    # print("candidate d:",candidate[d:(d+c)])
                    cuckoofit = self.doubleBridgeMove(candidate,a,b,c,d)
                    self.cek_fitness(cuckoofit)
                    if (self.currentFitness < self.pa):
                        self.cur_solution =  self.initialSolution()

                # x += 1
                self.generasi += 1
                # print(self.currentFitness)
                # print(self.tour)
                # print(self.cur_tsp)
            return self.tour,self.cur_tsp

#   Fungsi TSP untuk mereturn hasil tsp dalam 1 hari dan sisa tour untuk TSP hari selanjutnya
    def tsp(self):
        tsp = []
        rest = []
        if self.cur_tsp:
            tour,tsp = self.mainCuckoo()
            nama_tsp = [x.name for x in tsp ]
            rest = [x for x in tour if x.name not in nama_tsp]
            waktu = self.tmatrix(tsp[len(tsp)-1],self.endNode)
            jam = (tsp[len(tsp)-1].dttime.hour) + int(waktu // 3600)
            menit = (tsp[len(tsp)-1].dttime.minute) + int((waktu // 60) % 60 )
            detik = (tsp[len(tsp)-1].dttime.second) + int(waktu % 60)
            if detik > 59:
                menit += int(detik / 60)
                detik = int(detik % 60)
            if menit > 59:
                jam += int(menit / 60)
                menit = int(menit % 60)
            if jam > 23:
                jam -= 24
            self.endNode.dttime = datetime.time(jam,menit,detik)
        return tsp,rest
