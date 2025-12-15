"""
Toolvard RPG - Player
Classe du joueur avec contrôles FPS et système Astral
"""

from ursina import Entity, Vec3, Vec2, camera, mouse, held_keys, time, raycast, color
from ursina.prefabs.first_person_controller import FirstPersonController
import config


class Player(FirstPersonController):
    """
    Joueur de Toolvard avec système de race et Astral
    Hérite de FirstPersonController pour les contrôles de base
    """
    
    def __init__(self, race: str = config.RACE_SANGMELE, **kwargs):
        super().__init__(**kwargs)
        
        # === RACE ===
        self.race = race
        self._apply_race_bonuses()
        
        # === STATS DE BASE ===
        self.max_hp = config.MAX_HP
        self.hp = self.max_hp
        self.max_astral = config.MAX_ASTRAL
        self.astral = self.max_astral
        
        # === STATS DE COMBAT ===
        self.strength = 10
        self.magic = 10
        self.agility = 10
        self.defense = 10
        
        # === PROGRESSION ===
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        self.skill_points = 0
        
        # === MOUVEMENT ===
        self.speed = config.PLAYER_SPEED
        self.jump_height = config.PLAYER_JUMP_HEIGHT
        self.gravity = config.PLAYER_GRAVITY
        
        # === CONTRÔLES ===
        self.mouse_sensitivity = Vec2(config.MOUSE_SENSITIVITY, config.MOUSE_SENSITIVITY)
        
        # === ÉTAT ===
        self.is_attacking = False
        self.attack_cooldown = 0
        self.is_blocking = False
        self.is_sprinting = False
        
        # === INVENTAIRE (référence, sera initialisé plus tard) ===
        self.inventory = None
        self.equipped_weapon = None
        
        # Configuration visuelle
        self.cursor.color = color.white
        
    def _apply_race_bonuses(self):
        """Applique les bonus de race"""
        if self.race == config.RACE_CETRA:
            # Cetra: Force et vitesse
            self.strength_bonus = 1.5
            self.magic_bonus = 0.8
            self.speed_bonus = 1.3
        elif self.race == config.RACE_TETRA:
            # Tetra: Magie et régénération
            self.strength_bonus = 0.8
            self.magic_bonus = 1.5
            self.regen_bonus = 1.3
        else:  # Sang-Mêlé / Convergent
            # Équilibré avec accès aux deux
            self.strength_bonus = 1.0
            self.magic_bonus = 1.0
            self.speed_bonus = 1.0
            self.regen_bonus = 1.0
            
    def update(self):
        """Mise à jour chaque frame"""
        super().update()
        
        # Régénération d'Astral
        self._regen_astral()
        
        # Gestion du sprint
        self._handle_sprint()
        
        # Cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= time.dt
            
    def _regen_astral(self):
        """Régénère l'Astral lentement"""
        regen_rate = config.ASTRAL_REGEN_RATE
        if hasattr(self, 'regen_bonus'):
            regen_rate *= self.regen_bonus
            
        if self.astral < self.max_astral:
            self.astral = min(self.max_astral, self.astral + regen_rate * time.dt)
            
    def _handle_sprint(self):
        """Gère le sprint"""
        if held_keys['shift'] and self.astral > 0:
            self.is_sprinting = True
            self.speed = config.PLAYER_SPEED * 1.5
            self.astral -= 5 * time.dt  # Coût du sprint
        else:
            self.is_sprinting = False
            self.speed = config.PLAYER_SPEED
            
    def input(self, key):
        """Gestion des inputs"""
        super().input(key)
        
        # Attaque légère (clic gauche)
        if key == 'left mouse down' and self.attack_cooldown <= 0:
            self.light_attack()
            
        # Attaque lourde / Parade (clic droit)
        if key == 'right mouse down':
            self.block()
        if key == 'right mouse up':
            self.is_blocking = False
            
        # Compétences (1-4)
        if key == '1':
            self.use_skill(0)
        elif key == '2':
            self.use_skill(1)
        elif key == '3':
            self.use_skill(2)
        elif key == '4':
            self.use_skill(3)
            
    def light_attack(self):
        """Attaque légère"""
        if self.attack_cooldown > 0:
            return
            
        self.is_attacking = True
        self.attack_cooldown = 0.5  # Cooldown de 0.5s
        
        # Calculer les dégâts
        base_damage = config.BASE_ATTACK_DAMAGE
        
        if self.race == config.RACE_CETRA:
            damage = base_damage * self.strength_bonus * (1 + self.strength / 100)
        else:
            damage = base_damage * (1 + self.strength / 100)
            
        # Raycast pour détecter les ennemis
        hit_info = raycast(
            origin=camera.world_position,
            direction=camera.forward,
            distance=3,
            ignore=[self]
        )
        
        if hit_info.hit:
            if hasattr(hit_info.entity, 'take_damage'):
                hit_info.entity.take_damage(damage)
                print(f"[Combat] Attaque: {damage:.1f} dégâts")
                
        self.is_attacking = False
        
    def heavy_attack(self):
        """Attaque lourde (consomme Astral)"""
        astral_cost = 15
        if self.astral < astral_cost:
            return
            
        self.astral -= astral_cost
        damage = config.BASE_ATTACK_DAMAGE * 2.5
        
        if self.race == config.RACE_CETRA:
            damage *= self.strength_bonus
            
        # TODO: Implémenter l'animation et la hitbox
        print(f"[Combat] Attaque lourde: {damage:.1f} dégâts potentiels")
        
    def block(self):
        """Active la parade"""
        self.is_blocking = True
        
    def use_skill(self, slot: int):
        """Utilise une compétence équipée"""
        # TODO: Implémenter le système de compétences
        print(f"[Skill] Compétence {slot + 1} utilisée")
        
    def cast_spell(self, spell_id: str, astral_cost: int = 10):
        """Lance un sort (Tetra / Sang-Mêlé)"""
        if self.race == config.RACE_CETRA:
            print("[Magic] Les Cetras ne peuvent pas lancer de sorts!")
            return False
            
        if self.astral < astral_cost:
            print("[Magic] Pas assez d'Astral!")
            return False
            
        self.astral -= astral_cost
        
        # Calculer la puissance magique
        power = 10 * self.magic_bonus * (1 + self.magic / 100)
        
        # TODO: Implémenter différents sorts
        print(f"[Magic] Sort lancé avec puissance {power:.1f}")
        return True
        
    def take_damage(self, damage: float, damage_type: str = "physical"):
        """Reçoit des dégâts"""
        # Réduction par défense
        reduction = self.defense / (self.defense + 100)
        
        # Parade
        if self.is_blocking:
            reduction += 0.5  # +50% réduction si parade
            
        actual_damage = damage * (1 - reduction)
        self.hp -= actual_damage
        
        print(f"[Combat] Dégâts reçus: {actual_damage:.1f} (HP: {self.hp:.1f}/{self.max_hp})")
        
        if self.hp <= 0:
            self.die()
            
    def heal(self, amount: float):
        """Soigne le joueur"""
        self.hp = min(self.max_hp, self.hp + amount)
        print(f"[Heal] +{amount:.1f} HP (HP: {self.hp:.1f}/{self.max_hp})")
        
    def gain_xp(self, amount: int):
        """Gagne de l'expérience"""
        self.xp += amount
        print(f"[XP] +{amount} XP ({self.xp}/{self.xp_to_next_level})")
        
        # Level up
        while self.xp >= self.xp_to_next_level:
            self.level_up()
            
    def level_up(self):
        """Monte de niveau"""
        self.xp -= self.xp_to_next_level
        self.level += 1
        self.skill_points += 1
        
        # Augmenter XP requis
        self.xp_to_next_level = int(100 * (self.level ** 1.5))
        
        # Bonus de stats
        self.max_hp += 15
        self.hp = self.max_hp
        self.max_astral += 8
        self.astral = self.max_astral
        
        print(f"[LEVEL UP] Niveau {self.level}! +1 point de compétence")
        
    def die(self):
        """Mort du joueur"""
        print("[MORT] Le joueur est mort!")
        # TODO: Implémenter respawn
        
    def get_stats(self) -> dict:
        """Retourne les stats actuelles"""
        return {
            "race": self.race,
            "level": self.level,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "astral": self.astral,
            "max_astral": self.max_astral,
            "strength": self.strength,
            "magic": self.magic,
            "agility": self.agility,
            "defense": self.defense,
            "xp": self.xp,
            "xp_to_next": self.xp_to_next_level,
        }
