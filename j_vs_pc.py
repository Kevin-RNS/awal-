
import random

from fonc_action import coups_possibles, jouer_coup


def choisir_coup_pc(plateau, gains, joueur):
    """
    Choisit un coup pour l'ordinateur.

    Stratégie simple : on simule chaque coup possible et on garde celui
    qui capture le plus de graines. En cas d'égalité, on tire au sort.

    Retourne un indice de case, ou None si aucun coup n'est possible.
    """
    meilleur_score = -1
    meilleurs_coups = []

    for depart in coups_possibles(plateau, joueur):
        plateau_test = plateau.copy()
        gains_test = gains.copy()

        pris = jouer_coup(plateau_test, gains_test, depart, joueur)

        if pris > meilleur_score:
            meilleur_score = pris
            meilleurs_coups = [depart]
        elif pris == meilleur_score:
            meilleurs_coups.append(depart)

    if not meilleurs_coups:
        return None

    return random.choice(meilleurs_coups)


def tour_pc(plateau, gains, joueur):
    """
    Joue le tour complet de l'ordinateur.

    Retourne un couple (coup, graines_capturées).
    Si l'ordinateur ne peut pas jouer, retourne (None, 0).
    """
    coup = choisir_coup_pc(plateau, gains, joueur)

    if coup is None:
        return None, 0

    pris = jouer_coup(plateau, gains, coup, joueur)
    return coup, pris
