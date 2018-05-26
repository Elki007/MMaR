import numpy as np
import itertools as it

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
                    print(self.a[i],", ", sep='', end='')
                else:
                    print(self.a[i], sep='', end='')
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


    def cartesian_product(self,other):
        menge=[]
        for element in it.product(self.a,other.a):
            menge.append(element)
        return menge
        #return Set(menge)


    def power(self,pow):
        menge=Set([])
        lens=1
        lene=len(self.a)+1
        menge = menge.union(Set(Set([])))

        a=[] # list of indexes for each selection

        for i in range(lens,lene):
            a.extend(it.combinations(range((len(self.a))), i))
        '''for x in a:
            print("a: ", x)
        print("try!: ", a[1][0])

        print("self.a: ", self.a)
        print("len(a)",len(a))
        print("len(a)(a)",len(a[5]))'''

        for x in range(len(a)):
            m=[]
            for y in range(len(a[x])):
                m.append(self.a[a[x][y]])
            menge = menge.union(Set(Set(m)))

        return menge


class Kartesisches_Produkt(Set):
    def __init__(self,first,second):
        self.first=first
        self.second=second
        #print(self.first.cartesian_product(self.second))
        self.a = self.first.cartesian_product(self.second)

    '''def cartesian_product(self, other):
        menge = []
        import itertools
        for element in itertools.product(self.a, other.a):
            menge.append(element)
        return menge'''

class Relation(Kartesisches_Produkt):
    def __init__(self,Kartesisches_Produkt):
        self.k = Kartesisches_Produkt
        self.a = Kartesisches_Produkt.a


    #def Reflexivitaet(self):


    #def Symmetrie(self):


    #def Transitivitaet(self):


####################################Aufgabe 3.1.1#################################################################
print("Aufgabe 3.1.1: Mengenklasse\n")

A = Set(["hund","katze",7.8])
B = A.subset("a")
AuB =A.union(B)
C = Set (["auto", "vehicle"])
D = Set (["shep", "vehicle"])
AuBuC =AuB.union(C)

print("A:",A)
print("B:",B)
print("C:",C)
print("D:",D)
print("AuB:",AuB)
print("AuBuC:",AuBuC)

print("AuB intersect C:",AuB.intersect(C))
print("AuBuC intersect D:",AuBuC.intersect(D))


#N=Set( [Set([]),Set([Set([])])])
#print(N)

####################################Aufgabe 3.1.2#################################################################
print("\n\nAufgabe 3.1.2: Arbeiten mit der Mengenklasse\n")
def Menge(i,a=Set([])):
    if i==0:
        return a
    return Menge(i-1,a.union(Set(a)))

print ("Definition der Natürlichen Zahlen allein aus Mengen, n=5: ", Menge(5))

Apow=A.power(2)
print("A:",A)
print("Potenzmengen P(A): ", Apow)


####################################Aufgabe 3.1.3#################################################################
print("\n\nAufgabe 3.1.3: Kartesisches Produkt\n")
# AxC=A.cartesian_product(C)
#print("AxC: ",AxC)

AAxCC = Kartesisches_Produkt(A,C)
print(AAxCC)

####################################Aufgabe 3.1.5#################################################################
print("\n\nAufgabe 3.1.5: (Äquivalenz-)Relationen\n")

N = Set(range(101))
print("N:",N)

R = Relation(Kartesisches_Produkt(A,B))
print(R)