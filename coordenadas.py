from pyproj import Proj
p=Proj('+proj=utm +zone=24 +south +ellps=WGS84',preserve_units=False)
print(p)
print(p(34236427.27,7782226.35,inverse=True))
print(p(-120.108, 34.36116666))
