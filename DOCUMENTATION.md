# Guide complet — Jeu Awalé en Python

> **But de ce document**
>
> Expliquer **tout** le projet Awalé en Python : les règles, l'organisation
> des fichiers, chaque fonction, chaque test, et comment le reproduire
> soi-même depuis zéro.
>


---

## Table des matières

1. [Le jeu Awalé en 2 minutes](#1-le-jeu-awalé-en-2-minutes)
2. [Les fichiers du projet](#2-les-fichiers-du-projet)
3. [Installer et lancer](#3-installer-et-lancer)
4. [Représentation du plateau](#4-représentation-du-plateau)
5. [Explication fichier par fichier](#5-explication-fichier-par-fichier)
6. [Déroulement d'une partie pas à pas](#6-déroulement-dune-partie-pas-à-pas)
7. [Les tests expliqués](#7-les-tests-expliqués)
8. [Reproduire le projet de zéro](#8-reproduire-le-projet-de-zéro)
9. [Choix techniques et pièges à éviter](#9-choix-techniques-et-pièges-à-éviter)
10. [Bugs du code C corrigés](#10-bugs-du-code-c-corrigés)
11. [Pour aller plus loin](#11-pour-aller-plus-loin)
12. [Lexique](#12-lexique)

---

## 1. Le jeu Awalé en 2 minutes

L'Awalé est un jeu de semailles africain qui se joue à deux.

### Le plateau

Le plateau possède **2 rangées de 6 cases**, soit **12 cases**.
Au départ, chaque case contient **4 graines**, donc **48 graines** en tout.

```
        a6   a5   a4   a3   a2   a1      <- rangée du joueur A
        b1   b2   b3   b4   b5   b6      <- rangée du joueur B
```

Dans ce projet :

- le joueur de la rangée **`a`** est en haut ;
- le joueur de la rangée **`b`** est en bas ;
- le joueur 1 (ou « Vous ») joue la rangée **`b`** et commence.

### Le tour de jeu

À son tour, un joueur choisit une case **non vide de sa propre rangée**.
Il prend toutes les graines de cette case et les sème **une par une** dans
les cases suivantes, dans le sens anti-horaire :

```
a1 -> a2 -> ... -> a6 -> b1 -> ... -> b6 -> a1
```

Deux règles importantes :

1. On **saute la case de départ** : on ne remet jamais une graine dedans.
2. On continue à semer même si on passe dans la rangée adverse.

### La capture

Si la **dernière graine semée** tombe dans une case adverse qui contient
alors **2 ou 3 graines**, le joueur capture cette case.

Ensuite, il remonte vers les cases précédentes et capture aussi chaque
case adverse qui contient 2 ou 3 graines. Dès qu'une case ne contient
pas 2 ou 3 graines, la capture s'arrête.

Les graines capturées sont ajoutées aux gains du joueur.

### La fin de partie

La partie s'arrête si :

- un joueur atteint **25 graines** (la majorité absolue sur 48) ;
- ou une des deux rangées est complètement vide (règle de famine
  simplifiée, comme dans le sujet du TP).

Le gagnant est celui qui a le plus de graines capturées.

> **À retenir**
>
> Les règles sont volontairement simplifiées par rapport à certaines
> variantes de l'Awalé. Par exemple, on n'interdit pas de capturer
> toutes les graines de l'adversaire. C'est indiqué dans le README.

---

## 2. Les fichiers du projet

```
awale_sans_poo/
├── struct_game.py      Données, constantes et état global
├── fonc_start_end.py   Initialisation et fin de partie
├── fonc_action.py      Distribution, vidage et capture
├── j_vs_pc.py          Intelligence artificielle de l'ordinateur
├── affichage.py        Menu, plateau et résultat
├── main.py             Saisie, boucles de jeu et point d'entrée
└── test_awale.py       Tests unitaires
```

Chaque fichier a une responsabilité claire, comme dans le projet C :

| Fichier Python | Équivalent C | Responsabilité |
|---|---|---|
| `struct_game.py` | `struct_game.h` | Les données et les outils de conversion |
| `fonc_start_end.py` | `fonc_start_end.c` | Démarrer et terminer une partie |
| `fonc_action.py` | `fonc_action.c` | Les règles de semaille et de capture |
| `j_vs_pc.py` | `j_VS_pc.c` | Le coup de l'ordinateur |
| `affichage.py` | extrait de `main.c` | Tout ce qui s'affiche |
| `main.py` | `main.c` | Enchaîner les tours et gérer le menu |

### Qui appelle qui ?

```
main.py
 ├── affichage.py
 ├── fonc_start_end.py
 │    └── struct_game.py
 ├── fonc_action.py
 │    └── struct_game.py
 └── j_vs_pc.py
      └── fonc_action.py
```

`struct_game.py` ne dépend d'aucun autre fichier : c'est la base.
`main.py` dépend de presque tout : c'est le chef d'orchestre.

> **Remarque**
>
> Le projet contient aussi `awale.py`, une version en un seul fichier
> avec une classe `Jeu` (POO). Elle est équivalente mais moins proche
> de l'organisation du C. Ce guide se concentre sur la version sans POO.

---

## 3. Installer et lancer

### Prérequis

- **Python 3.8 ou plus récent**.
- Aucune bibliothèque externe à installer.

Vérifier la version de Python :

```bash
python3 --version
```

### Lancer le jeu

Depuis le dossier principal du projet :

```bash
python3 awale_sans_poo/main.py
```

Ou depuis le dossier `awale_sans_poo` :

```bash
cd awale_sans_poo
python3 main.py
```

### Lancer les tests

```bash
cd awale_sans_poo
python3 -m unittest test_awale.py -v
```

Résultat attendu :

```
Ran 13 tests in 0.003s

OK
```

### Lancer un seul test

```bash
python3 -m unittest test_awale.TestCapture.test_prise_contigue -v
```

C'est très utile quand on modifie une règle : on peut vérifier rapidement
seulement la partie concernée.

---

## 4. Représentation du plateau

### 4.1 Une liste de 12 entiers

En C, le plateau était une **liste chaînée circulaire** de 12 cases.
En Python, c'est beaucoup plus simple : une **liste de 12 entiers**.

```python
plateau = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
```

Chaque entier est le nombre de graines dans une case.

### 4.2 Correspondance indice / case

```
Indice :   0    1    2    3    4    5    6    7    8    9   10   11
Case   :  a1   a2   a3   a4   a5   a6   b1   b2   b3   b4   b5   b6
```

Autrement dit :

- indices `0` à `5`  : rangée **`a`** (`a1` à `a6`) ;
- indices `6` à `11` : rangée **`b`** (`b1` à `b6`).

### 4.3 Sens de distribution

L'ordre de la liste correspond exactement au sens de distribution :

```
a1 -> a2 -> a3 -> a4 -> a5 -> a6 -> b1 -> b2 -> b3 -> b4 -> b5 -> b6 -> a1
 0 ->  1 ->  2 ->  3 ->  4 ->  5 ->  6 ->  7 ->  8 ->  9 -> 10 -> 11 ->  0
```

Passer à la case suivante s'écrit donc :

```python
position = (position + 1) % 12
```

Le `% 12` (modulo 12) permet de revenir à `0` après `11`.
C'est ce qui rend le plateau **circulaire** sans liste chaînée.

### 4.4 Les fonctions de conversion

Trois petites fonctions évitent les erreurs d'indice.

#### `index_depuis_case(numero, rangee)`

Transforme un numéro de case (1 à 6) et une rangée (`'a'` ou `'b'`) en
indice de 0 à 11.

```python
def index_depuis_case(numero, rangee):
    if rangee not in ('a', 'b'):
        raise ValueError("La rangée doit être 'a' ou 'b'.")
    if not 1 <= numero <= 6:
        raise ValueError("Le numéro de case doit être entre 1 et 6.")
    return (numero - 1) + (0 if rangee == 'a' else 6)
```

Exemples :

| Appel | Calcul | Résultat |
|---|---|---|
| `index_depuis_case(1, 'a')` | `(1 - 1) + 0` | `0` |
| `index_depuis_case(6, 'a')` | `(6 - 1) + 0` | `5` |
| `index_depuis_case(1, 'b')` | `(1 - 1) + 6` | `6` |
| `index_depuis_case(6, 'b')` | `(6 - 1) + 6` | `11` |

#### `numero_depuis_index(index)`

Fait l'inverse : donne le numéro 1 à 6 à partir de l'indice.

```python
def numero_depuis_index(index):
    return (index % 6) + 1
```

Exemples : `0 -> 1`, `5 -> 6`, `6 -> 1`, `11 -> 6`.

#### `rangee_depuis_index(index)`

Donne la rangée d'une case.

```python
def rangee_depuis_index(index):
    return 'a' if index < 6 else 'b'
```

Exemples : `0 -> 'a'`, `5 -> 'a'`, `6 -> 'b'`, `11 -> 'b'`.

#### `autre_joueur(joueur)`

Donne la rangée de l'adversaire.

```python
def autre_joueur(joueur):
    return 'b' if joueur == 'a' else 'a'
```

Exemples : `'a' -> 'b'`, `'b' -> 'a'`.

> **Pourquoi ces fonctions ?**
>
> Sans elles, on écrirait partout des calculs comme `numero - 1 + 6`.
> Avec elles, le code se lit presque comme du français :
> « l'indice de la case 3 de la rangée b », au lieu de « 3 - 1 + 6 ».

---

## 5. Explication fichier par fichier

### 5.1 `struct_game.py` — les données

Ce fichier joue le rôle du `struct_game.h` en C.

#### Les constantes

```python
TAILLE_PLATEAU = 12
GRAINES_PAR_CASE = 4
GRAINES_POUR_GAGNER = 25
```

- `TAILLE_PLATEAU` : nombre total de cases.
- `GRAINES_PAR_CASE` : graines au début.
- `GRAINES_POUR_GAGNER` : seuil de victoire.

Utiliser des constantes évite les « nombres magiques » perdus dans le
code. Si on veut tester une variante avec 5 graines par case, on change
une seule ligne.

#### Les noms des joueurs

```python
NOMS_MODE_1 = {'a': "Joueur 2", 'b': "Joueur 1"}
NOMS_MODE_2 = {'a': "Ordinateur", 'b': "Vous"}
```

Ces dictionnaires servent uniquement à l'affichage. La logique du jeu
ne connaît que `'a'` et `'b'`.

#### L'état global `jeu`

```python
jeu = {
    "plateau": [GRAINES_PAR_CASE] * TAILLE_PLATEAU,
    "gains": {'a': 0, 'b': 0},
    "mode": 0,
    "rang_j1": 'b',
    "rang_j2": 'a',
}
```

C'est l'équivalent de :

```c
Jeu jeu;
```

Le dictionnaire contient :

| Clé | Type | Rôle |
|---|---|---|
| `plateau` | liste de 12 entiers | Les graines sur le plateau |
| `gains` | dictionnaire `{'a': int, 'b': int}` | Les graines capturées |
| `mode` | entier | `1` = 2 joueurs, `2` = contre l'ordinateur |
| `rang_j1` | `'a'` ou `'b'` | Rangée du joueur 1 |
| `rang_j2` | `'a'` ou `'b'` | Rangée du joueur 2 |

> **Attention importante**
>
> Ne jamais écrire `jeu = ...` dans une fonction. Cela créerait un
> **nouveau** dictionnaire local, et les autres fichiers continueraient
> à utiliser l'ancien.
>
> Il faut modifier le contenu :
>
> ```python
> jeu["plateau"][:] = [4] * 12   # correct
> jeu["gains"]['a'] = 0          # correct
> ```
>
> C'est exactement ce que fait `init_jeu()`.

---

### 5.2 `fonc_action.py` — le cœur des règles

C'est le fichier le plus important : il contient la distribution et la
capture. Toutes les fonctions reçoivent `plateau` et `gains` en
paramètres. Cela permet de tester facilement et de simuler un coup.

#### `distribuer(plateau, depart)`

```python
def distribuer(plateau, depart):
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
```

**Explication ligne par ligne :**

1. `graines = plateau[depart]` : on mémorise le nombre de graines à semer.
2. Si la case est vide, on lève une erreur : on ne peut pas jouer une
   case vide.
3. `plateau[depart] = 0` : on vide la case de départ.
4. `position = depart` : on commence à côté de la case de départ.
5. La boucle tourne une fois par graine.
6. `position = (position + 1) % 12` : on avance d'une case, en revenant
   à `0` après `11`.
7. Si on retombe sur la case de départ, `continue` saute le reste de la
   boucle et on avance encore : **on ne sème pas dans la case de départ**.
8. Sinon, on ajoute une graine et on décrémente le compteur.
9. La fonction retourne `position`, c'est-à-dire l'indice de la
   **dernière case semée**. C'est indispensable pour la capture.

**Exemple 1 — 4 graines depuis `a1`**

État de départ (on ne montre que les cases utiles) :

```
a1 = 4, toutes les autres = 0
```

On vide `a1`, puis on sème :

| Graine | Case recevant la graine | Graines restantes |
|---|---|---|
| 1 | `a2` | 3 |
| 2 | `a3` | 2 |
| 3 | `a4` | 1 |
| 4 | `a5` | 0 |

Résultat :

```
a1 = 0, a2 = 1, a3 = 1, a4 = 1, a5 = 1
dernier = a5
```

**Exemple 2 — 13 graines depuis `a1`**

On vide `a1`. On fait un tour complet :

- `a2`, `a3`, `a4`, `a5`, `a6`, `b1`, `b2`, `b3`, `b4`, `b5`, `b6`
  reçoivent chacune 1 graine (11 graines utilisées) ;
- on arrive sur `a1`, qui est la case de départ : on la saute ;
- `a2` reçoit une deuxième graine (12e graine) ;
- `a3` reçoit une deuxième graine (13e graine).

Résultat :

```
a1 = 0
a2 = 2, a3 = 2
a4 = a5 = a6 = b1 = b2 = b3 = b4 = b5 = b6 = 1
dernier = a3
```

La somme des graines reste **13** : on n'a rien créé ni perdu.

> **À retenir**
>
> La distribution ne fait que **déplacer** des graines. Si on additionne
> le plateau et les gains, on doit toujours trouver 48.

#### `vider(plateau, gains, index_case, joueur)`

```python
def vider(plateau, gains, index_case, joueur):
    graines = plateau[index_case]
    plateau[index_case] = 0
    gains[joueur] += graines
```

Cette fonction :

1. lit le nombre de graines de la case ;
2. vide la case ;
3. ajoute les graines aux gains du joueur.

En C, la fonction devinait le joueur à partir de la rangée vidée. Ici, on
passe directement `joueur`. C'est plus clair : la fonction sait
exactement à qui ajouter les points.

#### `prise(plateau, gains, dernier, joueur)`

```python
def prise(plateau, gains, dernier, joueur):
    adversaire = autre_joueur(joueur)

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
```

**Explication :**

1. On calcule la rangée de l'adversaire.
2. Si la dernière graine n'est **pas** tombée chez l'adversaire, il n'y a
   pas de capture : on retourne `0`.
3. Sinon, on part de la dernière case.
4. La boucle continue tant que :
   - on est encore dans la rangée adverse ;
   - la case contient 2 ou 3 graines.
5. On ajoute les graines au total `pris`, on vide la case, puis on
   recule d'une case avec `(position - 1) % 12`.
6. Dès qu'une condition est fausse, la boucle s'arrête.

**Exemple — capture de 5 graines**

Situation avant le coup :

```
a6 = 3
b1 = 4
b2 = 2
b3 = 1
toutes les autres cases = 0
```

Le joueur `a` joue `a6` (3 graines) :

| Graine | Case | Valeur après semaille |
|---|---|---|
| 1 | `b1` | 5 |
| 2 | `b2` | 3 |
| 3 | `b3` | 2 |

La dernière case est `b3`. On capture en remontant :

- `b3` vaut 2 → on capture 2 ; la case devient 0 ;
- `b2` vaut 3 → on capture 3 ; la case devient 0 ;
- `b1` vaut 5 → ni 2 ni 3 → **on s'arrête**.

Total capturé : `2 + 3 = 5`.
Les gains de `a` augmentent de 5.

> **Le bug du C**
>
> Dans la version C, la capture recommençait toujours à la case 6 au lieu
> de partir de la dernière case semée. Elle pouvait donc capturer des
> cases qui n'avaient rien à voir avec le coup. Ici, on part bien de
> `dernier`.

#### `jouer_coup(plateau, gains, depart, joueur)`

```python
def jouer_coup(plateau, gains, depart, joueur):
    if rangee_depuis_index(depart) != joueur:
        raise ValueError("Cette case n'appartient pas à ce joueur.")

    dernier = distribuer(plateau, depart)
    return prise(plateau, gains, dernier, joueur)
```

Cette fonction regroupe les deux étapes :

1. vérifier que la case appartient au joueur ;
2. distribuer les graines ;
3. capturer si nécessaire ;
4. retourner le nombre de graines capturées.

C'est la fonction que le jeu et l'ordinateur utilisent.

#### `coups_possibles(plateau, joueur)`

```python
def coups_possibles(plateau, joueur):
    debut = 0 if joueur == 'a' else 6
    return [
        debut + i
        for i in range(6)
        if plateau[debut + i] > 0
    ]
```

Cette fonction retourne la liste des indices des cases non vides du
joueur. Exemple : si `b1 = 0`, `b2 = 3`, `b3 = 0`, `b4 = 2`, `b5 = 0`,
`b6 = 1`, elle retourne `[7, 9, 11]`.

Elle sert à :

- savoir si un joueur peut encore jouer ;
- lister les coups à simuler pour l'ordinateur.

---

### 5.3 `fonc_start_end.py` — démarrer et finir

#### `init_jeu()`

```python
def init_jeu():
    jeu["plateau"][:] = [GRAINES_PAR_CASE] * TAILLE_PLATEAU
    jeu["gains"]['a'] = 0
    jeu["gains"]['b'] = 0
    jeu["mode"] = 0
    jeu["rang_j1"] = 'b'
    jeu["rang_j2"] = 'a'
```

Cette fonction remet la partie à zéro :

- 4 graines dans chaque case ;
- gains à 0 ;
- mode à 0 ;
- joueur 1 en `b`, joueur 2 en `a`.

Pourquoi `jeu["plateau"][:]` et pas `jeu["plateau"] = ...` ?

- `[:]` modifie la liste **existante** ;
- `=` remplacerait la liste par une nouvelle.

Les deux fonctionnent ici, mais `[:]` est plus sûr : si un autre fichier
a gardé une référence vers la liste, il verra quand même la mise à jour.

> **Règle d'or**
>
> On modifie l'état global **en place**, on ne le réassigne jamais.

#### `fin_jeu(plateau, gains)`

```python
def fin_jeu(plateau, gains):
    if gains['a'] >= GRAINES_POUR_GAGNER:
        return True
    if gains['b'] >= GRAINES_POUR_GAGNER:
        return True

    graines_a = sum(plateau[0:6])
    graines_b = sum(plateau[6:12])

    if graines_a == 0 or graines_b == 0:
        return True

    return False
```

Deux conditions d'arrêt :

1. un joueur a au moins 25 graines ;
2. une rangée est vide.

`plateau[0:6]` prend les indices 0 à 5 (rangée `a`) ;
`plateau[6:12]` prend les indices 6 à 11 (rangée `b`).

En Python, `plateau[0:6]` signifie « du début jusqu'à l'indice 6, exclu ».
C'est une source classique d'erreurs : `6` n'est **pas** inclus.

#### `gagnant(gains)`

```python
def gagnant(gains):
    if gains['a'] > gains['b']:
        return 'a'
    if gains['b'] > gains['a']:
        return 'b'
    return None
```

Retourne :

- `'a'` si le joueur `a` a plus de graines ;
- `'b'` si le joueur `b` a plus de graines ;
- `None` en cas d'égalité.

---

### 5.4 `j_vs_pc.py` — l'ordinateur

#### `choisir_coup_pc(plateau, gains, joueur)`

```python
def choisir_coup_pc(plateau, gains, joueur):
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
```

**Stratégie :**

1. On liste toutes les cases jouables.
2. Pour chacune, on **copie** le plateau et les gains.
3. On joue le coup sur la copie.
4. On note combien de graines ce coup capture.
5. On garde le ou les coups qui capturent le plus.
6. En cas d'égalité, on tire au sort avec `random.choice`.

**Pourquoi copier ?**

Si on jouait directement sur le vrai plateau pour tester, on modifierait
la vraie partie ! La copie permet de simuler sans conséquence.

```python
plateau_test = plateau.copy()   # nouvelle liste
gains_test = gains.copy()       # nouveau dictionnaire
```

`.copy()` fait une copie **superficielle**. Ici, c'est suffisant, car les
éléments sont des entiers (immuables).

**Exemple :**

Si les seuls coups possibles capturent respectivement 0, 5 et 2 graines,
l'ordinateur garde le coup qui capture 5. S'il y a plusieurs coups à 5,
il en choisit un au hasard.

#### `tour_pc(plateau, gains, joueur)`

```python
def tour_pc(plateau, gains, joueur):
    coup = choisir_coup_pc(plateau, gains, joueur)

    if coup is None:
        return None, 0

    pris = jouer_coup(plateau, gains, coup, joueur)
    return coup, pris
```

Cette fonction :

1. choisit un coup ;
2. si aucun coup n'est possible, retourne `(None, 0)` ;
3. sinon, joue réellement le coup sur le vrai plateau ;
4. retourne `(coup, graines_capturées)`.

Le `main` utilise ces deux valeurs pour afficher le coup et la capture.

---

### 5.5 `affichage.py` — tout ce qui s'affiche

#### `effacer_ecran()`

Efface la console avant chaque nouvel affichage, pour que le menu et le
plateau ne se répliquent pas : un seul écran reste visible à la fois.

```python
if not sys.stdout.isatty():
    return

if os.name == "nt":
    os.system("cls")
else:
    sys.stdout.write("\033[H\033[2J\033[3J")
    sys.stdout.flush()
```

- `sys.stdout.isatty()` évite d'écrire des codes ANSI quand la sortie est
  redirigée vers un fichier ou un pipe ;
- sous Windows, on utilise la commande `cls` ;
- ailleurs, `\033[H` replace le curseur en haut à gauche, `\033[2J`
  efface l'écran et `\033[3J` efface l'historique du terminal.

Cette fonction est appelée au début de `afficher_menu()` et de
`afficher_plateau()`. `afficher_resultat()` ne l'appelle pas : le plateau
final reste ainsi visible sous le résultat.

#### `afficher_menu()`

Efface l'écran puis affiche simplement les trois choix :

```
========================================
              JEU AWALÉ
========================================
  1. Joueur 1 contre Joueur 2
  2. Joueur 1 contre Ordinateur
  3. Quitter
========================================
```

#### `afficher_plateau(plateau, gains, noms)`

Cette fonction construit le plateau ligne par ligne. Contrairement au C,
il n'y a pas de `gotoxy()` : l'alignement est automatique.

```python
largeur = 33

print("=" * largeur)
print(noms['a'].center(largeur))
```

`"abc".center(33)` ajoute des espaces à gauche et à droite pour centrer
le texte dans une largeur de 33 caractères.

Ensuite, on affiche les en-têtes de la rangée `a` :

```python
print("  |" + "|".join(
    f"{label:^4}" for label in ("a6", "a5", "a4", "a3", "a2", "a1")
) + "|")
```

- `f"{label:^4}"` centre le label dans 4 caractères ;
- `"|".join(...)` colle les labels avec des `|` entre eux.

Puis les valeurs de la rangée `a`, de l'indice 5 à 0 :

```python
print("  |" + "|".join(
    f" {plateau[i]:2d} " for i in range(5, -1, -1)
) + "|")
```

- `range(5, -1, -1)` produit `5, 4, 3, 2, 1, 0` ;
- `f"{valeur:2d}"` affiche l'entier sur 2 caractères, aligné à droite.

On fait la même chose pour la rangée `b`, indices 6 à 11, puis on
affiche les gains.

Résultat :

```
=================================
             Joueur 2
  | a6 | a5 | a4 | a3 | a2 | a1 |
  +----+----+----+----+----+----+
  |  4 |  4 |  4 |  4 |  4 |  4 |
  +----+----+----+----+----+----+
  |  4 |  4 |  4 |  4 |  4 |  4 |
  +----+----+----+----+----+----+
  | b1 | b2 | b3 | b4 | b5 | b6 |
             Joueur 1
Gains : Joueur 2 0  |  Joueur 1 0
=================================
```

#### `afficher_resultat(gains, noms, gagnant)`

Affiche :

- `>>> ÉGALITÉ ! <<<` si `gagnant` vaut `None` ;
- `>>> Nom GAGNE ! <<<` sinon ;
- les gains des deux joueurs ;
- une attente sur `Entrée` pour revenir au menu.

---

### 5.6 `main.py` — le chef d'orchestre

#### `demander_coup(plateau, joueur, nom)`

Demande une case jusqu'à obtenir une saisie valide.

```python
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
```

Les vérifications, dans l'ordre :

1. l'entrée n'est pas vide ;
2. c'est bien un nombre (`int(saisie)`) ;
3. le nombre est entre 1 et 6 ;
4. la case correspondante n'est pas vide.

Tant qu'une vérification échoue, on redemande.

> **Pourquoi `try/except` ?**
>
> `int("abc")` lève une exception `ValueError`. Sans `try`, le programme
> s'arrêterait brutalement. Avec `try/except`, on affiche un message et on
> redemande.

#### `afficher_coup(nom, depart, pris)`

Affiche le coup joué sous la forme `a3`, `b5`, etc., puis la capture
éventuelle.

```python
case = f"{rangee_depuis_index(depart)}{numero_depuis_index(depart)}"
print(f"  {nom} joue la case {case}.")

if pris > 0:
    print(f"  --> {nom} capture {pris} graine(s) !")
```

#### `jouer_partie(mode)`

C'est la boucle principale d'une partie.

```python
def jouer_partie(mode):
    init_jeu()
    jeu["mode"] = mode

    noms = NOMS_MODE_1 if mode == 1 else NOMS_MODE_2
    joueur = 'b'

    while not fin_jeu(jeu["plateau"], jeu["gains"]):
        afficher_plateau(jeu["plateau"], jeu["gains"], noms)
        nom = noms[joueur]

        if mode == 2 and joueur == 'a':
            print("  Tour de l'ordinateur...")
            time.sleep(1)

            depart, pris = tour_pc(jeu["plateau"], jeu["gains"], joueur)

            if depart is None:
                break
        else:
            depart = demander_coup(jeu["plateau"], joueur, nom)
            pris = jouer_coup(jeu["plateau"], jeu["gains"], depart, joueur)

        afficher_coup(nom, depart, pris)
        input("  Appuyez sur Entrée pour continuer...")

        joueur = autre_joueur(joueur)

    afficher_plateau(jeu["plateau"], jeu["gains"], noms)
    afficher_resultat(jeu["gains"], noms, gagnant(jeu["gains"]))
```

Décomposition :

1. `init_jeu()` remet la partie à zéro.
2. On mémorise le mode.
3. On choisit les noms affichés.
4. Le joueur `b` (en bas) commence.
5. La boucle continue **tant que la partie n'est pas finie**.
6. À chaque tour :
   - on affiche le plateau ;
   - si c'est l'ordinateur en mode 2, il joue tout seul ;
   - sinon, on demande une case au joueur humain ;
   - on affiche le coup et la capture ;
   - on attend `Entrée` ;
   - on passe la main à l'autre joueur.
7. À la fin, on affiche le plateau final et le résultat.

> **Pourquoi vérifier `fin_jeu` au début de la boucle ?**
>
> Parce qu'un coup peut donner 25 graines ou vider une rangée. Au tour
> suivant, la condition est vraie et la boucle s'arrête. Le plateau final
> est quand même réaffiché après la boucle.

#### `main()`

```python
def main():
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
```

Le menu tourne en boucle jusqu'à ce que le joueur tape `3`.

#### Le point d'entrée

```python
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n  Partie interrompue. Au revoir !")
```

- `if __name__ == "__main__":` signifie « exécute ceci seulement si on
  lance ce fichier directement », pas si on l'importe.
- `KeyboardInterrupt` : l'utilisateur a fait `Ctrl+C`.
- `EOFError` : le flux d'entrée est fermé.
- Dans les deux cas, on quitte proprement au lieu d'afficher une trace
  d'erreur.

---

## 6. Déroulement d'une partie pas à pas

### 6.1 Plateau initial

```
        a6   a5   a4   a3   a2   a1
         4    4    4    4    4    4
         4    4    4    4    4    4
        b1   b2   b3   b4   b5   b6
```

Gains : `a = 0`, `b = 0`.

### 6.2 Premier tour : le joueur 1 joue `b1`

`b1` contient 4 graines. On les sème en `b2`, `b3`, `b4`, `b5`.

Après le coup :

```
        a6   a5   a4   a3   a2   a1
         4    4    4    4    4    4
         0    5    5    5    5    4
        b1   b2   b3   b4   b5   b6
```

La dernière graine est tombée en `b5`, qui est dans la rangée du joueur 1.
Il n'y a donc **pas de capture**.

### 6.3 Deuxième tour : le joueur 2 joue `a1`

`a1` contient 4 graines. On les sème en `a2`, `a3`, `a4`, `a5`.

Après le coup :

```
        a6   a5   a4   a3   a2   a1
         4    5    5    5    5    0
         0    5    5    5    5    4
        b1   b2   b3   b4   b5   b6
```

La dernière graine est tombée en `a5`, dans la rangée du joueur 2.
Pas de capture non plus.

### 6.4 Exemple de capture

Reprenons la situation du test `test_prise_contigue` :

```
a6 = 3
b1 = 4
b2 = 2
b3 = 1
toutes les autres cases = 0
```

Le joueur `a` joue `a6` :

1. `a6` est vidée ;
2. les 3 graines vont en `b1`, `b2`, `b3` ;
3. après semaille : `b1 = 5`, `b2 = 3`, `b3 = 2` ;
4. la dernière case est `b3` (2 graines) ;
5. on capture `b3` (2), puis `b2` (3) ;
6. `b1` vaut 5, donc la capture s'arrête.

Résultat :

```
b1 = 5, b2 = 0, b3 = 0
gains['a'] = 5
```

---

## 7. Les tests expliqués

### 7.1 Pourquoi des tests ?

Un test est un petit programme qui vérifie automatiquement qu'une règle
fonctionne. Si on modifie le code plus tard, on relance les tests : s'ils
passent encore, on n'a rien cassé.

Le projet utilise `unittest`, la bibliothèque de tests intégrée à Python.
Il n'y a donc rien à installer.

### 7.2 Structure d'un test

Un test suit presque toujours trois étapes, appelées **AAA** :

1. **Arrange** (préparer) : construire un plateau précis.
2. **Act** (agir) : appeler la fonction à tester.
3. **Assert** (vérifier) : comparer le résultat attendu au résultat réel.

Exemple :

```python
def test_prise_simple(self):
    # ARRANGE
    plateau, gains = plateau_vide()
    depart = index_depuis_case(6, 'a')
    plateau[depart] = 1
    plateau[index_depuis_case(1, 'b')] = 1

    # ACT
    pris = jouer_coup(plateau, gains, depart, 'a')

    # ASSERT
    self.assertEqual(pris, 2)
    self.assertEqual(gains['a'], 2)
```

### 7.3 La fonction `plateau_vide()`

```python
def plateau_vide():
    return [0] * 12, {'a': 0, 'b': 0}
```

Elle crée un plateau de 12 cases vides et des gains à zéro. C'est très
pratique pour les tests de capture : on peut placer exactement les
graines voulues, sans être gêné par les 4 graines de départ.

### 7.4 Les assertions utilisées

| Assertion | Vérifie que… |
|---|---|
| `assertEqual(a, b)` | `a` est égal à `b` |
| `assertTrue(x)` | `x` est vrai |
| `assertFalse(x)` | `x` est faux |
| `assertIsNone(x)` | `x` vaut `None` |
| `assertIn(a, b)` | `a` se trouve dans `b` |

### 7.5 Les 13 tests du projet

#### Classe `TestDistribution`

| Test | Ce qu'il vérifie | Résultat attendu |
|---|---|---|
| `test_distribution_normale` | 4 graines depuis `a1` vont en `a2`…`a5` | `a1 = 0`, `a2..a5 = 1`, dernier = `a5` |
| `test_on_ne_seme_pas_dans_la_case_de_depart` | 13 graines depuis `a1` ne retombent pas dans `a1` | `a1 = 0`, somme = 13, dernier = `a3` |

#### Classe `TestCapture`

| Test | Ce qu'il vérifie | Résultat attendu |
|---|---|---|
| `test_prise_simple` | Dernière graine sur `b1` qui vaut 2 | 2 graines capturées |
| `test_prise_contigue` | Capture de `b3` (2) puis `b2` (3), arrêt sur `b1` (5) | 5 graines capturées |
| `test_pas_de_prise_dans_sa_propre_rangee` | Dernière graine chez soi | 0 capture |
| `test_la_capture_ne_touche_pas_la_rangee_du_joueur` | La capture ne remonte pas dans sa propre rangée | `a6` reste à 0, plateau vide |

#### Classe `TestFinDePartie`

| Test | Ce qu'il vérifie | Résultat attendu |
|---|---|---|
| `test_init_jeu` | `init_jeu()` remet tout à zéro | 4 partout, gains 0, mode 0 |
| `test_fin_quand_un_joueur_a_25_graines` | Seuil de victoire | `fin_jeu` retourne `True` |
| `test_fin_quand_une_rangee_est_vide` | Règle de famine | `fin_jeu` retourne `True` |
| `test_partie_continue_au_debut` | Partie neuve | `fin_jeu` retourne `False` |
| `test_gagnant` | Comparaison des gains | `'a'`, `'b'` ou `None` |

#### Classe `TestOrdinateur`

| Test | Ce qu'il vérifie | Résultat attendu |
|---|---|---|
| `test_l_ordinateur_choisit_un_coup_valide` | L'IA choisit une case de sa rangée | indice entre 0 et 5 |
| `test_l_ordinateur_choisit_une_prise` | L'IA préfère un coup qui capture | `a6` |

### 7.6 Explication détaillée de `test_prise_contigue`

C'est le test le plus important, car il vérifie la capture complète.

```python
def test_prise_contigue(self):
    plateau, gains = plateau_vide()

    depart = index_depuis_case(6, 'a')  # a6 (indice 5)
    plateau[depart] = 3

    # Avant distribution : b1=4, b2=2, b3=1
    # Après distribution : b1=5, b2=3, b3=2
    plateau[index_depuis_case(1, 'b')] = 4
    plateau[index_depuis_case(2, 'b')] = 2
    plateau[index_depuis_case(3, 'b')] = 1

    pris = jouer_coup(plateau, gains, depart, 'a')

    self.assertEqual(pris, 5)
    self.assertEqual(gains['a'], 5)
    self.assertEqual(plateau[index_depuis_case(3, 'b')], 0)
    self.assertEqual(plateau[index_depuis_case(2, 'b')], 0)
    self.assertEqual(plateau[index_depuis_case(1, 'b')], 5)
```

**Pourquoi ces valeurs ?**

- `a6 = 3` : le joueur va semer 3 graines, donc la dernière tombera en
  `b3`.
- `b3 = 1` : après semaille, `b3` vaut 2 → capturable.
- `b2 = 2` : après semaille, `b2` vaut 3 → capturable.
- `b1 = 4` : après semaille, `b1` vaut 5 → **non capturable**, ce qui
  arrête la capture.

Si on avait mis `b1 = 1`, il serait devenu 2 et aurait aussi été capturé.
Le test vérifie donc à la fois la capture contiguë et l'arrêt correct.

### 7.7 Tester la conservation des graines

En plus des tests unitaires, on peut vérifier un **invariant** : la somme
des graines sur le plateau et dans les gains doit toujours valoir 48.

Voici un petit script à lancer depuis `awale_sans_poo/` :

```python
import random
from struct_game import autre_joueur
from fonc_start_end import fin_jeu
from fonc_action import jouer_coup
from j_vs_pc import choisir_coup_pc

random.seed(0)

for partie in range(1000):
    plateau = [4] * 12
    gains = {'a': 0, 'b': 0}
    joueur = 'b'

    while not fin_jeu(plateau, gains):
        depart = choisir_coup_pc(plateau, gains, joueur)
        if depart is None:
            break
        jouer_coup(plateau, gains, depart, joueur)

        total = sum(plateau) + gains['a'] + gains['b']
        assert total == 48, f"Graines perdues : {total}"

        joueur = autre_joueur(joueur)

print("1000 parties simulées : conservation des 48 graines OK")
```

Ce script a été utilisé pour valider la version actuelle.

---

## 8. Reproduire le projet de zéro

Voici l'ordre conseillé pour réécrire le projet soi-même.

> **Toutes les commandes de cette section se lancent depuis le dossier
> `awale_sans_poo/`.**

### Étape 1 — Créer le dossier et `struct_game.py`

1. Créer un dossier `awale_sans_poo/`.
2. Créer `struct_game.py`.
3. Y mettre :
   - les constantes (`TAILLE_PLATEAU`, `GRAINES_PAR_CASE`,
     `GRAINES_POUR_GAGNER`) ;
   - les noms des modes ;
   - le dictionnaire `jeu` ;
   - les fonctions `index_depuis_case`, `numero_depuis_index`,
     `rangee_depuis_index`, `autre_joueur`.

**Vérification dans le terminal :**

```bash
python3 -c "from struct_game import *; print(index_depuis_case(3, 'b'))"
```

Résultat attendu : `8`.

### Étape 2 — Écrire les règles dans `fonc_action.py`

Dans cet ordre :

1. `distribuer` ;
2. `vider` ;
3. `prise` ;
4. `jouer_coup` ;
5. `coups_possibles`.

**Vérification rapide :**

```bash
python3 -c "from fonc_action import distribuer; p=[4]*12; print(distribuer(p, 0)); print(p)"
```

Résultat attendu : `4` puis `[0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4]`.

### Étape 3 — Écrire `fonc_start_end.py`

1. `init_jeu` ;
2. `fin_jeu` ;
3. `gagnant`.

**Vérification :**

```bash
python3 -c "from fonc_start_end import init_jeu, fin_jeu; from struct_game import jeu; init_jeu(); print(fin_jeu(jeu['plateau'], jeu['gains']))"
```

Résultat attendu : `False`.

### Étape 4 — Écrire `j_vs_pc.py`

1. `choisir_coup_pc` ;
2. `tour_pc`.

**Vérification :**

```bash
python3 -c "from j_vs_pc import choisir_coup_pc; print(choisir_coup_pc([4]*12, {'a':0,'b':0}, 'a'))"
```

Résultat attendu : un entier entre 0 et 5.

### Étape 5 — Écrire `affichage.py`

1. `afficher_menu` ;
2. `afficher_plateau` ;
3. `afficher_resultat`.

**Vérification :**

```bash
python3 -c "from affichage import afficher_plateau; afficher_plateau([4]*12, {'a':0,'b':0}, {'a':'Haut','b':'Bas'})"
```

### Étape 6 — Écrire `main.py`

1. `demander_coup` ;
2. `afficher_coup` ;
3. `jouer_partie` ;
4. `main` ;
5. le bloc `if __name__ == "__main__":`.

**Vérification :**

```bash
python3 main.py
```

Le menu doit s'afficher.

### Étape 7 — Écrire les tests

1. Créer `test_awale.py`.
2. Écrire `plateau_vide`.
3. Écrire les tests de distribution.
4. Écrire les tests de capture.
5. Écrire les tests de fin de partie.
6. Écrire les tests de l'ordinateur.

**Vérification :**

```bash
python3 -m unittest test_awale.py -v
```

Résultat attendu : `Ran 13 tests ... OK`.

### Checklist finale

- [ ] `struct_game.py` : constantes, état, conversions.
- [ ] `fonc_action.py` : distribution et capture.
- [ ] `fonc_start_end.py` : initialisation et fin.
- [ ] `j_vs_pc.py` : IA.
- [ ] `affichage.py` : menu et plateau.
- [ ] `main.py` : boucle de jeu.
- [ ] `test_awale.py` : 13 tests qui passent.
- [ ] Une partie en mode 1 fonctionne.
- [ ] Une partie en mode 2 fonctionne.
- [ ] Les 48 graines sont conservées.

---

## 9. Choix techniques et pièges à éviter

### 9.1 Pourquoi pas de POO ?

Le C d'origine utilise une structure et une variable globale. La version
Python suit la même idée :

- un dictionnaire global `jeu` ;
- des fonctions qui reçoivent les données en paramètres.

C'est parfaitement adapté à un petit jeu et plus simple à suivre pour
quelqu'un qui vient du C.

La version `awale.py` montre l'alternative avec une classe `Jeu`. Elle
est plus « pythonique » pour un gros projet, mais pas nécessaire ici.

### 9.2 Pourquoi passer `plateau` et `gains` en paramètres ?

Parce que cela rend les fonctions :

- **testables** : on peut leur donner un faux plateau ;
- **prévisibles** : elles ne modifient que ce qu'on leur donne ;
- **réutilisables** : l'IA peut les appeler sur une copie.

Si `distribuer` utilisait directement le `jeu` global, il serait difficile
de simuler un coup sans modifier la vraie partie.

### 9.3 Le piège de la réassignation

Mauvais :

```python
def init_jeu():
    jeu = {"plateau": [4] * 12, "gains": {"a": 0, "b": 0}}  # FAUX
```

Ici, `jeu` devient une variable **locale**. Le `jeu` global n'est pas
modifié, et les autres fichiers ne voient rien.

Bon :

```python
def init_jeu():
    jeu["plateau"][:] = [4] * 12
    jeu["gains"]["a"] = 0
    jeu["gains"]["b"] = 0
```

### 9.4 Le piège de la copie pour l'IA

Mauvais :

```python
pris = jouer_coup(plateau, gains, depart, joueur)  # modifie la vraie partie !
```

Bon :

```python
plateau_test = plateau.copy()
gains_test = gains.copy()
pris = jouer_coup(plateau_test, gains_test, depart, joueur)
```

### 9.5 Les erreurs d'indice

Les numéros de case vont de **1 à 6**, mais les indices de liste vont de
**0 à 11**. Il faut toujours passer par `index_depuis_case`.

Erreur classique :

```python
plateau[numero] = 0   # FAUX : numero vaut 1..6, pas l'indice
```

Correct :

```python
plateau[index_depuis_case(numero, joueur)] = 0
```

### 9.6 Oublier le `% 12`

Sans modulo, après la case 11 on sortirait de la liste :

```python
position = position + 1          # FAUX après 11
position = (position + 1) % 12   # CORRECT
```

### 9.7 Oublier de sauter la case de départ

Si on ne saute pas la case de départ, on remet une graine dedans, ce qui
est interdit à l'Awalé.

```python
if position == depart:
    continue
```

### 9.8 La capture doit partir de la dernière case

Ne jamais faire :

```python
for i in range(6, 0, -1):   # FAUX : ne part pas de la dernière case semée
```

Il faut partir de `dernier`, puis reculer :

```python
position = dernier
while ...:
    ...
    position = (position - 1) % 12
```

### 9.9 Ne pas capturer dans sa propre rangée

La condition suivante est essentielle :

```python
if rangee_depuis_index(dernier) != adversaire:
    return 0
```

Sans elle, on pourrait capturer ses propres graines.

### 9.10 Ne pas oublier de changer de joueur

À la fin de chaque tour :

```python
joueur = autre_joueur(joueur)
```

Sinon, le même joueur rejoue indéfiniment.

---

## 10. Bugs du code C corrigés

| Bug dans le C | Conséquence | Correction en Python |
|---|---|---|
| `prise()` commençait toujours à la case 6 | Capturait des cases sans rapport avec le coup | On part de la dernière case semée |
| `fin_jeu()` arrêtait si `total_graines <= 3` | Parties terminées trop tôt | Condition supprimée |
| Test `24-24` redondant | Fin de partie incohérente | Supprimé, seuls 25 graines et famine comptent |
| `init_jeu()` ne libérait pas l'ancienne liste | Fuite mémoire | Le garbage collector Python s'en charge |
| `lire_coup()` bouclait sur une entrée invalide ou `EOF` | Blocage du programme | Saisie validée, `Ctrl+C`/`EOF` gérés |
| `windows.h`, `conio.h`, `gotoxy`, `Sleep` | Code non portable | Affichage console portable |
| Affichage avec positions codées en dur | Alignement fragile | Plateau construit ligne par ligne |
| IA purement aléatoire | Jeu peu intéressant | IA qui choisit la meilleure capture immédiate |
| Pas de vérification que la case appartient au joueur | Coup invalide possible | Vérifié dans `jouer_coup` |
| Liste chaînée complexe | Code difficile à lire | Liste de 12 entiers |

---

## 11. Pour aller plus loin

Voici des exercices pour améliorer le projet.

### 11.1 Choisir sa rangée

Au début d'une partie à deux joueurs, demander au joueur 1 s'il veut
jouer `a` ou `b`, puis attribuer l'autre rangée au joueur 2.

### 11.2 Interdire de capturer toutes les graines adverses

Certaines variantes interdisent de prendre **toutes** les graines de
l'adversaire. Avant d'appliquer la capture, calculer le total des graines
adverses. Si la capture les prend toutes, annuler la capture.

### 11.3 Améliorer l'IA

L'IA actuelle regarde seulement la capture immédiate. On peut :

- simuler la meilleure réponse de l'adversaire ;
- préférer les coups qui laissent peu de graines à l'adversaire ;
- ajouter une difficulté (facile / moyen / difficile).

### 11.4 Sauvegarder les scores

Écrire les résultats dans un fichier `scores.txt` avec la date et le
nom des joueurs.

### 11.5 Faire une interface graphique

Utiliser `tkinter` (inclus dans Python) pour dessiner le plateau et
cliquer sur les cases.

### 11.6 Ajouter un historique

Conserver la liste des coups joués pour pouvoir rejouer une partie.

### 11.7 Tests supplémentaires

- Une partie complète simulée.
- Un test qui vérifie que la somme des graines vaut toujours 48.
- Un test pour chaque fonction de conversion.

---

## 12. Lexique

| Terme | Définition |
|---|---|
| **Graine** | Unité de jeu. Il y en a 48 au départ. |
| **Case** | Un des 12 trous du plateau. |
| **Rangée** | Les 6 cases d'un joueur (`a` ou `b`). |
| **Semer** | Déposer une graine par case en avançant. |
| **Capturer** | Prendre les graines d'une case adverse à 2 ou 3 graines. |
| **Gains** | Total des graines capturées par un joueur. |
| **Famine** | Situation où une rangée est vide. |
| **Majorité absolue** | 25 graines sur 48. |
| **Anti-horaire** | Sens de distribution `a1 → a2 → … → b6 → a1`. |
| **Indice** | Position dans la liste Python (0 à 11). |
| **Numéro** | Numéro affiché d'une case (1 à 6). |
| **Invariant** | Propriété qui doit toujours rester vraie (ici : 48 graines en tout). |

---

## En résumé

- Le plateau est une **liste de 12 entiers**.
- Le sens de distribution est **`a1 → a2 → … → b6 → a1`**.
- On saute toujours la case de départ.
- La capture part de la **dernière case semée** et remonte tant que les
  cases adverses valent 2 ou 3.
- La partie s'arrête à **25 graines** ou si une rangée est vide.
- Les tests vérifient chaque règle sur des plateaux construits à la main.
- Pour reproduire le projet : suivre les étapes de la section 8.

Bon jeu et bon code !
