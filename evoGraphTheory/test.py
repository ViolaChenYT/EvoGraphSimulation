import math

ks = [1,2,4,8,16,32]
rho = 0.95

def getp0(k):
  ans = 0
  for i in range(k):
    ans += (k * rho)**i / math.factorial(i) 
  return 1 / (ans + (k * rho) ** k / (math.factorial(k) * (1 - rho)) )

def calcPQ(k):
  p0 = getp0(k)
  print(k, p0, end=' ')
  ans = p0 * (k * rho) ** k / (math.factorial(k) * (1-rho))
  return ans

def calcTQ(k, pq):
  return  1 / (k*(1-rho))

for k in ks:
  pq = calcPQ(k)
  tq = calcTQ(k,pq)
  print( pq, tq)