from collections import deque

def check(rows,cols,grid):
    visited = [[False]*cols for _ in range(rows)]
    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    def bfs(i,j):
        dq = deque()
        cells = []
        dq.append((i,j))
        cells.append((i,j))
        visited[i][j]=True
        while dq:
            x,y = dq.popleft()
            for dx,dy in dirs:
                nx = x + dx
                ny = y + dy
                if 0<=nx<rows and 0<=ny<cols:
                    if grid[nx][ny]=="*" and not visited[nx][ny]:
                       dq.append((nx,ny))
                       cells.append((nx,ny))
                       visited[nx][ny]=True 

        return cells  
    
        
    def t_t(cells):
        if len(cells)!=4:
            return False
        row_set = set()
        col_set = set()
        for x,y in cells:
            row_set.add(x)
            col_set.add(y)
        if len(row_set)!=2 or len(col_set)!=2:
            return False
        return True
        

    for i in range(rows):
        for j in range(cols):
            if grid[i][j]=="*" and not visited[i][j]:
                cells = bfs(i,j)
                if not t_t(cells):
                    return False
    return True

def main():
    ans = []
    T = int(input())
    for _ in range(T):
        n,m= map(int,input().split())
        rows=n
        cols=m
        grid = [input().strip() for _ in range(rows)]
        res = check(rows,cols,grid)
        if res:
            ans.append("Yes")
        else:
            ans.append("No")
    print("\n".join(ans))
    
if __name__ == "__main__":
    main()