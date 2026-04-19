def c2n(c):
    if c >= 'a' and c <='z':
        return ord(c)-ord('a')
    return ord(c)-ord('A')+26

def solve(grid,n):
    grid_num = [[c2n(c) for c in s] for s in grid]
    k = 52
    total = [0]*k
    count_r = [[0]*k for _ in range(n)]
    count_c = [[0]*k for _ in range(n)]
    

    for i in range(n):
        nums = grid_num[i]
        for j in range(n):
            num=nums[j]
            total[num]+=1
            count_r[i][num]+=1
            count_c[j][num]+=1
    counts = 0
    ways = 0
    for i in range(n):
        for j in range(n):
            for k_n in range(k):
                curren = total[k_n] + 2*n-1 -count_r[i][k_n] -count_c[j][k_n]
                if nums[i][j]==k_n:
                    curren+=1
                if curren > counts:
                    counts=curren
                    ways=1
                else:
                    ways+=1
    
    return counts,ways


def main():
    T = int(input())
    results = []
    for _ in range(T):
        n = int(input())
        grid = [input().strip() for _ in range(n)]
        counts,ways=solve(grid,n)
        results.append((counts,ways))
    for counts,ways in results:
        print(f"{counts} {ways}")

if __name__ =="__main__":
    main()