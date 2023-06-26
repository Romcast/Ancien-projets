import random
import time
import datetime

def dico():
    """ dico() -> liste  génère la liste des mots du dictionnnaire"""
    fichier = open('/Romain/EduPython/dico.txt','r') #pour accéder au dictionnaire
    dictionnaire = fichier.readlines()
    fichier.close()
    mots_valides = [] #on filtre les mots du dictionnaire en enlevant tous ceux qui ont strictement plus de 9 lettres
    for i in range(len(dictionnaire)):
        dictionnaire[i] = dictionnaire[i].rstrip('\n')# on retire aussi les retours à la ligne afin d'avoir que les lettres des mots
        if len(dictionnaire[i]) <= 9:
            mots_valides.append(dictionnaire[i])
    return mots_valides

mots_valides = dico()

def resultat(tab):
    """ resultat(liste) -> Rien  Archive les résultats des deux joueurs"""
    d = datetime.datetime.now()
    date = d.isoformat() #pour avoir la date et l'heure en str
    nom = date[0:10] + " " + date[11:13] + 'h' + date[14:16]
    r = open(nom + '.txt','w')
    print("ouai")
    res = "Joueur 1: " + str(tab[0]) + " points\n" + "Joueur 2: " + str(tab[1]) + " points"
    r.write(res)
    r.close()


def lettres9():
    """ lettres9() -> liste  Génère une liste de 9 lettres avec minimum 4 voyelles"""
    voyelle = ["A","E","I","O","U","Y"]
    consonne = ["B","C","D","F","G","H","J","K","L","M","N","P","Q","R","S","T","V","W","X","Z"]
    lettres = []
    v = 0
    for i in range(9):
        if i >= 5 and v <= i-5:
            liste = voyelle
            l = liste[random.randint(0,5)]
        else:
            liste = voyelle + consonne
            l = liste[random.randint(0,25)]

        if l in voyelle:
            v+=1
        lettres.append(l)
    return lettres

def chiffres6():
    """ chiffre6() -> liste Pioche 6 chiffres parmi une liste prédéfinie :
        [1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,25,50,75,100] """
    c = []
    liste = [1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,25,50,75,100]
    for _ in range(6):
        i = random.randint(0,len(liste)-1)
        c.append(liste.pop(i))
    return c


def verif(l,m):
    """ Verif2(Liste,chaine) -> chaine   Vérifie si l'on peut former un mot donné avec une liste de lettres"""
    ll = l.copy()
    for lettre in m:
        if lettre in ll:
            ll.remove(lettre)
        else:
            return False
    return True


def recherche (l,mots,dif):
    """ recherche(Liste1,Liste2,entier) -> chaine de charactère
    Renvoie le plus long mot que l'on peut former parmi une liste avec une liste de lettres donnée,
    avec une certaine probabilité de vérifier chaque mot"""
    max = 0
    rep = ''
    for mot in mots:
        p = random.randint(1,1000)
        if p > dif:
            pass
        else:
            if len(mot) < max:
                pass
            elif verif(l,mot):
                if len(mot) == len(l):
                    return mot
                max = len(mot)
                rep = mot
    return rep



def verifd(mot,dico):
    """verif2(chaine,liste) -> booléen    Vérifie si un mot se trouve dans le dictionnaire"""
    return mot in dico



def possible(operation,c1,c2):
    """ possible(charactère,chaine1,chaine2) -> booléen     vérifie si une opération est possible"""
    if operation == "-":
        if eval(c1)>eval(c2):
            return True
        else:
            return False

    if operation == "/":
        if eval(c1)%eval(c2) == 0:
            return  True
        else:
            return False
    if operation == " ":
        return False
    return True



def calcul(l1,l2):
    """ calcul(liste1,liste2) -> (entier,chaine)    crée et calcule une combinaison linéaire et renvoie le couple du résultat et du chemin"""
    l = str(l1[0])
    for i in range(0,len(l2)):
        if possible(l2[i],l,str(l1[i+1])):
            l = "(" + l + ")" + l2[i] + str(l1[i+1])
        else:
            pass
    return (eval(l),l)

def comb(n,l):
    """ comb(entier,liste1) -> liste2   Renvoie l'ensemble des n-listes d'une liste"""
    t=[]
    if n == 1:
        return[[n] for n in l]
    for i in l:
        ll = l.copy()
        ll.remove(i)
        for c in comb(n-1,ll):
            t.append([i] + c)
    return t


def comb2(n,i):
    """comb(entier1,entier2) -> liste   Renvoie l'ensemble des listes de taille n dont chaque élément est un élément d'une liste i"""
    t=[]
    if n == 1:
        return [[n] for n in i]
    for tab in comb2(n-1,i):
        for operation in i:
            t.append([operation] + tab)
    return t

def compte(l,n,difficulté):
    """compte(liste,entier1) -> (entier2, chaine)    renvoie le calcul utilisant une fois chaque entier d'une liste qui permet
    d'obtenir un entier donné ou au moins l'entier le plus proche"""
    dif = 100000
    k = 0
    rep = (max(l), str(max(l))) # cas où aucune réponse n'est trouvé ( plutôt rare )
    for i in comb(len(l),l):
        for j in comb2(len(l)-1,["+","-","*","/"," "]):
            p = random.randint(1,1000)
            if p > difficulté:
                pass
            else:
                r = calcul(i,j)
                if abs(r[0]-n) == 0:
                    return r
                if abs(r[0]-n) < dif:
                    dif = abs(r[0]-n)
                    rep = r
    return rep


def verifc(l,comb):
    """ verifc(liste,chaine) -> booléen     vérifie si tous les nombres de la combinaison sont présents une seule fois dans la liste """
    ll = l.copy()
    n = ''
    for i in range(len(comb)+1):
        try:    # on vérifie si on prend bien un chiffre et on l'ajoute à l'autre
            int(comb[i])
            n += comb[i]
        except:     # dès qu'il n'y a plus de chiffres on vérifie si le nombre formé avec les chiffres est dans la liste
            try:
                int(n)
                if int(n) in ll:
                    ll.remove(int(n))
                else:
                    return False
                n = ''
            except:
                pass
    return True


def pointsl(rep1,rep2):
    """ pointsl(chaine1,chaine2) -> couple   Compare les deux réponses pour le coup de lettres
    renvoie un couple indiquant le nombre de points et à qui ils sont attribués:
    0 -> joueur 1 (opérateur)
    1 -> joueur 2 (bot)
    2 -> les deux """
    if len(rep1) > len(rep2):
        return (len(rep1),0)
    if len(rep2) > len(rep1):
        return (len(rep2),1)
    else:
        return (len(rep1),2)



def pointsc(rep1,rep2,n):
    """ pointsl(chaine1,chaine2) -> couple    Compare les deux réponses pour le coup de chiffres
    renvoie un couple indiquant le nombre de points et à qui ils sont attribués:
    0 -> joueur 1 (opérateur)
    1 -> joueur 2 (bot)
    2 -> les deux"""
    if abs(rep1[0]-n) == abs(rep2[0]-n):
        if rep1[0] == n:
            return (9, 2)
        else:
            return (6, 2)
    if abs(rep1[0] - n) > abs(rep2[0]-n):
        if rep2[0] == n:
            return (9, 1)
        else:
            return (6, 1)
    else:
        if rep1[0] == n:
            return (9, 0)
        else:
            return (6, 0)


def coup_de_chiffres(dif):
    """ coup_de_chiffres(entier) -> couple Réalise une manche de coup de chiffres avec un indice de difficulté entre 1 et 1000
    renvoie les points gagnés et le gagnant des points"""
    nombre = random.randint(100,999)
    print("Nombre à trouver:",nombre)
    liste_chiffres = chiffres6()
    rep2 = compte(liste_chiffres,nombre,dif)
    print(liste_chiffres)
    debut = time.time()
    try:
        r1 = input("IL FAUT RETROUVER LE NOMBRE")
        rep1 = (eval(r1),r1)
        print("Vous avez trouvé:",rep1)
    except:
        print("Pas accepté")
        print("L'adversaire à trouvé:",rep2)
        if rep2[0] == nombre:
            return (9, 1)
        else:
            return (6, 1)
    fin = time.time()
    delta = fin - debut
    print("L'adversaire à trouvé:",rep2)
    opt = compte(liste_chiffres,nombre,1000)
    if abs(rep1[0]-nombre) > abs(opt[0]-nombre) and abs(rep2[0]-nombre) > abs(opt[0]-nombre):
        print("Une réponse optimale:",opt)
    if delta > 45 or not verifc(liste_chiffres,r1):
        print("Pas accepté")
        if rep2[0] == nombre:
            return (9, 1)
        else:
            return (6, 1)
    else:
        return pointsc(rep1,rep2,nombre)


def coup_de_lettres(dif,mots):
    """ coup_de_lettres(entier,liste) -> couple   Réalise une manche de coup de chiffres avec un dictionnaire prédéfini
     et un indice de difficulté entre 1 et 1000 renvoie les points gagnés et le gagnant des points """
    liste_lettres = lettres9()
    rep2 = recherche(liste_lettres,mots,dif)
    print("Lettres disponibles:",liste_lettres)
    debut = time.time()
    try:
        rep1 = input("IL FAUT FAIRE UN MOT AVEC CES LETTRES")
        print("Votre réponse",rep1)
    except:
        print("Pas accepté")
        return (len(rep2),1)
    fin = time.time()
    print("L'adversaire a trouvé:",rep2)
    opt = recherche(liste_lettres,mots,100)
    if len(opt) > len(rep1)  and len(opt) > len(rep2):
        print("Une réponse optimale:",opt)
    delta = fin - debut
    if delta > 30 or not verifd(rep1,mots) or not verif(liste_lettres,rep1): #on vérifie s'il n'y pas de triche ou si on a mis trop de temps
        print("Votre réponse n'est pas acceptée")
        if len(rep2) == 0:
            return (0,2)
        else:
            return (max(len(rep2),len(rep1)),1)
    else:
        return pointsl(rep1,rep2)


def attribution_points(res,points):
    """ attribution_points(couple,liste) -> liste   Ajoute les points gagnés
    dans une liste comptabilisant les points de chaque joueur : [joueur 1,joueur 2]"""
    if res[1] == 2:
        print('égalité',res[0],'points pour chacun')
        points[0] += res[0]
        points[1] += res[0]
    else:
        print(res[0],' points pour joueur',res[1] + 1)
        points[res[1]] += res[0]
    for i in range(2):
        print("Le joueur",i+1,"a",points[i],"points")
    return points


def jeu():
    """ jeu() -> entier Le jeu,renvoie le nombre de points du gagnant """
    points = [0,0]
    difficulte = int(input("Difficulté entre 1 et 1000"))
    for _ in range(1):
        input('Prêt pour un coup de chiffres ?')
        m1 = coup_de_chiffres(difficulte)
        points = attribution_points(m1,points)
        input('Prêt pour un coup de lettres ?')
        m2 = coup_de_lettres(difficulte,mots_valides)
        points = attribution_points(m2,points)
        input('Prêt pour un coup de lettres ?')
        m3 = coup_de_lettres(difficulte,mots_valides)
        points = attribution_points(m3,points)
    resultat(points)
    if points[1] == points[0]:
        print("égalité chaque joueur a:")
        return points[1]
    else:
        res = max(points[0],points[1])
        print("le joueur",points.index(res) + 1,"a gagné avec :" )
        return res











