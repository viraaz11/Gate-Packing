class Gate:
    def __init__(self,name,height,width,id,gate_delay):
        self.id=id
        self.height=height
        self.width=width
        self.connections=0
        self.more_gates=[] 
        self.placed=0
        self.x=0
        self.y=0
        self.name = name
        self.pins=[]
        self.left_pins = []
        self.right_pins=[]
        self.right_connections=0
        self.delay=gate_delay
        self.prev_delay=gate_delay
        self.prev_path=""