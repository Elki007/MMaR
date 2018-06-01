import numpy as np
import itertools as it


class Set:

    def __init__(self, a):
        new_list_Set = []
        for i in a:
            if i not in new_list_Set:
                new_list_Set.append(i)
        self.a = new_list_Set

        # self.a = a

    def __lt__(self, other):
        return len(self.a) < len(other.a)

    def __str__(self):
        if len(self.a) != 0:
            print("{", end='')
            for i in range(len(self.a)):
                print(self.a[i], ", ", sep='', end='') if i != len(self.a)-1 else print(self.a[i], sep='', end='')
            return "}"
        return u"\u2205" #unicode für leere Menge

    """
    def union(self, other):
        return Set(np.union1d(self.a, other.a))
    """

    # union als überladenes '+' ohne numpy
    def __add__(self, other):
        return Set(self.a + other.a)

    """
    def intersect(self, other):
        return Set(np.intersect1d(self.a, other.a))
    """

    # intersect als überladenes '&' ohne numpy
    def __and__(self, other):
        return Set([x for x in self.a if x in other.a])

    """
    def complement(self, other):
        return Set(np.setdiff1d(self.a,other.a))
    """

    # complement als überladenes '\' ohne numpy
    def __sub__(self, other):
        return Set([x for x in self.a if x not in other.a])

    def subset(self, auswahl):
        return Set(list(filter(auswahl, self.a)))

    # Nicht notwendig, da durch __getitem__ gelöst?
#    def __iter__(self):
#        pass

    def __contains__(self, item):
        return True if item in self.a else False

    def __len__(self):
        return len(self.a)

    def __getitem__(self, item):
        return self.a[item]

### Aufgabe 3.1.2 ###

    def powerset(self):
        menge = Set([])
        for i in range(len(self)+1):
            for j in it.combinations(self, i):
                menge += Set([Set(j)])

        return Set(menge)

### Aufgabe 3.1.3 ###

    def product(self, other):
        return [x for x in it.product(self.a, other.a)]


class Kartesisches_Produkt(Set):
    def __init__(self, first, second):
        self.first = first.a
        self.second = second.a
        self.a = first.product(second)


### Aufgabe 3.1.5 ###


class Relation(Kartesisches_Produkt):
    def __init__(self,Kartesisches_Produkt):
        #super().__init__(Kartesisches_Produkt)
        self.k = Kartesisches_Produkt
        self.a = Kartesisches_Produkt.a
        self.proof_one = []
        self.proof_two = []
        for x in self.a:
            if x[0] not in self.proof_one:
                self.proof_one.append(x[0])
            if x[1] not in self.proof_two:
                self.proof_two.append(x[1])

    def Reflexivitaet(self):
        y = []
        for x in self.a:
            if x[0] not in self.proof_one:
                self.proof_one.append(x[0])
            if x[1] not in self.proof_two:
                self.proof_two.append(x[1])
            if x[0] == x[1]:
                y.append(x[0])

        if len(y) != 0 and (y == self.proof_two) and(y == self.proof_one):
            return True
        return False

    def Symmetrie(self):
        y = []
        for i in range(len(self.a)):
            for j in range(len(self.a)):
                #if i!=j:
                if (self.a[i][0],self.a[i][1])==(self.a[j][1],self.a[j][0]):
                    y.append(self.a[i])
        #print("y", y)
        if len(y)==(len(self.proof_one)*len(self.proof_two)):

            #print(self.proof_one)
            #print(len(self.proof_two))
            return True
        return False


    def Transitivitaet(self):
        #(a,b)(b,c)(a,c)
        y = []
        b=""
        for i in range(len(self.a)):
            for j in range(len(self.a)):
                if i==j:
                    continue                        #i(a,b)
                if self.a[i][1]==self.a[j][0]:      #j(b,c)
                    a = self.a[i][0]
                    b = self.a[j][0]
                    c = self.a[j][1]
                    for k in range(len(self.a)):   #k(a,c)?
                        if k==i:
                            continue
                        if self.a[k][0]==a:
                            if self.a[k][1]==c:
                                y.append((self.a[i],self.a[j],self.a[k]))

                                #return True
        #print("len y:", len(y))
        #print(y)
        if len(y)==(len(self.proof_one)*len(self.proof_two)*3):
            return True
        return False

    def Aquivalenz(self):
        if (self.Transitivitaet()==True)and(self.Symmetrie()==True)and(self.Reflexivitaet()==True):
            return True
        return False



####################################  Aufgabe 3.1.1  ####################################

#"""
A = Set(["hund","katze","maus"])

# subset
print(A.subset(lambda x: len(x) == 4))

# __iter__
for i in A:
    print(i)

# __contains__
if "hund" in A:
    print("wau")

# __len__
print(len(A))

# _getitem_
print(A[2])
#"""

####################################  Aufgabe 3.1.2  ####################################


# Definition der Natürlichen Zahlen allein aus Mengen
def Menge(i, a = Set([])):
    return a if i == 0 else Menge(i-1, a + Set([a]))


# Binomialkoeffizienten berechnen mithilfe von "powerset()"
def binomialCoefficients(num):
    # Einzeiler, allerdings nicht gut verständlich und langsamer, daher darunter in mehreren Zeilen
    #return [[len(x) for x in Set([x for x in range(num)]).powerset()].count(x) for x in range(num + 1)]

    binomial_menge = Set([x for x in range(num)])

    binomial_combinations = binomial_menge.powerset()

    combination_anzahl = [len(x) for x in binomial_combinations]
    print(combination_anzahl)
    coefficients = [combination_anzahl.count(x) for x in range(num+1)]

    return coefficients


print("\n\nAufgabe 3.1.2: Arbeiten mit der Mengenklasse\n")
print("Definition der Natürlichen Zahlen allein aus Mengen, n=4: ", Menge(4))

A = Set(["hund","katze","maus"])

print(A.powerset())

print(binomialCoefficients(5))



####################################  Aufgabe 3.1.3  ####################################


print("\n\nAufgabe 3.1.3: Kartesisches Produkt\n")

A = Set([1, 2, 3, 4])
B = Set(["a", "b", "c", "d"])

print("A*B:", Kartesisches_Produkt(A, B))


####################################  Aufgabe 3.1.5  ####################################

print("\n\nAufgabe 3.1.5: (Äquivalenz-)Relationen\n")

A = Set([1, 2, 3, 4])
AA = Set([1, 2, 3])
B = Set(["a", "b", "c", "d"])

N = Set(range(101))
print("N:",N)
KP=Kartesisches_Produkt(A,AA)
print("try:",KP.second)
R = Relation(KP)
#print("try 2nd:",R.first)

print(A)
print(B)
print(R)
print("reflexiv") if R.Reflexivitaet()==True else print("nicht reflexiv")
print("symmetrisch") if R.Symmetrie()==True else print("nicht symmetrisch")
print("transitiv") if R.Transitivitaet()==True else print("nicht transitiv")

print("äquivalent") if R.Aquivalenz()==True else print("nicht äquivalent")