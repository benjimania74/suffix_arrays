def convertion_dico_condense(mot: str) -> tuple:
    res = {}
    for i in range(len(mot)):
        d = res.get(mot[i], [])
        d += [i]
        res[mot[i]] = d
    return (mot, res)

def est_dans_dico_condense(dico_condense: tuple, mot: str) -> bool:
    """Renvoie si le mot est dans le dico condensé"""
    res = mot == ""
    if not res:
        dico: dict = dico_condense[1]
        mot_origine = dico_condense[0]
        longueur_mot = len(mot)
        indices_depart = dico.get(mot[0], [])
        indices_fin = dico.get(mot[longueur_mot - 1], [])

        if indices_depart != [] and indices_fin != []:
            i = 0
            while i < len(indices_depart) and not res:
                indice_depart = indices_depart[i]
                indice_fin = indice_depart + longueur_mot - 1

                if indice_fin in indices_fin and mot == mot_origine[indice_depart:indice_fin + 1]:
                    res = True
                i += 1
    return res