"""
ESP Logic Module
Educational purpose: Demonstrates 3D to 2D coordinate transformation and ESP calculations
"""

import numpy as np
import math
from typing import Optional, Tuple, List
import logging


class ESPCalculator:
    """
    ESP calculation engine for world-to-screen projection.
    
    Educational Focus:
    - 3D mathematics and coordinate systems
    - Matrix transformations
    - World-to-screen projection
    - Distance calculations
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize ESP calculator.
        
        Args:
            screen_width: Width of the screen in pixels
            screen_height: Height of the screen in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.logger = logging.getLogger(__name__)
        
    def world_to_screen(
        self, 
        world_pos: Tuple[float, float, float],
        view_matrix: List[float]
    ) -> Optional[Tuple[int, int]]:
        """
        Convert 3D world coordinates to 2D screen coordinates.
        
        Educational Note:
        This is the core of ESP rendering. We multiply the world position
        by the view-projection matrix to get clip-space coordinates,
        then convert to screen space.
        
        The transformation pipeline:
        1. World Space (3D game coordinates)
        2. View Space (relative to camera)
        3. Clip Space (after projection)
        4. NDC (Normalized Device Coordinates, -1 to 1)
        5. Screen Space (pixel coordinates)
        
        Args:
            world_pos: (x, y, z) position in world space
            view_matrix: 4x4 view-projection matrix (16 elements, row-major)
            
        Returns:
            (screen_x, screen_y) tuple if visible, None if behind camera
        """
        try:
            # Extract position coordinates
            x, y, z = world_pos
            
            # Reshape view matrix to 4x4
            matrix = np.array(view_matrix).reshape(4, 4)
            
            # Create homogeneous coordinate (w=1 for positions)
            world_vec = np.array([x, y, z, 1.0])
            
            # Transform to clip space: clip = matrix * world
            clip_coords = np.dot(matrix, world_vec)
            
            # Check if point is behind camera (w <= 0)
            if clip_coords[3] <= 0.1:
                return None
            
            # Perspective divide to get NDC (Normalized Device Coordinates)
            # NDC range: -1 to 1 for visible screen area
            ndc_x = clip_coords[0] / clip_coords[3]
            ndc_y = clip_coords[1] / clip_coords[3]
            
            # Check if point is outside screen bounds
            if abs(ndc_x) > 1.0 or abs(ndc_y) > 1.0:
                return None
            
            # Convert NDC to screen coordinates
            # NDC (-1,-1) = top-left, (1,1) = bottom-right
            screen_x = int((ndc_x + 1.0) * 0.5 * self.screen_width)
            screen_y = int((1.0 - ndc_y) * 0.5 * self.screen_height)
            
            return (screen_x, screen_y)
            
        except Exception as e:
            self.logger.debug(f"Error in world_to_screen: {e}")
            return None
    
    def calculate_distance(
        self,
        pos1: Tuple[float, float, float],
        pos2: Tuple[float, float, float]
    ) -> float:
        """
        Calculate 3D distance between two points.
        
        Educational Note:
        Uses the 3D Euclidean distance formula:
        distance = sqrt((x2-x1)² + (y2-y1)² + (z2-z1)²)
        
        Args:
            pos1: First position (x, y, z)
            pos2: Second position (x, y, z)
            
        Returns:
            Distance in world units (typically meters in games)
        """
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        dz = pos2[2] - pos1[2]
        
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def calculate_2d_box(
        self,
        world_pos: Tuple[float, float, float],
        view_matrix: List[float],
        player_height: float = 1.8,
        player_width: float = 0.6
    ) -> Optional[Tuple[int, int, int, int]]:
        """
        Calculate 2D bounding box for a player.
        
        Educational Note:
        We project the player's head and feet positions to screen space,
        then calculate a box around them. The box width is estimated based
        on distance to maintain consistent visual size.
        
        Args:
            world_pos: Player's center position
            view_matrix: View-projection matrix
            player_height: Player model height in meters
            player_width: Player model width in meters
            
        Returns:
            (x, y, width, height) of bounding box, or None if not visible
        """
        # Calculate head and feet positions
        head_pos = (world_pos[0], world_pos[1], world_pos[2] + player_height/2)
        feet_pos = (world_pos[0], world_pos[1], world_pos[2] - player_height/2)
        
        # Project to screen
        head_screen = self.world_to_screen(head_pos, view_matrix)
        feet_screen = self.world_to_screen(feet_pos, view_matrix)
        
        if not head_screen or not feet_screen:
            return None
        
        # Calculate box dimensions
        # Height from feet to head
        box_height = abs(feet_screen[1] - head_screen[1])
        
        # Width proportional to height (maintain aspect ratio)
        box_width = int(box_height * (player_width / player_height))
        
        # Center the box horizontally on the player's screen position
        center_x = (head_screen[0] + feet_screen[0]) // 2
        top_y = min(head_screen[1], feet_screen[1])
        
        # Box coordinates: top-left corner
        box_x = center_x - box_width // 2
        box_y = top_y
        
        return (box_x, box_y, box_width, box_height)
    
    def calculate_3d_box_corners(
        self,
        world_pos: Tuple[float, float, float],
        view_matrix: List[float],
        box_size: Tuple[float, float, float] = (0.6, 0.6, 1.8)
    ) -> Optional[List[Tuple[int, int]]]:
        """
        Calculate screen positions for 3D box corners.
        
        Educational Note:
        This creates a full 3D bounding box by projecting all 8 corners
        of a box in world space. Useful for more accurate ESP visualization.
        
        Args:
            world_pos: Center position of the box
            view_matrix: View-projection matrix
            box_size: (width, depth, height) of the box in world units
            
        Returns:
            List of 8 (x, y) screen coordinates, or None if not visible
        """
        width, depth, height = box_size
        x, y, z = world_pos
        
        # Define 8 corners of the box
        corners_3d = [
            (x - width/2, y - depth/2, z - height/2),  # Bottom front-left
            (x + width/2, y - depth/2, z - height/2),  # Bottom front-right
            (x + width/2, y + depth/2, z - height/2),  # Bottom back-right
            (x - width/2, y + depth/2, z - height/2),  # Bottom back-left
            (x - width/2, y - depth/2, z + height/2),  # Top front-left
            (x + width/2, y - depth/2, z + height/2),  # Top front-right
            (x + width/2, y + depth/2, z + height/2),  # Top back-right
            (x - width/2, y + depth/2, z + height/2),  # Top back-left
        ]
        
        # Project all corners to screen
        corners_2d = []
        for corner in corners_3d:
            screen_pos = self.world_to_screen(corner, view_matrix)
            if not screen_pos:
                return None  # If any corner is not visible, return None
            corners_2d.append(screen_pos)
        
        return corners_2d
    
    def is_on_screen(
        self,
        world_pos: Tuple[float, float, float],
        view_matrix: List[float]
    ) -> bool:
        """
        Check if a world position is visible on screen.
        
        Args:
            world_pos: Position to check
            view_matrix: View-projection matrix
            
        Returns:
            True if position is visible, False otherwise
        """
        screen_pos = self.world_to_screen(world_pos, view_matrix)
        return screen_pos is not None
    
    def calculate_angle_to_target(
        self,
        from_pos: Tuple[float, float, float],
        to_pos: Tuple[float, float, float]
    ) -> Tuple[float, float]:
        """
        Calculate pitch and yaw angles to a target.
        
        Educational Note:
        Useful for aim assistance features. Calculates the rotation
        needed to look at a target from a given position.
        
        Args:
            from_pos: Source position (camera/player)
            to_pos: Target position
            
        Returns:
            (pitch, yaw) angles in degrees
        """
        # Calculate direction vector
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]
        dz = to_pos[2] - from_pos[2]
        
        # Calculate horizontal distance
        h_dist = math.sqrt(dx*dx + dy*dy)
        
        # Calculate angles
        pitch = math.degrees(math.atan2(dz, h_dist))
        yaw = math.degrees(math.atan2(dy, dx))
        
        return (pitch, yaw)
    
    def interpolate_color(
        self,
        color1: Tuple[int, int, int, int],
        color2: Tuple[int, int, int, int],
        factor: float
    ) -> Tuple[int, int, int, int]:
        """
        Interpolate between two colors.
        
        Educational Note:
        Useful for health bars or distance-based coloring.
        Factor should be between 0.0 and 1.0.
        
        Args:
            color1: Starting color (r, g, b, a)
            color2: Ending color (r, g, b, a)
            factor: Interpolation factor (0.0 to 1.0)
            
        Returns:
            Interpolated color (r, g, b, a)
        """
        factor = max(0.0, min(1.0, factor))  # Clamp to [0, 1]
        
        r = int(color1[0] + (color2[0] - color1[0]) * factor)
        g = int(color1[1] + (color2[1] - color1[1]) * factor)
        b = int(color1[2] + (color2[2] - color1[2]) * factor)
        a = int(color1[3] + (color2[3] - color1[3]) * factor)
        
        return (r, g, b, a)
