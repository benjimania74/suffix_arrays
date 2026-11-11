EOS = chr(28)

def convertion_suffix_array(mot: str) -> tuple:
    """Convertie le mot en suffix array"""
    mot += EOS
    array = [len(mot), 0]
    for i in range(1, len(mot)):
        array = ajouter_dans_array(array, mot, i)
    return (mot, array)

def convertion_suffix_array2(mot: str) -> tuple:
    """Convertie le mot en suffix array"""
    return (mot + EOS, trie_indices_fusion([i for i in range(len(mot) + 1)], mot + EOS))

def ajouter_dans_array(array: list, mot_origine: str, indice_mot: int) -> list:
    debut = 0
    fin = len(array) - 1

    mot_a_ajouter = mot_origine[indice_mot:]
    plus_grand = True

    while debut <= fin:
        mil = (debut + fin) // 2
        i = array[mil]

        if mot_a_ajouter < mot_origine[i:]:
            fin = mil - 1
            plus_grand = False
        else:
            debut = mil + 1
            plus_grand = True
    
    if plus_grand:
        array = array[:debut] + [indice_mot] + array[debut:]
    else:
        array = array[:fin + 1] + [indice_mot] + array[fin + 1:]

    return array

def est_dans_suffix_array(suffix_array: tuple, mot: str) -> bool:
    res = False

    mot_origine = suffix_array[0]
    array = suffix_array[1]
    longueur_mot_origine = len(mot_origine)
    longueur_mot = len(mot)

    debut = 0
    fin = len(array) - 1


    while debut <= fin and not res:
        mil = (debut + fin) // 2
        val_mil = array[mil]
        sous_mot = mot_origine[val_mil: min(val_mil + longueur_mot, longueur_mot_origine)]

        if mot == sous_mot:
            res = True
        elif mot < sous_mot:
            fin = mil - 1
        else:
            debut = mil + 1
    return res

def trie_indices_fusion(liste_indices: list, mot: str) -> list:
    taille_liste = len(liste_indices)
    if taille_liste == 1:
        res = liste_indices
    else:
        return fusion(
            trie_indices_fusion(
                liste_indices[:taille_liste//2],
                mot
            ), trie_indices_fusion(
                liste_indices[taille_liste//2:],
                mot
            ), mot
        )
    return res

def compare(a: int, b: int, mot: str, taille: int) -> bool:
    if taille == a:
        return True
    
    if taille == b:
        return False
    
    if mot[a] < mot[b]:
        return True
    
    if mot[b] < mot[a]:
        return False
    
    return compare(a+1, b+1, mot, taille)
    


def fusion(liste_a: list, liste_b: list, mot: str) -> list:
    r = []
    
    i, j = 0, 0
    taille_a = len(liste_a)
    taille_b = len(liste_b)
    taille_mot = len(mot)
    while i < taille_a and j < taille_b:
        #if mot[liste_a[i]:] < mot[liste_b[j]:]:
        if compare(liste_a[i], liste_b[j], mot, taille_mot):
            r.append(liste_a[i])
            i += 1
        else:
            r.append(liste_b[j])
            j += 1
    if i != taille_a:
        r += liste_a[i:]
    else:
        r += liste_b[j:]
    return r

def sa_en_bw(suffix_array: tuple) -> str:
    """Transforme le suffix array en transformé de Burrows Wheeler"""
    mot = suffix_array[0]
    array = suffix_array[1]
    taille_mot = len(mot)
    return "".join([mot[(i-1) % taille_mot] for i in array])


def bw_en_sa(bw: str) -> tuple:
    """Transforme le transformé de Burrows Wheeler en suffix array"""
    taille = len(bw)
    chaine_triee = list(enumerate(list(bw)))
    chaine_triee.sort(key=lambda e: e[1])
    indice = bw.find(EOS)
    mot = ""
    sa = [0 for j in range(taille)]
    i = 0
    for j in range(taille):
        caractere = chaine_triee[indice][1]
        mot += caractere
        sa[indice] = i
        i += 1
        indice = chaine_triee[indice][0]
    return (mot, sa)

def convertion_bw(mot: str) -> str:
    mot = mot + EOS
    taille_mot = len(mot)
    tab = [mot[i:] + mot[:i] for i in range(taille_mot)]
    tab.sort()
    return "".join([ligne[taille_mot - 1] for ligne in tab])

def deconvertion_bw(bw: str) -> str:
    chaine_triee = list(enumerate(list(bw)))
    chaine_triee.sort(key=lambda e: e[1]) 
    indice = bw.find(EOS)
    mot = ""
    i = 0
    for j in range(len(bw)):
        caractere = chaine_triee[indice][1]
        mot += caractere
        i += 1
        indice = chaine_triee[indice][0]
    return mot

def convertion_suffix_array_bw(mot: str) -> tuple:
    return bw_en_sa(convertion_bw(mot))