from pins import *
from cluster import *
from rec import *
from grid_pack import *
from costfun import *
from sl import *
from loop import *
"""
EXAMPLE USAGE:

    (the below use of the functions would take input.txt file as input which is the location of the input file and
    write the output in the output.txt file as per the instructions mentioned in the assignment.)

    algo("input.txt","output.txt")

"""

def algo(input_file,output_file):
    def read_input(input_file):
        gate_list=[[]]
        f=open(input_file,"r")
        l=f.readlines()
        f.close()
        i=0
        wire_delay=0
        while i<len(l):
            if l[i][0]=='g':
                info=l[i].split()
                gate_id=int(info[0][1:])
                width=int(info[1])
                height=int(info[2])
                gate_delay=int(info[3])
                gate=Gate(info[0],height,width,gate_id,gate_delay)
                pin_info=l[i+1].split()
                n=(len(pin_info)-2)//2
                for j in range(n):
                    pin=Pin(j+1,int(pin_info[2*(j+1)]),int(pin_info[2*(j+1)+1]))
                    pin.owner=gate.id
                    gate.pins.append(pin)
                gate_list.append(gate)
                i+=2
            elif l[i].startswith("wire_delay"):
                a=l[i].split()
                wire_delay=int(a[1])
                i+=1
            else:
                a=l[i].split()
                i1=a[1].split(".")
                i2=a[2].split(".")
                gate1=int(i1[0][1:])
                pin1=int(i1[1][1:])
                gate2=int(i2[0][1:])
                pin2=int(i2[1][1:])
                gate_list[gate1].more_gates.append(gate2)
                gate_list[gate1].connections+=1
                gate_list[gate2].more_gates.append(gate1)
                gate_list[gate2].connections+=1
                gate_list[gate1].pins[pin1-1].more_pins.append(gate_list[gate2].pins[pin2-1])
                gate_list[gate2].pins[pin2-1].more_pins.append(gate_list[gate1].pins[pin1-1])
                gate_list[gate1].pins[pin1-1].used=1
                gate_list[gate2].pins[pin2-1].used=1
                if gate_list[gate1].pins[pin1-1].relative_pos[0]!=0:
                    gate_list[gate1].right_connections+=1
                if gate_list[gate2].pins[pin2-1].relative_pos[0]!=0:
                    gate_list[gate2].right_connections+=1
                i+=1
        for gate in gate_list[1:]:
            for pin in gate.pins:
                if pin.relative_pos[0]==0:
                    gate.left_pins.append(pin)
                else:
                    gate.right_pins.append(pin)
        return gate_list,wire_delay

    def write_output(file_path, best_solution, bx,by,max_time,path):
        with open(file_path, 'w') as f:
            f.write(f"bounding_box {bx} {by}\n")
            f.write(f"critical_path {path}\n")
            f.write(f"critical_path_delay {max_time}\n")
            for gate in best_solution:
                f.write(f"{gate.name} {gate.x} {gate.y}\n")

    def main_for_grid(gate_list,wire_delay):
        bx=0
        by=0
        final_placement=[]
        clusters=cluster_formation(gate_list)
        max_time=0
        path=""
        for j in clusters:
            grid=[[False]]
            w,h,coordinates=func(j.gates,grid)
            for i in coordinates:
                gate =gate_list[int(i[0][1:])]
                gate.x=i[1]+bx
                gate.y=i[2]
            c=cal(j,gate_list)
            try:
                curr,p=maxcrit(j.gates,gate_list,wire_delay)
            except:
                raise LoopDetected()
            if max_time<curr:
                max_time=curr
                path=p
            bx+=w
            by=max(by,h)    
            final_placement+=j.gates
        write_output(output_file, final_placement, bx, by,max_time,path)
    def main_for_sl(gate_list,wire_delay):
        bx=0
        by=0
        final_placement=[]
        clusters=cluster_formation(gate_list)
        max_time=0
        path=""
        for j in clusters:
            coordinates=sleator(j.gates)
            for i in coordinates:
                gate =gate_list[int(i[0][1:])]
                gate.x=i[1]+bx
                gate.y=i[2]
            c=cal(j,gate_list)
            try:
                curr,p=maxcrit(j.gates,gate_list,wire_delay)
            except:
                raise LoopDetected()
            if max_time<curr:
                max_time=curr
                path=p
            bounding_box = calculate_bounding_box(j.gates)
            bx+=(bounding_box[2]-bounding_box[0])
            by=max(by,bounding_box[3]-bounding_box[1])  
            final_placement+=j.gates
        write_output(output_file, final_placement, bx, by,max_time,path)
        
    gate_list,wire_delay=read_input(input_file)
    
    loop=True
    for i in gate_list[1:]:
        if sum(j.used for j in i.left_pins)==0:
            loop =False
            break
    if loop: raise LoopDetected()
    if len(gate_list)>700:
        main_for_sl(gate_list,wire_delay)
    else:
        main_for_grid(gate_list,wire_delay)