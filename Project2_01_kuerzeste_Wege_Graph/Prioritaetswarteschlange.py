class PQueue:
    def __init__(self, iniList=[]):
        self.items=[]
        for i in iniList:
            self.push_tuple(i)

    def print(self):
        print(self.items)

    def push_tuple(self, t):
        self.push(t[0],t[1])

    def push(self,u,value):
        print("add "+ u +",",value)
        self.items.append((u,value))
        if len(self.items)>1:
            # we added new element to the end of the array
            # so we need to move it to keep asc order
            new = len(self.items)-1
            while self.items[new-1][1] > value and new > 0:
                self.items[new] = self.items[new-1]
                new -= 1
            self.items[new] = (u, value)


    def decrease_key(self,u,value):
        print("change "+u+",",value)
        for i in range(len(self.items)-1,0,-1):
            if self.items[i][0] == u:
                # convert tuple to list due to immutability of the tuple type
                l = list(self.items[i])
                l[1] += value
                # reassign tuple item to changed list instance
                self.items.pop(i)
        self.push(l[0],l[1])

    def pop_min(self):
        self.items.pop(0)

# Testing base functions
print("Aufgabe 3")
pq=PQueue([("u",5),("v",42),("w",23)])
pq.print()
pq.push("q",11)
pq.print()
pq.decrease_key("v",-41)
pq.print()
pq.pop_min()
pq.print()
pq.push("q",0)
pq.print()
pq.push("n",22)
pq.print()
pq.push("m",43)
pq.print()
pq.decrease_key("w",20)
pq.print()