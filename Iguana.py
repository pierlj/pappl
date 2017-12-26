# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 22:57:38 2017

@author: Jules Paris et Pierre Le Jeune
"""

#importation des modules nécessaires à l'application 
import sys
import os
from PyQt5 import QtWidgets
from py2cytoscape.data.cyrest_client import CyRestClient
import psutil
import networkx as nx


#import du fichier génrant l'interface graphique
import interface_ui

global dir_path

dir_path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(dir_path)

#classe principale permettant de lancer l'application
class Pappl(QtWidgets.QWidget, interface_ui.Ui_Form):
    
    fname = ""
    grapheLoc=[]
    grapheLoc2=[]
    table=[]
    
    def __init__(self):
        super(Pappl, self).__init__()
        self.setupUi(self)
        self.connectActions()
        
    #fonction permettant de lier les boutons de l'interface avec les fonctions correspondantes
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
        # self.color.setEnabled(False)
        self.color_1.clicked.connect(self.afficheColor)
        # self.color_1.setEnabled(False)
        self.nCompo.clicked.connect(self.nComposantesAux)
        # self.nCompo.setEnabled(False)"
        
    #ouverture d'une fenetre d'erreur lorsque cytoscape n'est pas lancé    
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
    
    #affichage d'un message lorsque la réduction est terminée
    def doneR(a):
        msglabel = QtWidgets.QLabel("\t\tLa réduction est finie.\t\t")
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Fini")
        ok = QtWidgets.QPushButton('OK', dialog)
        ok.clicked.connect(dialog.accept)
        ok.setDefault(True)
        dialog.layout = QtWidgets.QGridLayout(dialog)
        dialog.layout.addWidget(msglabel, 0, 0, 1, 3)
        dialog.layout.addWidget(ok, 1, 1)
        dialog.exec_()
    
    #affichage d'un message lorsque l'identification des colorations est terminée
    def doneI(a):
        msglabel = QtWidgets.QLabel("\t\tL'identification des composants est finie.\t\t")
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Fini")
        ok = QtWidgets.QPushButton('OK', dialog)
        ok.clicked.connect(dialog.accept)
        ok.setDefault(True)
        dialog.layout = QtWidgets.QGridLayout(dialog)
        dialog.layout.addWidget(msglabel, 0, 0, 1, 3)
        dialog.layout.addWidget(ok, 1, 1)
        dialog.exec_()
    
    #affichage d'un message lorsque la coloration du graphe est terminée   
    def doneC(a):
        msglabel = QtWidgets.QLabel("\t\tLa coloration est finie.\t\t")
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Fini")
        ok = QtWidgets.QPushButton('OK', dialog)
        ok.clicked.connect(dialog.accept)
        ok.setDefault(True)
        dialog.layout = QtWidgets.QGridLayout(dialog)
        dialog.layout.addWidget(msglabel, 0, 0, 1, 3)
        dialog.layout.addWidget(ok, 1, 1)
        dialog.exec_()
    
    #affichage d'un message lorsque l'exportation des composants est terminée
    def doneN(a):
        msglabel = QtWidgets.QLabel("\t\tL'exportation des composants est terminée.\t\t")
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Fini")
        ok = QtWidgets.QPushButton('OK', dialog)
        ok.clicked.connect(dialog.accept)
        ok.setDefault(True)
        dialog.layout = QtWidgets.QGridLayout(dialog)
        dialog.layout.addWidget(msglabel, 0, 0, 1, 3)
        dialog.layout.addWidget(ok, 1, 1)
        dialog.exec_()
    
    #affichage d'un message lorsque l'on veut effectuer une tâche sans que les fichiers nécessaires soient présents dans le répertoire correspondant
    def pb(a):
        msglabel = QtWidgets.QLabel("Attention : il manque les fichiers necéssaires pour effectuer cette opération.\nMerci d'effectuer d'abord la réduction du graphe.")
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Attention")
        ok = QtWidgets.QPushButton('OK', dialog)
        ok.clicked.connect(dialog.accept)
        ok.setDefault(True)
        dialog.layout = QtWidgets.QGridLayout(dialog)
        dialog.layout.addWidget(msglabel, 0, 0, 1, 3)
        dialog.layout.addWidget(ok, 1, 1)
        dialog.exec_()
    
    #fonction determinant si Cytoscape est lancé
    def isRunning(s):
        for pid in psutil.pids():
            p=psutil.Process(pid)
            if p.name()=="Cytoscape.exe":
                return True
        return False
    
    #chargement des graphes en ouvrant un explorateur de fichier
    def loading(self):
        nom=QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', "C:\\", '*.sif')
        if (len(nom[0])>0):
            self.grapheLoc.append(nom[0])
            self.grapheLoc2.append(nom[0])
            self.graph.addItem(os.path.basename(str(nom[0])))
            self.graph_2.addItem(os.path.basename(str(nom[0])))
            self.graph_3.addItem(os.path.basename(str(nom[0])))
            self.display.setEnabled(True)
            self.reduc.setEnabled(True)
            self.color.setEnabled(True)
            
    #lancement de la réduction, appel de l'algorithme Iggy-poc avec les bons fichiers
    def reduction(self):
        self.fname = self.graph_2.currentItem().text()
        l=len(self.grapheLoc2[self.graph_2.currentRow()])
        reduced=self.grapheLoc2[self.graph_2.currentRow()][:l-4]+"-reduced.sif"
        self.compaction(self.grapheLoc2[self.graph_2.currentRow()],self.grapheLoc2[self.graph_2.currentRow()][:l-4]+"-reduced.sif", self.grapheLoc2[self.graph_2.currentRow()][:l-4]+"-reduced-hash.txt", self.grapheLoc2[self.graph_2.currentRow()][:l-4]+"-reduced-logic.txt")
        self.grapheLoc.append(reduced)
        self.graph.addItem(os.path.basename(str(reduced)))
        self.doneR()

    #lancement, via commande dos du script asp avec clingo
    #dépend des options sélectionnées dans l'application (temps d'exécution)
    def colorations(self):
        nbColor=0 # possibilite de changer le nombre de reponse:  0 -> all answers n -> n answers
        name = self.grapheLoc2[self.graph_3.currentRow()]
        input=os.path.splitext(name)[0]+"-reduced-logic.txt"
        output=dir_path+"\ASPout.txt"
        #option apres input : --opt-mode=optN --enum-mode=cautious --quiet=1
        print(input)
        if (self.time.value()==0):
            command=dir_path+"\clingo.exe " +str(nbColor)+" "+dir_path +"\optimizationComponent.lp "+input+" --opt-mode=optN --enum-mode=cautious --parallel-mode=2  > "+ os.path.splitext(input)[0] +"-colorations.txt"
        else:
            command=dir_path+"\clingo.exe " +str(nbColor)+" "+dir_path +"\optimizationComponent.lp "+input+" --time-limit="+str(self.time.value())+" --opt-mode=optN --enum-mode=cautious > "+ os.path.splitext(input)[0] +"-colorations.txt"
        print(command)
    
        os.system(command)
        try:
            self.processASP(os.path.splitext(name)[0]+"-reduced-logic-colorations.txt")
            self.identificationColor(os.path.splitext(name)[0]+"-reduced-logic-colorations-processed.txt")
            self.doneI()
        except (IndexError, EnvironmentError):
            self.pb()
    
        #self.processASP(os.path.splitext(name)[0]+"-reduced-logic-colorations.txt")
        #self.identificationColor(os.path.splitext(name)[0]+"-reduced-logic-colorations-processed.txt")
        #self.doneI()
    #lancement de la fonction d'affichage        
    def afficheColor(self):
        self.colorGraphe(self.table)
    
        
    def nComposantesAux(self):
        self.nComposantes(self.table)
        self.doneN()
    
    
    #lancement de cytoscape --> si cytoscape n'est pas installé dans le bon répertoire, il y aura une erreur
    #Il faudrait proposer une option dans l'application pour donner le chemin d'accès de cytoscape et le changer ici. 
    def lancement(self):
        os.startfile(r'C:\Program Files\Cytoscape_v3.5.1\Cytoscape.exe')
    
    #affichage du graphe selectionné dans cytoscape
    def affichage(self):
        if not self.isRunning():
            self.alerte()
        else:
            cy = CyRestClient()
        
            style1 = cy.style.create('sample_style1')
            #feuille de style cytoscape
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
            
            self.fname = self.grapheLoc[self.graph.currentRow()]
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

    #fonction effectuant la réduction
    def compaction(self,input,out1,out2,out3):
        file=open(input,"r")
        data=file.readlines()
        file.close()
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
                #listeConsistent
                
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
        

    
    def InversionTupleID(self,tuple):
    
        signe=tuple.split(" ")[1]
        node=tuple.split(" ")[0]
        if(signe=="+"):
            return (node+" -")
        else:
            return(node+" +")
    
    def FusionTuplesID(self,node1,node2,signe):
        nouveauTuple=node1
        #print(node1)
        #print(node2)
        #print(signe)
        for sousTuple in node2.split(","):
            #print(sousTuple)
            tupleCalcule=sousTuple
            if(signe == -1):
                #print("inversion")
                tupleCalcule=self.InversionTupleID(tupleCalcule)
            
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
        
    def rechercheTupleID(self,G,node,tupleCourant,listeNodes,signe):
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
                # Calcul du signe l'Ã©lÃ©ment selon signe
                #print(signe)
                signe=signe*signeInteraction
            #print(voisin+" : "+str(signe)+" "+str(signeInteraction)+" from "+node)
                element=voisin
                # Si l'interaction est nÃ©gative
                #print("fusion :"+voisin+" : "+str(signe))
                tupleCourant=self.FusionTuplesID(tupleCourant,voisin,signe)
                # Relancer algo sur noeud ajoutÃ©
                tupleCourant=self.rechercheTupleID(G,voisin,tupleCourant,listeNodes,signe)
                
        return tupleCourant
    
    
    
    
    # Fonction effectuant l'identifcation des colorations
    def identificationColor(self,path):
        Dico={}
        DicoInverse={}
        name = self.grapheLoc2[self.graph_3.currentRow()]
        input=os.path.splitext(name)[0]+"-reduced-hash.txt"
        # Charger Dico des nodes
        
        file=open(input,'r')
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
        file=open(path,'r')
        data=file.readlines()
        file.close()
        # print(data) 
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
            # cas nÃ©gatif
            else:
                G.add_edge(source,target,edge_type=-1)
        
        
        
        listeTuples=[]
        
        listeNodes=[]
        
        #Identifier les noeuds hors graphe de corrÃ©lation : tuples simples ou non listÃ©s
        
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
                nouveauTuple=self.rechercheTupleID(G,node,nouveauTuple,listeNodes,1)
                listeTuples.append(nouveauTuple)
        
            
        # Affichage des tuples
        #for tuple in listeTuples:
        #	print(tuple) 
        file=open(os.path.splitext(self.grapheLoc2[self.graph_3.currentRow()])[0]+"-coloration-table.csv",'w')
        tableTuple=[]
        for i in range(len(listeTuples)):
            tuple=listeTuples[i]
            tuple=tuple.split(",")
            for node in tuple:
                if(node.split(" ")[1] == '-'):
                    tableTuple.append([node.split(" ")[0],i,-1])
                else:
                    tableTuple.append([node.split(" ")[0],i,1])
        
        self.table=tableTuple
        file.write("\"Node\", \"Coloration\", \"Signe\""+"\n")
        for tuple in tableTuple:
            file.write("\""+tuple[0]+"\", "+str(tuple[1])+", "+str(tuple[2])+"\n")
        file.close()
    
    #affichage des colorations
    def colorGraphe(self,tableTuple):
        if not self.isRunning():
            self.alerte()
        else:
            cy = CyRestClient()
            net1 = cy.network.create_from(self.grapheLoc2[self.graph_3.currentRow()])
            net1.create_node_column("composant", data_type='Integer',is_immutable=False)
            net1.create_node_column("signe",data_type='Integer',is_immutable=False)
            table=net1.get_node_table()
            nodeTable={}
            nodes=net1.get_nodes()
            for node in nodes:
                nodeTable[net1.get_node_value(node)['name']]=node
            
            
            
            for line in tableTuple:
            
                table.set_value(nodeTable[line[0]],"composant",line[1])
                table.set_value(nodeTable[line[0]],"signe",line[2])
                
            net1.update_node_table(table,network_key_col='name', data_key_col='name')
            style1 = cy.style.create('sample_style1')
        
            points = [{
            'value': '0.0',
            'lesser':'blue',
            'equal':'blue',
            'greater': 'blue'
            },{
            'value': '1.0',
            'lesser':'red',
            'equal':'red',
            'greater': 'red'
            }]
            
            points[1]["value"]=self.nbComposantes(tableTuple)-1
            style1.create_continuous_mapping(column='composant', col_type='Integer', vp='NODE_FILL_COLOR',points=points)
            cy.style.apply(style1,net1)
            cy.layout.apply(name='organic',network=net1)
            self.doneC()
    
    #fonction qui transforme la sortie du script ASP afin qu'il soit compréhensible pour le script d'identification
    def processASP(self,path):
        file=open(path,'r')
        lines=file.readlines()

        
        correle=self.lastAns(lines)
        correleSep=correle.split()
        file.close()
        name=os.path.splitext(path)[0]+"-processed"+os.path.splitext(path)[1]
        file=open(name,'w')
        for line in correleSep:
            file.write(line+"\n")
        file.close()

    #renvoie le nombre de composants obtenus
    def nbComposantes(self,table):
        nb=0
        for line in table:
            if (line[1]>nb):
                nb=line[1]
        return (nb+1)
    
    #renvoie la dernière réponse (optimum ou non) du script ASP    
    def lastAns(self,lines):
        res=0
        line=lines[0]
        for k in range(len(lines)):
            if( "Answer" in lines[k]):
                res=res+1
                line=lines[k+1]
        return line
    
    #extraction des n composants et export des fichiers correspondants
    def nComposantes(self,tableTuple):
        n=self.nbComposantes(tableTuple)
        listeComposante=[[] for _ in range(n)]
        for line in tableTuple:
            listeComposante[line[1]-1].append(line[0])
        file=open(self.grapheLoc2[self.graph_3.currentRow()],'r')
        base=file.readlines()
        file.close()
        graphesComposantes=[]
        for compo in listeComposante:
            current=[]
            if (len(compo)==1):
                current.append(compo[0])
            else:
                for line in base:
                    lineSliced=line[:-1]
                    edge=lineSliced.split("\t")
                    
                    if (edge[0] in compo and edge[2] in compo ):
                        current.append(line)
            graphesComposantes.append(current)
        name = self.grapheLoc2[self.graph_3.currentRow()]
        directory=os.path.dirname(name)+"//Composants_"+os.path.basename(os.path.splitext(name)[0])
        if not os.path.exists(directory):
            os.makedirs(directory)
        for i in range(len(graphesComposantes)):
            strOpen=directory+"//composant"+str(i+1)+".sif"
            file=open(strOpen,'w')
            for line in graphesComposantes[i]:
                file.write(line)
                file.write("\n")
        
    def main(self):
        self.show()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pappl = Pappl()
    pappl.main()
    sys.exit(app.exec_())
