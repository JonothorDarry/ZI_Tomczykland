import numpy as np

#L1  = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
L1  = [0, 1, 1, 0, 1, 0, 0, 0, 0, 0]
L2  = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
#L3  = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
L3  = [0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
L4  = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
L5  = [0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
L6  = [0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
L7  = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
L8  = [0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
L9  = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
L10 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

L = np.array([L1, L2, L3, L4, L5, L6, L7, L8, L9, L10])

ITERATIONS = 100

def getM(L):
    M = np.zeros([10, 10], dtype=float)
    # number of outgoing links
    c = np.zeros([10], dtype=int)
    
    ## TODO 1 compute the stochastic matrix M
    for i in range(0, 10):
        c[i] = sum(L[i])
    
    for i in range(0, 10):
        for j in range(0, 10):
            if L[j][i] == 0: 
                M[i][j] = 0
            else:
                M[i][j] = 1.0/c[j]
    return M

def sortis(lees):
    xv=list(zip(list(lees), range(len(lees))))
    return sorted(xv, key=lambda x:x[0])

def trustis(q, d):
    c = np.asarray([sum(L[i])+(0.01 if sum(L[i])==0 else 0) for i in range(len(L))])

    mtx=np.asarray([[((1-q)*L[y,x])/c[y] for y in range(len(L))] for x in range(len(L))])
    for x in range(len(mtx)):
        mtx[x,x]-=1
    res=np.asarray([-q*x for x in d])
    return np.linalg.solve(mtx, res)


    
print("Matrix L (indices)")
print(L)    

M = getM(L)

print("Matrix M (stochastic matrix)")
print(M)

### TODO 2: compute pagerank with damping factor q = 0.15
### Then, sort and print: (page index (first index = 1 add +1) : pagerank)
### (use regular array + sort method + lambda function)

print("PAGERANK")
q = 0.15
pr = np.zeros([10], dtype=float)
fun=trustis(q, [1]*len(L))
c=sortis(fun)
print(c)
print()

### TODO 3: compute trustrank with damping factor q = 0.15
### Documents that are good = 1, 2 (indexes = 0, 1)
### Then, sort and print: (page index (first index = 1, add +1) : trustrank)
### (use regular array + sort method + lambda function)
print("TRUSTRANK (DOCUMENTS 1 AND 2 ARE GOOD)")
q = 0.15
lees=[0,1]
tr = [int(i in lees)/len(lees) for i in range(len(L))]
fun=trustis(q, tr)
c=sortis(fun)
print(c)
print()

### TODO 4: Repeat TODO 3 but remove the connections 3->7 and 1->5 (indexes: 2->6, 0->4) 
### before computing trustrank
print("TRUSTRANK2 (DOCUMENTS 1 AND 2 ARE GOOD)")
L[2,6], L[0,4]=0, 0
q = 0.15
lees=[0,1]
tr = [int(i in lees)/len(lees) for i in range(len(L))]
fun=trustis(q, tr)
c=sortis(fun)
print(c)
