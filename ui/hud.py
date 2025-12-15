"""
Toolvard RPG - HUD
Interface utilisateur principale (vie, Astral, XP)
"""

from ursina import Entity, Text, color, window, camera
import config


class HUD(Entity):
    """HUD principal du jeu"""
    
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        
        # === BARRES DE VIE ===
        self.hp_bar_bg = Entity(
            parent=self,
            model='quad',
            color=color.dark_gray,
            scale=(0.4, 0.03),
            position=(-0.65, 0.45),
            origin=(-0.5, 0)
        )
        
        self.hp_bar = Entity(
            parent=self,
            model='quad',
            color=color.red,
            scale=(0.4, 0.025),
            position=(-0.65, 0.45),
            origin=(-0.5, 0)
        )
        
        self.hp_text = Text(
            parent=self,
            text='HP',
            position=(-0.66, 0.47),
            scale=0.8,
            color=color.white
        )
        
        # === BARRE D'ASTRAL ===
        self.astral_bar_bg = Entity(
            parent=self,
            model='quad',
            color=color.dark_gray,
            scale=(0.4, 0.025),
            position=(-0.65, 0.41),
            origin=(-0.5, 0)
        )
        
        self.astral_bar = Entity(
            parent=self,
            model='quad',
            color=color.cyan,
            scale=(0.4, 0.02),
            position=(-0.65, 0.41),
            origin=(-0.5, 0)
        )
        
        self.astral_text = Text(
            parent=self,
            text='ASTRAL',
            position=(-0.66, 0.43),
            scale=0.7,
            color=color.white
        )
        
        # === BARRE D'XP ===
        self.xp_bar_bg = Entity(
            parent=self,
            model='quad',
            color=color.dark_gray,
            scale=(0.4, 0.015),
            position=(-0.65, 0.37),
            origin=(-0.5, 0)
        )
        
        self.xp_bar = Entity(
            parent=self,
            model='quad',
            color=color.yellow,
            scale=(0.4, 0.012),
            position=(-0.65, 0.37),
            origin=(-0.5, 0)
        )
        
        # === INFOS NIVEAU ===
        self.level_text = Text(
            parent=self,
            text='Lv. 1',
            position=(-0.25, 0.45),
            scale=1.0,
            color=color.gold
        )
        
        # === RACE ===
        self.race_text = Text(
            parent=self,
            text='',
            position=(-0.25, 0.41),
            scale=0.8,
            color=color.white
        )
        self._update_race_display()
        
        # === CROSSHAIR ===
        self.crosshair = Text(
            parent=self,
            text='+',
            origin=(0, 0),
            scale=2,
            color=color.white
        )
        
        # === DEBUG INFO ===
        if config.DEBUG_MODE:
            self.debug_text = Text(
                parent=self,
                text='',
                position=(-0.85, -0.4),
                scale=0.7,
                color=color.lime
            )
        
        # === STATS (coin droit) ===
        self.stats_text = Text(
            parent=self,
            text='',
            position=(0.5, 0.45),
            scale=0.7,
            color=color.white
        )
        
    def _update_race_display(self):
        """Met à jour l'affichage de la race"""
        race_names = {
            config.RACE_CETRA: "[CETRA]",
            config.RACE_TETRA: "[TETRA]", 
            config.RACE_SANGMELE: "[CONVERGENT]"
        }
        self.race_text.text = race_names.get(self.player.race, "Inconnu")
        
    def update(self):
        """Mise à jour du HUD chaque frame"""
        # Mettre à jour les barres
        hp_percent = self.player.hp / self.player.max_hp
        self.hp_bar.scale_x = 0.4 * hp_percent
        
        astral_percent = self.player.astral / self.player.max_astral
        self.astral_bar.scale_x = 0.4 * astral_percent
        
        xp_percent = self.player.xp / self.player.xp_to_next_level if self.player.xp_to_next_level > 0 else 0
        self.xp_bar.scale_x = 0.4 * xp_percent
        
        # Textes
        self.hp_text.text = f'HP: {int(self.player.hp)}/{int(self.player.max_hp)}'
        self.astral_text.text = f'ASTRAL: {int(self.player.astral)}/{int(self.player.max_astral)}'
        self.level_text.text = f'Lv. {self.player.level}'
        
        # Stats
        stats = self.player.get_stats()
        self.stats_text.text = (
            f"FOR: {stats['strength']}\n"
            f"MAG: {stats['magic']}\n"
            f"AGI: {stats['agility']}\n"
            f"DEF: {stats['defense']}"
        )
        
        # Debug
        if config.DEBUG_MODE and hasattr(self, 'debug_text'):
            pos = self.player.position
            self.debug_text.text = (
                f"POS: ({pos.x:.1f}, {pos.y:.1f}, {pos.z:.1f})\n"
                f"Sprint: {self.player.is_sprinting}\n"
                f"Block: {self.player.is_blocking}"
            )
            
    def show_damage_number(self, damage: float, position):
        """Affiche un nombre de dégâts flottant"""
        # TODO: Implémenter les nombres de dégâts animés
        pass
    
    def show_message(self, message: str, duration: float = 2.0):
        """Affiche un message temporaire"""
        msg = Text(
            parent=self,
            text=message,
            origin=(0, 0),
            y=-0.3,
            scale=1.2,
            color=color.white
        )
        msg.animate_color(color.clear, duration=duration)
        # TODO: Détruire après animation
