#!/usr/bin/env python3
# pump.py  Nigel Ward, 2021.  Based on John Osterhout's Producer/Consumer code.


import sys, threading, time, asyncio

global count, putIndex,  getIndex, cbuffer, bufLock, mutex, empty, full


def pumpProducer():
    print('starting Producer')
    arpaciQuote = '"Yeats famously said “Education is not the filling of a pail but the lighting of a fire.” He was right but wrong at the same time. You do have to “fill the pail” a bit, and these notes are certainly here to help with that part of your education; after all, when you go to interview at Google, and they ask you a trick question about how to use semaphores, it might be good to actually know what a semaphore is, right? But Yeats’s larger point is obviously on the mark: the real point of education is to get you interested in something, to learn something more about the subject matter on your own and not just what you have to digest to get a good grade in some class. As one of our fathers (Remzi’s dad, Vedat Arpaci) used to say, “Learn beyond the classroom”.'
    for charToSend in arpaciQuote:
        putChar(charToSend)
    putChar(0)    # the solution!!
      

def putChar(character):
    global count, putIndex, bufLock, mutex, full, empty
    # print("in the producer") # TODO: Delete
    # bufLock.acquire() # TODO: I dont think I need this
    
    
    # TODO: I don't think I need this
    # while count >= bufsize:
    #     #print("waiting to send", end="")
    #     bufLock.release()
    #     bufLock.acquire()
    empty.acquire()
    # print("prodicer - empty acquire") # TODO: Delete
    mutex.acquire()
    count += 1
    cbuffer[putIndex] = character
    putIndex += 1
    mutex.release()
    full.release()
    
    if putIndex == bufsize:
        putIndex = 0
    # bufLock.release() # TODO: I don't I need this


def pumpConsumer():
    print('starting Consumer')
    while (1):
        for i in range(100):
            c = getChar()
            if c == 0:
                return
            print(c,end="")
        print("")  # newline

def getChar():
    global count, getIndex, bufLock, mutex, full, empty
    # bufLock.acquire()# TODO: I don't I need this
    # TODO: I don't think I need this
    # while (count == 0):
        #print("waiting to receive", end="")
        # bufLock.release() # I don't think I need this
        # bufLock.acquire() # I don't think I need this S
    # print("in consumer") # TODO: Delete Later 
    full.acquire()
    # print("consumer - acquire") #TODO: delete later 
    mutex.acquire()
    count -= 1
    c = cbuffer[getIndex]
    getIndex += 1
    mutex.release()
    empty.release()
    
    if (getIndex == bufsize):
        getIndex = 0
    # bufLock.release() # I don't think I need this
    return c       


### main ###
if len(sys.argv) != 2:
    print(len(sys.argv))
    print("usage: pump bufferSize")
    exit(1)





bufsize = int(sys.argv[1])
cbuffer = ['x'] * bufsize    # circular buffer; x means uninitialized
count = putIndex = getIndex = 0
# bufLock = threading.Lock() #  I might not need this

mutex = threading.Semaphore() # The Mutual exclusive semaphore
empty = threading.Semaphore(value = 2) # Indicate that the buffer is empty and is ready to put stuff into it
full = threading.Semaphore(value = 0)  # Indiate that the buffer is full and is ready to be consummed

consumer = threading.Thread(target=pumpConsumer)
consumer.start()

producer = threading.Thread(target=pumpProducer)
producer.start()

producer.join()
