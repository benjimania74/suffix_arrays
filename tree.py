def convertion_tree(mot: str) -> tuple:
    """Transforme une chaîne de caractère en arbre de suffixe"""
    arbre = {}
    
    for i in range(len(mot)):
        ajouter_tree(arbre, mot, i)

    return (mot, arbre)

def ajouter_tree(branche: dict, mot: str, offset: int):
    """Ajouter une chaîne de caractère dans un arbre"""
    keys = list(branche.keys())
    nb_total_keys = len(keys)
    nb_key = 0
    est_dedans = mot[offset:] == ""
    longueur_mot_a_placer = len(mot) - offset

    while nb_key < nb_total_keys and not est_dedans:
        key = keys[nb_key]

        if mot[key[0]] == mot[offset]:
            nb_egaux = 1
            stop = False
            while nb_egaux < min(key[1], longueur_mot_a_placer) and not stop:
                if mot[key[0] + nb_egaux] != mot[offset + nb_egaux]:
                    stop = True
                else:
                    nb_egaux += 1
            
            if nb_egaux != longueur_mot_a_placer:
                if nb_egaux == key[1]:
                    ajouter_tree(branche[key], mot, offset + nb_egaux)
                else:
                    branche[(key[0], nb_egaux)] = {
                        (key[0] + nb_egaux, key[1] - nb_egaux): branche[key],
                        (offset + nb_egaux, longueur_mot_a_placer - nb_egaux): {}
                    }
                    branche.pop(key)
            est_dedans = True

        nb_key += 1
    
    if not est_dedans:
        branche[(offset, len(mot) - offset)] = {}
    
def est_dans_tree(arbre: tuple, mot: str) -> bool:
    """Renvoie si la chaîne de caractère est contenue dans l'arbre"""
    return est_dans_branche(arbre[1], arbre[0], mot)

def est_dans_branche(branche: dict, mot_origine: str, mot: str) -> bool:
    """Renvoie si la chaîne de caractère est contenue dans la branche"""
    est_dedans = mot == ""
    fin = False
    keys = list(branche.keys())
    nb_key = 0
    longueur_mot = len(mot)

    while nb_key < len(keys) and not fin and not est_dedans:
        key = keys[nb_key]
        if mot_origine[key[0]] == mot[0]:
            if key[1] == longueur_mot:
                est_dedans = mot_origine[key[0] : key[0] + key[1]] == mot
            elif longueur_mot < key[1]:
                est_dedans = mot_origine[key[0] : key[0] + longueur_mot] == mot
            else:
                est_dedans = est_dans_branche(branche[key], mot_origine, mot[key[1]:])
            fin = True

        nb_key += 1

    return est_dedans

def convertion_tree2(mot: str) -> tuple:
    arbre = {}
    for i in range(len(mot)):
        ajouter_arbre2(arbre, i, mot, True)
    fusion_branches(arbre)
    return (mot, arbre)

def ajouter_arbre2(branche: dict, indice: int, mot: str, root: bool = False):
    keys = list(branche.keys())
    nb_keys = len(keys)

    if nb_keys == 0:
        branche[ (indice, 1) ] = {}
    elif nb_keys == 1 and len( list( branche[ keys[0] ].keys() ) ) == 0:
        k = keys[0]
        branche[ (k[0], k[1] + 1) ] = {}
        branche.pop(k)
    else:
        peut_diviser = False
        for k in keys:
            if k == (0, 0):
                peut_diviser = True
            else:
                ss_branche_keys = list(branche[k].keys())
                nb_ss_branche_keys = len(ss_branche_keys)
                if nb_ss_branche_keys == 0:
                    branche[ (k[0], k[1]+1) ] = {}
                    branche.pop(k)
                else:
                    ajouter_arbre2(branche[k], indice, mot)
        if peut_diviser:
            ajout_division(branche, indice, mot)
    if root:
        keys = list(branche.keys())
        nb_keys = len(keys)
        peut_proceder = True
        if nb_keys == 1:
            if keys[0][0] == indice:
                peut_proceder = False
        

        if peut_proceder:
            ajout_division(branche, indice, mot)


def ajout_division(branche: dict, indice: int, mot: str):
    branche.pop( (0,0), None)
    keys = list(branche.keys())
    place = False
    i = 0
    while not place and i < len(keys):
        k = keys[i]
        if mot[ k[0] ] == mot[indice]:
            if k[1] == 1:
                branche[k][ (0, 0) ] = {}
            else:
                branche[ (k[0], 1) ] = {
                    (0,0): {},
                    (k[0] + 1, k[1] - 1): branche[k]
                }
                branche.pop(k)
            place = True
        i += 1
    if not place:
        branche[ (indice, 1) ] = {}

        

def fusion_branches(branche: dict):
    """Fusionne les branches d'un arbre de suffixe non réduit"""
    keys = list(branche.keys())
    for k in keys:
        sous_branche = branche[k]
        sous_branche.pop( (0,0) , None )
        fusion_branches(sous_branche)
        sub_keys = list(sous_branche.keys())
        if len(sub_keys) == 1:
            kb = sub_keys[0]
            nk = (k[0], k[1] + kb[1])
            branche[nk] = sous_branche[kb]
            branche.pop(k)