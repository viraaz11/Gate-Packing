class Gate:
    def __init__(self,name,height,width,id):
        self.id=id
        self.height=height
        self.width=width
        self.connections=0
        self.more_gates=[] 
        self.placed=0
        self.x=0
        self.y=0
        self.name = name
        self.pins = []
        self.right_connections=0