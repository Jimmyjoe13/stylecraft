"""
Toolvard RPG - Chunk Manager
Gestion du chargement/déchargement des chunks
"""

import numpy as np
from typing import Dict, Tuple, Optional
from ursina import Entity, Mesh, Vec3, color, destroy
import config
from engine.block_registry import BlockRegistry
from world.terrain_generator import TerrainGenerator


class Chunk:
    """Représente un chunk du monde"""
    
    def __init__(self, x: int, z: int, blocks: np.ndarray):
        self.x = x
        self.z = z
        self.blocks = blocks
        self.entity: Optional[Entity] = None
        self.dirty = True  # Besoin de rebuild mesh
        
    def get_block(self, x: int, y: int, z: int) -> int:
        """Récupère un bloc à une position locale"""
        if 0 <= x < config.CHUNK_SIZE and 0 <= y < config.CHUNK_HEIGHT and 0 <= z < config.CHUNK_SIZE:
            return self.blocks[x, y, z]
        return BlockRegistry.AIR
    
    def set_block(self, x: int, y: int, z: int, block_id: int):
        """Modifie un bloc à une position locale"""
        if 0 <= x < config.CHUNK_SIZE and 0 <= y < config.CHUNK_HEIGHT and 0 <= z < config.CHUNK_SIZE:
            self.blocks[x, y, z] = block_id
            self.dirty = True


class ChunkManager:
    """Gestionnaire de chunks avec lazy loading"""
    
    def __init__(self, seed: int = None):
        self.terrain_gen = TerrainGenerator(seed)
        self.chunks: Dict[Tuple[int, int], Chunk] = {}
        self.render_distance = config.RENDER_DISTANCE
        
    def update(self, player_pos: Vec3):
        """Met à jour les chunks autour du joueur"""
        player_chunk = self.world_to_chunk(player_pos)
        
        # Charger les chunks proches
        for dx in range(-self.render_distance, self.render_distance + 1):
            for dz in range(-self.render_distance, self.render_distance + 1):
                chunk_pos = (player_chunk[0] + dx, player_chunk[1] + dz)
                
                # Charger si pas déjà chargé
                if chunk_pos not in self.chunks:
                    self._load_chunk(chunk_pos[0], chunk_pos[1])
        
        # Décharger les chunks éloignés
        chunks_to_remove = []
        for pos in self.chunks:
            dist = abs(pos[0] - player_chunk[0]) + abs(pos[1] - player_chunk[1])
            if dist > self.render_distance + 2:
                chunks_to_remove.append(pos)
        
        for pos in chunks_to_remove:
            self._unload_chunk(pos)
            
    def _load_chunk(self, chunk_x: int, chunk_z: int):
        """Charge un chunk"""
        # Générer le terrain
        blocks = self.terrain_gen.generate_chunk(chunk_x, chunk_z)
        
        # Créer le chunk
        chunk = Chunk(chunk_x, chunk_z, blocks)
        self.chunks[(chunk_x, chunk_z)] = chunk
        
        # Générer les arbres (désactivé pour perf)
        # self.terrain_gen.generate_trees(blocks, chunk_x, chunk_z)
        
        # Créer le mesh
        self._build_chunk_mesh(chunk)
        
    def _unload_chunk(self, pos: Tuple[int, int]):
        """Décharge un chunk"""
        if pos in self.chunks:
            chunk = self.chunks[pos]
            if chunk.entity:
                destroy(chunk.entity)
            del self.chunks[pos]
            
    def _build_chunk_mesh(self, chunk: Chunk):
        """Construit le mesh d'un chunk avec greedy meshing simplifié"""
        vertices = []
        triangles = []
        colors = []
        vertex_count = 0
        
        size = config.CHUNK_SIZE
        height = config.CHUNK_HEIGHT
        
        # Pour chaque bloc visible
        for x in range(size):
            for y in range(height):
                for z in range(size):
                    block_id = chunk.blocks[x, y, z]
                    
                    # Skip air et transparents
                    if block_id == BlockRegistry.AIR or BlockRegistry.is_transparent(block_id):
                        continue
                    
                    block_color = BlockRegistry.get_color(block_id)
                    
                    # Vérifier chaque face
                    # Face supérieure (+Y)
                    if y == height - 1 or self._is_face_visible(chunk, x, y + 1, z):
                        self._add_face(vertices, triangles, colors, vertex_count,
                                       x, y + 1, z, 'top', block_color)
                        vertex_count += 4
                    
                    # Face inférieure (-Y)
                    if y == 0 or self._is_face_visible(chunk, x, y - 1, z):
                        self._add_face(vertices, triangles, colors, vertex_count,
                                       x, y, z, 'bottom', block_color)
                        vertex_count += 4
                    
                    # Face avant (+Z)
                    if z == size - 1 or self._is_face_visible(chunk, x, y, z + 1):
                        self._add_face(vertices, triangles, colors, vertex_count,
                                       x, y, z + 1, 'front', block_color)
                        vertex_count += 4
                    
                    # Face arrière (-Z)
                    if z == 0 or self._is_face_visible(chunk, x, y, z - 1):
                        self._add_face(vertices, triangles, colors, vertex_count,
                                       x, y, z, 'back', block_color)
                        vertex_count += 4
                    
                    # Face droite (+X)
                    if x == size - 1 or self._is_face_visible(chunk, x + 1, y, z):
                        self._add_face(vertices, triangles, colors, vertex_count,
                                       x + 1, y, z, 'right', block_color)
                        vertex_count += 4
                    
                    # Face gauche (-X)
                    if x == 0 or self._is_face_visible(chunk, x - 1, y, z):
                        self._add_face(vertices, triangles, colors, vertex_count,
                                       x, y, z, 'left', block_color)
                        vertex_count += 4
        
        # Créer l'entité si on a des vertices
        if vertices:
            # Détruire l'ancien mesh si existant
            if chunk.entity:
                destroy(chunk.entity)
            
            mesh = Mesh(vertices=vertices, triangles=triangles, colors=colors)
            
            chunk.entity = Entity(
                model=mesh,
                position=(chunk.x * size, 0, chunk.z * size),
                color=color.white,
                collider='mesh'  # Collision avec le terrain
            )
            print(f"[Chunk] Chunk ({chunk.x}, {chunk.z}) cree")
        
        chunk.dirty = False
        
    def _is_face_visible(self, chunk: Chunk, x: int, y: int, z: int) -> bool:
        """Vérifie si une face doit être rendue (bloc adjacent transparent/air)"""
        block = chunk.get_block(x, y, z)
        return block == BlockRegistry.AIR or BlockRegistry.is_transparent(block)
    
    def _add_face(self, vertices, triangles, colors, start_idx, x, y, z, face_type, block_color):
        """Ajoute une face au mesh"""
        # Couleurs avec variation légère pour effet 3D
        c = block_color
        if face_type == 'top':
            shade = 1.0
        elif face_type == 'bottom':
            shade = 0.5
        elif face_type in ['front', 'back']:
            shade = 0.7
        else:
            shade = 0.8
        
        face_color = color.rgb(int(c[0] * shade * 255), 
                               int(c[1] * shade * 255), 
                               int(c[2] * shade * 255))
        
        if face_type == 'top':
            vertices.extend([
                (x, y, z), (x + 1, y, z), (x + 1, y, z + 1), (x, y, z + 1)
            ])
        elif face_type == 'bottom':
            vertices.extend([
                (x, y, z + 1), (x + 1, y, z + 1), (x + 1, y, z), (x, y, z)
            ])
        elif face_type == 'front':
            vertices.extend([
                (x, y, z), (x + 1, y, z), (x + 1, y + 1, z), (x, y + 1, z)
            ])
        elif face_type == 'back':
            vertices.extend([
                (x + 1, y, z), (x, y, z), (x, y + 1, z), (x + 1, y + 1, z)
            ])
        elif face_type == 'right':
            vertices.extend([
                (x, y, z + 1), (x, y, z), (x, y + 1, z), (x, y + 1, z + 1)
            ])
        elif face_type == 'left':
            vertices.extend([
                (x, y, z), (x, y, z + 1), (x, y + 1, z + 1), (x, y + 1, z)
            ])
        
        # Triangles (deux triangles par face)
        triangles.extend([
            start_idx, start_idx + 1, start_idx + 2,
            start_idx, start_idx + 2, start_idx + 3
        ])
        
        # Couleurs pour chaque vertex
        colors.extend([face_color] * 4)
    
    def world_to_chunk(self, pos: Vec3) -> Tuple[int, int]:
        """Convertit une position monde en coordonnées chunk"""
        return (int(pos.x // config.CHUNK_SIZE), int(pos.z // config.CHUNK_SIZE))
    
    def get_block_at(self, x: int, y: int, z: int) -> int:
        """Récupère un bloc à une position mondiale"""
        chunk_x = x // config.CHUNK_SIZE
        chunk_z = z // config.CHUNK_SIZE
        local_x = x % config.CHUNK_SIZE
        local_z = z % config.CHUNK_SIZE
        
        chunk = self.chunks.get((chunk_x, chunk_z))
        if chunk:
            return chunk.get_block(local_x, y, local_z)
        return BlockRegistry.AIR
    
    def set_block_at(self, x: int, y: int, z: int, block_id: int):
        """Modifie un bloc à une position mondiale"""
        chunk_x = x // config.CHUNK_SIZE
        chunk_z = z // config.CHUNK_SIZE
        local_x = x % config.CHUNK_SIZE
        local_z = z % config.CHUNK_SIZE
        
        chunk = self.chunks.get((chunk_x, chunk_z))
        if chunk:
            chunk.set_block(local_x, y, local_z, block_id)
            # Rebuild le mesh
            self._build_chunk_mesh(chunk)
