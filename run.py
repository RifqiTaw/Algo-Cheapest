from cuckoo import CuckooSearch
from koneksi import ConDB
from tourmanager import TourManager
import matplotlib.pyplot as plt
import random
import math
import copy
import time

def main(tourid,idhotel,dwaktu,drating,dtarif):
    start = time.time()
    db = ConDB()
    tspperday = []
    waktuDatang = []
    for i in range(3):
        tspperday.append([])
        waktuDatang.append([])
    hotel = db.HotelbyID(idhotel)
    tur = db.WisatabyID(tourid)
    timematrix = db.TimeMatrixbyID(tourid)
    tmhotelfrom = db.TMHfrombyID(idhotel,tourid)
    tmhotelto = db.TMHtobyID(idhotel,tourid)
    i = 0

    while i < 3 and tur:
        cs = CuckooSearch(tour= tur, pa = 0.2, sarang = 10, maxgenerasi = 1000, timematrix= timematrix, tmhotelfrom= tmhotelfrom, tmhotelto= tmhotelto, hotel= hotel, drating=drating, dtarif=dtarif, dtime=dwaktu)
        tsp,rest = cs.tsp()
        tur = rest
        for node in tsp:
            tspperday[i].append(node._id)
            waktuDatang[i].append(str(node.timedatang))
        waktuDatang[i].insert(0,str(hotel.dttime))
        waktuDatang[i].append(str(cs.endNode.dttime))
        hotel = copy.copy(cs.hotel)
        print("hari ke-: ",i+1 , "rute: ",tspperday[i],"waktu datang: ",waktuDatang[i])
        i += 1
    end = time.time()
    print("running time: ",end - start)
    return tspperday,waktuDatang


if __name__ == '__main__':
    # tsp,waktudatang = main([1,2],32,1,1,1)
    tsp,waktudatang = main([1,2,3,5,6,7,14,15,16,17,18,19,20,21,22,23,25,26,27,28],32,1,1,1)
    print(tsp)
