def is_same(res,i,j):
    for r in res[i+1:j+1]:
        if r != res[i]:
            return False
    return True

def merge(res,k):
    
def solve(n,k):
    res=[]
    for i in range(n):
        res.append(1)
        merge(res,k)

    return res

def main():
    n,k = map(int,input().split())
    res = solve(n,k)
    print(' '.join(map(str,str)))
if __name__ == "__main__":
    main()