"""
Toolvard RPG - Block Registry
Définition des 30+ types de blocs du monde de Toolvard
"""

from dataclasses import dataclass
from typing import Optional, Tuple
from ursina import color


@dataclass
class Block:
    """Représente un type de bloc dans le monde"""
    id: int
    name: str
    color: Tuple[float, float, float]  # RGB 0-1
    hardness: float = 1.0              # Temps de minage
    transparent: bool = False
    solid: bool = True
    drop_id: Optional[int] = None      # ID du bloc droppé (None = même bloc)
    biome: Optional[str] = None        # Biome principal
    light_level: int = 0               # Émission de lumière (0-15)


class BlockRegistry:
    """Registre de tous les types de blocs"""
    
    # IDs des blocs
    AIR = 0
    DIRT = 1
    GRASS = 2
    STONE = 3
    IRON_ASMODIA = 4
    OBSIDIAN = 5
    CRYSTAL_ASTRAL = 6
    MARBLE = 7
    ANCIENT_WOOD = 8
    MIST_STONE = 9
    LAVA = 10
    CORRUPTION = 11
    KARTHAX_ORE = 12
    ASTRAL_ESSENCE = 13
    SAND = 14
    WATER = 15
    COAL = 16
    TITANIUM = 17
    BEDROCK = 18
    LEAVES = 19
    LOG = 20
    GLASS = 21
    BRICK_ASMODIA = 22
    CRYSTAL_BLOCK = 23
    CORRUPTED_STONE = 24
    DRAGON_SCALE = 25
    FORGE_BLOCK = 26
    CRAFTING_TABLE = 27
    CHEST = 28
    TORCH = 29
    PORTAL_BLOCK = 30
    
    # Dictionnaire des blocs
    _blocks: dict = {}
    
    @classmethod
    def init(cls):
        """Initialise tous les blocs"""
        # === BLOCS DE BASE ===
        cls._register(Block(cls.AIR, "Air", (0, 0, 0), 0, True, False))
        cls._register(Block(cls.DIRT, "Terre", (0.4, 0.25, 0.1), 1.0))
        cls._register(Block(cls.GRASS, "Herbe", (0.2, 0.5, 0.15), 1.0, drop_id=cls.DIRT))
        cls._register(Block(cls.STONE, "Pierre", (0.5, 0.5, 0.5), 3.0))
        cls._register(Block(cls.SAND, "Sable", (0.9, 0.85, 0.6), 0.5))
        cls._register(Block(cls.WATER, "Eau", (0.2, 0.4, 0.8), 0, True, False, light_level=0))
        cls._register(Block(cls.BEDROCK, "Substrat", (0.1, 0.1, 0.1), float('inf')))
        
        # === BLOCS ASMODIA (Cetras) ===
        cls._register(Block(cls.IRON_ASMODIA, "Fer d'Asmodia", (0.45, 0.45, 0.5), 4.0, biome="terres_grises"))
        cls._register(Block(cls.OBSIDIAN, "Obsidienne", (0.1, 0.05, 0.15), 6.0, biome="karthax"))
        cls._register(Block(cls.BRICK_ASMODIA, "Brique d'Asmodia", (0.3, 0.25, 0.25), 3.0, biome="terres_grises"))
        cls._register(Block(cls.FORGE_BLOCK, "Forge Cetra", (0.35, 0.2, 0.1), 4.0, light_level=8))
        
        # === BLOCS ÉLYSÉIA (Tetras) ===
        cls._register(Block(cls.CRYSTAL_ASTRAL, "Cristal d'Astral", (0.6, 0.8, 1.0), 5.0, biome="cite_cristalline", light_level=10))
        cls._register(Block(cls.MARBLE, "Marbre Blanc", (0.95, 0.95, 0.95), 3.0, biome="cite_cristalline"))
        cls._register(Block(cls.CRYSTAL_BLOCK, "Bloc de Cristal", (0.7, 0.85, 0.95), 4.0, True, biome="cite_cristalline", light_level=5))
        
        # === BLOCS PORT-BRUME ===
        cls._register(Block(cls.MIST_STONE, "Pierre de Brume", (0.4, 0.45, 0.5), 3.0, biome="port_brume"))
        
        # === BLOCS KARTHAX (Montagnes/Dragons) ===
        cls._register(Block(cls.LAVA, "Lave", (1.0, 0.3, 0.0), 0, False, False, light_level=15))
        cls._register(Block(cls.KARTHAX_ORE, "Minerai de Karthax", (0.6, 0.3, 0.2), 5.0, biome="karthax"))
        cls._register(Block(cls.DRAGON_SCALE, "Écaille de Dragon", (0.2, 0.15, 0.3), 8.0))
        
        # === BLOCS FORÊT D'ÉTERNITÉ ===
        cls._register(Block(cls.ANCIENT_WOOD, "Bois Ancien", (0.25, 0.4, 0.2), 2.0, biome="foret_eternite"))
        cls._register(Block(cls.ASTRAL_ESSENCE, "Essence d'Astral", (0.5, 0.9, 0.7), 4.0, True, biome="foret_eternite", light_level=8))
        cls._register(Block(cls.LEAVES, "Feuilles", (0.15, 0.45, 0.1), 0.3, True))
        cls._register(Block(cls.LOG, "Tronc", (0.35, 0.2, 0.1), 2.0))
        
        # === BLOCS ASTRAL NOIR (Corruption) ===
        cls._register(Block(cls.CORRUPTION, "Corruption", (0.15, 0.0, 0.2), 4.0, biome="astral_noir", light_level=3))
        cls._register(Block(cls.CORRUPTED_STONE, "Pierre Corrompue", (0.25, 0.15, 0.3), 3.5, biome="astral_noir"))
        
        # === BLOCS UTILITAIRES ===
        cls._register(Block(cls.COAL, "Charbon", (0.15, 0.15, 0.15), 3.0))
        cls._register(Block(cls.TITANIUM, "Titane", (0.7, 0.75, 0.8), 6.0))
        cls._register(Block(cls.GLASS, "Verre", (0.9, 0.95, 1.0), 0.5, True))
        cls._register(Block(cls.CRAFTING_TABLE, "Établi", (0.5, 0.35, 0.2), 2.0))
        cls._register(Block(cls.CHEST, "Coffre", (0.5, 0.35, 0.15), 2.0))
        cls._register(Block(cls.TORCH, "Torche", (0.9, 0.7, 0.3), 0, True, False, light_level=14))
        cls._register(Block(cls.PORTAL_BLOCK, "Portail Astral", (0.5, 0.2, 0.8), float('inf'), False, False, light_level=12))
        
    @classmethod
    def _register(cls, block: Block):
        """Enregistre un bloc"""
        cls._blocks[block.id] = block
        
    @classmethod
    def get(cls, block_id: int) -> Block:
        """Récupère un bloc par son ID"""
        return cls._blocks.get(block_id, cls._blocks[cls.AIR])
    
    @classmethod
    def get_color(cls, block_id: int) -> Tuple[float, float, float]:
        """Récupère la couleur d'un bloc"""
        return cls.get(block_id).color
    
    @classmethod
    def is_solid(cls, block_id: int) -> bool:
        """Vérifie si un bloc est solide"""
        return cls.get(block_id).solid
    
    @classmethod
    def is_transparent(cls, block_id: int) -> bool:
        """Vérifie si un bloc est transparent"""
        return cls.get(block_id).transparent


# Initialiser le registre au chargement du module
BlockRegistry.init()
