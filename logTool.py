import math

re= math.log(4,2)
# re=math.sqrt(5)
# re=math.pow(3,2)
re= math.log(6.3,2)
re= 6/7
re= 6/7
rePrecision=46/56
reRecall= 46/75

print('-----------'+'\n')
print(rePrecision)
print(reRecall)

array1=[0.81, 0.32, 0.65, 0.2, 1.0, 0.15, 1.0, 0.37]
array2=w = [3, 1, 2, 2, 1, 1, 1, 2]
res=0
for idx in range(len(array1)):
  val1=array1[idx]
  val2=array2[idx]
  res+=val1*val2

print(res)

i1=1180000
i2=6000*5999*0.5
print('i2=',i2)
print (1-i1/i2)