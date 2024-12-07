import datetime
import enum
import random
from baseWindow import BaseWindow
from firework import Firework
from particleText import ParticleText
from timezones import TimeZones, TimezoneOffset
import pygame

ColorValue = pygame.Color | tuple[int, int, int] | tuple[int, int, int, int] | str


class MainWindow(BaseWindow):
    fireworks: list[Firework]
    gravity = pygame.Vector2(0, 0.2)
    __timezoneOffset = TimezoneOffset()

    @property
    def Now(self):
        return datetime.datetime.now()

    def keyPressed(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LALT] and keys[pygame.K_RETURN]:
            self.ToggleFullscreen()

    def ToggleFullscreen(self):
        self.__isFullScreen = not self.__isFullScreen
        if self.__isFullScreen:
            self._backgroundSurface = pygame.display.set_mode(
                (self._width, self._height), self._flags | pygame.FULLSCREEN)
        else:
            self._backgroundSurface = pygame.display.set_mode((self._width, self._height), self._flags)
        self.UpdateLogic()

    def SetDebug(self):
        self.Debug = True

    def SetTimezoneOffset(self, timezone: TimeZones):
        self.__timezoneOffset = TimezoneOffset(timezone)

    def Setup(self):
        self.fireworks = []
        self.StartCelebration = 2
        self.EndCelebration = 58
        self.background((0, 0, 0))
        self.__isFullScreen = False
        # Timezone countdown setup
        # self.__timezoneOffset = TimezoneOffset(TimeZones.Central_Europe)
        self.listOfTimeZones = [x.value - TimeZones.Central_Europe for x in TimeZones]
        self.timeZoneIndex = 0
        self.__setCountdownPoint()
        self.__lastUpdate = self.Now.second
        # Text Display setup
        self.setFont(fontSize=80)
        self.timezoneText = ParticleText(self.Width, self.Height, 20, 20, self._font, align="topleft")
        self.countDownText = ParticleText(self.Width, self.Height, self.Width-20,
                                          self.Height-20, self._font, align="bottomright")
        self.__mode = ProgramMode.TimeZoneDisplay
        self.UpdateLogic()

    def __setCountdownPoint(self):
        if not self.Debug:
            return
        hours = self.listOfTimeZones[self.timeZoneIndex]
        self.__timezoneOffset.setCountdownPoint(
            datetime.datetime.now() + datetime.timedelta(hours=hours, minutes=0, seconds=30))
        self.timeZoneIndex += 1

    def UpdateLogic(self):
        match self.__mode:
            case ProgramMode.PreCountDown:
                self.__BgImage = pygame.image.load(
                    "Resources/"+self.timezoneText.Text.replace(' ', '_')+".png").convert_alpha()
                self.setFont(fontSize=120)
                self.countDownText.setFont(self._font, generate=False)
                self.countDownText.setAlignment("midtop", generate=False)
                self.countDownText.setPosition(self.Width//2, self.Height//2+20, generate=False)

                self.timezoneText.setFont(self._font, generate=False)
                self.timezoneText.setAlignment("midbottom", generate=False)
                self.timezoneText.setPosition(self.Width//2, self.Height//2+20, generate=False)
            case ProgramMode.CountDown:
                self.__BgImage = pygame.image.load(
                    "Resources/"+self.timezoneText.Text.replace(' ', '_')+".png").convert_alpha()
                self.setFont(fontSize=120)
                self.timezoneText.setFont(self._font, generate=False)
                self.timezoneText.setAlignment("midbottom", generate=False)
                self.timezoneText.setPosition(self.Width//2, self.Height//4)
                self.setFont(fontSize=240)
                self.countDownText.setFont(self._font, generate=False)
                self.countDownText.setAlignment("center", generate=False)
                self.countDownText.setPosition(self.Width//2, self.Height//2, generate=False)
            case ProgramMode.PostCountDown:
                self.setFont(fontSize=80)
                self.countDownText.setFont(self._font, generate=False)
                self.countDownText.setAlignment("bottomright", generate=False)
                self.countDownText.setPosition(self.Width-20, self.Height-20, generate=False)

                self.timezoneText.setFont(self._font, generate=False)
                self.timezoneText.setAlignment("topleft", generate=False)
                self.timezoneText.setPosition(20, 20, generate=False)
            case _:
                self.__BgImage = pygame.image.load("Resources/timezoneBg.jpg").convert_alpha()
                self.setFont(fontSize=80)
                self.timezoneText.setFont(self._font, generate=False)
                self.timezoneText.setAlignment("topleft", generate=False)

                self.countDownText.setAlignment("bottomright", generate=False)
                self.countDownText.setFont(self._font, generate=False)
                self.countDownText.setPosition(self.Width-20, self.Height-20, generate=False)

        self.timezoneText.setSize(self.Width, self.Height)
        self.countDownText.setSize(self.Width, self.Height)
        self.__BgToDisplay = pygame.transform.scale(self.__BgImage, (self.Width, self.Height))

    def Logic(self):
        if (self.Now.second != self.__lastUpdate):
            self.__lastUpdate = self.Now.second
            timezone, hours, minutes, seconds = self.__timezoneOffset.getLowestTimedelta()
            if timezone:
                if (minutes > self.EndCelebration):
                    self.timezoneText.updateText(f"Next: {timezone}")
                else:
                    self.timezoneText.updateText(timezone)
                if hours:
                    self.countDownText.updateText(f"{hours+1} hours")
                    if self.__mode != ProgramMode.TimeZoneDisplay:
                        self.__mode = ProgramMode.TimeZoneDisplay
                        self.UpdateLogic()
                elif minutes:
                    self.countDownText.updateText(f"{minutes+1} minutes")
                    if minutes < self.StartCelebration and self.__mode == ProgramMode.TimeZoneDisplay:
                        self.__mode = ProgramMode.PreCountDown
                        self.UpdateLogic()
                    elif minutes > self.EndCelebration and self.__mode == ProgramMode.CountDown:
                        self.__mode = ProgramMode.PostCountDown
                        self.UpdateLogic()
                    elif self.EndCelebration >= minutes > self.StartCelebration and self.__mode != ProgramMode.TimeZoneDisplay:
                        self.__setCountdownPoint()
                        self.__mode = ProgramMode.TimeZoneDisplay
                        self.UpdateLogic()
                else:
                    self.countDownText.updateText(f"{seconds}")
                    if self.__mode != ProgramMode.CountDown:
                        self.__mode = ProgramMode.CountDown
                        self.UpdateLogic()

    def Draw(self):
        self.Logic()
        self.BackgroundSurface.blit(self.__BgToDisplay, (0, 0))
        self.DisplaySurface.fill((0, 0, 0, 0))
        if self.__mode == ProgramMode.PostCountDown:
            if random.random() < 0.2:
                self.fireworks.append(Firework(self.Width, self.Height, self.gravity))
        else:
            self.countDownText.update()
            self.DrawParticles(self.countDownText.Particles)
            self.timezoneText.update()
            self.DrawParticles(self.timezoneText.Particles)
        if self.fireworks:
            for i in range(len(self.fireworks) - 1, -1, -1):
                self.fireworks[i].update()
                self.fireworks[i].show(self.DisplaySurface)
                if self.fireworks[i].offScreen:
                    self.fireworks.pop(i)

    def DrawParticles(self, particles: list[ParticleText.Particle], radius: int = 2):
        self.fill((255, 255, 255))
        # self.stroke((0, 0, 0, 128))
        # self.strokeWeight(1)
        # for particle in particles:
        #     self.circle(particle.X, particle.Y, radius+2)
        self.noStroke()
        for particle in particles:
            self.circle(particle.X, particle.Y, radius)


class ProgramMode(enum.Enum):
    TimeZoneDisplay = enum.auto()
    PreCountDown = enum.auto()
    CountDown = enum.auto()
    PostCountDown = enum.auto()
