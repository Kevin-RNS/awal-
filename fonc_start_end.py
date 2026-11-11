
"""
Initialisation et fin de partie.

Équivalent de `fonc_start_end.c` dans le projet C.
"""

from struct_game import (
    jeu,
    TAILLE_PLATEAU,
    GRAINES_PAR_CASE,
    GRAINES_POUR_GAGNER,
)


def init_jeu():
    """
    Réinitialise complètement la partie (Consigne 1).

    En C, cette fonction recréait les 12 cases de la liste chaînée.
    Ici, on remplit simplement la liste avec 4 graines par case.

    On modifie le dictionnaire `jeu` en place (pas de réassignation),
    pour que les autres fichiers voient bien les changements.
    """
    jeu["plateau"][:] = [GRAINES_PAR_CASE] * TAILLE_PLATEAU
    jeu["gains"]['a'] = 0
    jeu["gains"]['b'] = 0
    jeu["mode"] = 0
    jeu["rang_j1"] = 'b'
    jeu["rang_j2"] = 'a'


def fin_jeu(plateau, gains):
    """
    Retourne True si la partie doit s'arrêter (Consigne 5).

    Deux conditions :
      - un joueur a atteint 25 graines (majorité absolue) ;
      - une des deux rangées est vide (règle de famine simplifiée).
    """
    if gains['a'] >= GRAINES_POUR_GAGNER:
        return True
    if gains['b'] >= GRAINES_POUR_GAGNER:
        return True

    graines_a = sum(plateau[0:6])
    graines_b = sum(plateau[6:12])

    if graines_a == 0 or graines_b == 0:
        return True

    return False


def gagnant(gains):
    """
    Retourne 'a', 'b' ou None en cas d'égalité.
    """
    if gains['a'] > gains['b']:
        return 'a'
    if gains['b'] > gains['a']:
        return 'b'
    return None
