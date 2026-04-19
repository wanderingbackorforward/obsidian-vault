from collections import defaultdict

def dfs(node):
    pass

def solve(weights,uvs):
    res = []

    return res

def main():
    T = map(int,input())
    weights = map(int,input().split())
    uvs = defaultdict(list)
    for _ in range(T-1):
        u,v = map(int,input())
        uvs[u-1].append(v-1)
        uvs[v-1].append(u-1)
    res = solve(weights,uvs)
    print(" ".join(res))

if __name__ == "__main__":
    main()