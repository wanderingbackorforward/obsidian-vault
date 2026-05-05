def main():
    n = int(input())
    grid = [list(map(int,input().split())) for _ in range(n)]
    def max_2(i,j):
        l = [grid[i][j],grid[i][j+1],grid[i+1][j],grid[i+1][j+1]]
        l.sort(reverse= True)
        return l[1]
    while len(grid)>1:
        new_grid = []
        size = len(grid)
        for i in range(0,size,2):
            new_grid_row=[]
            for j in range(0,size,2):
                val = max_2(i,j)
                new_grid_row.append(val)
            new_grid.append(new_grid_row)
        grid = new_grid
        
        
        
    print(grid[0][0])
    
if __name__ == "__main__":
    main()