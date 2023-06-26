import math
import random
import time
import matplotlib.pyplot as plt

def pgcd(a,b):
    r = a%b
    if r == 0:
        return b
    else:
        return pgcd(b,r)


def test_primalite(n):
    i = 2
    for i in range(2,int(n**(1/2))):
        if n%i == 0:
            return False
    return True

def rpremier(deb,fin):
    """retourne un premier aléatoire dans [deb,fin] """
    a = random.randint(deb,fin)
    while not test_primalite(a):
        a = a = random.randint(deb,fin)
    return a

def rpremier2(n,deb,fin):
    """ retourne un nombre entre dans [deb,fin] qui est premier avec n """
    a = random.randint(deb,fin)
    while pgcd(a,n) != 1:
        a = random.randint(deb,fin)
    return a

def identité_Bézout(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = identité_Bézout(b%a,a)
    return (g, x - (b//a) * y, y)

def inv_mod(a, m):
    g, x, y = identité_Bézout(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m

def chiffrage(m,cle):
    if len(cle) == 2:
        if m != int(m):
            pass
        else:
            return pow(m,cle[1],cle[0])
    else:
        if m != int(m):
            pass
        else:
            return pow(m,cle[2],cle[0]*cle[1])



def cles():
    p = int(input('un nombre premier'))
    q = int(input('un nombre premier'))
    while not test_primalite(p) or not test_primalite(q):
        print('ils ne sont pas premiers')
        p = int(input('un nombre premier'))
        q = int(input('un nombre premier'))
    n = p*q
    φ = (p-1)*(q-1)
    e = int(input('nombre premier avec :' + str(φ)))
    while pgcd(e,φ) != 1:
        print('ils ne sont pas premiers entre eux')
        e = int(input('nombre premier avec :' + str(φ)))
    cle_pub = (n,e)
    d = inv_mod(e,φ)
    while d < 0:
        d += φ
    cle_priv = (p*q,d)
    return [cle_pub,cle_priv]

def rcles(deb,fin):
    p = rpremier(deb,fin)
    q = rpremier(deb,fin)
    while q == p:
        q = rpremier(deb,fin)
    φ = (p-1)*(q-1)
    e = rpremier2(φ,deb,fin)
    cle_pub = (p*q,e)
    d = inv_mod(e,φ)
    while d < 0:
        d += φ
    cle_priv = (p,q,d)
    return [cle_pub,cle_priv]


def decomposition(n):
    """ Retourne la décomposition adaptée pour le test de Miler-Rabin"""
    d = n-1
    s = 0
    while d%2 == 0:
        d = d // 2
        s+=1
    return (s,d)



def Miler_Rabin_test(n,a,s,d):
    """ Test de Miler-Rabin pour n, a est un entier entre 2 et n,
     s et d sont des paramètres dépendant de la décomposition de n """
    if pow(a,d,n) == 1 :
        return True
    for i in range(s):
        if pow(a,((2**i)*d),n) == n-1:
            return True
    return False





def Miler_Rabin(n):
    """ Détermine si n est premier"""
    if n == 1:
        return False
    if n == 2:
        return True
    s,d = decomposition(n)
    for k in range(20):
        a = random.randrange(2,n)
        if not Miler_Rabin_test(n,a,s,d):
            return False
    return True

def grand_premier(bits):
    """ Retourne un nombre premier aléatoire de taille bits"""
    while True:
        n = random.getrandbits(bits)
        n |= n | 1
        n |= n | 2**(bits-1)
        if Miler_Rabin(n):
            return(n)

def grand_premier2(a,b):
    """ Retourne un nombre premier aléatoire dans [a,b]"""
    while True:
        n = random.randrange(a,b)
        n |= 1
        if Miler_Rabin(n):
            return(n)

def taille_b(n):
    """ Renvoie la taille de n """
    k = 0
    while 2**k <= n:
        k += 1
    return k

def rcles_module_c(bits):
    """ Retourne un liste de clés ayant le même module de chiffrement n
    et dont les exposants de chiffrement sont premiers entre eux"""
    p = grand_premier((bits//2) + 1)
    q = grand_premier((bits//2) + 1)
    n = p*q
    while taille_b(n) != bits:
        p = grand_premier((bits//2) + 1)
        q = grand_premier((bits//2) + 1)
        n = p*q
    φ = (p-1)*(p-1)
    e = random.randint(0,n)
    while not pgcd(e,φ) == 1 :
        e = random.randint(0,n)
    d = inv_mod(e,φ)
    l = [((n,e),(p,q,d))]
    ee = random.randint(0,n)
    while pgcd(ee,e) != 1 or pgcd(ee,φ) != 1 :
        ee = random.randint(0,n)
    dd = inv_mod(ee,φ)
    l.append(((n,ee),(p,q,dd)))
    return l


def pown(a,r,n):
    """ equivalent de la fonction pow pour r négatif """
    return pow(inv_mod(a,n),-r,n)

def module_c(l_c,l_e,n):
    """ l_c est de la forme (c1,c2) , l_e de la forme (e1,e2) tel que
    m**e1 = c1 mod n et m**e2 = c2 mod n où m est le message original,
    la fonction renvoie m """
    (c,a,b)= identité_Bézout(l_e)
    c1,c2 = l_c
    try:
        if a < 0:
            return (pown(c1,a,n)*pow(c2,b,n)) % n
        if b < 0:
            return (pow(c1,a,n)*pown(c2,b,n)) % n
    except:
        return (c1,c2)


def rcles_e(bits,e):
    """ Renvoie un couple de clés ((n,e),(p,q,d)),
    e est choisi dans les paramètres, n de taille bits"""
    p = grand_premier((bits//2) + 1)
    q = grand_premier((bits//2) + 1)
    φ = (p-1)*(q-1)
    n = p*q
    while q == p or pgcd(e,φ) != 1 or taille_b(n) != bits:
        p = grand_premier((bits//2) + 1)
        q = grand_premier((bits//2) + 1)
        φ = (p-1)*(q-1)
        n = p*q
    cle_pub = (n,e)
    d = inv_mod(e,φ)
    while d < 0:
        d += φ
    cle_priv = (p,q,d)
    return (cle_pub,cle_priv)

def verif(cle,l):
    """ Vérifie si le module de chiffrement de cle est premier
    avec tous ceux des cles de la liste l """
    rep = True
    for i in range(len(l)):
        if pgcd(cle[0][0],l[i][0][0]) != 1:
            rep = False
    return rep

def prod_n(l):
    """ Renvoie le produit de tous les modules de chiffrement
    des cles de la liste l """
    rep = l[0][0][0]
    for i in range(1,len(l)):
        rep = rep * l[i][0][0]
    return rep





def rcles_Hastad(bits,n,e):
    """ Renvoie une liste de n clés
    valides pour l'attaque de Hastad en fixant l'exposant e """
    k = 1
    l = [rcles_e(bits,e)]
    while k < n:
        c = rcles_e(bits,e)
        if verif(c,l):
            l.append(c)
            k += 1
    return l

def restes_chinois(l):
    """ l est une liste de couples d'entiers correspondant à un système de congruences.
    La fonction renvoie la solution de ce système modulo le produit des modules"""
    m = 1
    for i in l:
        m = m*i[1]
    rep = 0
    for j in l:
        mj = (m//j[1])
        rep += j[0]*mj*inv_mod(mj,j[1])
    return (rep%m,m)


def cle_Wiener(bits):
    """ Retourne un couple de clés valides pour l'attaque de Wiener"""
    p = grand_premier((bits//2) + 1)
    q = grand_premier2(p+1,2*p)
    n = p*q
    while taille_b(n) != bits:
        p = grand_premier((bits//2) + 1)
        q = grand_premier2(p+1,2*p)
        n = p*q
    φ = (p-1)*(q-1)
    while True :
        d = random.getrandbits(bits//4)
        if pgcd(φ,d) == 1 and 3*d < pow(n,1/4):
            e = inv_mod(d,φ)
            return (n,e),(n,d)

def fractions_continue(n,d):
    """ Retourne la décomposition en fraction continue du rationel n/d """
    pe = n//d
    if n/d == pe:
        return [pe]
    return [pe] + fractions_continue(d,n - pe*d)


def val_fraction_continue(l):
    """ Retourne la valeur de d'un nombre à partir de sa décompostion """
    if len(l) == 1:
        return (l[0],1)
    x = val_fraction_continue(l[1:])
    return ((l[0]*x[0])+x[1],x[0])





def isqrt(n):
    """ Retourne le plus grand entier inférieur ou égal à la racine de n """
    x = n
    y = (x+1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def equation_deg2(som,prod):
    """ Retourne les nombres dont on entre le produit et la somme """
    delta = pow(som,2) - (4*prod)
    if delta < 0:
        return False
    x1 = (som + isqrt(delta))//2
    x2 = (som - isqrt(delta))//2
    return (x1,x2)

def Wiener(n,e):
    fc = fractions_continue(e,n)
    for i in range(len(fc)):
        réduite = fc[:i+1]
        k,d = val_fraction_continue(réduite)
        if k == 0:
            pass
        else:
            φ = (e*d - 1) // k
            somme = n + 1 - φ
            solutions = equation_deg2(somme,n)
            if solutions != False:
                p,q = solutions
            if p < 0 or q < 0:
                pass
            elif Miler_Rabin(int(p)) and Miler_Rabin(int(q)):
                return (d,réduite,(k,d),p,q)


def rho_pollard(n):
    """ Si n le permet, renvoie la factorisation de n
    en produit de 2 nombres premiers """
    def f(x):
        return (x**4)+1
    d=1
    x=2
    y=2
    while d==1:
        x = f(x)%n
        y = f(f(y))%n
        d = pgcd(x-y, n)
    return d










def graphe_wiener(n,pas):
    """ renvoie le graphe de la moyenne (sur 10 valeurs) de temps mis par la fonction à trouver les clés
    en fonction de leur taille """
    rep = []
    for k in range(100,n+1,pas):
        delta = 0
        for _ in range(10):
            (a,b) = cle_Wiener(k)
            deb = time.time()
            Wiener(a[0],a[1])
            fin = time.time()
            delta += (fin-deb) / 10
        rep.append(delta)
    lx = range(100,n+1,pas)
    ly = rep
    plt.plot(lx,ly)
    plt.title('Attaque de Wiener')
    plt.xlabel('taille de n (bits)')
    plt.ylabel('temps(s)')
    plt.show()

def rcle2(bits):
    """ Retourne un couple de clés ((n,e),(p,q,d)) dont n est de taille bits"""
    p = grand_premier((bits//2) + 1)
    q = grand_premier((bits//2) + 1)
    n = p*q
    while taille_b(n) != bits:
        p = grand_premier((bits//2) + 1)
        q = grand_premier((bits//2) + 1)
        n = p*q
    φ = (p-1)*(p-1)
    e = random.randint(0,n)
    while not pgcd(e,φ) == 1 :
        e = random.randint(0,n)
    d = inv_mod(e,φ)
    return ((n,e),(p,q,d))

def graphe_pollard(n,pas):
    """ renvoie le graphe de la moyenne (sur 10 valeurs) de temps mis
    par la fonction à factoriser n, en fonction de la taille de n"""
    rep = []
    for k in range(10,n+1,pas):
        delta = 0
        for _ in range(10):
            (a,b) = rcle2(k)
            deb = time.time()
            rho_pollard(a[0])
            fin = time.time()
            delta += (fin-deb) / 10
        rep.append(delta)
    lx = range(10,n+1,pas)
    ly = rep
    plt.title('Algorithme rho de Pollard')
    plt.xlabel('taille de n (bits)')
    plt.ylabel('temps(s)')
    plt.plot(lx,ly)
    plt.show()




def chiffrage_l(m,l):
    """ Renvoie la liste des couples (m**e,n) pour chaque clé de la forme (n,e)
    dans l """
    rep = []
    for i in range(len(l)):
        rep.append((chiffrage(m,l[i][0]),l[i][0][0]))
    return rep

def graphe_Hastad(n,pas):
    """ renvoie le graphe de la moyenne (sur 10 valeurs) de temps mis
    par la fonction à résoudre un système de 5 congruences
    en fonction de la taille des clés, on fixe l'exposant e = 5 """
    rep = []
    for k in range(10,n+1,pas):
        delta = 0
        for _ in range(10):
            m = random.randint(0,n)
            l = rcles_Hastad(k,5,3)
            ll = chiffrage_l(m,l)
            deb = time.time()
            restes_chinois(ll)
            fin = time.time()
            delta += (fin-deb) / 10
        rep.append(delta)
    lx = range(10,n+1,pas)
    ly = rep
    plt.title('Theéorème des restes chinois')
    plt.xlabel('taille de n (bits)')
    plt.ylabel('temps(s)')
    plt.plot(lx,ly)
    plt.show()

def graphe_module_c(n,pas):
    """ renvoie le graphe de la moyenne (sur 10 valeurs) de temps mis
    par la fonction à déterminer le message original, en fonction de la taille des clés"""
    rep = []
    for k in range(10,n+1,pas):
        delta = 0
        for _ in range(10):
            m = random.randint(0,k)
            l = rcles_module_c(k)
            ll = chiffrage_l(m,l)
            deb = time.time()
            module_c([ll[0][0],ll[1][0]],[l[0][0][1],l[1][0][1]],l[0][0][0])
            fin = time.time()
            delta += (fin-deb) / 10
        rep.append(delta)
    lx = range(10,n+1,pas)
    ly = rep
    plt.plot(lx,ly)
    plt.title('Faille du module commun')
    plt.xlabel('taille de n (bits)')
    plt.ylabel('temps(s)')
    plt.show()






def verif2(l):
    """ vérifie si les modules de clés de la liste l sont premiers entre eux"""
    for i in range(len(l)):
        for j in range(i+1,len(l)):
            if pgcd(l[i][0][0],l[j][0][0]) != 1:
                return  False
    return True

def graphe_verif_Hastad(n,pas):
    """ Renvoie le graphe de la moyenne (sur 10 valeurs) du nombre de clés crées
    avant d'en avoir une respectant les conditions voulues, en fonction de leur taille,
    pour des systèmes de 10 congruences"""
    rep = []
    for k in range(10,n+1,pas):
        essais = 0
        for _ in range(10):
            i = 1
            l = [rcles_e(k,3) for _ in range(10)]
            while not verif2(l):
                i+1
                l = [rcles_e(k,3) for _ in range(10)]
            essais += i/10
        rep.append(essais)
    lx = range(10,n+1,pas)
    ly = rep
    plt.title("nombre d'essais avant d'être dans les conditions")
    plt.xlabel('nombre de messages')
    plt.ylabel("nb d'essais")
    plt.plot(lx,ly)
    plt.show()

def graphe2_verif_Hastad(n,pas):
    """ Renvoie le graphe de la moyenne (sur 10 valeurs) du nombre de clés crées
    avant d'en avoir une respectant les conditions voulues, en fonction de la
    taille des systèmes, pour des cles de 100 bits"""
    rep = []
    for k in range(3,n+1,pas):
        essais = 0
        for _ in range(10):
            i = 1
            l = [rcles_e(100,3) for _ in range(k)]
            while not verif2(l):
                i+1
                l = [rcles_e(100,3) for _ in range(k)]
            essais += i/10
        rep.append(essais)
    lx = range(3,n+1,pas)
    ly = rep
    plt.title("nombre d'essais avant d'être dans les conditions")
    plt.xlabel('nombre de messages')
    plt.ylabel("nb d'essais")
    plt.plot(lx,ly)
    plt.show()







def verif_wiener(cle):
    ((n,e),(p,q,d)) = cle
    if p<q:
        if p<q<2*p and d<(1/3)*pow(n,1/4):
            return True
    if q<p:
        if q<p<2*q and d<(1/3)*pow(n,1/4):
            return True
    return False



def graphe_verif_wiener(n,pas):
    """ Renvoie le graphe de la moyenne (sur 10 valeurs) du nombre de clés crées
    avant d'en avoir une respectant les conditions voulues, en fonction de leur taille """
    rep = []
    for k in range(100,n+1,pas):
        essais = 0
        for _ in range(10):
            i = 1
            cle = rcle2(k)
            while not verif_wiener(cle):
                i += 1
                cle = rcle2(k)
            essais += i/10
        rep.append(essais)

    lx = range(100,n+1,pas)
    ly = rep
    plt.plot(lx,ly)
    plt.title('Attaque de Wiener')
    plt.xlabel('taille de n (bits)')
    plt.ylabel("nb d'essais")
    plt.show()



def rcles_module_c2(bits):
    """ Retourne un liste de clés ayant le même module de chiffrement n """
    p = grand_premier((bits//2) + 1)
    q = grand_premier((bits//2) + 1)
    n = p*q
    while taille_b(n) != bits:
        p = grand_premier((bits//2) + 1)
        q = grand_premier((bits//2) + 1)
        n = p*q
    φ = (p-1)*(p-1)
    e = random.randint(0,n)
    while not pgcd(e,φ) == 1 :
        e = random.randint(0,n)
    d = inv_mod(e,φ)
    l = [((n,e),(p,q,d))]
    ee = random.randint(0,n)
    while pgcd(ee,φ) != 1 :
        ee = random.randint(0,n)
    dd = inv_mod(ee,φ)
    l.append(((n,ee),(p,q,dd)))
    return l


def graphe_verif_module_c(n,pas):
    """ Renvoie le graphe de la moyenne (sur 10 valeurs) du nombre de clés crées
    avant d'en avoir une respectant les conditions voulues, en fonction de leur taille """
    rep = []
    for k in range(6,n+1,pas):
        essais = 0
        for _ in range(10):
            i = 1
            cle = rcles_module_c2(k)
            while pgcd(cle[0][0][1],cle[1][0][1]) != 1:
                i+= 1
                cle = rcles_module_c2(k)
            essais += i/10
        rep.append(essais)

    lx = range(6,n+1,pas)
    ly = rep
    plt.plot(lx,ly)
    plt.title('Faille du module commun')
    plt.xlabel('taille de n (bits)')
    plt.ylabel("nb d'essais")
    plt.show()



