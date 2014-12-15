import time
alist =[]
t1 = time.clock()
for i in range(21):
    for j in range(20):
        alist.append(i*j)
t2 = time.clock()

print "process took", t2-t1, "seconds"
