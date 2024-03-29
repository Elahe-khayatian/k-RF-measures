import networkx as nx
import re
def gettrees(tree_file):
  A=[[x for x in line.translate({ord(c): None for c in '\n'}).split(' ')]for line in tree_file]
  trees_index=[]
  for i in A:
    if 'tree'in i:
        trees_index.append(A.index(i))
  trees=[]
  for i in range(len(trees_index)):
    T=[]
    if i+1<len(trees_index):
       for j in range(trees_index[i+1]-trees_index[i]-1):
           T.append(A[j+trees_index[i]+1])
    else:
       for j in range(len(A)-trees_index[-1]-1):
           T.append(A[j+trees_index[-1]+1])
    trees.append(T)
  return(trees)
def getpartitions(trees, k):
    P_Total=[]
    for T in trees:
     T_split=[[[1],[1]] for i in range(len(T))]
     T1=[[1,1] for i in range(len(T))]
     for i in range(len(T)):
         T_split[i][0], T_split[i][1]=re.split( ',|\:',T[i][0]), re.split( ',|\:',T[i][1])
         T1[i][0], T1[i][1]=T_split[i][0][0], T_split[i][1][0]
     tree_edges=[]
     for i in range(len(T)):
         tree_edges.append((T1[i][0], T1[i][1]))
     tree_vertices=[]
     tree_labelofvertices=[]
     for i in range(len(T)):
         if T1[i][0] not in tree_vertices:
            tree_vertices.append(T1[i][0])
            tree_labelofvertices.append(T_split[i][0][1:])
         if T1[i][1] not in tree_vertices:
            tree_vertices.append(T1[i][1])
            tree_labelofvertices.append(T_split[i][1][1:])
     S0=nx.Graph(tree_edges)
     spl=nx.all_pairs_shortest_path_length(S0)
     dspl={x[0]:x[1] for x in spl}
     P=[]
     for e in  tree_edges:
        L_A_1_0=[]
        L_A_1_1=[]
        for i in range(len(tree_vertices)):
          if dspl[e[0]][tree_vertices[i]]<dspl[e[1]][tree_vertices[i]] and dspl[e[0]][tree_vertices[i]]<k+1:
            for a in tree_labelofvertices[i]:
                      L_A_1_1.append(a)
          if dspl[e[1]][tree_vertices[i]]<dspl[e[0]][tree_vertices[i]] and dspl[e[1]][tree_vertices[i]]<k+1:
            for a in tree_labelofvertices[i]:
                      L_A_1_0.append(a)
        P.append([sorted(L_A_1_0), sorted(L_A_1_1)])  
     P_Total.append(P) 
    return(P_Total)
def getkRFmeasure_rooted(P_Total):
 d_Total=[]
 for i in range(len(P_Total)):
  d=[]
  P_Supp=[]
  for p in P_Total[i]:
    if p not in P_Supp:
       P_Supp.append(p)
  for j in range(len(P_Total)):
     d_k=len(P_Total[i])+len(P_Total[j])
     for p in P_Supp:
          if P_Total[i].count(p)> P_Total[j].count(p):
              d_k=d_k-2*(P_Total[j].count(p))
          else:
              d_k=d_k-2*(P_Total[i].count(p))
     d.append(d_k)
  d_Total.append(d)
 return(d_Total)

def getkRFmeasure_unrooted(P_Total):
 d_Total=[]
 for i in range(len(P_Total)):
  d=[]
  P_Supp=[]
  for p in P_Total[i]:
    if p not in P_Supp and [p[1],p[0]] not in P_Supp:
       P_Supp.append(p)
  for j in range(len(P_Total)):
     d_k=len(P_Total[i])+len(P_Total[j])
     for p in P_Supp:
       if P_Total[i].count(p)+P_Total[i].count([p[1], p[0]])> (P_Total[j].count(p)+ P_Total[j].count([p[1],p[0]])):
        d_k=d_k-2*(P_Total[j].count(p)+P_Total[j].count([p[1],p[0]]))
       else:
        d_k=d_k-2*(P_Total[i].count(p)+P_Total[i].count([p[1], p[0]]))
     d.append(d_k)
  d_Total.append(d)
 return(d_Total)

