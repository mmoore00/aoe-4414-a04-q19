# llh_to_ecef.py
#
# Usage: python3 llh_to_ecef.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km
# Converts radii in ECEF to radii in ECI
#
# Parameters:
#  Y: Gregorian calendar year
#  M: Gregorian calendar month
#  D: Gregorian calendar day
#  h: Gregorian calendar hour
#  m: Gregorian calendar minute
#  s: Gregorian calendar second
#  ecef_x_km: x directional ECEF value in kilometers
#  ecef_y_km: y directional ECEF value in kilometers
#  ecef_z_km: z directional ECEF value in kilometers
#  
# Output:
#  Print the radii in the x, y, and z ECI directions
#
# Written by Matthew Moore
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
import math # math module
import sys # argv

# "constants"
w = 7.292115 * 10.0**-5.0 # constant in rad/s

# helper functions
def int_div(l):
    if (l > 0):
        return math.floor(l)
    if (l == math.floor(l)):
        return l
    return math.ceil(l)

# initialize script arguments
rECI = [0, 0, 0]
rECEF = [0, 0, 0]
GMST_angle = float('nan')

# parse script arguments
if len(sys.argv) == 10:
    Y = float(sys.argv[1])
    M = float(sys.argv[2])
    D = float(sys.argv[3])
    h = float(sys.argv[4])
    m = float(sys.argv[5])
    s = float(sys.argv[6])
    ecef_x_km = float(sys.argv[7])
    ecef_y_km = float(sys.argv[8])
    ecef_z_km = float(sys.argv[9])
else:
    print('Usage: python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km')
    exit()

# write script below this line

# calculate JDfractional given Gregorian calendar input
JD = D - 32075 + int_div(int_div(1461 * (Y + 4800 + int_div((M - 14)/12)))/4) + int_div(int_div(367 * (M - 2 - int_div((M - 14)/12) * 12))/12) - int_div(int_div(3 * int_div((Y + 4900 + int_div((M - 14)/12))/100))/4)
JDmidnight = JD - 0.5
Dfractional = (s + 60.0*(m+60.0*h))/86400.0
JDf = JDmidnight + Dfractional

# calculate GMST angle
# this part is the only part that might be iffy, it's kind of working but also not???
TUT1 = (JDf - 2451545.0) / 36525.0
GMST_s = 67310.54841 + ((876600.0 * 60.0 * 60.0 + 8640184.812866) * TUT1) + (0.093104 * (TUT1**2.0)) - (6.2 * (10.0**-6.0) * (TUT1**3.0))
GMST_angle = math.fmod(GMST_s, 86400.0) * w
GMST_angle = math.fmod((GMST_angle + (2.0 * math.pi)), (2.0 * math.pi))

# calculate the ECEF values given ECI and GMST angle
RzGMST = [[math.cos(-GMST_angle), math.sin(-GMST_angle), 0], [-math.sin(-GMST_angle), math.cos(-GMST_angle), 0], [0, 0, 1]]
rECEF = [ecef_x_km, ecef_y_km, ecef_z_km]

for i in range(len(RzGMST)):
    for j in range(len(RzGMST[0])):
        rECI[i] += RzGMST[i][j] * rECEF[j]
print(rECI[0])
print(rECI[1])
print(rECI[2])
