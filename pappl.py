# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 22:57:38 2017

@author: Jules
"""

import sys
import os
from PyQt5 import QtWidgets
from py2cytoscape.data.cyrest_client import CyRestClient
import psutil
import networkx as nx

file_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(file_dir)

import interface

global dir_path

dir_path = os.path.dirname(os.path.realpath(__file__))


class Pappl(QtWidgets.QWidget, interface.Ui_Form):
    
    fname = ""
    grapheLoc=[]
    
    def __init__(self):
        
        
        super(Pappl, self).__init__()
        self.setupUi(self)
        self.connectActions()

    def connectActions(self):
        self.load.clicked.connect(self.loading)
        self.load_2.clicked.connect(self.loading)
        self.load_3.clicked.connect(self.loading)
        self.launch.clicked.connect(self.lancement)
        self.display.clicked.connect(self.affichage)
        self.display.setEnabled(False)
        self.reduc.clicked.connect(self.reduction)
        self.reduc.setEnabled(False)
        self.color.clicked.connect(self.colorations)
        self.color.setEnabled(False)
        
    def alerte(a):
        msglabel = QtWidgets.QLabel("Attention Cytoscape.exe n'est pas lancé ! \nVeuillez lancer l'application avant d'afficher un graphe.")
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Attention")
        ok = QtWidgets.QPushButton('OK', dialog)
        ok.clicked.connect(dialog.accept)
        ok.setDefault(True)
        dialog.layout = QtWidgets.QGridLayout(dialog)
        dialog.layout.addWidget(msglabel, 0, 0, 1, 3)
        dialog.layout.addWidget(ok, 1, 1)
        dialog.exec_()
    
    def isRunning(s):
        for pid in psutil.pids():
            p=psutil.Process(pid)
            if p.name()=="Cytoscape.exe":
                return True
        return False
    
    def loading(self):
        nom=QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', dir_path+"\Graphes", '*.sif')
        if (len(nom[0])>0):
            self.grapheLoc.append(nom[0])
            self.graph.addItem(os.path.basename(str(nom[0])))
            self.graph_2.addItem(os.path.basename(str(nom[0])))
            self.graph_3.addItem(os.path.basename(str(nom[0])))
            self.display.setEnabled(True)
            self.reduc.setEnabled(True)
            self.color.setEnabled(True)
    
    def reduction(self):
        self.fname = self.graph_2.currentItem().text()
        l=len(self.grapheLoc[self.graph.currentRow()])
        reduced=self.grapheLoc[self.graph.currentRow()][:l-4]+"-reduced.sif"
        self.compaction(self.grapheLoc[self.graph.currentRow()],self.grapheLoc[self.graph.currentRow()][:l-4]+"-reduced.sif", self.grapheLoc[self.graph.currentRow()][:l-4]+"-hash.txt", self.grapheLoc[self.graph.currentRow()][:l-4]+"-logic.txt")
        self.grapheLoc.append(reduced)
        self.graph.addItem(os.path.basename(str(reduced)))

    def colorations(self):
        nbColor=0 # possibilite de changer le nombre de reponse:  0 -> all answers n -> n answers
        self.fname = self.graph_3.currentItem().text()
        input=os.path.splitext(self.fname)[0]+"-logic.txt"
        output=dir_path+"\ASPout.txt"
        command=dir_path+"\clingo.exe " +str(nbColor)+" "+dir_path +"\optimizationComponent.lp "+input+" --opt-mode=optN --enum-mode=cautious --quiet=1 > "+ os.path.splitext(input)[0] +"-colorations.txt"
        os.system(command)
            
    def lancement(self):
        os.startfile(r'C:\Program Files\Cytoscape_v3.5.1\Cytoscape.exe')
    
    def affichage(self):
        if not self.isRunning():
            self.alerte()
        else:
            cy = CyRestClient()
        
            style1 = cy.style.create('sample_style1')

            new_defaults = {
                    
            # Node defaults
            'NODE_FILL_COLOR': '#ff5500',
            'NODE_SIZE': 20,
            'NODE_BORDER_WIDTH': 0,
            'NODE_TRANSPARENCY': 120,
            'NODE_LABEL_COLOR': 'white',
            
            # Edge defaults
            'EDGE_WIDTH': 3,
            'EDGE_STROKE_UNSELECTED_PAINT': '#aaaaaa',
            #'EDGE_LINE_TYPE': 'LONG_DASH',
            'EDGE_TRANSPARENCY': 120,
            
            
            # Network defaults
            'NETWORK_BACKGROUND_PAINT': 'white'
            }
            
            # Update
            style1.update_defaults(new_defaults)
            
            kv_pair = {
                '-1': 'T',
                '1': 'Arrow'
            }
            style1.create_discrete_mapping(column='interaction', 
                                        col_type='String', vp='EDGE_SOURCE_ARROW_SHAPE', mappings=kv_pair)
            
            self.fname = self.graph.currentItem().text()
            net1 = cy.network.create_from(self.grapheLoc[self.graph.currentRow()])
            cy.style.apply(style1,net1)

    def InversionTuple(self,node):
        Dico={}
        Dico["+"]="-"
        Dico["-"]="+"
        tupleInverse=""
        for sousTuple in node.split(","):
            #print(sousTuple)
            sousNode=sousTuple.split(" ")[0]
            sousSigne=sousTuple.split(" ")[1]
            #print(sousNode)
        #    print(sousSign
            tupleInverse=tupleInverse+","+sousNode+" "+Dico[sousSigne]    
        tupleInverse=(tupleInverse[1:len(tupleInverse)+1])
        return tupleInverse
    
    
    
    # Renvoie le nom du tuple fusionnant les prÃ©dÃ©cesseurs fusionnables (en prenant en compte le type d'arc)
    def FusionTuples(self,PredecesseursFusionnables,node,G):
        nouveauTuple=""
        for sousTuple in PredecesseursFusionnables:
            #print(sousTuple)
            tupleCalcule=sousTuple
            arc=G[sousTuple][node][0]['edge_type']
            if(arc == "-1"):
    #            print("inversion")
                tupleCalcule=self.InversionTuple(tupleCalcule)
                
            nouveauTuple=nouveauTuple+","+tupleCalcule
        nouveauTuple=(nouveauTuple[1:len(nouveauTuple)+1])
        return(nouveauTuple)     
    
    
    
    # Renvoie la liste des prÃ©dÃ©cesseurs qui peuvent fusionner
    def IdentificationPredecessorsFusionnables(self,G,ListePredecesseurs,Compacte):
        fusionnable=[]
        for node in ListePredecesseurs:
            listeSuccesseurs=G.successors(node)        
            listePredecessors=G.predecessors(node)
            if((len(listeSuccesseurs)==1) and (len(listePredecessors)==0) and (len(G[node][listeSuccesseurs[0]])==1) and (node not in Compacte) and (listeSuccesseurs[0] not in Compacte) ):
                fusionnable.append(node)
        return(fusionnable)
    
    
    # Renvoie false si 
        # la target a un arc vers la source de signe diffÃ©rent
    def FusionPossible(self,source,target, G, arc):
        resultat=True
        listeTarget=G.successors(target)
        # Parcours de successeurs de la cible
        if(source in listeTarget):
            for edge in G[target][source]:
                if(G[target][source][edge]['edge_type'] != arc):
                    return False
    
        return True
    
    def FusionNodes(self,graphe,dico,inversionArc):
        # CrÃ©er un nouveau graphe H
        H=nx.MultiDiGraph()
        ListeArcs=[]
        inversion={}
        inversion["1"]="-1"
        inversion["-1"]="1"
        # Pour chaque noeud du graphe
        for node in graphe.nodes():
            H.add_node(dico[node])
        # Pour chaque arc du graphe G
        for edges in graphe.edges():
            #print(edges)
            source=edges[0]
            target=edges[1]
            #print("ci")
            for edge in graphe[source][target]:
                #print(graphe[source][target][edge])
                arc=graphe[source][target][edge]['edge_type']
                if(source in inversionArc):
                    arc=inversion[arc]
                    #print(dico[source]+" => "+str(arc)+" => "+dico[target])
                edge=dico[source]+dico[target]+str(arc)
                #print(edge)
                # Si l'arc n'existe pas encore
                if(edge not in ListeArcs):
                    #print("non existant")
                    ListeArcs.append(edge)
                    # Ajouter un arc en mappant les noeud du dico
                    H.add_edge(dico[source],dico[target],edge_type=arc)
        # Renvoyer nouveauGraphe
        return(H)
    
    
    # Renvoie le tuple avec les signes inversÃ©s
    def inversionTuple(self,tuple):
        inversion={}
        inversion["+"]="-"
        inversion["-"]="+"
        TupleInverse=""
        for sousTuple in tuple.split(","):
            node=sousTuple.split(" ")[0]
            signe=inversion[sousTuple.split(" ")[1]]
            TupleInverse=TupleInverse+","+node+" "+signe
        # Enlever l'entÃªte
        TupleInverse=TupleInverse[1:len(TupleInverse)+1]
        #print(TupleInverse)
        return(TupleInverse)
            
    
    # Renvoie le signe du noeud du tuple connectant le noeud au tuple initialement
    def ArcOriginel(self,TuplePred,noeudSource,grapheOriginel):
        noeudTarget=noeudSource.split(" ")[0]+" +"
        # Pour chaque noeud du Tuple    
        for sousTuple in TuplePred.split(","):
            node=sousTuple.split(" ")[0]+" +"
            signe=sousTuple.split(" ")[1]
            if(grapheOriginel.has_edge(node,noeudTarget)):
                return(signe)
            # S'il existe un arc entre ce noeud et le noeudSource
                # Renvoyer signe
    
    # Fonction de generation des Tuples
    def generationTuple(self,predecesseur, noeudSource, arc,grapheOriginel):
        #print("Fusion de "+predecesseur+" avec "+noeudSource)
        if(arc=="1"):
            arc="+"
        elif(arc=="-1"):
            arc="-"
        else:
            print("erreur d'arc : "+str(arc))
        if(arc=="-"):
            # Noeud source inverse
            #print("inversion")
            noeudSource=self.inversionTuple(noeudSource)
        # Gestion des cas de doubles inhibition
        SigneLastNode=self.ArcOriginel(predecesseur,noeudSource,grapheOriginel)
        #print(SigneLastNode)
        #if(SigneLastNode=="-"):
            #print("avant : "+noeudSource)
            #noeudSource=inversionTuple(noeudSource)
            #print("apres : "+noeudSource)
        nouveauTuple=predecesseur+","+noeudSource
        return(nouveauTuple)

    def compaction(self,input,out1,out2,out3):
        file=open(input,"r")
        data=file.readlines()
        
        #print(data) 
        G=nx.MultiDiGraph()
        GOrigine=nx.MultiDiGraph()
        #print(data)
        separateur="\t"
        node_type={}
        for row in data:
            if (len(row.split(separateur)) == 3):
                sourceOrigine=row.split(separateur)[0]
                source=row.split(separateur)[0]+" +"
                modele=row.split(separateur)[1]
                targetOrigine=row.split(separateur)[2].split("\n")[0].split("\r")[0]
                target=row.split(separateur)[2].split("\n")[0].split("\r")[0]+" +"
                #G.add_edge(source,target,edge_type=str(modele))
                if(modele=="inhibitor" or modele=="-1"):
                    G.add_edge(source,target,edge_type="-1")
                    GOrigine.add_edge(sourceOrigine,targetOrigine,edge_type="-1")
                else:
                    G.add_edge(source,target,edge_type="1")
                    GOrigine.add_edge(sourceOrigine,targetOrigine,edge_type="1")
                
        #print("graphe initial de "+str(len(G.nodes()))+" nodes")
        #print("graphe initial de "+str(len(G.edges()))+" arcs")
        Copie=G.copy()
        nbreTuples=len(G.nodes())
        nbreArcs=len(G.edges())
        nouveauNbreTuples=0
        nouveauNbreArcs=0
        
        NxNombreTuplesGlobal=0
        NombreTuplesGlobal=nbreTuples
        NxNombreArcsGlobal=0
        NombreArcsGlobal=len(G.edges())
        listeIsole=[]
        
        print("graph with "+str(len(G.nodes()))+" nodes and "+str(len(G.edges()))+" edges")
        while(NxNombreTuplesGlobal!=NombreTuplesGlobal or NombreArcsGlobal!=NxNombreArcsGlobal):
            #print("cycle "+str(NombreTuplesGlobal)) 
            NxNombreTuplesGlobal=NombreTuplesGlobal
            NxNombreArcsGlobal=NombreArcsGlobal
            # REDUCTION SUR LA COHERENCE
            suppression=[]
            # Tant que le nbre de Tuples varie
            while(nbreTuples!=nouveauNbreTuples):
                nbreTuples=nouveauNbreTuples
                # Reinitialisation des fusions
                Fusion=[]
                Dico={}
                InversionArc=[]
                for node in G.nodes():
                    Dico[node]=node
                # Pour chaque Noeud
                for node in G.nodes():
                
                    predecesseurs=G.predecessors(node)
                    #print (predecesseurs)
                    # Si nbre Predecesseur == 1 ET predec ne fusionne pas ET node ne fusionne pas
                    if(len(predecesseurs)==1 and predecesseurs[0] not in Fusion and node not in Fusion and len(G[predecesseurs[0]][node])==1 and self.FusionPossible(predecesseurs[0],node, G, G[predecesseurs[0]][node][0]['edge_type'])):
                    
                        #print(node+ " fusion avec "+predecesseurs[0])
                        # Si le pred et noeud partagent 2 arcs diffÃ©rent
                        #print(node+" avec "+predecesseurs[0])
                        Fusion.append(node)
                        Fusion.append(predecesseurs[0])
                        #print(G[predecesseurs[0]][node])
                        NouveauTuple=self.generationTuple(predecesseurs[0], node,G[predecesseurs[0]][node][0]['edge_type'],Copie)
                        Dico[node]=NouveauTuple
                        Dico[predecesseurs[0]]=NouveauTuple
                        if(G[predecesseurs[0]][node][0]['edge_type']=="-1"):
                            InversionArc.append(node)
                        # Fusionner(noeud, pred, arc)
                # Mise Ã  jour du nbre de Tuples    
                G=self.FusionNodes(G,Dico,InversionArc)
            
                G.remove_edges_from(G.selfloop_edges())
                nouveauNbreTuples=len(G.nodes())
        
            
            #print("reduction par perfection")
            suppression=[]
            reduction=False
            rename={}
            # RÃ©initialiser la liste des noeuds Ã  compacter
            Compacte=[]
            # Pour chaque noeud
            for node in G.nodes():
                
                rename[node]=node
                # rÃ©cupÃ©rer liste prÃ©decesseurs
                ListePredecesseurs=G.predecessors(node)
                PredecesseursFusionnables=self.IdentificationPredecessorsFusionnables(G,ListePredecesseurs,Compacte)
                
                # Si plus d'un prÃ©dÃ©cesseur fusionnable
                if(len(PredecesseursFusionnables)>1):
                    # FUsion de ces noeuds
                        # CrÃ©er un nom de tuple commun et mettre en dico rename
                        reduction=True
                        NouveauTuple=self.FusionTuples(PredecesseursFusionnables,node,G)
                        
                        G.add_edge(NouveauTuple,node,edge_type="1")
                        # Stocker les autres noeud en suppression
                        for sousNode in PredecesseursFusionnables:
                            suppression.append(sousNode)
            G.remove_nodes_from(suppression)
        
            Copie=G.copy()
            nbreTuples=len(G.nodes())
            nbreArcs=len(G.edges())
            nouveauNbreTuples=0
            nouveauNbreArcs=0
        
            nbreNoeudsCycle=0
            NxnbreNoeudsReduction=nbreTuples
            listeConsistent=[]
        
        
            while(nbreNoeudsCycle!=NxnbreNoeudsReduction):
                nbreNoeudsCycle=len(G.nodes())
                suppression=[]
                rename={}
                # RÃ©initialiser la liste des noeuds Ã  compacter
                Compacte=[]
                # Pour chaque noeud
                for node in G.nodes():
                    rename[node]=node
                for node in G.nodes():
                    successeur=G.successors(node)
                    predecesseur=G.predecessors(node)
                    # Si noeud sans predecesseur, 1 successeur et un seul signe entre les 2
                    if(len(successeur)==1 and len(predecesseur)==0 and len(G[node][successeur[0]])==1):
                        tete=successeur[0].split(",")[0]
                        if(tete not in listeConsistent):
                            listeConsistent.append(tete)
                        suppression.append(node)
                        nouveauTuple=node
                        # Si arc inhibiteur => Inversion du tuple
                        if(G[node][successeur[0]][0]['edge_type']=="-1"):
                            nouveauTuple=self.InversionTuple(nouveauTuple)
                
                        rename[successeur[0]]=rename[successeur[0]]+","+nouveauTuple
                G.remove_nodes_from(suppression)
                NxnbreNoeudsReduction=len(G.nodes())
                G=nx.relabel_nodes(G,rename)
                listeConsistent
                
            DicoNodes={}
            DicoInverse={}
            nbreNode=0
            for node in G.nodes(): 
                DicoInverse[node]="node"+str(nbreNode)
                DicoNodes[DicoInverse[node]]=node
                nbreNode=nbreNode+1
                
            Copie=nx.MultiDiGraph()
            Copie.add_nodes_from(G.nodes())
            #print("reduction des arcs")
            for edge in G.edges():
                poidsActivation=0
                poidsInhibition=0
                source=edge[0]
                target=edge[1]
                if(len(source.split("\"")) > 1 ):
                    source=source.split("\"")[1]
                if(len(target.split("\"")) > 1 ):
                    target=target.split("\"")[1]
                for sousTuple1 in source.split(","):
                    # Pour chaque sousNoeud de tuple2
                    for sousTuple2 in target.split(","):
                        node1=sousTuple1.split(" ")[0]
                        signeSource=sousTuple1.split(" ")[1]
                        #print(sousTuple1+ " to "+node1+" "+signeSource)
                        node2=sousTuple2.split(" ")[0]
                        if(GOrigine.has_edge(node1,node2)):
                            
                            for edgeOrigine in GOrigine[node1][node2]:
                                arc=(GOrigine[node1][node2][edgeOrigine]['edge_type'])
                            #    print(node1+" to "+node2+" "+arc)
                                if(arc == "1"):
                                    if(signeSource=="+"):
                                        poidsActivation=poidsActivation+1
                                    else:
                                        poidsInhibition=poidsInhibition+1
                                elif(arc=="-1"):
                                    if(signeSource=="+"):
                                        poidsInhibition=poidsInhibition+1
                                    else:
                                        poidsActivation=poidsActivation+1
        
                poidsMin=min(poidsActivation,poidsInhibition)  
                retour=True
        #        poidsMin=0 
                if(poidsActivation-poidsMin >0):
                    Copie.add_edge(source,target,edge_type="1")  
                if(poidsInhibition-poidsMin >0):
                    Copie.add_edge(source,target,edge_type="-1") 
                # Cas isolement d'un arc 
                if(poidsActivation==poidsInhibition and poidsActivation !=0):
                    # Stocker tuple pour prÃ©ciser target : consistent + imperfect
                    tete=edge[1].split(",")[0]
                    if(tete not in listeIsole):
                        listeIsole.append(tete)
        
        #    print(Copie.edges())
        #    print(G.edges())
            G=Copie
        
            nouveauNbreTuples=len(G.nodes())
            nouveauNbreArcs=len(G.edges())
            NombreArcsGlobal=nouveauNbreArcs
            NombreTuplesGlobal=nouveauNbreTuples
            print("Reduction to "+str(len(G.nodes()))+" nodes and "+str(len(G.edges()))+" edges")
        
        # Listing des arcs
        listeArcs=[]
        for i in G.edges():
            #print(i)
            source=i[0]
            target=i[1]
            for arc in (G[source][target]):
                edge="\""+source+"\""+"\t"+str(G[source][target][arc]['edge_type'])+"\t"+"\""+target+"\""
                if(edge not in listeArcs):
                    listeArcs.append(edge)
            if(source==target):
                print("Frappe "+source+" => "+str(G[source][target][arc]['edge_type']))
        
        
        file=open(out1,"w") #ecriture format sif
        for i in listeArcs:
            file.write(i+"\n")
        #    print(G[
        file.close()
        
        
        # Ecriture du Dictionnaire
        file=open(out2,"w")
        for node in G.nodes():
            file.write("\""+node+"\" : "+DicoInverse[node]+"\n")
        
        file.close()
        
        
        
        
        fileOutput=open(out3,"w")
        # Ecriture du graphe Mis en forme
        NodeUtilise=G.nodes()
        for edge in G.edges():
            poidsActivation=0
            poidsInhibition=0
            source=edge[0]
            target=edge[1]
            if(len(source.split("\"")) > 1 ):
                source=source.split("\"")[1]
            if(len(target.split("\"")) > 1 ):
                    target=target.split("\"")[1]
            for sousTuple1 in source.split(","):
                # Pour chaque sousNoeud de tuple2
                    for sousTuple2 in target.split(","):
                        node1=sousTuple1.split(" ")[0]
                    signeSource=sousTuple1.split(" ")[1]
                    #print(sousTuple1+ " to "+node1+" "+signeSource)
                    node2=sousTuple2.split(" ")[0]
                    # print("test "+node1+" to "+node2)
                    if(GOrigine.has_edge(node1,node2)):
                        for edgeOrigine in GOrigine[node1][node2]:
                            arc=(GOrigine[node1][node2][edgeOrigine]['edge_type'])
                        #    print(node1+" to "+node2+" "+arc)
                            if(arc == "1"):
                                if(signeSource=="+"):
                                    poidsActivation=poidsActivation+1
                                else:
                                    poidsInhibition=poidsInhibition+1
                            elif(arc=="-1"):
                                if(signeSource=="+"):
                                    poidsInhibition=poidsInhibition+1
                                else:
                                    poidsActivation=poidsActivation+1
            poidsMin=min(poidsActivation,poidsInhibition)
            if(poidsActivation-poidsMin!=0):
                if(edge[0] in NodeUtilise):
                    NodeUtilise.remove(edge[0])
                if(edge[1] in NodeUtilise):
                    NodeUtilise.remove(edge[1])
        
        
            #print("("+source+ ","+target+",1,"+str(poidsActivation)+").")
                    fileOutput.write("edge("+DicoInverse[edge[0]]+ ","+DicoInverse[edge[1]]+",1,"+str(poidsActivation-poidsMin)+").\n")
            if(poidsInhibition-poidsMin!=0):
                if(edge[0] in NodeUtilise):
                    NodeUtilise.remove(edge[0])
                if(edge[1] in NodeUtilise):
                    NodeUtilise.remove(edge[1])
                #print("("+source+ ","+target+",-1,"+str(poidsInhibition)+").")
                fileOutput.write("edge("+DicoInverse[edge[0]]+ ","+DicoInverse[edge[1]]+",-1,"+str(poidsInhibition-poidsMin)+").\n")
        
            # Checker si besoin d'afficher les composants prÃ©-identifiÃ©s : En liste "NodeUtilise"    
        
            
        # Recuperation des cibles imparfaites
        for component in listeIsole:
            #print(component)
            for node in G.nodes():
                if(node.find(component)!=-1):
                    fileOutput.write("imperfectcoloring("+DicoInverse[node]+").")
                    fileOutput.write("consistentTarget("+DicoInverse[node]+").\n")                          
        
        
        
        
        # Recuperation des cibles cohÃ©rentes
        for component in listeConsistent:
            #print(component)
            for node in G.nodes():
                if(node.find(component)!=-1):    
                    fileOutput.write("consistentTarget("+DicoInverse[node]+").\n")                          
        
        
        
        
        
        
        fileOutput.close()
        
    def main(self):
        self.show()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pappl = Pappl()
    pappl.main()
    sys.exit(app.exec_())
        