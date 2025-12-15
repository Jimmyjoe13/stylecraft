"""
Toolvard RPG - Configuration globale
"""

# === WINDOW ===
WINDOW_TITLE = "Toolvard RPG - Le Monde de l'Astral"
WINDOW_SIZE = (1280, 720)
FULLSCREEN = False
VSYNC = True

# === WORLD GENERATION ===
CHUNK_SIZE = 16          # Largeur/profondeur d'un chunk
CHUNK_HEIGHT = 32        # Hauteur maximale (réduite pour perf)
RENDER_DISTANCE = 2      # Chunks visibles autour du joueur (réduit pour démarrage rapide)
WORLD_SEED = 42          # Seed pour génération procédurale

# === TERRAIN ===
SEA_LEVEL = 20
TERRAIN_SCALE = 0.02     # Échelle du bruit Perlin
TERRAIN_OCTAVES = 4
TERRAIN_PERSISTENCE = 0.5
TERRAIN_LACUNARITY = 2.0

# === PLAYER ===
PLAYER_SPEED = 5
PLAYER_JUMP_HEIGHT = 2
PLAYER_GRAVITY = 0.5
MOUSE_SENSITIVITY = 40

# === ASTRAL SYSTEM ===
MAX_HP = 100
MAX_ASTRAL = 100
ASTRAL_REGEN_RATE = 1    # Points par seconde

# === COMBAT ===
BASE_ATTACK_DAMAGE = 10
CETRA_STRENGTH_BONUS = 1.5
TETRA_MAGIC_BONUS = 1.5

# === RACES ===
RACE_CETRA = "cetra"
RACE_TETRA = "tetra"
RACE_SANGMELE = "sangmele"

# === BIOMES ===
BIOME_TERRES_GRISES = "terres_grises"      # Asmodia
BIOME_CITE_CRISTALLINE = "cite_cristalline" # Élyséia
BIOME_PORT_BRUME = "port_brume"
BIOME_KARTHAX = "karthax"
BIOME_FORET_ETERNITE = "foret_eternite"
BIOME_ASTRAL_NOIR = "astral_noir"

# === DEBUG ===
DEBUG_MODE = True
SHOW_FPS = True
SHOW_CHUNK_BORDERS = False
