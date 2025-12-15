"""
Toolvard RPG - Noise Generator
Wrapper pour le bruit Perlin/Simplex
"""

import math
from opensimplex import OpenSimplex
import config


class NoiseGenerator:
    """Générateur de bruit pour terrain procédural"""
    
    def __init__(self, seed: int = None):
        self.seed = seed or config.WORLD_SEED
        self.simplex = OpenSimplex(seed=self.seed)
        
    def noise2d(self, x: float, z: float) -> float:
        """Bruit 2D simple entre -1 et 1"""
        return self.simplex.noise2(x, z)
    
    def noise3d(self, x: float, y: float, z: float) -> float:
        """Bruit 3D simple entre -1 et 1"""
        return self.simplex.noise3(x, y, z)
    
    def octave_noise2d(
        self, 
        x: float, 
        z: float, 
        octaves: int = None,
        persistence: float = None,
        lacunarity: float = None,
        scale: float = None
    ) -> float:
        """
        Bruit 2D avec plusieurs octaves (fractal brownian motion)
        Retourne une valeur entre 0 et 1
        """
        octaves = octaves or config.TERRAIN_OCTAVES
        persistence = persistence or config.TERRAIN_PERSISTENCE
        lacunarity = lacunarity or config.TERRAIN_LACUNARITY
        scale = scale or config.TERRAIN_SCALE
        
        total = 0.0
        frequency = scale
        amplitude = 1.0
        max_value = 0.0
        
        for _ in range(octaves):
            total += self.noise2d(x * frequency, z * frequency) * amplitude
            max_value += amplitude
            amplitude *= persistence
            frequency *= lacunarity
            
        # Normaliser entre 0 et 1
        return (total / max_value + 1.0) / 2.0
    
    def octave_noise3d(
        self,
        x: float,
        y: float,
        z: float,
        octaves: int = 3,
        persistence: float = 0.5,
        scale: float = 0.05
    ) -> float:
        """Bruit 3D avec octaves (pour caves)"""
        total = 0.0
        frequency = scale
        amplitude = 1.0
        max_value = 0.0
        
        for _ in range(octaves):
            total += self.noise3d(x * frequency, y * frequency, z * frequency) * amplitude
            max_value += amplitude
            amplitude *= persistence
            frequency *= 2.0
            
        return (total / max_value + 1.0) / 2.0
    
    def get_biome_value(self, x: float, z: float) -> float:
        """Valeur pour déterminer le biome (variation lente)"""
        return self.octave_noise2d(x, z, octaves=2, scale=0.005)
    
    def get_temperature(self, x: float, z: float) -> float:
        """Température pour variation de biome"""
        return self.octave_noise2d(x + 1000, z + 1000, octaves=2, scale=0.008)
    
    def get_humidity(self, x: float, z: float) -> float:
        """Humidité pour variation de biome"""
        return self.octave_noise2d(x + 2000, z + 2000, octaves=2, scale=0.008)
