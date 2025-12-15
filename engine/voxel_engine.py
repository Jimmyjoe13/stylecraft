"""
Toolvard RPG - Voxel Engine
Moteur principal gérant le monde voxel
"""

from ursina import Vec3
import config
from engine.chunk_manager import ChunkManager
from engine.block_registry import BlockRegistry


class VoxelEngine:
    """Moteur voxel principal pour Toolvard"""
    
    def __init__(self, seed: int = None):
        """Initialise le moteur voxel"""
        self.seed = seed or config.WORLD_SEED
        self.chunk_manager = ChunkManager(self.seed)
        self.is_initialized = False
        
    def initialize(self, spawn_pos: Vec3 = None):
        """
        Initialise le monde autour d'une position de spawn
        """
        if spawn_pos is None:
            spawn_pos = Vec3(0, 30, 0)
        
        # Charger les chunks initiaux
        self.chunk_manager.update(spawn_pos)
        self.is_initialized = True
        
        print(f"[VoxelEngine] Monde initialisé avec seed {self.seed}")
        print(f"[VoxelEngine] {len(self.chunk_manager.chunks)} chunks chargés")
        
    def update(self, player_pos: Vec3):
        """
        Met à jour le monde (appelé chaque frame)
        - Charge/décharge les chunks selon la position du joueur
        """
        if not self.is_initialized:
            return
            
        self.chunk_manager.update(player_pos)
        
    def get_block(self, x: int, y: int, z: int) -> int:
        """Récupère le type de bloc à une position"""
        return self.chunk_manager.get_block_at(x, y, z)
    
    def set_block(self, x: int, y: int, z: int, block_id: int):
        """Place un bloc à une position"""
        self.chunk_manager.set_block_at(x, y, z, block_id)
        
    def break_block(self, x: int, y: int, z: int) -> int:
        """Casse un bloc et retourne son ID (pour drops)"""
        block_id = self.get_block(x, y, z)
        if block_id != BlockRegistry.AIR and block_id != BlockRegistry.BEDROCK:
            self.set_block(x, y, z, BlockRegistry.AIR)
            return block_id
        return BlockRegistry.AIR
    
    def get_spawn_height(self, x: int, z: int) -> int:
        """Trouve la hauteur de spawn (premier bloc d'air au-dessus du sol)"""
        for y in range(config.CHUNK_HEIGHT - 1, 0, -1):
            if self.get_block(x, y, z) != BlockRegistry.AIR:
                return y + 1
        return config.SEA_LEVEL + 1
    
    def raycast_block(self, origin: Vec3, direction: Vec3, max_distance: float = 5.0):
        """
        Lance un rayon et retourne le premier bloc touché
        Retourne (hit_pos, block_id, normal) ou None
        """
        step = 0.1
        current = origin
        
        for _ in range(int(max_distance / step)):
            current = current + direction * step
            x, y, z = int(current.x), int(current.y), int(current.z)
            
            block = self.get_block(x, y, z)
            if block != BlockRegistry.AIR and BlockRegistry.is_solid(block):
                # Calculer la normale (simplifié)
                normal = Vec3(0, 1, 0)  # Par défaut vers le haut
                return (Vec3(x, y, z), block, normal)
        
        return None
    
    def get_stats(self) -> dict:
        """Retourne des statistiques sur le monde"""
        return {
            "seed": self.seed,
            "chunks_loaded": len(self.chunk_manager.chunks),
            "render_distance": self.chunk_manager.render_distance,
        }
