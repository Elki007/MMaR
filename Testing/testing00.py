import math
import numpy as np

array = [[0.43852835,  0.07928864,  0.33829191],
         [0.60776121,  0.02688291,  0.67274362],
         [0.2188034,  0.58202254,  0.44704166]]
print(array)

maxed = max([max(inner_array) for inner_array in array])
#maxed = max(array)
print(maxed)
