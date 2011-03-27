import pygame
import random
import os
import sys
from pygame.locals import *
from helpers import *

if not pygame.font: 
    print 'Warning, fonts disabled'
if not pygame.mixer: 
    print 'Warning, sound disabled'

#DO WORK

stages = ['spark', 'zeal', 'moxie', 'vigor', 'drive', 'fire']
class GameMain:
    def __init__(self):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = 640
        self.height = 480
        """Create the Screen"""
        pygame.display.set_caption("SO ENERGETIC! By Jrabbit!", "SO-ENERGETIC")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.POINTS = 0
    def MainLoop(self):
        """This is the Main Loop of the Game"""
        self.load_sprites()
        # if pygame.mixer:
        #     self.load_music()
        self.showing_credits = 0
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if ((event.key == K_RIGHT)
                    or (event.key == K_LEFT)
                    or (event.key == K_UP)
                    or (event.key == K_DOWN)):
                        self.thedude.move(event.key)
            if pygame.key.get_pressed()[K_q]:
                print 'you pressed q'
                if self.showing_credits:
                    pygame.time.wait(1000)
                    sys.exit()
                else:
                    self.show_credits()
            # if POINTS > 20:
            #     if not self.showing_credits:
            #         self.show_credits()
            self.background = pygame.Surface(self.screen.get_size())
            self.background = self.background.convert()
            # if POINTS < 3:
            #     self.bkg_color = (85,98,112)
            # elif POINTS > 3:
            #     self.bkg_color = (199,244,100)
            # elif POINTS > 5:
            #     self.bkg_color = (196,77,88)
            # elif POINTS > 10:
            #     self.bkg_color = (78,205,196)
            # elif POINTS > 15:
            #     self.bkg_color = (255,107,107)
            self.bkg_color = (85,98,112)
            self.background.fill(self.bkg_color)
            self.screen.blit(self.background, (0, 0))
            self.meterSprites.draw(self.screen)
            self.dudesprites.draw(self.screen)
            self.meterSprites.update(pygame.time.get_ticks())
            # self.cop_sprites.update(pygame.time.get_ticks())
            # self.lstCols = pygame.sprite.spritecollide(self.bear, self.cop_sprites, False)
            if self.showing_credits:
                self.credits_sprites.draw(self.screen)
            # if self.lstCols:
            #     self.collision()
                # print self.lstCols
            pygame.display.flip()
    
    def load_sprites(self):
        self.energymeter = Energymeter()
        self.meterSprites = pygame.sprite.RenderPlain(self.energymeter)
        self.thedude = Dude()
        self.dudesprites = pygame.sprite.RenderPlain(self.thedude)
        
    def load_music(self):
        pygame.mixer.music.load(os.path.join('data', 'music', '05 - What would Freud say.ogg'))
        pygame.mixer.music.play()
        
    def collision(self):
        global POINTS
        wilhelm = pygame.mixer.Sound(os.path.join('data', 'music', 'wscream1.ogg'))
        pygame.mixer.Sound.play(wilhelm)
        POINTS += 1
        self.score_sprites.update() #draw score to screen
        #kill the cop and respawn
        self.cop_sprites.remove(self.cop)
        self.bear_sprites.remove(self.bear)
        #respawn
        self.cop = Cop()
        self.cop_sprites = pygame.sprite.RenderPlain(self.cop)
        self.bear = Bear()
        self.bear_sprites = pygame.sprite.RenderPlain(self.bear)
        
    def advance(self):
        self.current_stage = stages.pop(0)
        #do stuff to make different stages

class Dude(pygame.sprite.Sprite):
    """Custom sprite"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('thedude_sized.gif', -1)
        self.y_dist = 15
        self.x_dist = 15

    def move(self, key):
        xMove = 0
        yMove = 0
        if MainWindow.POINTS > 0:
            if (key == K_RIGHT):
                xMove = self.x_dist
            elif (key == K_LEFT):
                xMove = -self.x_dist
            elif (key == K_UP):
                yMove = -self.y_dist
            elif (key == K_DOWN):
                yMove = self.y_dist
            MainWindow.POINTS -= 1
            self.rect.move_ip(xMove,yMove)

class Energymeter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ubuntu_font = os.path.join('data', 'ubuntu-font', 'Ubuntu-R.ttf')
        self.font = pygame.font.Font(self.ubuntu_font, 20)
        self.color = Color('white')
        self.lastscore = -1
        self.last_update = 0
        self.delay = 3000
        self.update(pygame.time.get_ticks())
        self.rect = self.image.get_rect().move(10, 450)
        
        
    def update(self,t):
        if t - self.last_update > self.delay:
            # print "granting energy"
            MainWindow.POINTS += 5
            self.last_update = t
        self.meter = '['+ "|" * int(MainWindow.POINTS) + ' ' * (50 - int(MainWindow.POINTS)) + ']'
        if MainWindow.POINTS != self.lastscore:
            msg = "ENERGY: %s" % self.meter
            self.image = self.font.render(msg, 1, self.color)

class scene(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
         
    def update(self):
        self.image , self.rect = load_image('bg_%s' % MainWindow.current_stage, -1)
        self.position = self.move
        

if __name__ == "__main__":
    MainWindow = GameMain()
    MainWindow.MainLoop()