"""
Toolvard RPG - Terrain Generator
Génération procédurale du terrain avec biomes
"""

import numpy as np
from typing import Tuple
import config
from engine.block_registry import BlockRegistry
from world.noise_generator import NoiseGenerator
from world.biome_manager import BiomeManager


class TerrainGenerator:
    """Générateur de terrain procédural pour Toolvard"""
    
    def __init__(self, seed: int = None):
        self.noise = NoiseGenerator(seed)
        self.chunk_size = config.CHUNK_SIZE
        self.chunk_height = config.CHUNK_HEIGHT
        self.sea_level = config.SEA_LEVEL
        
    def generate_chunk(self, chunk_x: int, chunk_z: int) -> np.ndarray:
        """
        Génère un chunk de terrain
        Retourne un array numpy 3D de block IDs
        """
        # Créer le tableau vide (rempli d'air)
        chunk = np.zeros((self.chunk_size, self.chunk_height, self.chunk_size), dtype=np.uint8)
        
        # Générer le terrain bloc par bloc
        for x in range(self.chunk_size):
            for z in range(self.chunk_size):
                # Position mondiale
                world_x = chunk_x * self.chunk_size + x
                world_z = chunk_z * self.chunk_size + z
                
                # Déterminer le biome
                biome = self._get_biome_at(world_x, world_z)
                
                # Calculer la hauteur du terrain
                height = self._get_height(world_x, world_z, biome)
                
                # Remplir la colonne
                self._fill_column(chunk, x, z, height, biome)
        
        # Générer les caves (désactivé pour perf)
        # self._carve_caves(chunk, chunk_x, chunk_z)
        
        return chunk
    
    def _get_biome_at(self, x: int, z: int):
        """Détermine le biome à une position"""
        noise_val = self.noise.get_biome_value(x, z)
        temp = self.noise.get_temperature(x, z)
        humidity = self.noise.get_humidity(x, z)
        return BiomeManager.get_biome_at(x, z, noise_val, temp, humidity)
    
    def _get_height(self, x: int, z: int, biome) -> int:
        """Calcule la hauteur du terrain à une position"""
        # Valeur de bruit normalisée 0-1
        noise_val = self.noise.octave_noise2d(x, z)
        
        # Interpoler entre min et max height du biome
        height = int(biome.min_height + noise_val * (biome.max_height - biome.min_height))
        
        # Limiter à la hauteur du chunk
        return min(height, self.chunk_height - 1)
    
    def _fill_column(self, chunk: np.ndarray, x: int, z: int, height: int, biome):
        """Remplit une colonne verticale avec les blocs appropriés"""
        
        # Bedrock au fond (indestructible)
        chunk[x, 0, z] = BlockRegistry.BEDROCK
        
        # Pierre/bloc de base
        for y in range(1, height - 3):
            chunk[x, y, z] = biome.stone_block
            
            # Chance d'ajouter des blocs spéciaux (minerais, etc.)
            for special_block, prob in biome.special_blocks:
                if np.random.random() < prob:
                    chunk[x, y, z] = special_block
                    break
        
        # Sous-surface (3 blocs)
        for y in range(max(1, height - 3), height):
            chunk[x, y, z] = biome.subsurface_block
        
        # Surface
        if height > 0:
            chunk[x, height, z] = biome.surface_block
        
        # Eau si sous le niveau de la mer
        if height < self.sea_level:
            for y in range(height + 1, self.sea_level + 1):
                chunk[x, y, z] = BlockRegistry.WATER
    
    def _carve_caves(self, chunk: np.ndarray, chunk_x: int, chunk_z: int):
        """Génère des caves dans le chunk"""
        cave_threshold = 0.65  # Seuil pour créer une cave
        
        for x in range(self.chunk_size):
            for z in range(self.chunk_size):
                for y in range(2, self.chunk_height - 10):  # Pas de caves trop hautes/basses
                    world_x = chunk_x * self.chunk_size + x
                    world_z = chunk_z * self.chunk_size + z
                    
                    # Valeur de bruit 3D pour les caves
                    cave_noise = self.noise.octave_noise3d(world_x, y, world_z)
                    
                    # Si au-dessus du seuil et pas bedrock/eau, creuser
                    if cave_noise > cave_threshold:
                        current_block = chunk[x, y, z]
                        if current_block != BlockRegistry.BEDROCK and current_block != BlockRegistry.WATER:
                            chunk[x, y, z] = BlockRegistry.AIR
    
    def generate_trees(self, chunk: np.ndarray, chunk_x: int, chunk_z: int):
        """Génère des arbres dans le chunk (appelé séparément)"""
        for x in range(2, self.chunk_size - 2):
            for z in range(2, self.chunk_size - 2):
                world_x = chunk_x * self.chunk_size + x
                world_z = chunk_z * self.chunk_size + z
                
                # Obtenir le biome
                biome = self._get_biome_at(world_x, world_z)
                
                # Probabilité d'arbre basée sur densité du biome
                if np.random.random() < biome.tree_density:
                    # Trouver la surface
                    for y in range(self.chunk_height - 1, 0, -1):
                        if chunk[x, y, z] != BlockRegistry.AIR and chunk[x, y, z] != BlockRegistry.WATER:
                            # Surface trouvée, placer arbre
                            if chunk[x, y, z] in [BlockRegistry.GRASS, BlockRegistry.DIRT, BlockRegistry.ANCIENT_WOOD]:
                                self._place_tree(chunk, x, y + 1, z, biome)
                            break
    
    def _place_tree(self, chunk: np.ndarray, x: int, y: int, z: int, biome):
        """Place un arbre à la position donnée"""
        # Vérifier qu'on a assez de place
        tree_height = np.random.randint(4, 7)
        if y + tree_height >= self.chunk_height:
            return
        
        # Déterminer les blocs selon le biome
        if biome.id == config.BIOME_FORET_ETERNITE:
            log_block = BlockRegistry.ANCIENT_WOOD
            leaf_block = BlockRegistry.LEAVES
        elif biome.id == config.BIOME_CITE_CRISTALLINE:
            log_block = BlockRegistry.CRYSTAL_BLOCK
            leaf_block = BlockRegistry.CRYSTAL_ASTRAL
        else:
            log_block = BlockRegistry.LOG
            leaf_block = BlockRegistry.LEAVES
        
        # Tronc
        for dy in range(tree_height):
            if y + dy < self.chunk_height:
                chunk[x, y + dy, z] = log_block
        
        # Feuillage (sphère simple)
        leaf_start = y + tree_height - 2
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                for dy in range(3):
                    nx, ny, nz = x + dx, leaf_start + dy, z + dz
                    if (0 <= nx < self.chunk_size and 
                        0 <= ny < self.chunk_height and 
                        0 <= nz < self.chunk_size):
                        if chunk[nx, ny, nz] == BlockRegistry.AIR:
                            # Forme arrondie
                            if abs(dx) + abs(dz) + abs(dy - 1) <= 3:
                                chunk[nx, ny, nz] = leaf_block
