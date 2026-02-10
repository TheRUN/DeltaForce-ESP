"""
Delta Force 2025 ESP Overlay - Main Entry Point
Educational Project for Graphics Programming and Memory Reading

DISCLAIMER: This is an educational project for learning purposes only.
It demonstrates:
- OpenGL rendering and overlay techniques
- Memory reading and process interaction
- 3D mathematics and coordinate transformations
- Software architecture and design patterns

For educational use only. Do not use in online games or violate terms of service.
"""

import json
import logging
import sys
import time
from typing import Optional
import pygame

from memory_reader import MemoryReader, Player
from overlay import Overlay
from esp import ESPCalculator


class ESPApplication:
    """
    Main application class for the ESP overlay system.
    
    Manages the lifecycle of all components and coordinates the rendering loop.
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the ESP application.
        
        Args:
            config_path: Path to configuration file
        """
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.memory_reader: Optional[MemoryReader] = None
        self.overlay: Optional[Overlay] = None
        self.esp_calculator: Optional[ESPCalculator] = None
        
        # State variables
        self.running = False
        self.esp_enabled = self.config['esp']['enabled']
        self.box_enabled = self.config['esp']['box_enabled']
        self.distance_enabled = self.config['esp']['distance_enabled']
        self.health_bar_enabled = self.config['esp']['health_bar_enabled']
        
        # Performance tracking
        self.frame_count = 0
        self.last_fps_update = time.time()
        self.current_fps = 0
    
    def _load_config(self, config_path: str) -> dict:
        """
        Load configuration from JSON file.
        
        Args:
            config_path: Path to config file
            
        Returns:
            Configuration dictionary
        """
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.logger.info(f"Configuration loaded from {config_path}")
            return config
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            # Return default config
            return {
                'window': {'width': 1920, 'height': 1080, 'fps': 60},
                'esp': {'enabled': True, 'box_enabled': True, 'distance_enabled': True},
                'colors': {
                    'enemy': [255, 0, 0, 200],
                    'teammate': [0, 255, 0, 200],
                    'box_thickness': 2.0
                },
                'game': {'process_name': 'DeltaForce.exe'}
            }
    
    def initialize(self) -> bool:
        """
        Initialize all components.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing ESP Application...")
            
            # Initialize memory reader
            process_name = self.config['game']['process_name']
            self.memory_reader = MemoryReader(process_name)
            
            self.logger.info("Note: Memory reader initialized in demo mode.")
            self.logger.info("In production, it would attach to the game process.")
            
            # Initialize overlay window
            width = self.config['window']['width']
            height = self.config['window']['height']
            self.overlay = Overlay(width, height, "Delta Force ESP - Educational Project")
            
            # Initialize ESP calculator
            self.esp_calculator = ESPCalculator(width, height)
            
            self.logger.info("All components initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")
            return False
    
    def handle_input(self) -> bool:
        """
        Handle keyboard input and hotkeys.
        
        Returns:
            True to continue running, False to exit
        """
        # Handle pygame events
        if not self.overlay.handle_events():
            return False
        
        # Check for hotkeys
        keys = pygame.key.get_pressed()
        
        # F1 - Toggle ESP
        if keys[pygame.K_F1]:
            self.esp_enabled = not self.esp_enabled
            self.logger.info(f"ESP {'enabled' if self.esp_enabled else 'disabled'}")
            time.sleep(0.2)  # Debounce
        
        # F2 - Toggle boxes
        if keys[pygame.K_F2]:
            self.box_enabled = not self.box_enabled
            self.logger.info(f"Boxes {'enabled' if self.box_enabled else 'disabled'}")
            time.sleep(0.2)
        
        # F3 - Toggle distance
        if keys[pygame.K_F3]:
            self.distance_enabled = not self.distance_enabled
            self.logger.info(f"Distance {'enabled' if self.distance_enabled else 'disabled'}")
            time.sleep(0.2)
        
        # F10 - Exit
        if keys[pygame.K_F10]:
            return False
        
        return True
    
    def update_fps(self):
        """Update FPS counter."""
        self.frame_count += 1
        current_time = time.time()
        
        if current_time - self.last_fps_update >= 1.0:
            self.current_fps = self.frame_count
            self.frame_count = 0
            self.last_fps_update = current_time
    
    def render_player(self, player: Player, local_player: Player, view_matrix: list):
        """
        Render ESP for a single player.
        
        Args:
            player: Player to render
            local_player: Local player (for distance calculation)
            view_matrix: View matrix for world-to-screen conversion
        """
        if not player.is_valid or player.is_local:
            return
        
        # Calculate distance
        distance = self.esp_calculator.calculate_distance(
            local_player.position,
            player.position
        )
        
        # Skip if too far
        max_distance = self.config['esp'].get('max_distance', 500.0)
        if distance > max_distance:
            return
        
        # Determine color based on team
        if player.team_id == local_player.team_id:
            color = tuple(self.config['colors']['teammate'])
        else:
            color = tuple(self.config['colors']['enemy'])
        
        # Calculate 2D box
        box = self.esp_calculator.calculate_2d_box(
            player.position,
            view_matrix
        )
        
        if not box:
            return
        
        box_x, box_y, box_width, box_height = box
        
        # Draw bounding box
        if self.box_enabled:
            thickness = self.config['colors'].get('box_thickness', 2.0)
            self.overlay.draw_box(
                box_x, box_y, box_width, box_height,
                color, thickness
            )
        
        # Draw distance text
        if self.distance_enabled:
            distance_text = f"{int(distance)}m"
            text_offset = self.config['rendering'].get('text_offset_y', -20)
            self.overlay.draw_text(
                distance_text,
                box_x + box_width // 2 - 15,  # Center approximately
                box_y + text_offset,
                color
            )
        
        # Draw health bar
        if self.health_bar_enabled and player.health > 0:
            health_percent = player.health / 100.0
            bar_width = box_width
            bar_height = 4
            self.overlay.draw_health_bar(
                box_x,
                box_y - 8,
                bar_width,
                bar_height,
                health_percent
            )
    
    def render(self):
        """
        Main rendering function.
        
        Educational Note:
        This is the core render loop that:
        1. Clears the screen
        2. Reads game data from memory
        3. Calculates screen positions
        4. Renders ESP elements
        5. Displays the result
        """
        # Clear screen
        self.overlay.clear()
        
        if not self.esp_enabled:
            # Draw disabled message
            self.overlay.draw_text(
                "ESP Disabled (Press F1 to enable)",
                10, 10,
                (255, 255, 0, 255)
            )
            self.overlay.update()
            return
        
        # Get game data
        try:
            local_player = self.memory_reader.get_local_player()
            players = self.memory_reader.get_player_list()
            view_matrix = self.memory_reader.get_view_matrix()
            
            if not local_player or not view_matrix:
                self.overlay.draw_text(
                    "Waiting for game data...",
                    10, 10,
                    (255, 255, 0, 255)
                )
                self.overlay.update()
                return
            
            # Render each player
            for player in players:
                self.render_player(player, local_player, view_matrix)
            
        except Exception as e:
            self.logger.error(f"Render error: {e}")
        
        # Draw status information
        self.draw_status_ui()
        
        # Update display
        self.overlay.update()
    
    def draw_status_ui(self):
        """Draw status information on screen."""
        y_offset = 10
        line_height = 20
        
        # FPS counter
        fps_text = f"FPS: {self.current_fps}"
        self.overlay.draw_text(fps_text, 10, y_offset, (0, 255, 0, 255))
        y_offset += line_height
        
        # ESP status
        esp_text = f"ESP: {'ON' if self.esp_enabled else 'OFF'} (F1)"
        self.overlay.draw_text(esp_text, 10, y_offset, (255, 255, 255, 255))
        y_offset += line_height
        
        # Box status
        box_text = f"Boxes: {'ON' if self.box_enabled else 'OFF'} (F2)"
        self.overlay.draw_text(box_text, 10, y_offset, (255, 255, 255, 255))
        y_offset += line_height
        
        # Distance status
        dist_text = f"Distance: {'ON' if self.distance_enabled else 'OFF'} (F3)"
        self.overlay.draw_text(dist_text, 10, y_offset, (255, 255, 255, 255))
        y_offset += line_height
        
        # Help text
        self.overlay.draw_text(
            "F10: Exit | ESC: Exit",
            10, self.config['window']['height'] - 30,
            (200, 200, 200, 255)
        )
    
    def run(self):
        """
        Main application loop.
        
        Educational Note:
        This is a typical game loop structure:
        1. Process input
        2. Update game state
        3. Render
        4. Maintain target FPS
        """
        if not self.initialize():
            self.logger.error("Failed to initialize application")
            return 1
        
        self.running = True
        target_fps = self.config['window'].get('fps', 60)
        frame_time = 1.0 / target_fps
        
        self.logger.info("ESP Application started")
        self.logger.info("Hotkeys:")
        self.logger.info("  F1  - Toggle ESP")
        self.logger.info("  F2  - Toggle Boxes")
        self.logger.info("  F3  - Toggle Distance")
        self.logger.info("  F10 - Exit")
        self.logger.info("  ESC - Exit")
        
        try:
            while self.running:
                frame_start = time.time()
                
                # Handle input
                if not self.handle_input():
                    break
                
                # Render
                self.render()
                
                # Update FPS counter
                self.update_fps()
                
                # Maintain target FPS
                frame_elapsed = time.time() - frame_start
                if frame_elapsed < frame_time:
                    time.sleep(frame_time - frame_elapsed)
        
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user")
        except Exception as e:
            self.logger.error(f"Runtime error: {e}", exc_info=True)
            return 1
        finally:
            self.cleanup()
        
        return 0
    
    def cleanup(self):
        """Clean up resources."""
        self.logger.info("Cleaning up...")
        
        if self.memory_reader:
            self.memory_reader.detach()
        
        if self.overlay:
            self.overlay.cleanup()
        
        self.logger.info("Cleanup complete")


def main():
    """Main entry point."""
    print("=" * 60)
    print("Delta Force 2025 ESP Overlay - Educational Project")
    print("=" * 60)
    print()
    print("EDUCATIONAL DISCLAIMER:")
    print("This software is for educational purposes only.")
    print("It demonstrates graphics programming, memory reading,")
    print("and overlay techniques.")
    print()
    print("Do NOT use this in online games or to violate any")
    print("terms of service. Use responsibly for learning only.")
    print("=" * 60)
    print()
    
    app = ESPApplication()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
