"""
EXAMPLE USAGE:

    (the below use of the functions would take input.txt file as input which is the location of the input file and
    write the output in the output.txt file as per the instructions mentioned in the assignment.)
    
    sleator("input.txt","output.txt")
    and 
    FFDH("input.txt","output.txt")
    and 
    Grid_packing("input.txt","output.txt")
    
"""
def sleator(input_file,output_file):
    class Rectangle:
        def __init__(self, name, width, height):
            self.name = name
            self.width = width
            self.height = height
    def func(arr,w):
        ans=[]
        h0=0
        wmax=0
        i=0
        large = [rect for rect in arr if rect.width > w // 2]
        while i<len(large):
            ans.append((large[i].name,0,h0))
            wmax=max(wmax,large[i].width)
            h0+=large[i].height
            i+=1
        small=[rect for rect in arr if rect.width <= w // 2]
        small.sort(key=lambda r: r.height,reverse=True)
        hmax=h0
        level=h0
        hl=hr=h0
        curr=0
        i=0
        while i<len(small) and curr+small[i].width<=w:
            ans.append((small[i].name,curr,level))
            hmax=max(hmax,level+small[i].height)
            curr+=small[i].width
            wmax=max(wmax,curr)
            if curr<=w//2:
                hl=max(level+small[i].height,hl)
            if curr>w//2:
                hr=max(level+small[i].height,hr)
            i+=1
        while i<len(small):
            if hl<=hr:
                level=hl
                curr=0
                while i<len(small) and curr+small[i].width<=w//2:
                    ans.append((small[i].name,curr,level))
                    curr+=small[i].width
                    hl=max(hl,level+small[i].height)
                    wmax=max(wmax,curr)
                    i+=1
                hmax=max(hl,hmax)
            else:
                level=hr
                curr=w//2
                while i<len(small) and curr+small[i].width<=w:
                    ans.append((small[i].name,curr,level))
                    curr+=small[i].width
                    hr=max(hr,level+small[i].height)
                    wmax=max(wmax,curr)
                    i+=1
                hmax=max(hmax,hr)
        return wmax,hmax,ans

    with open(input_file, 'r') as f:
        a = f.readlines()
    rectangles = []
    startw=0
    sumw=0
    for i in a:
        name, width, height = i.split()
        rectangles.append(Rectangle(name, int(width), int(height)))
        sumw+=int(width)
        startw=max(startw,int(width))
    height=10**5
    width=10**5
    coordinates=[]
    gates=rectangles
    for i in range(startw,sumw+1):
        w,h,b=func(gates,i)
        if(w*h<height*width):
            width=w
            height=h
            coordinates=b
        gates=rectangles
    with open(output_file, 'w') as f:
        f.write(f"bounding_box {width} {height}\n")
        for i in range(len(coordinates)):
            f.write(f"{coordinates[i][0]} {coordinates[i][1]} {coordinates[i][2]}\n")

def FFDH(input,output):
    class Rectangle:
        def __init__(self, name, width, height):
            self.name = name
            self.width = width
            self.height = height
    def func(arr, w):
        ans = []
        hmax,wmax = 0,0
        height = 0
        curx,cury = 0,0
        arr.sort(key=lambda r: r.height, reverse=True)
        for gate in arr:
            if curx + gate.width <= w:
                ans.append((gate.name, curx, cury))
                curx += gate.width
                height = max(height, gate.height)
            else:
                cury += height
                curx = 0
                height = gate.height
                ans.append((gate.name, curx, cury))
                curx += gate.width
            hmax = max(hmax, cury + height)
            wmax = max(wmax, curx)
        return wmax, hmax, ans

    with open(input, 'r') as f:
        a = f.readlines()
    rectangles = []
    startw=0
    sumw=0
    for i in a:
        name, width, height = i.split()
        rectangles.append(Rectangle(name, int(width), int(height)))
        sumw+=int(width)
        startw=max(startw,int(width))
    height=10**5
    width=10**5
    coordinates=[]
    gates=rectangles
    for i in range(startw,sumw+1):
        w,h,b=func(gates,i)
        if(w*h<height*width):
            width=w
            height=h
            coordinates=b
        gates=rectangles
    with open(output, 'w') as f:
        f.write(f"bounding_box {width} {height}\n")
        for i in range(len(coordinates)):
            f.write(f"{coordinates[i][0]} {coordinates[i][1]} {coordinates[i][2]}\n")

def Grid_packing(input_f,output_f):
    class Rectangle:
        def __init__(self, name, width, height):
            self.name = name
            self.width = width
            self.height = height
            self.a=0
            self.b=0
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
        arr=sorted(arr,key=lambda r: r.height,reverse=True)
        i=0
        while i<len(arr):
            placed=False
            for y in range(len(grid)):
                if placed==True:
                    break
                for x in range(len(grid)):
                    if check(arr[i],x,y,grid)==True:
                        arr[i].a=x
                        arr[i].b=y
                        ans.append((arr[i].name,x,y))
                        put(arr[i],x,y,grid)
                        placed=True
                        break
            if placed==False:
                n=max(2*len(grid),max(arr[i].a+arr[i].width,arr[i].b+arr[i].height))
                new=[[False for l in range(n)] for j in range(n)]
                inc=len(new)-len(grid)
                for l in range(len(grid)):
                    for j in range(len(grid)):
                        new[inc+l][j]=grid[l][j]
                grid=new
            else:
                i+=1
        wmax=max(r.a + r.width for r in arr)
        hmax=max(r.b + r.height for r in arr)
        return wmax,hmax,ans

    grid=[[False]]
    with open(input_f, 'r') as f:
        a = f.readlines()
    rectangles = []
    for i in a:
        name, width, height = i.split()
        rectangles.append(Rectangle(name, int(width), int(height)))
    w,h,coordinates=func(rectangles,grid)
    with open(output_f, 'w') as f:
        f.write(f"bounding_box {w} {h}\n")
        for i in range(len(coordinates)):
            f.write(f"{coordinates[i][0]} {coordinates[i][1]} {coordinates[i][2]}\n")