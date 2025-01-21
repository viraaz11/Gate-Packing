from rec import *
from pins import *
from cluster_obj import *
from loop import *
def critical(gate_list,gate,wire_delay):
    if gate.delay!=gate.prev_delay:
        return (gate.prev_delay,gate.prev_path)
    maxi=0
    ans=""
    last=True
    for left_pin in gate.left_pins:
        if left_pin.used==0:
            continue
        else:
            last=False
            w=left_pin.semi_peri*wire_delay
            gate2=gate_list[left_pin.more_pins[0].owner]
            curr=gate2.name+"."+left_pin.more_pins[0].name+" "+gate.name+"."+left_pin.name
            d,p=critical(gate_list,gate2,wire_delay)
            if w+d> maxi:
                maxi=max(maxi,w+d+gate.delay)
                ans=p+" "+curr
    gate.prev_delay=maxi
    gate.prev_path=ans
    if last:
        ans=gate.name+"."+gate.left_pins[0].name
        maxi=gate.delay
    return (maxi,ans)
def maxcrit(gates,gate_list,wire_delay):
    max_time=0
    critical_path=""
    for gate in gates:
        pout=True
        for right_pins in gate.right_pins:
            if right_pins.used: 
                pout=False
                break
        if pout and len(gate.right_pins)>0:
            loop=False
            curr,p=critical(gate_list,gate,wire_delay)

            if curr>max_time:
                max_time=curr
                critical_path=p+" "+gate.name+"."+ gate.right_pins[0].name

    return max_time,critical_path