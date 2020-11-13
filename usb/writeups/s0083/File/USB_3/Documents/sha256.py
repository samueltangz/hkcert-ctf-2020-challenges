import hashlib
import sys
import os
import time



data = "Pak Sha Tsuen".encode('utf-8')
a = 1337
s = hashlib.sha256()
s.update(data)
h = s.digest()
print("First hash: " + str(s.digest()))

for a in range(a):
    # time.sleep(0.01)
    sys.stdout.write("\r\n")
    s = hashlib.sha256()
    
    s.update(h)
    h = s.digest()
    sys.stdout.write("running... " + str(a) + " | PWN--> "+ h.hex())
    sys.stdout.flush()
    if a == 1335:
        sys.stdout.write("\n Done: " + str(a) + " |Solve: "+ str(h))
        break