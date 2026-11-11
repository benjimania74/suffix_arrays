def convertion_tries(mot: str) -> dict:
    """Transforme une chaîne de caractère en tries"""
    res = {}
    for i in range(len(mot)):
        actuel = res
        for n in range(i, len(mot)):
            actuel[mot[n]] = actuel.get(mot[n], {})
            actuel = actuel[mot[n]]
    return res

def est_dans_tries(tries: dict, mot: str) -> bool:
    """Renvoie si une chaîne de caractère est décomposée dans le tries"""
    res = True
    i = 0
    actuel = tries
    while i < len(mot) and res:
        prochain = actuel.get(mot[i], None)
        if prochain != None:
            actuel = prochain
        else:
            res = False
        i += 1
    return res

#print(convertion_tries("abracadabradad"))