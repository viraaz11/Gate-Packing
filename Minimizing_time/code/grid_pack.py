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
    if len(arr)==2:
        if sum(i.used for i in arr[0].right_pins)>sum(i.used for i in arr[1].right_pins):
            arr[1].x=arr[0].width
            arr[1].y=arr[0].right_pins[0].relative_pos[1]-arr[1].left_pins[0].relative_pos[1]
            miny=min(arr[1].y,arr[0].y)
            arr[1].y-=miny   
        else:
            arr[0].x=arr[1].width
            arr[0].y=arr[1].right_pins[0].relative_pos[1]-arr[0].left_pins[0].relative_pos[1]
            miny=min(arr[0].y,arr[1].y)
            arr[0].y-=miny  
        wmax=max(r.x + r.width for r in arr)
        hmax=max(r.y + r.height for r in arr)
        ans=[(arr[0].name,arr[0].x,arr[0].y),(arr[1].name,arr[1].x,arr[1].y)]
        # print(ans)
        return wmax,hmax,ans
    else:
        ans=[]
        if len(arr)>15 and len(arr)<100: arr=sorted(arr,key=lambda r: r.right_connections) 
        elif len(arr)>4 and len(arr)<=15: arr=sorted(arr,key=lambda r: r.delay-r.right_connections)
        elif len(arr)<4: arr=sorted(arr,key=lambda r: r.connections)
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