def solve(grid):
    pass

def main():
    T = int(input())
    results = []
    for _ in range(T):
        n = int(input())
        grid = [input().strip() for _ in range(n)]
        counts,ways=solve(grid)
        results.append((counts,ways))
    for counts,ways in results:
        print(f"{counts} {ways}")

if __name__ =="__main__":
    main()