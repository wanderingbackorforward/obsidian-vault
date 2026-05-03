import math

def check(a,k,x):
    pass

def main():
    ans = []
    T = int(input())
    for _ in range(T):
        x=0
        n,k= map(int,input().split())
        a = list(map(int,input().split()))
        while not check(a,k,x):
            x+=1

        ans.append(str(x))
    print("\n".join(ans))
    
if __name__ == "__main__":
    main()