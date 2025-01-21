from pins import *
from rec import *
from cluster_obj import *
def cluster_formation(gate_list):
    n_gates=len(gate_list)-1
    vis=[0 for i in range(n_gates+1)]
    adj=[[] for i in range(n_gates+1)]
    for i in range(1,n_gates+1):
        for l in gate_list[i].more_gates:
            adj[i].append(l)
    def grouping(vis,adj,gate_list,final):
        def dfs(k,cluster):
            if vis[k]==1:
                return
            if vis[k]==0:
                cluster.gates.append(gate_list[k])
                vis[k]=1
                for i in adj[k]:
                    if vis[i]==1:
                        continue
                    g1=gate_list[k]
                    g2=gate_list[i]
                    for pin in g1.pins:
                        for other in pin.more_pins:
                            if other.owner==g2.id:
                                t=(g1.name,pin.id,g2.name,other.id )
                                cluster.pin_clusters.append(t)
                    dfs(i,cluster)
                    
        for i in range(1,len(gate_list)):
            if vis[i]==0:
                cluster=cluster_obj()
                dfs(i,cluster)
                final.append(cluster)
                
    final=[]
    grouping(vis,adj,gate_list,final)
    return final

def cal(cluster,gate_list):
    def dfs(pin,pin_groups):
        if pin.used==0:
            return
        if pin.vis==1:
            return
        else:
            pin_groups.append(pin)
            pin.vis=1
            for other in pin.more_pins:
                dfs(other,pin_groups)
    useful_pins=[]
    for gate in cluster.gates:
        for pin in gate.pins:
            if pin.used==1:
                useful_pins.append(pin)
    ans=[]
    for i in range(len(useful_pins)):
        if useful_pins[i].vis==1:
            continue
        else:
            pin_group=[]
            dfs(useful_pins[i],pin_group)
            ans.append(pin_group)
    for i in useful_pins:
        i.vis=0
    ct=0
    def f(pin_group):
        minx=10**18
        miny=10**18
        maxx=-1
        maxy=-1
        for pin in pin_group:
            minx=min(minx,pin.relative_pos[0]+gate_list[pin.owner].x)
            miny=min(miny,pin.relative_pos[1]+gate_list[pin.owner].y)
            maxx=max(maxx,pin.relative_pos[0]+gate_list[pin.owner].x)
            maxy=max(maxy,pin.relative_pos[1]+gate_list[pin.owner].y)
        l=maxx-minx
        b=maxy-miny
        return l+b
    for pin_group in ans:
        ct+=f(pin_group)
    return ct

