def sleator(gate):
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
    rectangles = gate
    startw=0
    sumw=0
    for i in rectangles:
        sumw+=int(i.width)
        startw=max(startw,int(i.width))
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
    return coordinates