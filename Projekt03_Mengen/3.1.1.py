import numpy as np

class Set():

    def __init__(self,a):
        self.a=a


    def __lt__(self, other):
        return (len(self.a)<len(other.a))


    def __str__(self):
        if len(self.a) != 0:
            print("{", end='')
            for i in range(0,len(self.a)):
                if i != len(self.a)-1:
                    print(self.a[i],", ", end='')
                else:
                    print(self.a[i], end='')
            return ("}")
        return  u"\u2205" #unicode für lehre Menge

    def subset(self, auswahl):
        menge=[]
        for x in self.a:
            try:
                if auswahl in x:
                    menge.append(x)
            except TypeError:
                continue
        return Set(menge)


    def union(self,other):
        return Set(np.union1d(self.a, other.a))


    def intersect(self,other):
        return Set(np.intersect1d(self.a, other.a))


    def complement(self,other):
        return Set(np.setdiff1d(self.a,other.a))

    #ohne unterclasse!!!!!!!!!!!!!!!Wofür???
    def cartesian_product(self,other):
        menge=[]
        import itertools
        for element in itertools.product(self.a,other.a):
            menge.append(element)
        return Set(menge)






A = Set(["hund","katze",7.8])
B = A.subset("a")
AuB =A.union(B)
C = Set (["auto", "vehicle"])

AuBuC =AuB.union(C)
print(A)
print(B)
print(AuB)
print(AuBuC)

print(AuB.intersect(C))

N=Set( [Set([]),Set([Set([])])])
print(N)

####################################Aufgabe 3.1.2#################################################################

def Menge(i,a=Set([])):
    if i==0:
        return a
    return Menge(i-1,a.union(Set(a)))

print (Menge(5))

####################################Aufgabe 3.1.3#################################################################

AxC=A.cartesian_product(C)
print(AxC)