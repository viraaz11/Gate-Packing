def check(r,x,y,grid):
    if x+r.width>len(grid) or y+r.height>len(grid):
        return  False
    for i in range(r.height):
        for j in range(r.width):
            if grid[len(grid)-y-i-1][x+j]==True:
                return False
    return True
def put(r,x,y,grid):
    for i in range(r.height):
        for j in range(r.width):
            grid[len(grid)-y-i-1][x+j]=True
def func(arr,grid):
    ans=[]
    arr=sorted(arr,key=lambda r: r.right_connections,reverse=True)
    i=0
    while i<len(arr):
        placed=False
        for y in range(len(grid)):
            if placed==True:
                break
            for x in range(len(grid)):
                if check(arr[i],x,y,grid)==True:
                    arr[i].x=x
                    arr[i].y=y
                    ans.append((arr[i].name,x,y))
                    put(arr[i],x,y,grid)
                    placed=True
                    break
        if placed==False:
            n=max(2*len(grid),max(arr[i].x+arr[i].width,arr[i].y+arr[i].height))
            new=[[False for l in range(n)] for j in range(n)]
            inc=len(new)-len(grid)
            for l in range(len(grid)):
                for j in range(len(grid)):
                    new[inc+l][j]=grid[l][j]
            grid=new
        else:
            i+=1
    wmax=max(r.x + r.width for r in arr)
    hmax=max(r.y + r.height for r in arr)
    return wmax,hmax,ans


