#Multiobjective Dijkstra Algorithm for multi-objective shortest path problem
#3 values in the cost vector and the first is non summable (Ploss)
#To get summable ploss the log10 it is used.


import time
import math



#The following function is used to sort the labels inside the priority queue H
#in a lexicographic way. It is a bubble sort.
#Input: the queue H, output the queue H sorted and the lexmin label in H
def extract_sort_lex_min(H):
    scambio=1
    temp=0
    while scambio!=0:
        scambio=0
        for i in range(len(H)-1):
            if check_lexographic_label(H[i],H[i+1])==0 and H[i][1]!=H[i+1][1]:
                temp=H[i+1]
                H[i+1]=H[i]
                H[i]=temp
                scambio+=1

            if H[i][1]==H[i+1][1]:
                continue

    return H, H[0]






#This function simply return the index associated to the string "node"
#which is the name of the node.
#It wants as input the list of the name of nodes.
def node_to_index(node):
    for i in range(len(nodes)):
        if node == nodes[i]:
            index=i
    return index



#This function does the opposite function of the previous function. Index as
#input and node name as outpud.

def index_to_node(index):
    nodename=nodes[index]
    return nodename

#This function wants the labels as input and performs the sum of the two cost
#vectors of the labels
def sum_list(l1,l2):
    if l1[1]=='NULL' or l2[1]=='NULL':
        print("ONE IS NULL")
        return 'NULL'
    else:
        summed=[l1[1][0]+l2[1][0],l1[1][1]+l2[1][1],l1[1][2]+l2[1][2]]
        return summed



#This function returns the list of the index of previou node with respect to the
#actual_node_index. The input is the index of the node that you want to consider
def previous_nodes_index(actual_node_index):

    previous_nodes_index=[]
    index=actual_node_index

    for i in range(len(nodes)):
        if connections[i][index]!=0:
            previous_nodes_index.append(i)
    return previous_nodes_index

#This function returns the next nodes index with respect to the actual_node_index.
#(the nodes that are connected with the outgoing arcs)
def next_nodes_index(actual_node_index):
    next_nodes_index=[]
    index=actual_node_index
    for i in range(len(nodes)):
        if connections[index][i]!=0:
            next_nodes_index.append(i)
    return next_nodes_index

"""
def arc_out(node_index):
    next_nodes_name=[]
    for j in range(len(connections[node_index])):
        if connections[node_index][j]!=0:
            next_nodes_name.append(index_to_node(j))
    return next_nodes_name
"""
"""
def arc_gen(connections):
    a=0
    arc=[0 for i in range(int(len(nodes)*(len(nodes)-1)/2))]
    for i in range(len(connections)):
        for j in range(len(connections[0])):
            if connections[i][j]!=0:
                arc[a]=index_to_node(i) + "-" + index_to_node(j)
                a+=1
    return arc
"""
"""
def arc_num(connections):
    card=0
    arc=arc_gen(connections)
    for i in range(len(arc)):
        if arc[i]!=0:
            card+=1
    return card
"""

#This function performs the lexicographic label check.
#It must be modified in the case of more or less than 3 costs
def check_lexographic_label(l1,l2):
    a=0
    #print(len(l1[1]))
    for i in range(len(l1[1])):
        if l1[1][i]>l2[1][i]:
            return 0
        if l1[1][i]==l2[1][i]:
            continue
        if l1[1][i]<l2[1][i]:
            return 1

#This function performs the dominance check. It wants as input the list (L[v]) of non-dominated label for a given node
#and the label (l) to compare
def check_dominance_L(L,l):
    x=l[1][0]
    y=l[1][1]
    z=l[1][2]
    dom_flag=0
    for i in range(1,len(L)):
        a=L[i][1][0]
        b=L[i][1][1]
        c=L[i][1][2]

        if a<=x and b<=y and c<=z:
            if a<x:
                dom_flag+=1
            if b<y:
                dom_flag+=1
            if c<z:
                dom_flag+=1

        if a==x and b==y and c==z:
            dom_flag+=1

    if dom_flag>=1:
        return 1
    else:
        return 0

#This function checks if a label of a node w exists in the H queue
def H_contains(H,w):
    if H==[]:
        return None
    else:
        for i in range(len(H)):
            if H[i][0]==index_to_node(w):
                return i

#This function performs the pseudofuncion described in the paper (same name)
def propagate(lv_star,w,H,L):
    v=node_to_index(lv_star[0])

    l_new=[index_to_node(w),sum_list(lv_star,[0,connections[v][w],0]),[node_to_index(lv_star[0]),L[v].index(lv_star)]]
    indice=H_contains(H,w)
    if check_dominance_L(L[w],l_new)==0:
        if indice==None:
            H.append(l_new)
        elif check_lexographic_label(l_new,H[indice])==1:
            H[indice]=l_new
    return H


#This function performs the pseudofuncion described in the paper (same name)
def nextCandidateLabel(v,lastProcessedLabel,u,L):
    lv=[index_to_node(v),[1e6,1e6,1e6],['NULL','NULL']]
    for item in u:
        for k in range(int(lastProcessedLabel[item][v]),len(L[item])):
            if L[item][k]==[]:
                continue
            else:
                lu=L[item][k]
                lnew=[index_to_node(v),sum_list(L[item][k],[0,connections[item][v],0]), [item,k]]
                lastProcessedLabel[item][v]=k
            if L[v]!=[[]] and check_dominance_L(L[v],lnew)==0:
                if check_lexographic_label(lnew,lv)==1:
                    lv=lnew
                    break
    if lv[1]==[1e6,1e6,1e6]:
        return lastProcessedLabel,None
    else:
        return lastProcessedLabel,lv

#This function does the log10 of the first element of each cost vector on the arcs
def first_to_log10(nodes,connections):
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if connections[i][j]!=0:
                if connections[i][j][0]!=1:
                    connections[i][j][0]=-math.log10(1-connections[i][j][0])
                elif connections[i][j][0]==1:
                    connections[i][j][0]=-math.log10(1-0.99999999)
    return connections

#This function performs the inverse of the log10 in order to get back the linear
#value of the first element of the cost vector
def first_to_linear(L):
    for i in range(len(L)):
        for j in range(1,len(L[i])):
            L[i][j][1][0]=10**(-L[i][j][1][0])
    return L

#This function performs the complementar of the first cost to take the ploss
def first_to_complementar(L):
    for i in range(len(L)):
        for j in range(1,len(L[i])):
            L[i][j][1][0]=round(1-(L[i][j][1][0]),7)
    return L

#This is the equivalent of "algorithm1" in the paper
#The outputs are the list containing the non dominated labels for each node
#Node: v6 ( 6 ) --> L: [['v6', [0.0005, 3, 14], [3, 1]], ['v6', [1.0, 4, 11], [4, 2]]]
#This example provides the non-dominated labels of node 6. In this case there are two
#non-dominated labels. The last element of a label means that (i.e. [3,1]) the previous node
#is 3 and the associated label of a node 3 is the first.
def MDA(node,connection):
    global nodes
    global connections
    global t_start
    global t_finish
    global L
    nodes=node
    connections=connection

    t_start=time.time()

    H=[] #Priority Queue

    L=[[[]] for i in range(len(nodes))] #Efficient labels Lv <-- []

    global lastProcessedLabel
    lastProcessedLabel=[[0 for i in range(len(nodes)) ] for j in range(len(nodes))]
    ls=[nodes[0],[0,0,0],['NULL','NULL']]
    H.append(ls)


    while H!=[]:
        H,lv_star=extract_sort_lex_min(H)
        H.pop(0)
        index=node_to_index(lv_star[0])
        v=index
        L[index].append(lv_star)
        u=previous_nodes_index(index)
        lastProcessedLabel,lv_new=nextCandidateLabel(v,lastProcessedLabel,u,L)
        if lv_new != None:
            H.append(lv_new)
        w=next_nodes_index(v)
        for item in w:
            H=propagate(lv_star,item,H,L)
    t_finish=time.time()
    return L

#This function just print the output
def print_output(L):
    for i in range(len(nodes)):
        print("\n","Node:", index_to_node(i), "(",i,")", "--> L:",L[i][1:])
        if i==len(nodes)-1:
            print("")





if __name__ == "__main__":

    nodes=['s','v1','v2','v3','v4','v5','v6','v7','v8','MEH5','MEH6','MEH7','MEH8']
    s=[0,[0,1,10],[0.0017,2,5],[0,2,10],0,0,0,0,0,0,0,0,0]
    v1=[0,0,0,0,[0.0025,3,3],[0.002,1,5],0,0,0,0,0,0,0]
    v2=[0,0,0,0,[0,1,3],0,0,0,0,0,0,0,0]
    v3=[0,0,[0,1,2],0,0,0,[0.0005,1,4],[0.001,38,1],0,0,0,0,0]
    v4=[0,0,0,0,0,[0,2,4],[1,1,3],0,0,0,0,0,0]
    v5=[0,0,0,0,0,0,0,0,[0,1,3],[0.3,0,15],0,0,0]
    v6=[0,0,0,0,0,0,0,0,[0.0021,1,1],0,[0.1,0,10],0,0]
    v7=[0,0,0,0,0,0,0,0,[0,4,10],0,0,[0.1,0,15],0]
    v8=[0,0,0,0,0,0,0,0,0,0,0,0,[0.3,0,15]]
    MEH5=[0,0,0,0,0,0,0,0,0,0,0,0,0]
    MEH6=[0,0,0,0,0,0,0,0,0,0,0,0,0]
    MEH7=[0,0,0,0,0,0,0,0,0,0,0,0,0]
    MEH8=[0,0,0,0,0,0,0,0,0,0,0,0,0]
    connections=[s,v1,v2,v3,v4,v5,v6,v7,v8,MEH5,MEH6,MEH7,MEH8]

    connections=first_to_log10(nodes,connections)
    L=MDA(nodes,connections)
    L=first_to_linear(L)
    L=first_to_complementar(L)
    #epsilon_constraint=[0.002,40]
    #L=eps_const(epsilon_constraint,L)
    print_output(L)
