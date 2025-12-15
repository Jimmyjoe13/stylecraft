# 🌌 Toolvard RPG - Le Monde de l'Astral

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Ursina](https://img.shields.io/badge/Ursina-6.0+-FF6B6B?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-En%20Développement-yellow?style=for-the-badge)

_Un RPG 3D voxel immersif basé sur l'univers original de Toolvard_

[🎮 Jouer](#-installation) • [📖 Lore](#-lunivers-de-toolvard) • [🛠️ Contribuer](#-contribution)

</div>

---

## 📋 Table des Matières

- [🌟 Présentation](#-présentation)
- [✨ Fonctionnalités](#-fonctionnalités)
- [🎭 L'Univers de Toolvard](#-lunivers-de-toolvard)
- [🚀 Installation](#-installation)
- [🎮 Comment Jouer](#-comment-jouer)
- [🏗️ Architecture Technique](#️-architecture-technique)
- [🌍 Système de Monde](#-système-de-monde)
- [📊 Configuration](#-configuration)
- [🗺️ Roadmap](#️-roadmap)
- [🤝 Contribution](#-contribution)

---

## 🌟 Présentation

**Toolvard RPG** est un jeu de rôle voxel 3D développé avec le moteur **Ursina** (Python). Le jeu plonge les joueurs dans un univers fantastique riche où deux empires millénaires s'affrontent pour le contrôle de l'**Astral**, une énergie mystique qui imprègne tout le monde de Toolvard.

Incarnez un **Cetra**, un **Tetra**, ou un rare **Sang-Mêlé (Convergent)**, et forgez votre destin dans un monde en proie à la guerre, aux dragons anciens et à la corruption de l'Astral Noir.

### 🎯 Points Forts

- 🗺️ **Monde procédural** généré avec du bruit Simplex
- ⚔️ **Système de combat** basé sur les statistiques et l'Astral
- 🧬 **3 races jouables** avec des bonus uniques
- 🌋 **6 biomes distincts** inspirés du lore
- 📈 **Système de progression** avec niveaux et compétences
- 🎨 **Rendu voxel optimisé** avec culling des faces

---

## ✨ Fonctionnalités

### 🎭 Système de Races

| Race          | Spécialité      | Bonus                                     |
| ------------- | --------------- | ----------------------------------------- |
| **Cetra**     | Force & Vitesse | +50% Force, +30% Vitesse, -20% Magie      |
| **Tetra**     | Magie & Soins   | +50% Magie, +30% Régénération, -20% Force |
| **Sang-Mêlé** | Équilibré       | Accès aux deux voies                      |

### ⚔️ Système de Combat

- **Attaque légère** (Clic gauche) - Dégâts rapides
- **Attaque lourde** - Consomme de l'Astral pour des dégâts massifs
- **Parade** (Clic droit) - Réduit les dégâts entrants de 50%
- **Compétences** (Touches 1-4) - Sorts et techniques spéciales

### 🌍 Monde Voxel

- **Chunks 16×32×16** générés procéduralement
- **30+ types de blocs** thématiques
- **Système de biomes** avec transitions naturelles
- **Distance de rendu** configurable

---

## 🎭 L'Univers de Toolvard

> _"Dix mille ans. Une éternité gravée dans le sang, l'acier et la magie."_

### 📜 Histoire

Il y a 10 000 ans, les **Dragons Anciens** régnaient sur Toolvard. Le roi **Tanas**, un Teostra Alpha, gouvernait par la terreur. Les races humanoïdes — **Cetras** et **Tetras** — vivaient en esclavage.

Deux héros changèrent le cours de l'histoire :

- **Asmond** - Guerrier Cetra légendaire
- **Élyséa** - La plus grande magicienne Tetra

Ensemble, ils menèrent la **Grande Rébellion** et renversèrent les dragons. Mais leur alliance se brisa, et deux empires rivaux naquirent.

### ⚔️ Les Empires

| Empire      | Race   | Capitale          | Philosophie                  |
| ----------- | ------ | ----------------- | ---------------------------- |
| **Asmodia** | Cetras | Les Terres Grises | Force, Industrie, Hiérarchie |
| **Élyséia** | Tetras | Cité Cristalline  | Magie, Sagesse, Harmonie     |

### 🌋 Les Biomes

| Biome                    | Description                     | Ressources Clés                        |
| ------------------------ | ------------------------------- | -------------------------------------- |
| **Terres Grises**        | Territoire industriel d'Asmodia | Fer, Charbon, Obsidienne               |
| **Cité Cristalline**     | Merveille magique d'Élyséia     | Cristaux d'Astral, Marbre              |
| **Port-Brume**           | Zone neutre commerciale         | Trésors cachés                         |
| **Montagnes de Karthax** | Repaire des dragons             | Minerai de Karthax, Écailles de Dragon |
| **Forêt d'Éternité**     | Forêt sacrée ancienne           | Bois Ancien, Essence d'Astral          |
| **Astral Noir**          | Zones de corruption             | Blocs corrompus                        |

### 🏆 Légendes Vivantes

- **Darius Realvor** - Sparta n°1, 2500 ans d'expérience
- **Kyle Realvor** - Sparta n°2 (le plus puissant en réalité)
- **Krad Maoury** - L'Archange guerrier-mage

> 📖 _Consultez `Toolvard_Lore_Complet.md` pour l'histoire détaillée_

---

## 🚀 Installation

### Prérequis

- **Python 3.8+**
- Carte graphique compatible OpenGL

### Installation Rapide

```bash
# Cloner le projet
git clone https://github.com/votre-repo/stylecraft.git
cd stylecraft

# Installer les dépendances
pip install -r requirements.txt

# Lancer le jeu
python main.py
```

### Dépendances

```
ursina>=6.0.0      # Moteur de jeu 3D
perlin-noise>=1.12 # Génération de bruit
opensimplex>=0.4   # Bruit Simplex optimisé
numpy>=1.24.0      # Calculs numériques
pillow>=10.0.0     # Manipulation d'images
```

---

## 🎮 Comment Jouer

### Contrôles

| Touche        | Action                   |
| ------------- | ------------------------ |
| `WASD`        | Déplacement              |
| `Souris`      | Regarder autour          |
| `Espace`      | Sauter                   |
| `Shift`       | Sprint (consomme Astral) |
| `Clic Gauche` | Attaque légère           |
| `Clic Droit`  | Parade                   |
| `1-4`         | Compétences              |
| `Échap`       | Pause                    |

### Démarrage

1. Lancez le jeu avec `python main.py`
2. Choisissez votre race (1, 2 ou 3)
3. Explorez le monde généré procéduralement
4. Combattez, gagnez de l'XP, et progressez !

---

## 🏗️ Architecture Technique

```
stylecraft/
├── main.py                 # Point d'entrée & GameManager
├── config.py               # Configuration globale
├── requirements.txt        # Dépendances Python
│
├── engine/                 # Moteur de jeu
│   ├── voxel_engine.py     # Moteur voxel principal
│   ├── chunk_manager.py    # Gestion des chunks
│   └── block_registry.py   # Registre des 30+ blocs
│
├── entities/               # Entités du jeu
│   └── player.py           # Joueur avec système Astral
│
├── world/                  # Génération de monde
│   ├── terrain_generator.py  # Génération procédurale
│   ├── biome_manager.py      # 6 biomes de Toolvard
│   └── noise_generator.py    # Bruit Simplex/Perlin
│
├── ui/                     # Interface utilisateur
│   └── hud.py              # HUD (vie, Astral, stats)
│
└── Toolvard_Lore_Complet.md  # Lore de l'univers
```

### 🔧 Composants Clés

#### VoxelEngine

Moteur principal gérant le monde voxel :

- Initialisation et mise à jour du monde
- Gestion des blocs (get/set/break)
- Raycast pour détection de blocs

#### ChunkManager

Système de chunks avec lazy loading :

- Génération/destruction dynamique des chunks
- Building de mesh optimisé (face culling)
- Conversion coordonnées monde ↔ chunk

#### TerrainGenerator

Génération procédurale :

- Bruit Simplex multi-octaves
- Sélection de biomes par température/humidité
- Placement de blocs spéciaux et arbres

#### Player

Joueur avec système RPG complet :

- Statistiques (HP, Astral, Force, Magie, etc.)
- Bonus de race
- Système de progression (XP, niveaux)
- Mécaniques de combat

---

## 🌍 Système de Monde

### Génération de Terrain

Le terrain est généré avec **Fractal Brownian Motion** :

```python
# Paramètres de génération
TERRAIN_SCALE = 0.02       # Échelle du bruit
TERRAIN_OCTAVES = 4        # Détail du terrain
TERRAIN_PERSISTENCE = 0.5  # Amplitude des octaves
TERRAIN_LACUNARITY = 2.0   # Fréquence des octaves
```

### Types de Blocs

Le jeu contient **30+ types de blocs** organisés par thème :

| Catégorie       | Exemples                                       |
| --------------- | ---------------------------------------------- |
| **Base**        | Air, Pierre, Terre, Herbe, Sable, Eau          |
| **Asmodia**     | Fer d'Asmodia, Obsidienne, Brique, Forge Cetra |
| **Élyséia**     | Cristal d'Astral, Marbre, Bloc de Cristal      |
| **Karthax**     | Minerai de Karthax, Lave, Écaille de Dragon    |
| **Forêt**       | Bois Ancien, Essence d'Astral, Feuilles        |
| **Corruption**  | Corruption, Pierre Corrompue                   |
| **Utilitaires** | Établi, Coffre, Torche, Portail                |

---

## 📊 Configuration

Le fichier `config.py` permet de personnaliser le jeu :

```python
# Fenêtre
WINDOW_SIZE = (1280, 720)
FULLSCREEN = False

# Monde
CHUNK_SIZE = 16
RENDER_DISTANCE = 2
WORLD_SEED = 42

# Joueur
PLAYER_SPEED = 5
MOUSE_SENSITIVITY = 40

# Combat
MAX_HP = 100
MAX_ASTRAL = 100
BASE_ATTACK_DAMAGE = 10

# Debug
DEBUG_MODE = True
SHOW_FPS = True
```

---

## 🗺️ Roadmap

### ✅ Implémenté

- [x] Moteur voxel de base
- [x] Génération procédurale avec biomes
- [x] Système de race (Cetra/Tetra/Sang-Mêlé)
- [x] Contrôles FPS (FirstPersonController)
- [x] HUD avec barres de vie/Astral/XP
- [x] Système de combat basique
- [x] Système de progression (XP, niveaux)

### 🔄 En cours

- [ ] Ennemis et IA
- [ ] Système d'inventaire
- [ ] Compétences spéciales par race

### 📅 Planifié

- [ ] Quêtes et PNJs
- [ ] Donjons générés
- [ ] Mode multijoueur
- [ ] Système de craft
- [ ] Boss (Dragons anciens)
- [ ] Sauvegarde/Chargement

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment participer :

1. **Fork** le projet
2. Créez une **branche feature** (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une **Pull Request**

### 📝 Guidelines

- Suivez le style de code existant
- Documentez les nouvelles fonctions
- Testez vos modifications
- Respectez le lore de Toolvard

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 🙏 Remerciements

- **Ursina Engine** - Pour ce fantastique moteur de jeu Python
- **OpenSimplex** - Pour la génération de bruit optimisée
- L'équipe de développement et les testeurs

---

<div align="center">

**⭐ Si ce projet vous plaît, n'hésitez pas à lui donner une étoile !**

_Fait avec ❤️ et beaucoup de ☕_

_An 0 — L'Aube du Changement_

</div>
