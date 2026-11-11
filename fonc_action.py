
from struct_game import TAILLE_PLATEAU, autre_joueur, rangee_depuis_index


def distribuer(plateau, depart):
    """
    prend toutes les graines de la case `depart` et les
    sème une par une dans les cases suivantes.

    On ne remet jamais de graine dans la case de départ.

    Retourne l'indice de la dernière case où une graine a été posée.
    """
    graines = plateau[depart]

    if graines == 0:
        raise ValueError("Impossible de jouer une case vide.")

    plateau[depart] = 0
    position = depart

    while graines > 0:
        position = (position + 1) % TAILLE_PLATEAU

        # On saute la case de départ.
        if position == depart:
            continue

        plateau[position] += 1
        graines -= 1

    return position


def vider(plateau, gains, index_case, joueur):
    """
     vide une case et ajoute ses graines aux gains du joueur.
    """
    graines = plateau[index_case]
    plateau[index_case] = 0
    gains[joueur] += graines


def prise(plateau, gains, dernier, joueur):
    """
    capture les graines adverses.

    On part de la dernière case semée (`dernier`) et on remonte vers les
    cases précédentes tant que :
      - on reste dans la rangée de l'adversaire ;
      - la case contient 2 ou 3 graines.

    Retourne le nombre de graines capturées.
    """
    adversaire = autre_joueur(joueur)

    # La dernière graine doit être tombée chez l'adversaire.
    if rangee_depuis_index(dernier) != adversaire:
        return 0

    pris = 0
    position = dernier

    while (
        rangee_depuis_index(position) == adversaire
        and plateau[position] in (2, 3)
    ):
        pris += plateau[position]
        vider(plateau, gains, position, joueur)
        position = (position - 1) % TAILLE_PLATEAU

    return pris


def jouer_coup(plateau, gains, depart, joueur):
    """
    Joue un coup complet : distribution puis capture éventuelle.

    Vérifie aussi que la case appartient bien au joueur.
    Retourne le nombre de graines capturées.
    """
    if rangee_depuis_index(depart) != joueur:
        raise ValueError("Cette case n'appartient pas à ce joueur.")

    dernier = distribuer(plateau, depart)
    return prise(plateau, gains, dernier, joueur)


def coups_possibles(plateau, joueur):
    """Retourne la liste des indices des cases non vides du joueur."""
    debut = 0 if joueur == 'a' else 6
    return [
        debut + i
        for i in range(6)
        if plateau[debut + i] > 0
    ]
