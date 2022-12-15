def mex(nList: list):
    m = 0
    while m in nList:
        m += 1
    return m

closed = {0:0,1:1,2:1,3:1}
semiOpen = {0:0,1:0,2:0,3:2}
open = {0:0,1:0,2:0,3:1}

def nimOpen(num):
    if num in open.keys():
        return open[num]
    return mex(
        {1^nimOpen(num-2)}|
        {nimOpen(i)^nimOpen(num-1-i) for i in range(2,(num-3)//2)}
        )

def nimSemiOpen(num):
    if len(semiOpen) > num:
        return semiOpen[num]
    return mex(
        {1^nimSemiOpen(num-2)}|
        {nimOpen(i)^nimSemiOpen(num-1-i) for i in range(2,num)}
    )

def nimClosed(num):
    if len(closed) > num:
        return closed[num] 
    return mex({nimSemiOpen(i) ^ nimSemiOpen(num-1-i) for i in range(0,(num+3)//2)})

N = 20
print([nimOpen(i) for i in range(1,N)])
print([nimSemiOpen(i) for i in range(1,N)])
print([nimClosed(i) for i in range(1,N)])