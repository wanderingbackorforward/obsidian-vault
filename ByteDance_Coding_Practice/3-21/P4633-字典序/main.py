def c2n(c):
    if c > 'a' and c <'z':
        return ord(c)-ord('a')
    return ord(c)-ord('A')+26

def solve(grid,n):
    grid_num = [[c2n(c) for c in s] for s in grid]
    k = 52
    total = [0]*k
    count_r = [[0]*k for _ in range(n)]
    count_c = [[0]*k for _ in range(n)]
    char_counts_r = [[0]*n for _ in range(k)]
    char_counts_c = [[0]*n for _ in range(k)]

    for i in range(n):
        nums = grid_num[i]
        for j in range(n):
            num=nums[j]
            total[num]+=1
            count_r[i][num]+=1
            count_c[j][num]+=1
            char_counts_r[num][i]+=1
            char_counts_c[num][j]+=1    

    char_min_rc = [min(char_counts_r(k))+min(char_counts_c(k)) for _ in range(k)]

    

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