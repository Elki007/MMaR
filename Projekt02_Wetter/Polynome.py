import numpy as np
def polynome(x,pointx,pointy):
    total = 0
    n = len(points)
    for i in range(n):
        xi, yi = pointx[i],pointy[i]

        total += yi * g(i, n,x,pointx,xi)
    return total


def g(i, n,x,pointx,xk):
    tot_mul = 1
    for j in range(n):
        if i != j:
            xj = pointx[j]
            tot_mul *= (x - xj) /(xk - xj)
    return tot_mul

pointx= np.array(np.arange(10))
pointy=np.array(np.arange(5,15))
points=[[1.6,2],[0.8,4],[67.9,45],[76.76,98]]
print(polynome(20,pointx,pointy))

