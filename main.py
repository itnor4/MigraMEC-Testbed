from MDA_firstisploss_DEF import MDA, first_to_complementar, first_to_log10, first_to_linear, print_output
from API_post_mobility import post_mobility
from zoneofcoverage import p_choose, p_choose_noMEC
import time
import random
import os


#The following function is not used for selecting the MEC, please refer to the function named as poa_selector_noMEC
def poa_selector(last,selected_poa_last, Ploss):
    nodes=['e1','op1','z1','z2','z3','wifi1','4g1','5g1','wifi2','4g2','5g2','b_ner']#'fog1',
    ztopoa=[0,3,5]
    optoz=[0,1,6]
    e1=[0,0,0,0,ztopoa,0,0,0,0,0,0,0]
    op1=[0,0,optoz,optoz,0,0,0,0,0,0,0,0]
    z1=[0,0,0,0,0,ztopoa,0,0,ztopoa,0,0,0]
    z2=[0,optoz,0,0,0,0,ztopoa,0,0,ztopoa,0,0]
    z3=[0,optoz,0,0,0,0,0,ztopoa,0,0,ztopoa,0]


    w1=[0,0,0,0,0,0,0,0,0,0,0,[0,1,4]]
    g41=[0,0,0,0,0,0,0,0,0,0,0,[0.00016,4,9]]
    g51=[0,0,0,0,0,0,0,0,0,0,0,[0,3,20]]
    w2=[0,0,0,0,0,0,0,0,0,0,0,[0,4,4]]
    g42=[0,0,0,0,0,0,0,0,0,0,0,[0.000079,3,17]]
    g52=[0,0,0,0,0,0,0,0,0,0,0,[0,7,20]]
    b_ner=[0,0,0,0,0,0,0,0,0,0,0,0]

    connections=[e1,op1,z1,z2,z3,w1,g41,g51,w2,g42,g52,b_ner]

    modificato=0
    p, uename, p_description=p_choose()

    print(p[0],p[1])

    if p!=last:

        for k in range(len(p[0])):
            if p[0][k]==0:
                connections[-7+k][-1]=0
                modificato=1
            if p[1][k]==0:
                connections[-4+k][-1]=0
                modificato=1
        if modificato==1:
            connections=first_to_log10(nodes,connections)
            L=MDA(nodes,connections)
            first_to_linear(L)
            first_to_complementar(L)
            selected_poa=nodes[L[-1][1][2][0]]
            last=p
            if selected_poa_last!=selected_poa:
                r=post_mobility(uename,selected_poa)
                print(uename,"connected to",selected_poa)
                selected_poa_last=selected_poa
                Ploss=L[-1][1][1][0]
                Jitter=L[-1][1][1][1]
                print("Expected Jitter: ",Jitter)
                Latency=L[-1][1][1][2]
                print("Expected RTT: ",Latency)

    print("Expected Ploss: ", Ploss)

    return last,selected_poa_last,Ploss

#this function and the following values are used for the selection of MEC and PoA experiment.
def poa_selector_noMEC(last,selected_poa_last, Ploss):
    nodes=['e1','op1','z1','z2','z3','wifi1','4g1','5g1','wifi2','4g2','5g2','b_ner']
    ztopoa=[0,3,5]
    optoz=[0,1,6]
    e1=[0,0,0,0,ztopoa,0,0,0,0,0,0,0]
    op1=[0,0,optoz,optoz,0,0,0,0,0,0,0,0]
    z1=[0,0,0,0,0,ztopoa,0,0,ztopoa,0,0,0]
    z2=[0,optoz,0,0,0,0,ztopoa,0,0,ztopoa,0,0]
    z3=[0,optoz,0,0,0,0,0,ztopoa,0,0,ztopoa,0]
    w1=[0,0,0,0,0,0,0,0,0,0,0,[0,1,4]]
    g41=[0,0,0,0,0,0,0,0,0,0,0,[0.00016,4,9]]
    g51=[0,0,0,0,0,0,0,0,0,0,0,[0,3,5]]
    w2=[0,0,0,0,0,0,0,0,0,0,0,[0,4,4]]
    g42=[0,0,0,0,0,0,0,0,0,0,0,[0.000079,3,17]]
    g52=[0,0,0,0,0,0,0,0,0,0,0,[0.00016,4,9]]
    b_ner=[0,0,0,0,0,0,0,0,0,0,0,0]

    connections=[e1,op1,z1,z2,z3,w1,g41,g51,w2,g42,g52,b_ner]

    modificato=0
    p, uename, p_description= p_choose_noMEC()
  
    config.load_kube_config()
    v1 = client.CoreV1Api()
    #print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        a = i.metadata.name
        data = str(a)
        if 'video' in data:
            podname = data 
            print(podname)
            break
            
    if p!=last:
       if p[0][2]==1:
          selected_poa=p_description[0][2]
          r=post_mobility(uename,selected_poa)
          last=p
          selected_poa_last=selected_poa
          dt1 = datetime.now()
          args = ['kubectl', 'migrate', str(podname) , 'worker1-virtualbox']
          popen = subprocess.Popen(args, stdout=subprocess.PIPE)
          popen.wait()
          output = popen.stdout.read()
          dt3 = datetime.now()
          print("PoA:", dt1, selected_poa_last)
          print("Start Migration Edge1 to Edge2, Date and time is: " , dt3, output)
          
       elif p[1][1]==1:
          selected_poa=p_description[1][1]
          r=post_mobility(uename,selected_poa)
          last=p
          selected_poa_last=selected_poa
          dt2 = datetime.now()
          args = ['kubectl', 'migrate', str(podname) , 'master-virtualbox']
          popen = subprocess.Popen(args, stdout=subprocess.PIPE)
          popen.wait()
          output = popen.stdout.read()
          dt4 = datetime.now()
          print("PoA:", dt2, selected_poa_last)
          print("Start Migration Edge2 to Edge1, Date and time is:", dt4, output)

    return last,selected_poa_last,Ploss



if __name__ == "__main__":
    Ploss="Not available"
    last=[[0,0,0],[0,0,0]]
    selected_poa_last='foo'
   

    while True:
        time.sleep(1)
        last,selected_poa_last, Ploss=poa_selector_noMEC(last,selected_poa_last, Ploss)
