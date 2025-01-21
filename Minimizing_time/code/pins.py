class Pin:
    def __init__(self,id,x,y):
        self.owner=None
        self.relative_pos=(x,y)
        self.id=id
        self.more_pins=[]
        self.used=0
        self.vis=0
        self.semi_peri=None
        self.name="p"+str(self.id)