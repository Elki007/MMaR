def ggT(a,b):
    if a<b:
        return ggT(b,a)
    if b == 0:
        return a
    return (ggT(b,a%b))


print(ggT(10,4))

