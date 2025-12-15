"""
Toolvard RPG - Point d'entrée principal
Un RPG 3D voxel basé sur l'univers de Toolvard
"""

from ursina import *
import config
from engine.voxel_engine import VoxelEngine
from entities.player import Player
from ui.hud import HUD


# Variables globales
game = None


class GameManager(Entity):
    """Gestionnaire principal du jeu"""
    
    def __init__(self):
        super().__init__()
        
        # Variables d'état
        self.voxel_engine = None
        self.player = None
        self.hud = None
        self.is_paused = False
        self.menu_active = True
        self.menu_elements = []
        
        # Afficher le menu
        self.show_race_selection()
        
    def show_race_selection(self):
        """Affiche le menu de sélection de race"""
        # Fond
        self.menu_bg = Sky(color=color.rgb(20, 20, 40))
        self.menu_elements.append(self.menu_bg)
        
        # Titre
        title = Text(
            text="TOOLVARD",
            origin=(0, 0),
            y=0.35,
            scale=4,
            color=color.gold
        )
        self.menu_elements.append(title)
        
        # Sous-titre
        subtitle = Text(
            text="Le Monde de l'Astral",
            origin=(0, 0),
            y=0.25,
            scale=1.5,
            color=color.white
        )
        self.menu_elements.append(subtitle)
        
        # Instruction
        instruction = Text(
            text="Choisissez votre race:",
            origin=(0, 0),
            y=0.08,
            scale=1.2,
            color=color.light_gray
        )
        self.menu_elements.append(instruction)
        
        # Options de race - affichées séparément pour éviter problèmes
        option1 = Text(
            text="[1] CETRA - Guerriers, Force et vitesse",
            origin=(0, 0),
            y=-0.02,
            scale=1,
            color=color.orange
        )
        self.menu_elements.append(option1)
        
        option2 = Text(
            text="[2] TETRA - Mages, Magie et soins",
            origin=(0, 0),
            y=-0.12,
            scale=1,
            color=color.cyan
        )
        self.menu_elements.append(option2)
        
        option3 = Text(
            text="[3] SANG-MELE - Convergent, Les deux voies",
            origin=(0, 0),
            y=-0.22,
            scale=1,
            color=color.violet
        )
        self.menu_elements.append(option3)
        
        # Instruction en bas
        start_text = Text(
            text="Appuyez sur 1, 2 ou 3 pour commencer",
            origin=(0, 0),
            y=-0.4,
            scale=0.9,
            color=color.yellow
        )
        self.menu_elements.append(start_text)
        
        print("[Menu] Menu de selection affiche - Appuyez sur 1, 2 ou 3")
        
    def input(self, key):
        """Gestion des inputs"""
        # Menu de sélection de race
        if self.menu_active:
            if key == '1':
                print("[Menu] Cetra selectionne!")
                self.start_game(config.RACE_CETRA)
            elif key == '2':
                print("[Menu] Tetra selectionne!")
                self.start_game(config.RACE_TETRA)
            elif key == '3':
                print("[Menu] Sang-Mele selectionne!")
                self.start_game(config.RACE_SANGMELE)
            return
        
        # Pause en jeu
        if key == 'escape':
            self.toggle_pause()
                
    def start_game(self, race: str):
        """Démarre le jeu avec la race choisie"""
        print(f"[Game] Demarrage avec race: {race}")
        
        # Nettoyer le menu
        for element in self.menu_elements:
            destroy(element)
        self.menu_elements.clear()
        self.menu_active = False
        
        # Créer le ciel
        Sky(color=color.rgb(135, 206, 235))
        
        # Ajouter un sol invisible avec collision (fallback)
        self.ground = Entity(
            model='plane',
            scale=(500, 1, 500),
            position=(0, 15, 0),  # Au niveau du terrain moyen
            color=color.rgba(0, 0, 0, 0),  # Invisible
            collider='box',
            visible=False
        )
        
        # Initialiser le moteur voxel
        print("[Game] Initialisation du monde...")
        self.voxel_engine = VoxelEngine(config.WORLD_SEED)
        self.voxel_engine.initialize()
        
        # Position de spawn fixe au-dessus du sol
        spawn_x, spawn_z = 8, 8
        spawn_y = 20  # Hauteur fixe au-dessus du sol
        
        # Créer le joueur
        print(f"[Game] Spawn joueur a ({spawn_x}, {spawn_y}, {spawn_z})")
        self.player = Player(
            race=race,
            position=(spawn_x, spawn_y, spawn_z)
        )
        
        # Créer le HUD
        self.hud = HUD(self.player)
        
        # Message de bienvenue
        race_names = {
            config.RACE_CETRA: "Cetra d'Asmodia",
            config.RACE_TETRA: "Tetra d'Elysia",
            config.RACE_SANGMELE: "Sang-Mele (Convergent)"
        }
        print(f"[Game] Bienvenue, {race_names[race]}!")
        
        # Afficher les contrôles
        self.show_controls()
        
    def show_controls(self):
        """Affiche les contrôles temporairement"""
        controls = Text(
            text=(
                "CONTROLES:\n"
                "WASD - Deplacement\n"
                "Souris - Regarder\n"
                "Espace - Sauter\n"
                "Shift - Sprint\n"
                "Clic Gauche - Attaquer\n"
                "Clic Droit - Parer\n"
                "Echap - Pause"
            ),
            position=(-0.85, 0.2),
            scale=0.7,
            color=color.white,
            background=True,
            background_color=color.rgba(0, 0, 0, 0.7)
        )
        destroy(controls, delay=8)
        
    def update(self):
        """Mise à jour principale du jeu"""
        if self.menu_active or self.is_paused:
            return
            
        # Mise à jour du monde
        if self.voxel_engine and self.player:
            self.voxel_engine.update(self.player.position)
            
    def toggle_pause(self):
        """Active/désactive la pause"""
        if self.menu_active:
            return
            
        self.is_paused = not self.is_paused
        if self.is_paused:
            if self.player:
                self.player.enabled = False
            print("[Game] PAUSE")
        else:
            if self.player:
                self.player.enabled = True
            print("[Game] REPRISE")


def main():
    """Point d'entrée principal"""
    print("=" * 50)
    print("  TOOLVARD RPG")
    print("  Le Monde de l'Astral")
    print("=" * 50)
    
    # Créer l'application Ursina
    app = Ursina(
        title=config.WINDOW_TITLE,
        size=config.WINDOW_SIZE,
        fullscreen=config.FULLSCREEN,
        vsync=config.VSYNC,
        development_mode=config.DEBUG_MODE
    )
    
    # Configuration de la fenêtre
    window.borderless = False
    window.exit_button.visible = False
    
    # Créer le gestionnaire de jeu
    global game
    game = GameManager()
    
    # Lancer le jeu
    app.run()


if __name__ == '__main__':
    main()
