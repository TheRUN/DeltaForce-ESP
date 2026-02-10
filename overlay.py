"""
OpenGL Overlay Module
Educational purpose: Demonstrates transparent overlay window and OpenGL rendering
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import logging
from typing import Tuple, List, Optional
import numpy as np


class Overlay:
    """
    OpenGL-based transparent overlay window.
    
    Educational Focus:
    - OpenGL rendering pipeline
    - Transparent window creation
    - 2D rendering in OpenGL
    - Alpha blending for transparency
    - Text rendering
    """
    
    def __init__(self, width: int, height: int, title: str = "ESP Overlay"):
        """
        Initialize the overlay window.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
            title: Window title
        """
        self.width = width
        self.height = height
        self.title = title
        self.running = False
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Font for text rendering
        self.font = None
        
        # Initialize pygame and OpenGL
        self._init_window()
    
    def _init_window(self):
        """
        Initialize pygame and OpenGL window.
        
        Educational Note:
        - Sets up a transparent overlay window using pygame
        - Configures OpenGL for 2D rendering
        - Enables alpha blending for transparency effects
        """
        try:
            # Initialize pygame
            pygame.init()
            
            # Set OpenGL attributes
            pygame.display.gl_set_attribute(pygame.GL_ALPHA_SIZE, 8)
            pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
            pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)
            
            # Create window with OpenGL
            # Note: For true transparency overlay on Windows, additional platform-specific
            # code would be needed (Win32 API). This is a simplified version.
            self.screen = pygame.display.set_mode(
                (self.width, self.height),
                DOUBLEBUF | OPENGL
            )
            pygame.display.set_caption(self.title)
            
            # Initialize font for text rendering
            pygame.font.init()
            self.font = pygame.font.SysFont('Arial', 14)
            
            # Setup OpenGL for 2D rendering
            self._setup_opengl()
            
            self.logger.info(f"Overlay window initialized: {self.width}x{self.height}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize overlay window: {e}")
            raise
    
    def _setup_opengl(self):
        """
        Configure OpenGL for 2D rendering.
        
        Educational Note:
        - Sets up orthographic projection for 2D rendering
        - Enables alpha blending for transparency
        - Configures blend function for proper alpha compositing
        - Disables depth testing (not needed for 2D)
        """
        # Set viewport to window dimensions
        glViewport(0, 0, self.width, self.height)
        
        # Setup orthographic projection (2D)
        # This maps screen coordinates directly: (0,0) = top-left, (width,height) = bottom-right
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)
        
        # Setup modelview matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Enable alpha blending for transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Disable depth testing (not needed for 2D)
        glDisable(GL_DEPTH_TEST)
        
        # Enable smooth lines
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        
        # Set clear color (transparent black)
        glClearColor(0.0, 0.0, 0.0, 0.0)
    
    def clear(self):
        """Clear the screen."""
        glClear(GL_COLOR_BUFFER_BIT)
    
    def draw_line(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        color: Tuple[int, int, int, int],
        thickness: float = 1.0
    ):
        """
        Draw a line on the overlay.
        
        Educational Note:
        Uses OpenGL's immediate mode rendering (legacy but educational).
        Modern OpenGL would use VBOs (Vertex Buffer Objects).
        
        Args:
            start: Starting point (x, y)
            end: Ending point (x, y)
            color: RGBA color (0-255 for each component)
            thickness: Line thickness in pixels
        """
        # Convert color to 0.0-1.0 range
        r, g, b, a = [c / 255.0 for c in color]
        
        # Set line width
        glLineWidth(thickness)
        
        # Draw line
        glBegin(GL_LINES)
        glColor4f(r, g, b, a)
        glVertex2f(start[0], start[1])
        glVertex2f(end[0], end[1])
        glEnd()
    
    def draw_box(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Tuple[int, int, int, int],
        thickness: float = 2.0,
        filled: bool = False
    ):
        """
        Draw a rectangular box.
        
        Educational Note:
        Can draw either outlined or filled rectangles.
        Uses GL_LINE_LOOP for outlines and GL_QUADS for filled boxes.
        
        Args:
            x: Top-left X coordinate
            y: Top-left Y coordinate
            width: Box width
            height: Box height
            color: RGBA color
            thickness: Line thickness (for outlined boxes)
            filled: If True, draw filled box; if False, draw outline
        """
        r, g, b, a = [c / 255.0 for c in color]
        
        if filled:
            # Draw filled rectangle
            glBegin(GL_QUADS)
            glColor4f(r, g, b, a)
            glVertex2f(x, y)
            glVertex2f(x + width, y)
            glVertex2f(x + width, y + height)
            glVertex2f(x, y + height)
            glEnd()
        else:
            # Draw outlined rectangle
            glLineWidth(thickness)
            glBegin(GL_LINE_LOOP)
            glColor4f(r, g, b, a)
            glVertex2f(x, y)
            glVertex2f(x + width, y)
            glVertex2f(x + width, y + height)
            glVertex2f(x, y + height)
            glEnd()
    
    def draw_3d_box(
        self,
        corners: List[Tuple[int, int]],
        color: Tuple[int, int, int, int],
        thickness: float = 2.0
    ):
        """
        Draw a 3D bounding box from corner points.
        
        Educational Note:
        Connects the 8 corners of a 3D box with lines to create
        a wireframe 3D box visualization.
        
        Args:
            corners: List of 8 (x, y) screen coordinates for box corners
            color: RGBA color
            thickness: Line thickness
        """
        if len(corners) != 8:
            return
        
        r, g, b, a = [c / 255.0 for c in color]
        glLineWidth(thickness)
        glColor4f(r, g, b, a)
        
        # Draw bottom face
        glBegin(GL_LINE_LOOP)
        for i in range(4):
            glVertex2f(corners[i][0], corners[i][1])
        glEnd()
        
        # Draw top face
        glBegin(GL_LINE_LOOP)
        for i in range(4, 8):
            glVertex2f(corners[i][0], corners[i][1])
        glEnd()
        
        # Draw vertical edges
        glBegin(GL_LINES)
        for i in range(4):
            glVertex2f(corners[i][0], corners[i][1])
            glVertex2f(corners[i + 4][0], corners[i + 4][1])
        glEnd()
    
    def draw_text(
        self,
        text: str,
        x: int,
        y: int,
        color: Tuple[int, int, int, int] = (255, 255, 255, 255)
    ):
        """
        Draw text on the overlay.
        
        Educational Note:
        Text rendering in OpenGL is complex. We use pygame's font system
        to render text to a surface, then convert it to an OpenGL texture.
        This is one of several approaches to text rendering.
        
        Args:
            text: Text to display
            x: X coordinate
            y: Y coordinate
            color: RGBA color
        """
        if not self.font:
            return
        
        try:
            # Render text to pygame surface
            text_surface = self.font.render(text, True, color[:3])
            text_data = pygame.image.tostring(text_surface, "RGBA", True)
            
            # Get text dimensions
            text_width = text_surface.get_width()
            text_height = text_surface.get_height()
            
            # Create OpenGL texture from text
            glEnable(GL_TEXTURE_2D)
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            
            glTexImage2D(
                GL_TEXTURE_2D, 0, GL_RGBA,
                text_width, text_height, 0,
                GL_RGBA, GL_UNSIGNED_BYTE, text_data
            )
            
            # Draw textured quad
            glColor4f(1.0, 1.0, 1.0, color[3] / 255.0)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex2f(x, y)
            glTexCoord2f(1, 0)
            glVertex2f(x + text_width, y)
            glTexCoord2f(1, 1)
            glVertex2f(x + text_width, y + text_height)
            glTexCoord2f(0, 1)
            glVertex2f(x, y + text_height)
            glEnd()
            
            # Cleanup
            glDeleteTextures([texture_id])
            glDisable(GL_TEXTURE_2D)
            
        except Exception as e:
            self.logger.debug(f"Error rendering text: {e}")
    
    def draw_health_bar(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        health_percent: float,
        border_color: Tuple[int, int, int, int] = (255, 255, 255, 255),
        low_health_color: Tuple[int, int, int, int] = (255, 0, 0, 200),
        high_health_color: Tuple[int, int, int, int] = (0, 255, 0, 200)
    ):
        """
        Draw a health bar.
        
        Educational Note:
        Demonstrates color interpolation and layered rendering.
        Combines a background, border, and colored fill.
        
        Args:
            x: X coordinate
            y: Y coordinate
            width: Bar width
            height: Bar height
            health_percent: Health percentage (0.0 to 1.0)
            border_color: Color of the border
            low_health_color: Color at 0% health
            high_health_color: Color at 100% health
        """
        # Clamp health to 0-1 range
        health_percent = max(0.0, min(1.0, health_percent))
        
        # Draw background (black)
        self.draw_box(x, y, width, height, (0, 0, 0, 150), filled=True)
        
        # Interpolate health bar color based on health percentage
        r = int(low_health_color[0] + (high_health_color[0] - low_health_color[0]) * health_percent)
        g = int(low_health_color[1] + (high_health_color[1] - low_health_color[1]) * health_percent)
        b = int(low_health_color[2] + (high_health_color[2] - low_health_color[2]) * health_percent)
        a = int(low_health_color[3] + (high_health_color[3] - low_health_color[3]) * health_percent)
        
        # Draw health fill
        fill_width = int(width * health_percent)
        if fill_width > 0:
            self.draw_box(x, y, fill_width, height, (r, g, b, a), filled=True)
        
        # Draw border
        self.draw_box(x, y, width, height, border_color, thickness=1.0)
    
    def draw_circle(
        self,
        x: int,
        y: int,
        radius: float,
        color: Tuple[int, int, int, int],
        segments: int = 32,
        filled: bool = False
    ):
        """
        Draw a circle.
        
        Educational Note:
        Circles are approximated using line segments or triangles.
        More segments = smoother circle but more performance cost.
        
        Args:
            x: Center X coordinate
            y: Center Y coordinate
            radius: Circle radius
            color: RGBA color
            segments: Number of segments (higher = smoother)
            filled: If True, draw filled circle
        """
        r, g, b, a = [c / 255.0 for c in color]
        glColor4f(r, g, b, a)
        
        if filled:
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(x, y)  # Center point
        else:
            glBegin(GL_LINE_LOOP)
        
        for i in range(segments):
            angle = 2.0 * 3.14159 * i / segments
            dx = radius * np.cos(angle)
            dy = radius * np.sin(angle)
            glVertex2f(x + dx, y + dy)
        
        glEnd()
    
    def update(self):
        """
        Update the display.
        
        Educational Note:
        Swaps the front and back buffers (double buffering).
        This prevents flickering by rendering to an off-screen buffer
        then displaying it all at once.
        """
        pygame.display.flip()
    
    def handle_events(self) -> bool:
        """
        Handle window events.
        
        Returns:
            True if window should continue running, False to quit
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def cleanup(self):
        """Clean up resources and close window."""
        pygame.quit()
        self.logger.info("Overlay window closed")
