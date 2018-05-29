import numpy as np
import itertools as it

class Set():

    def __init__(self,a):
        # Hier müssen wir noch die Liste von doppelten Elementen befreien, geht ähnlich wie bei der Methode von subset

        """
        new_list_Set = []
        for i in a:
            if i not in new_list_Set:
                new_list_Set.append(i)

        self.a = new_list_Set
        """

        self.a = a

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


    #def power(self,pow):
    def power(self):
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

    def binomialCoefficients(num):
        binomial_menge = Set([x for x in range(num)])
        coeffi = binomial_menge.power()

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

    def Reflexivitaet(self):
        y = []
        for x in self.a:
            if x[0]==x[1]:
                y.append(x)
        '''for i in range(len(self.a)):
            for j in range(len(self.a)):
                if i!=j:
                    if self.a[i]==self.a[j]:
                        y.append(self.a[i])'''
        if len(y)!=0:
            return True
        return False

    def Symmetrie(self):
        y = []
        for i in range(len(self.a)):
            for j in range(len(self.a)):
                if i!=j:
                    if (self.a[i][0],self.a[i][1])==(self.a[j][1],self.a[j][0]):
                        y.append(self.a[i])
        if len(y)!=0:
            return True
        return False


    def Transitivitaet(self):
        #(a,b)(b,c)(a,c)
        y = []
        for i in range(len(self.a)):
            for j in range(len(self.a)):
                if i!=j:
                    a=self.a[i][0]
                    if self.a[i][1]==self.a[j][0]:
                        b=self.a[j][0]
                    for k in range(len(self.a)):
                        if k!=i:
                            if self.a[k][0]==b:
                                if self.a[k][1]==a:
                                    return True
        return False

    def Aquivalenz(self):
        if (self.Transitivitaet()==True)and(self.Symmetrie()==True)and(self.Reflexivitaet()==True):
            return True
        return False



####################################Aufgabe 3.1.1#################################################################
print("Aufgabe 3.1.1: Mengenklasse\n")

A = Set(["hund","katze",7.8, "hund"])
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
#print(Symmetrie(A))


#N=Set( [Set([]),Set([Set([])])])
#print(N)

####################################Aufgabe 3.1.2#################################################################
print("\n\nAufgabe 3.1.2: Arbeiten mit der Mengenklasse\n")
def Menge(i,a=Set([])):
    if i==0:
        return a
    return Menge(i-1,a.union(Set(a)))

print("Definition der Natürlichen Zahlen allein aus Mengen, n=5: ", Menge(5))

Apow=A.power()
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

R = Relation(Kartesisches_Produkt(A,A))
print(A)
print(B)
print("Hier:", R)
print("reflexiv") if R.Reflexivitaet()==True else print("nicht reflexiv")
print("symmetrisch") if R.Symmetrie()==True else print("nicht symmetrisch")
print("transitiv") if R.Transitivitaet()==True else print("nicht transitiv")

print("äquivalent") if R.Aquivalenz()==True else print("nicht äquivalent")
