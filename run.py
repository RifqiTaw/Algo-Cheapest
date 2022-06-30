from koneksi import ConDB
from tourmanager import TourManager
import matplotlib.pyplot as plt
import random
import math
import copy
import time
import cheapest

def main(tourid,idhotel,dwaktu,drating,dtarif):

    db = ConDB()
    rute_perhari = []
    waktuDatang = []

    start = time.time()

    hotel = db.HotelbyID(idhotel)
    tur = db.WisatabyID(tourid)
    timematrix = db.TimeMatrixbyID(tourid)
    tmhotelfrom = db.TMHfrombyID(idhotel,tourid)
    tmhotelto = db.TMHtobyID(idhotel,tourid)
    
    rute_perhari,waktuDatang = cheapest.cheapest(listWisata = tourid,idhotel = int(idhotel),timematrix_dest = timematrix, timematrix_from_h = tmhotelfrom,timematrix_to_h = tmhotelto, dwaktu = dwaktu, dtarif = dtarif, drating = drating)

    nodeLen = len(rute_perhari[0] + rute_perhari[1] + rute_perhari[2])
    end = time.time()

    print("Time    : ", end - start)

    return rute_perhari,waktuDatang


if __name__ == '__main__':

    tsp,waktudatang = main([1,2,3,5,6,7,14,15,16,17,18,19,20,21,22,23,25,26,27,28],32,1,0,0)

    print(tsp)
    print(waktudatang)
