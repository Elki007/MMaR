"""
Maybe create two tuples (u, d) and (d, u) which are a reference to each other to be able to allow binary search?
"""


class PQueue:
    def __init__(self, ini_list=[]):
        self.items = []
        for i in ini_list:
            self.push_tuple(i)

    def print(self):
        print(self.items)

    def push_tuple(self, t):
        self.push(t[0], t[1])

    def push(self, u, value):
        print("add " + u + ",", value)

        index = self.get_insert_index_sorted(value, 0, len(self.items)-1)
        self.items.insert(index, (u, value))

    # decrease the value of u by value
    def decrease_key(self, u, value):
        print("change " + u + ",", value)
        tmp_list = []

        for i in range(len(self.items)-1, 0, -1):
            if self.items[i][0] == u:
                # convert tuple to list due to immutability of the tuple type
                tmp_list = list(self.items[i])
                tmp_list[1] -= value
                # reassign tuple item to changed list instance
                self.items.pop(i)
                break  # There's only one element with that name
        self.push(tmp_list[0], tmp_list[1])

    def pop_min(self):
        return self.items.pop(0) if len(self.items) > 0 else None

    # binary search for index, returns index
    def get_insert_index_sorted(self, value, start, end):
        if start == end:
            return start if self.items[start][1] > value else start+1

        if start > end:
            return start

        mid = (start + end) // 2
        if self.items[mid][1] < value:
            return self.get_insert_index_sorted(value, mid+1, end)
        elif self.items[mid][1] > value:
            return self.get_insert_index_sorted(value, start, mid-1)
        else:
            return mid


# Testing base functions
print("Aufgabe 3")
pq = PQueue([("u", 5), ("v", 42), ("w", 23)])
pq.print()
pq.push("q", 11)
pq.print()
pq.decrease_key("v", 41)
pq.print()
print("Removed: ", pq.pop_min())
pq.print()
pq.push("q", 0)
pq.print()
pq.push("n", 22)
pq.print()
pq.push("m", 43)
pq.print()
pq.decrease_key("w", 20)
pq.print()
