from collections import defaultdict

def dfs(node,parent,weights,uvs,res,visited):
    weight = weights[node]
    res[weight]+=visited[weight]
    visited[weight]+=1
    for child in uvs[node]:
        if child != parent:
            dfs(child,node,weights,uvs,res,visited)

def solve(weights,uvs):    
    res = defaultdict(int)
    visited = defaultdict(int)
    dfs(0,-1,weights,uvs,res,visited)
    return res

def main():
    T = int(input())
    weights = map(int,input().split())
    uvs = defaultdict(list)
    for _ in range(T-1):
        u,v = map(int,input().split())
        uvs[u-1].append(v-1)
        uvs[v-1].append(u-1)
    res = solve(weights,uvs)
    print(" ".join(res))

if __name__ == "__main__":
    main()