# get, ret = int(input()), []
# [ret.append('FizzBuzz' if x%3==0 and x%5==0 else ('Fizz' if x%3==0 else ('Buzz' if x%5==0 else str(x)))) for x in range(1,get+1)]
# print('\n'.join(ret))
# a=10
# b=5
# conditionValue=8
# value=(b*(conditionValue>10))+(a*(conditionValue<=10))

# if conditionValue>10:
#     value=b
# else:
#     value=a

fbStr=["","Fizz","Buzz","FizzBuzz"]
inValue=int(input())
outStr=""
for x in range(1, inValue+1):
    index=(2*(x%5==0 and x%3!=0))+(1*(x%3==0 and x%5!=0))+(3*(x%5==0 and x%3==0))
    fbStr[0]=str(x)
    outStr+=(fbStr[index]) + ","
print(outStr)
