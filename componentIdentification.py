# -*-coding:Latin-1 -*

import sys
import os
from PyQt4 import QtGui, QtCore
from py2cytoscape.data.cyrest_client import CyRestClient
import random
import psutil
import networkx as nx
import subprocess

global dir_path


def InversionTuple(tuple):

	signe=tuple.split(" ")[1]
	node=tuple.split(" ")[0]
	if(signe=="+"):
		return (node+" -")
	else:
		return(node+" +")

def FusionTuples(node1,node2,signe):
	nouveauTuple=node1
	#print(node1)
	#print(node2)
	#print(signe)
	for sousTuple in node2.split(","):
		#print(sousTuple)
		tupleCalcule=sousTuple
		if(signe == -1):
			#print("inversion")
			tupleCalcule=InversionTuple(tupleCalcule)
		
		#print(tupleCalcule)	
		nouveauTuple=nouveauTuple+","+tupleCalcule
	#nouveauTuple=(nouveauTuple[1:len(nouveauTuple)+1])
	#print(nouveauTuple)
	return(nouveauTuple) 	


# Renvoie a chaque fin d'appel un tuple contenant le nouveau noeud s'il est dans la liste
# Appel nouveauTuple=rechercheTuple(G,node,tupleCourant,listeNodes,signe):
	# G : graphe
	# Noeud : noeud en cours d'exploration
	# tupleCourange : tuple en cours de construction
	# ListeNodes : liste des noeuds
	# signe = signe de la correlation
	
def rechercheTuple(G,node,tupleCourant,listeNodes,signe):
	# Pour le noeud courant
	#print(node)
	signeInitial=signe
	listeVoisins=G.neighbors(node)
	for voisin in listeVoisins:
		signe=signeInitial
		if(voisin in listeNodes):	
			
			listeNodes.remove(voisin)
			#print(node+" "+voisin)
			signeInteraction=G[voisin][node]['edge_type']
			# Calcul du signe l'élément selon signe
			#print(signe)
			signe=signe*signeInteraction
		#	print(voisin+" : "+str(signe)+" "+str(signeInteraction)+" from "+node)
			element=voisin
			# Si l'interaction est négative
			#print("fusion :"+voisin+" : "+str(signe))
			tupleCourant=FusionTuples(tupleCourant,voisin,signe)
			# Relancer algo sur noeud ajouté
			tupleCourant=rechercheTuple(G,voisin,tupleCourant,listeNodes,signe)
			
	return tupleCourant




# Charger Dico des noeuds

Dico={}
DicoInverse={}

# Charger Dico des nodes
file=open("D:\\Documents\\Centrale\\Ei2\PAPPL\\App\\test-hash.txt",'r')
data=file.readlines()
file.close()

for i in data:
	#print(i)
	node=i.split(" : ")[0].split("\"")[1]
	#print(node)
	conversion=i.split(" : ")[1].split("\n")[0]
	#print(conversion)
	Dico[conversion]=node
	DicoInverse[node]=conversion

# Charger le graphe


# convertir le graphe en graphe networkX
file=open("D:\\Documents\\Centrale\\Ei2\PAPPL\\App\\test-logic-colorations-processed.txt",'r')
data=file.readlines()
file.close()
#print(data) 
G=nx.Graph()
	
# Pour chaque ligne :
for i in data:
	# Identifier source & target : convertir
	source=Dico[i.split("(")[1].split(",")[0]]
	target=Dico[i.split(",")[1].split(")")[0]]

	# Identifier le type de correlation : signe de l'arc
	# cas positif
	if(len(i.split("Positif"))==2):
		G.add_edge(source,target,edge_type=1)
	# cas négatif
	else:
		G.add_edge(source,target,edge_type=-1)



listeTuples=[]

listeNodes=[]

#Identifier les noeuds hors graphe de corrélation : tuples simples ou non listés

for i in DicoInverse.keys():
	if(i in G.nodes()):
		listeNodes.append(i)
	else:
		listeTuples.append(i)
		

# Pour chaque noeud :
	# Fonction recursive d'exploration : parametre : graphe, tuple actuel, 
while (len(listeNodes)!=0):
	for node in listeNodes:
		#print(node)
		nouveauTuple=node
		listeNodes.remove(node)
		# Appel fonction de recherche
		nouveauTuple=rechercheTuple(G,node,nouveauTuple,listeNodes,1)
		listeTuples.append(nouveauTuple)

	
# Affichage des tuples
#for tuple in listeTuples:
#	print(tuple) 

tableTuple=[]
for i in range(len(listeTuples)):
	tuple=listeTuples[i]
	tuple=tuple.split(",")
	for node in tuple:
		tableTuple.append([node.split(" ")[0],i])


cy = CyRestClient()
net1 = cy.network.create_from("D:\\Documents\\Centrale\\Ei2\\PAPPL\\App\\test.sif")
table=net1.get_node_table()
print(table)
net1.create_node_column("coloration", data_type='Integer',is_immutable=False)
nodes=net1.get_nodes()
for node in nodes:
	nodes.








