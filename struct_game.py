TAILLE_PLATEAU = 12
GRAINES_PAR_CASE = 4
GRAINES_POUR_GAGNER = 25

# Noms affichés selon le mode de jeu.
NOMS_MODE_1 = {'a': "Joueur 2", 'b': "Joueur 1"}
NOMS_MODE_2 = {'a': "Ordinateur", 'b': "Vous"}

jeu = {
    "plateau": [GRAINES_PAR_CASE] * TAILLE_PLATEAU,
    "gains": {'a': 0, 'b': 0},
    "mode": 0,
    "rang_j1": 'b',
    "rang_j2": 'a',
}


def index_depuis_case(numero, rangee):
    """Transforme (numéro 1-6, rangée 'a'/'b') en indice de 0 à 11."""
    if rangee not in ('a', 'b'):
        raise ValueError("La rangée doit être 'a' ou 'b'.")
    if not 1 <= numero <= 6:
        raise ValueError("Le numéro de case doit être entre 1 et 6.")
    return (numero - 1) + (0 if rangee == 'a' else 6)


def numero_depuis_index(index):
    """Retourne le numéro (1-6) d'une case à partir de son indice."""
    return (index % 6) + 1


def rangee_depuis_index(index):
    """Retourne 'a' ou 'b' selon la rangée de la case."""
    return 'a' if index < 6 else 'b'


def autre_joueur(joueur):
    """Retourne la rangée de l'adversaire."""
    return 'b' if joueur == 'a' else 'a'
