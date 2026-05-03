import math

def main():
    ans = []
    T = int(input())
    for _ in range(T):
        n,k= map(int,input().split())
        a = list(map(int,input().split()))
        res=0
        for x in a:
            res = math.gcd(res,x)
        ans.append(str(res))
    print("\n".join(ans*k))
    
if __name__ == "__main__":
	main()