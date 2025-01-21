class cluster_obj:
    def __init__(self):
        self.gates=[]
        self.pin_clusters=[]
        
def calculate_bounding_box(gates):
    if not gates:
        return None
    min_x = min(gate.x for gate in gates)
    min_y = min(gate.y for gate in gates)
    max_x = max(gate.x + gate.width for gate in gates)
    max_y = max(gate.y + gate.height for gate in gates)
    return (min_x, min_y, max_x, max_y)
