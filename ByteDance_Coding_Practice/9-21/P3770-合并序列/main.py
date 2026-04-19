def is_same(res,i,j):
    for r in res[i+1:j+1]:
        if r != res[i]:
            return False
    return True

def merge(res,k):
    if len(res)<k:
        return res
    start = 0
    while len(res)-start>=k:
        while len(res)-start>=k and is_same(res,start,start+k-1):
            new_num = res[start]+1
            res = res[:start]+[new_num]+res[start+k:]
        start+=1

    return res
    
def solve(n,k):
    res=[]
    for i in range(n):
        res.append(1)
        merge(res,k)

    return res

def main():
    n,k = map(int,input().split())
    res = solve(n,k)
    print(' '.join(map(res,str)))
if __name__ == "__main__":
    main()