#!/usr/bin/env python
#A lancer depuis bin
import string, re, struct, sys, math, os
import subprocess, multiprocessing

nbcoeur = 4


grad = [1.e-10,1.e-9,1.e-8,1.e-7,1.e-6,1.e-5,1.e-4,1.e-3,1.e-2,0.1,1]
rho = [1e-5,1e-4,1.e-3,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14]

rep0  = 'res'
rep1i = 'rezo_PNM888_L160_R5_RHO='
rep2i = 'deltaV='

list=[ [rho[i],grad[j]] for i in range(len(rho)) for j in range(len(grad)) ]

def arboresdigitale(l):
    global rep0, rep1i, rep2i, list
    
    rep1 = rep1i + '%s' %list[l][0]
    param1 = math.log(0.6*list[l][0])
    rep2 = rep2i + '%s' %list[l][1]
    param2 = list[l][1]
    
    replanceur = os.getcwd()     # pwd
    absrep = os.path.join(replanceur,rep0,rep1,rep2)
    
    if os.path.isdir( absrep ):
        pass
    else:
        os.makedirs( absrep ) # creation du sous dossier ou on lance le process et si nécessaire de l'arborescence 
    
    cmd = 'sed -e s/POTEN/%s/g -e s/LNRHO/%s/g  PNP.pattern > %s/PNP.in_data' %(param2,param1,absrep)
    os.system(cmd)
    
    cmd = 'cp canaux_d_L.dat %s/' %absrep
    os.system(cmd)
    
    fich = open(absrep+'/renseignements', 'w')
    process = subprocess.Popen( ['time', 'nohup', './../../../solveur'] , cwd=absrep , stdout=fich ) #lance le process ds le repertoire cwd et redirige la sortie dans le fichier stdout

    fich.close()
    
    process.wait() #on attend que le processus se finisse


print '%s processus par groupe de %s sur %s coeurs logiques.'%(len(grad)*len(rho),nbcoeur,multiprocessing.cpu_count())




poule = multiprocessing.Pool(nbcoeur) #on se réserve un nbre de thread = à nbcoeur
poule.map_async( arboresdigitale , range(len(list)) ) #on lance len(list) fois la fonction arboresdigitale sur les thread reserves

poule.close() # on signifie que le pool n'aura pas de fonction supplementaire a prendre en charge 
poule.join() # on attend que ttes les fonctions aient terminé avant de quitter 














