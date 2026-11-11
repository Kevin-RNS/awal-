
import os
import sys


def effacer_ecran():
    """
    Efface la console avant un nouvel affichage.

    On évite ainsi que le menu et le plateau se répliquent : un seul
    écran reste visible à la fois. Si la sortie n'est pas un terminal
    (redirection vers un fichier, tests...), on n'écrit rien pour ne pas
    polluer le texte avec des codes ANSI.
    """
    if not sys.stdout.isatty():
        return

    if os.name == "nt":
        os.system("cls")
    else:
        sys.stdout.write("\033[H\033[2J\033[3J")
        sys.stdout.flush()


def afficher_menu():
    """Affiche le menu principal."""
    effacer_ecran()
    print()
    print("=" * 40)
    print("              JEU AWALÉ")
    print("=" * 40)
    print("  1. Joueur 1 contre Joueur 2")
    print("  2. Joueur 1 contre Ordinateur")
    print("  3. Quitter")
    print("=" * 40)


def afficher_plateau(plateau, gains, noms):
    """
    Affiche le plateau et les gains.

    Disposition :

            a6   a5   a4   a3   a2   a1      <- rangée 'a'
            b1   b2   b3   b4   b5   b6      <- rangée 'b'
    """
    largeur = 33

    # On repart d'un écran vierge : le plateau précédent disparaît
    # au lieu de s'empiler avec le nouveau.
    effacer_ecran()

    print()
    print("=" * largeur)
    print(noms['a'].center(largeur))

    # En-tête de la rangée 'a' : a6, a5, ..., a1.
    print("  |" + "|".join(
        f"{label:^4}" for label in ("a6", "a5", "a4", "a3", "a2", "a1")
    ) + "|")
    print("  +----+----+----+----+----+----+")

    # Rangée 'a' : indices 5 à 0.
    print("  |" + "|".join(
        f" {plateau[i]:2d} " for i in range(5, -1, -1)
    ) + "|")
    print("  +----+----+----+----+----+----+")

    # Rangée 'b' : indices 6 à 11.
    print("  |" + "|".join(
        f" {plateau[i]:2d} " for i in range(6, 12)
    ) + "|")
    print("  +----+----+----+----+----+----+")

    # En-tête de la rangée 'b' : b1, b2, ..., b6.
    print("  |" + "|".join(
        f"{label:^4}" for label in ("b1", "b2", "b3", "b4", "b5", "b6")
    ) + "|")
    print(noms['b'].center(largeur))
    print(
        f"Gains : {noms['a']} {gains['a']}"
        f"  |  {noms['b']} {gains['b']}"
    )
    print("=" * largeur)


def afficher_resultat(gains, noms, gagnant):
    """Affiche le gagnant et les scores finaux."""
    print()
    if gagnant is None:
        print("  >>> ÉGALITÉ ! <<<")
    else:
        print(f"  >>> {noms[gagnant]} GAGNE ! <<<")

    print(
        f"  Gains : {noms['a']} = {gains['a']}"
        f"  |  {noms['b']} = {gains['b']}"
    )
    input("  Appuyez sur Entrée pour revenir au menu...")
