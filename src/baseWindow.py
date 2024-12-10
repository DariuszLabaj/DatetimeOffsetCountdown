from abc import ABC, abstractmethod
from typing import Literal, Optional
import pygame

ColorValue = pygame.Color | tuple[int, int, int] | tuple[int, int, int, int] | str

class joystickButton:
    xBoxLayout: dict[int, str] = {
        0: "A",
        1: "B",
        2: "X",
        3: "Y",
        4: "L1",
        5: "R1",
        6: "Menu",
        7: "View",
        9: "L3",
        10: "L4"
    }
    @classmethod
    def name(cls, button: int):
        return cls.xBoxLayout.get(button, "Unknown")

class BaseWindow(ABC):
    _fill: Optional[ColorValue] = None
    _stroke: Optional[ColorValue] = None
    _strokeWeight: int = 0
    _keyCode: int = -1
    _keyName: str = ""
    _fps: int
    _height: int
    _width: int
    _mousePosition: tuple[int, int]
    _backgroundSurface: pygame.surface.Surface
    _translationMatrix: list[tuple[float, float]] = [(0.0, 0.0)]
    _displaySurface: pygame.surface.Surface
    _running: bool

    @property
    def Width(self) -> int:
        return self._backgroundSurface.get_width()

    @property
    def Height(self) -> int:
        return self._backgroundSurface.get_height()

    @property
    def IsRunning(self):
        return self._running

    @property
    def BackgroundSurface(self):
        return self._backgroundSurface

    @property
    def DisplaySurface(self):
        return self._displaySurface

    @property
    def keyCode(self) -> int:
        return self._keyCode

    @property
    def keyName(self) -> str:
        return self._keyName

    @property
    def MousePosition(self):
        self._mousePosition = pygame.mouse.get_pos()
        return self._mousePosition

    @property
    def _xTranslation(self) -> float:
        return self._translationMatrix[self._translationIndex][0]

    @property
    def _yTranslation(self) -> float:
        return self._translationMatrix[self._translationIndex][1]

    @property
    def _translationIndex(self) -> int:
        return len(self._translationMatrix)-1

    @property
    def Joystick(self):
        return self._joystick

    def __init__(self, width: int = 800, height: int = 600, caption: Optional[str] = None, fps: Optional[int] = None, flags: int = pygame.SRCALPHA):
        self._running = False
        self._flags = pygame.DOUBLEBUF | pygame.HWSURFACE | flags
        self._width = width
        self._height = height
        if self._flags & pygame.FULLSCREEN == pygame.FULLSCREEN:
            self._backgroundSurface = pygame.display.set_mode((0, 0), self._flags)
        else:
            self._backgroundSurface = pygame.display.set_mode((self._width, self._height), self._flags)
        self._displaySurface = pygame.Surface(self._backgroundSurface.get_rect().size, pygame.SRCALPHA)
        self._fps = fps if fps is not None else 60
        self._FramePerSec = pygame.time.Clock()
        self.Debug = False
        pygame.font.init()
        if caption:
            pygame.display.set_caption(caption)
        
        pygame.joystick.init()
        self._joystick : pygame.joystick.JoystickType | None = None
        self._joysticks: list[pygame.joystick.JoystickType] = []
        if pygame.joystick.get_count() > 0:
            for i in range(pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                self._joysticks.append(joystick)
            self._joystick = self._joysticks[0]  # Use the first joystick by default

    def Stop(self):
        self._running = False

    def _checkForEvents(self):
        events = pygame.event.get()
        for event in events:
            match event.type:  # type: ignore
                case pygame.QUIT:
                    self._running = False
                case pygame.KEYDOWN:
                    self._keyCode = event.key
                    self._keyName = pygame.key.name(event.key)
                    self.keyPressed()
                case pygame.KEYUP:
                    self._keyCode = event.key
                    self._keyName = pygame.key.name(event.key)
                    self.keyReleased()
                case pygame.MOUSEBUTTONDOWN:
                    self._mousePosition = pygame.mouse.get_pos()
                    self.mousePressed()
                case pygame.MOUSEBUTTONUP:
                    self._mousePosition = pygame.mouse.get_pos()
                    self.mouseReleased()
                case pygame.JOYBUTTONDOWN:
                    self._keyCode = event.button
                    self._keyName = joystickButton.name(event.button)
                    self.keyPressed()
                case pygame.JOYBUTTONUP:
                    self._keyCode = event.button
                    self._keyName = joystickButton.name(event.button)
                    self.keyPressed()
                case pygame.JOYAXISMOTION:
                    if not(-0.05 < event.value < 0.05):
                        self.axisMoved(event.axis, event.value)
                case pygame.JOYBALLMOTION:
                    self.ballMoved(event.ball, event.value)
                case pygame.JOYHATMOTION:
                    self.hatMoved(event.hat, event.value)

    def Start(self):
        pygame.init()
        self._running = True
        self.Setup()
        while self.IsRunning:
            self._checkForEvents()
            self._translationMatrix[self._translationIndex] = (0.0, 0.0)
            self.Draw()
            self.BackgroundSurface.blit(self.DisplaySurface, (0, 0))
            pygame.display.flip()
            self._FramePerSec.tick(self._fps)

    def keyPressed(self):
        pass

    def keyReleased(self):
        pass

    def mousePressed(self):
        pass

    def mouseReleased(self):
        pass

    def axisMoved(self, axis: int, value: float):
        pass
    
    def ballMoved(self, ball: int, value: float):
        pass
    
    def hatMoved(self, hat: int, value: float):
        pass

    @abstractmethod
    def Setup(self):
        ...

    @abstractmethod
    def Draw(self):
        ...

    def setFont(self, fontName: str = '', fontSize: int = 24):
        self._font = pygame.font.SysFont(fontName, fontSize)

    def fill(self, color: ColorValue):
        self._fill = color

    def noFill(self):
        self._fill = None

    def stroke(self, color: ColorValue):
        self._stroke = color

    def noStroke(self):
        self._stroke = None

    def strokeWeight(self, value: int):
        self._strokeWeight = value

    def background(self, color: ColorValue):
        self._backgroundSurface.fill(color)
        self._displaySurface = pygame.Surface(self._backgroundSurface.get_rect().size, pygame.SRCALPHA)

    def text(self, content: str, x: float, y: float, align: Optional[Literal["top", "left", "bottom", "right", "topleft", "bottomleft", "topright", "bottomright", "midtop", "midleft", "midbottom", "midright", "center", "centerx", "centery"]] = None):
        """Draw text on the screen."""
        text_surface = self._font.render(content, True, self._fill or (255, 255, 255, 255))
        match align:
            case "top":
                text_rect = text_surface.get_rect(top=(self._xTranslation+x, self._yTranslation+y))
            case "left":
                text_rect = text_surface.get_rect(left=(self._xTranslation+x, self._yTranslation+y))
            case "bottom":
                text_rect = text_surface.get_rect(bottom=(self._xTranslation+x, self._yTranslation+y))
            case "right":
                text_rect = text_surface.get_rect(right=(self._xTranslation+x, self._yTranslation+y))
            case "topleft":
                text_rect = text_surface.get_rect(topleft=(self._xTranslation+x, self._yTranslation+y))
            case "bottomleft":
                text_rect = text_surface.get_rect(bottomleft=(self._xTranslation+x, self._yTranslation+y))
            case "topright":
                text_rect = text_surface.get_rect(topright=(self._xTranslation+x, self._yTranslation+y))
            case "bottomright":
                text_rect = text_surface.get_rect(bottomright=(self._xTranslation+x, self._yTranslation+y))
            case "midtop":
                text_rect = text_surface.get_rect(midtop=(self._xTranslation+x, self._yTranslation+y))
            case "midleft":
                text_rect = text_surface.get_rect(midleft=(self._xTranslation+x, self._yTranslation+y))
            case "midbottom":
                text_rect = text_surface.get_rect(midbottom=(self._xTranslation+x, self._yTranslation+y))
            case "midright":
                text_rect = text_surface.get_rect(midright=(self._xTranslation+x, self._yTranslation+y))
            case "center":
                text_rect = text_surface.get_rect(center=(self._xTranslation+x, self._yTranslation+y))
            case "centerx":
                text_rect = text_surface.get_rect(centerx=(self._xTranslation+x, self._yTranslation+y))
            case "centery":
                text_rect = text_surface.get_rect(centery=(self._xTranslation+x, self._yTranslation+y))
            case _:
                text_rect = text_surface.get_rect()
        self.DisplaySurface.blit(text_surface, text_rect)

    def circle(self, x: float, y: float, radius: float):
        """Draw a circle."""
        if self._stroke:
            pygame.draw.circle(self.DisplaySurface, self._stroke, (int(self._xTranslation+x),
                               int(self._yTranslation+y)), int(radius), self._strokeWeight)
        else:
            pygame.draw.circle(self.DisplaySurface, self._fill or (255, 255, 255),
                               (int(self._xTranslation+x), int(self._yTranslation+y)), int(radius))

    def line(self, x1: float, y1: float, x2: float, y2: float):
        """Draw a line."""
        pygame.draw.line(self.DisplaySurface, self._stroke or (255, 255, 255),
                         (int(self._xTranslation+x1), int(self._yTranslation+y1)), (int(self._xTranslation+x2), int(self._yTranslation+y2)), self._strokeWeight)

    def rect(self, x: float, y: float, width: float, height: float):
        """Draw a rectangle."""
        rect = pygame.Rect(self._xTranslation+x, self._yTranslation+y, width, height)
        if self._fill and not self._stroke:
            pygame.draw.rect(self.DisplaySurface, self._fill, rect, width=0)
        elif not self._fill and self._stroke:
            pygame.draw.rect(self.DisplaySurface, self._stroke, rect, width=1 or self._strokeWeight)
        elif self._fill and self._stroke:
            if self._strokeWeight:
                pygame.draw.rect(self.DisplaySurface, self._stroke, rect, width=self._strokeWeight)
            else:
                pygame.draw.rect(self.DisplaySurface, self._stroke, rect, width=1)
        else:
            pygame.draw.rect(self.DisplaySurface, (255, 255, 255), rect, width=0)
        if self._stroke:
            pygame.draw.rect(self.DisplaySurface, self._stroke, rect, self._strokeWeight)

    def translate(self, x: float, y: float):
        """Translate (move) the origin."""
        self._translationMatrix[self._translationIndex] = (x, y)

    def rotate(self, angle: float):
        """Rotate the entire display surface."""
        self._displaySurface = pygame.transform.rotate(self._displaySurface, angle)
