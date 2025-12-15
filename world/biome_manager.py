"""
Toolvard RPG - Biome Manager
Gestion des 6 biomes du monde de Toolvard
"""

from dataclasses import dataclass
from typing import Tuple, List
import config
from engine.block_registry import BlockRegistry


@dataclass
class Biome:
    """Représente un biome du monde"""
    id: str
    name: str
    surface_block: int           # Bloc de surface
    subsurface_block: int        # Bloc sous la surface
    stone_block: int             # Bloc de pierre
    special_blocks: List[Tuple[int, float]]  # (block_id, probabilité)
    min_height: int              # Hauteur min du terrain
    max_height: int              # Hauteur max du terrain
    tree_density: float          # Densité d'arbres (0-1)
    enemy_types: List[str]       # Types d'ennemis qui spawn


class BiomeManager:
    """Gestionnaire des biomes de Toolvard"""
    
    _biomes: dict = {}
    
    @classmethod
    def init(cls):
        """Initialise tous les biomes"""
        
        # === TERRES GRISES (Asmodia - Empire Cetra) ===
        cls._register(Biome(
            id=config.BIOME_TERRES_GRISES,
            name="Terres Grises d'Asmodia",
            surface_block=BlockRegistry.DIRT,
            subsurface_block=BlockRegistry.STONE,
            stone_block=BlockRegistry.IRON_ASMODIA,
            special_blocks=[
                (BlockRegistry.COAL, 0.05),
                (BlockRegistry.IRON_ASMODIA, 0.03),
                (BlockRegistry.OBSIDIAN, 0.01),
            ],
            min_height=15,
            max_height=40,
            tree_density=0.02,
            enemy_types=["soldier_cetra", "berserker"]
        ))
        
        # === CITÉ CRISTALLINE (Élyséia - Empire Tetra) ===
        cls._register(Biome(
            id=config.BIOME_CITE_CRISTALLINE,
            name="Cité Cristalline d'Élyséia",
            surface_block=BlockRegistry.MARBLE,
            subsurface_block=BlockRegistry.STONE,
            stone_block=BlockRegistry.CRYSTAL_BLOCK,
            special_blocks=[
                (BlockRegistry.CRYSTAL_ASTRAL, 0.08),
                (BlockRegistry.ASTRAL_ESSENCE, 0.03),
            ],
            min_height=20,
            max_height=50,
            tree_density=0.05,
            enemy_types=["mage_tetra", "healer"]
        ))
        
        # === PORT-BRUME (Zone Neutre) ===
        cls._register(Biome(
            id=config.BIOME_PORT_BRUME,
            name="Port-Brume",
            surface_block=BlockRegistry.MIST_STONE,
            subsurface_block=BlockRegistry.STONE,
            stone_block=BlockRegistry.STONE,
            special_blocks=[
                (BlockRegistry.CHEST, 0.001),  # Trésors cachés
            ],
            min_height=10,
            max_height=30,
            tree_density=0.03,
            enemy_types=["mercenary", "smuggler"]
        ))
        
        # === MONTAGNES DE KARTHAX (Dragons) ===
        cls._register(Biome(
            id=config.BIOME_KARTHAX,
            name="Montagnes de Karthax",
            surface_block=BlockRegistry.STONE,
            subsurface_block=BlockRegistry.OBSIDIAN,
            stone_block=BlockRegistry.OBSIDIAN,
            special_blocks=[
                (BlockRegistry.KARTHAX_ORE, 0.04),
                (BlockRegistry.DRAGON_SCALE, 0.005),
                (BlockRegistry.LAVA, 0.02),
            ],
            min_height=30,
            max_height=64,  # Très hautes montagnes
            tree_density=0.0,
            enemy_types=["dragon_young", "prospector"]
        ))
        
        # === FORÊT D'ÉTERNITÉ ===
        cls._register(Biome(
            id=config.BIOME_FORET_ETERNITE,
            name="Forêt d'Éternité",
            surface_block=BlockRegistry.GRASS,
            subsurface_block=BlockRegistry.DIRT,
            stone_block=BlockRegistry.ANCIENT_WOOD,
            special_blocks=[
                (BlockRegistry.ASTRAL_ESSENCE, 0.05),
                (BlockRegistry.ANCIENT_WOOD, 0.1),
            ],
            min_height=18,
            max_height=35,
            tree_density=0.4,  # Forêt dense
            enemy_types=["astral_beast", "guardian"]
        ))
        
        # === ZONES D'ASTRAL NOIR (Corruption) ===
        cls._register(Biome(
            id=config.BIOME_ASTRAL_NOIR,
            name="Zones d'Astral Noir",
            surface_block=BlockRegistry.CORRUPTED_STONE,
            subsurface_block=BlockRegistry.CORRUPTION,
            stone_block=BlockRegistry.CORRUPTION,
            special_blocks=[
                (BlockRegistry.CORRUPTION, 0.2),
            ],
            min_height=5,
            max_height=25,
            tree_density=0.01,
            enemy_types=["abomination", "specter"]
        ))
        
    @classmethod
    def _register(cls, biome: Biome):
        """Enregistre un biome"""
        cls._biomes[biome.id] = biome
        
    @classmethod
    def get(cls, biome_id: str) -> Biome:
        """Récupère un biome par son ID"""
        return cls._biomes.get(biome_id, cls._biomes[config.BIOME_TERRES_GRISES])
    
    @classmethod
    def get_biome_at(cls, x: float, z: float, noise_value: float, temp: float, humidity: float) -> Biome:
        """
        Détermine le biome à une position donnée
        basé sur les valeurs de bruit, température et humidité
        """
        # Logique simplifiée de sélection de biome
        # En production, utiliser Voronoi ou transition plus douce
        
        # Astral Noir: zones de corruption (valeur très basse)
        if noise_value < 0.15:
            return cls._biomes[config.BIOME_ASTRAL_NOIR]
        
        # Karthax: hautes montagnes (valeur très haute)
        if noise_value > 0.75:
            return cls._biomes[config.BIOME_KARTHAX]
        
        # Basé sur température et humidité
        if temp > 0.6:
            # Chaud
            if humidity > 0.5:
                return cls._biomes[config.BIOME_FORET_ETERNITE]
            else:
                return cls._biomes[config.BIOME_TERRES_GRISES]
        else:
            # Froid
            if humidity > 0.5:
                return cls._biomes[config.BIOME_CITE_CRISTALLINE]
            else:
                return cls._biomes[config.BIOME_PORT_BRUME]


# Initialiser au chargement
BiomeManager.init()
