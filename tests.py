from multiprocessing import Process, Manager
from random import randint
from time import *

class SharedList:
    def __init__(self, parent=None):
        self.parent = parent
        self.content = Manager().list()
    
    def getParent(self):
        return self.parent
    
    def addToParent(self, values: list):
        if self.parent != None:
            self.parent.addContent(values)

    def getContent(self):
        return self.content
    
    def addContent(self, c: list):
        self.content += [c]

EOF = chr(28)

def convertion_suffix_array2(mot: str) -> tuple:
    """Convertie le mot en suffix array"""
    mot += EOF
    t = [i for i in range(len(mot))]
    t.sort(key=lambda x: mot[x:])
    return t
    #return (mot + EOF, trie_indices_fusion([i for i in range(len(mot) + 1)], mot + EOF))

def trie_indices_fusion(liste_indices: list, mot: str, parentSharedList: SharedList = None, deep: int = 0):
    print(deep)
    sharedList = SharedList(parentSharedList)
    taille_liste = len(liste_indices)
    if taille_liste == 1:
        res = liste_indices
    else:
        if deep == 0:
            p1 = Process(
                target=trie_indices_fusion,
                args=(
                    liste_indices[:taille_liste//2],
                    mot,
                    sharedList,
                    1000
                )
            )

            p2 = Process(
                target=trie_indices_fusion,
                args=(
                    liste_indices[taille_liste//2:],
                    mot,
                    sharedList,
                    1000
                )
            )

            p1.start()
            p2.start()

            p1.join()
            p2.join()

            res = fusion(sharedList.getContent()[0], sharedList.getContent()[1], mot)
        else:
            res = fusion(
                trie_indices_fusion(liste_indices[taille_liste//2:], mot, deep=deep-1),
                trie_indices_fusion(liste_indices[:taille_liste//2], mot, deep=deep-1),
                mot
            )

    sharedList.addToParent(res)

    if parentSharedList == None:
        return res

def fusion(liste_a: list, liste_b: list, mot: str) -> list:
    r = []
    
    i, j = 0, 0

    while i < len(liste_a) and j < len(liste_b):
        if mot[liste_a[i]:] < mot[liste_b[j]:]:
            r.append(liste_a[i])
            i += 1
        else:
            r.append(liste_b[j])
            j += 1
    if i != len(liste_a):
        r += liste_a[i:]
    else:
        r += liste_b[j:]
    return r

def fusion_normale(liste_a: list, liste_b: list) -> list:
    r = []
    
    i, j = 0, 0

    while i < len(liste_a) and j < len(liste_b):
        if liste_a[i] < liste_b[j]:
            r.append(liste_a[i])
            i += 1
        else:
            r.append(liste_b[j])
            j += 1
    if i != len(liste_a):
        r += liste_a[i:]
    else:
        r += liste_b[j:]
    return r

def test(c: SharedList):
    processus = [Process(target=bonjour, args=(c,)) for i in range(2)]
    for p in processus:
        p.start()
    print("Process start")

    for p in processus:
        p.join()
    print("Process fini")
    t = fusion_normale(c.getContent()[0], c.getContent()[1])
    print(t)

def bonjour(c: SharedList):
    t = [i for i in range(50)]
    c.addContent(t)


def parseTests() -> list:
    tests = []
    file = open("tests.txt", "r")
    ligne = file.readline()
    while ligne != "":
        t = {}
        t["mot"] = ligne[:-1]
        t["cherche"] = file.readline()[:-1]
        ligne = file.readline()
        t["res"] = ligne[:-1] if ligne[-1] == "\n" else ligne
        tests += [t]
        ligne = file.readline()
    file.close()
    return tests

def executerTests(tests: list, debut: int = 0, fin: int = -1) -> list:
    fn = [test_suffix_array]
    res = []
    
    if fin == -1:
        fin = len(tests)
    if debut <= fin:
        t = time()
        for i in range(debut, fin):
            test = tests[i]
            mot = test["mot"]
            cherche = test["cherche"]
            v = [fn[i](mot, cherche) for i in range(len(fn))]
            v += [test["res"]]
            res += [v]
    return res

def sauvegarderResultats(resultats: list):
    file = open("resultats.txt", "w")
    i = 0
    while i < len(resultats):
        r = resultats[i]
        file.write("-"*30 + "\n")
        file.write("Test - " + str(i) + "\n")
        for j in range(len(r) - 1):
            file.write(str(r[j]) + "\n")
        file.write(str(r[-1]) + "\n")
        file.write("-"*30 + "\n")
        i += 1
    file.close()

def test_suffix_array(mot: str, cherche: str) -> list:
    return test_structure(mot, cherche, convertion_suffix_array2)

def test_structure(mot: str, cherche: str, convertionFn) -> list:
    t = time()
    struct = convertionFn(mot)
    d = time()
    tps_construction = d - t

    print(tps_construction)


def fusion(liste_a: list, liste_b: list, mot: str) -> list:
    r = []
    
    i, j = 0, 0
    taille_a = len(liste_a)
    taille_b = len(liste_b)
    while i < taille_a and j < taille_b:
        if mot[liste_a[i]:] < mot[liste_b[j]:]:
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

if __name__ == "__main__":
    print("Main")