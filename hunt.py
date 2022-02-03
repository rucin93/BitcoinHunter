#!/usr/bin/env python3
import addresses
import env
import os
import math
import time
import binascii
import multiprocessing
from bitcoinlib.services.services import Service
from bitcoinlib.keys import HDKey

def hunter(seconds, workerId, dict):
    btcWallets = set(addresses.addresses)
    i = 0
    start = time.time()
    while ((time.time() - start)) < seconds:
        privateKey = binascii.hexlify(os.urandom(32)).decode('utf-8')
        key = HDKey(privateKey)
        address = key.address()
    
        if address in btcWallets:
            try: balance = str((Service().getbalance(address))/1e8)
            except Exception as e: balance = "NULL"

            text  = "--------------------------------------\n"
            text += "PRIVATE KEY = " + privateKey + "\n"
            text += "ADDRESS = " + address + "\n"
            text += "BALANCE = " + balance + " BTC" + "\n"
            text += "--------------------------------------\n"

            print(text)
            
            fl = open(env.OUT_FILE, "anything")
            fl.write(text)
            fl.close()

        i = i + 1
    dict[workerId] = i

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    dict = manager.dict()
    processes = []

    if env.NUM_INSTANCES == 0:
        instances = multiprocessing.cpu_count()
    else:
        instances = env.NUM_INSTANCES

    for i in range(instances):
        p= multiprocessing.Process(target=hunter, args=(env.MAX_SECONDS, i, dict))
        processes.append(p)
        p.start()

    total = 0
    for i in range(instances):
        processes[i].join()
        proc_ret = dict[i]
        total += proc_ret

    print("Tried " + str(total) +
    " keys - " + str(math.floor(total/env.MAX_SECONDS)) + 
    " key/s.")
