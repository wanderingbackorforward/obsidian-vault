def solve(a,k):
    def count(x,num):
        count=0
        while x % num ==0:
            count+=1
            x //= num
        return count
            
    n=len(a)
    count_2 = [count(x,2) for x in a]
    count_5 = [count(x,5) for x in a]

    i=0
    while k>0 and i<n-1:
        if count_2[i] <k:
            k-=count_2[i]
            count_2[-1] += count_2[i]
            count_2[i] = 0
        else:
            count_2[-1] += k
            count_2[i] -= k
            break
        i+=1

    ans = []
    for i in range(n):
        ans.append (min(count_2[i],count_5[i]) )
    return ans

def main():
    n,k = map(int,input().split())
    a = list(map(int,input().split()))
    ans = solve(a,k)
    print(" ".join(map(str,ans)))

if __name__ == "__main__":
    main()