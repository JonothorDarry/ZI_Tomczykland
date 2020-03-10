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
    ll=len(L)
    M = np.zeros([ll, ll], dtype=float)
    # number of outgoing links
    c = np.zeros([ll], dtype=int)
    
    ## TODO 1 compute the stochastic matrix M
    for i in range(0, ll):
        c[i] = sum(L[i])
    
    for i in range(0, ll):
        for j in range(0, ll):
            if L[j][i] == 0: 
                M[i][j] = 0
            else:
                M[i][j] = 1.0/c[j]
    return M

def trustis(q, d):
    ll=len(L)
    c = np.asarray([sum(L[i])+(0.01 if sum(L[i])==0 else 0) for i in range(ll)])

    mtx=np.asarray([[((1-q)*L[y,x])/c[y] for y in range(ll)] for x in range(ll)])
    for x in range(len(mtx)):
        mtx[x,x]-=1
    res=np.asarray([-q*x for x in d])
    return np.linalg.solve(mtx, res)

def sortis(lees):
    xv=list(zip(list(lees), range(len(lees))))
    return sorted(xv, key=lambda x:x[0])

def whole(typ, *args):
    fun=trustis(*args)
    c=sortis(fun)
    _=[print(f"index {x[1]} has value {round(x[0], 5)}, : {typ}") for x in c]
    print()



#L=np.asarray([[0,1,1,0],[0,0,0,1],[0,1,0,1],[0,0,0,1]])
    
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
whole("pagerank", q, [1]*len(L))

### TODO 3: compute trustrank with damping factor q = 0.15
### Documents that are good = 1, 2 (indexes = 0, 1)
### Then, sort and print: (page index (first index = 1, add +1) : trustrank)
### (use regular array + sort method + lambda function)
print("TRUSTRANK (DOCUMENTS 1 AND 2 ARE GOOD)")
q = 0.15
lees=[0,1]
tr = [int(i in lees)/len(lees) for i in range(len(L))]
whole("trustrank", q, tr)

### TODO 4: Repeat TODO 3 but remove the connections 3->7 and 1->5 (indexes: 2->6, 0->4) 
### before computing trustrank
print("TRUSTRANK2 (DOCUMENTS 1 AND 2 ARE GOOD), removed links 2->6 and 0->4")
L[2,6], L[0,4]=0, 0
lees=[0,1]
tr = [int(i in lees)/len(lees) for i in range(len(L))]
whole("trustrank", q, tr)
