
import time

from struct_game import (
    jeu,
    NOMS_MODE_1,
    NOMS_MODE_2,
    index_depuis_case,
    numero_depuis_index,
    rangee_depuis_index,
    autre_joueur,
)
from fonc_start_end import init_jeu, fin_jeu, gagnant
from fonc_action import jouer_coup
from j_vs_pc import tour_pc
from affichage import afficher_menu, afficher_plateau, afficher_resultat


def demander_coup(plateau, joueur, nom):
    """Demande une case au joueur jusqu'à obtenir une saisie valide."""
    while True:
        saisie = input(f"  {nom}, choisissez une case (1-6) : ").strip()

        if saisie == "":
            print("  Entrée vide, réessayez.")
            continue

        try:
            numero = int(saisie)
        except ValueError:
            print("  Entrée invalide : tapez un nombre entre 1 et 6.")
            continue

        if not 1 <= numero <= 6:
            print("  Numéro invalide : il faut choisir entre 1 et 6.")
            continue

        depart = index_depuis_case(numero, joueur)

        if plateau[depart] == 0:
            print("  Cette case est vide, choisissez-en une autre.")
            continue

        return depart


def afficher_coup(nom, depart, pris):
    """Affiche le coup joué et la capture éventuelle."""
    case = f"{rangee_depuis_index(depart)}{numero_depuis_index(depart)}"
    print(f"  {nom} joue la case {case}.")

    if pris > 0:
        print(f"  --> {nom} capture {pris} graine(s) !")


def jouer_partie(mode):
    """
    Lance une partie.

    mode 1 : Joueur 1 contre Joueur 2
    mode 2 : Joueur 1 contre Ordinateur
    """
    init_jeu()
    jeu["mode"] = mode

    noms = NOMS_MODE_1 if mode == 1 else NOMS_MODE_2

    # Le joueur 1 joue la rangée 'b' (en bas) et commence.
    joueur = 'b'

    while not fin_jeu(jeu["plateau"], jeu["gains"]):
        afficher_plateau(jeu["plateau"], jeu["gains"], noms)
        nom = noms[joueur]

        # --- Tour de l'ordinateur ---
        if mode == 2 and joueur == 'a':
            print("  Tour de l'ordinateur...")
            time.sleep(1)

            depart, pris = tour_pc(jeu["plateau"], jeu["gains"], joueur)

            if depart is None:
                break
        # --- Tour d'un joueur humain ---
        else:
            depart = demander_coup(jeu["plateau"], joueur, nom)
            pris = jouer_coup(jeu["plateau"], jeu["gains"], depart, joueur)

        afficher_coup(nom, depart, pris)
        input("  Appuyez sur Entrée pour continuer...")

        # On passe la main à l'autre joueur.
        joueur = autre_joueur(joueur)

    # Affichage final (le plateau peut avoir changé au dernier coup).
    afficher_plateau(jeu["plateau"], jeu["gains"], noms)
    afficher_resultat(jeu["gains"], noms, gagnant(jeu["gains"]))


def main():
    """Affiche le menu et lance le mode choisi."""
    while True:
        afficher_menu()
        choix = input("  Votre choix : ").strip()

        if choix == "1":
            jouer_partie(1)
        elif choix == "2":
            jouer_partie(2)
        elif choix == "3":
            print("  Merci d'avoir joué au jeu Awalé !")
            break
        else:
            print("  Choix invalide : tapez 1, 2 ou 3.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C ou fin du flux d'entrée : on quitte proprement.
        print("\n  Partie interrompue. Au revoir !")
