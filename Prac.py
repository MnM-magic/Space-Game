import pygame
import random
from os.path import join#for joinnig paths for images)
# general setup

pygame.init()
pygame.joystick.init()
WINDOW_WIDTH, Window_HEIGHT = 1280,720

class stars(pygame.sprite.Sprite):
    def __init__(self,groups,surf):
        super().__init__(groups)
        self.image=surf

    def update(self):
        self.rect=self.image.get_rect(center=(random.randint(0,WINDOW_WIDTH),random.randint(0,Window_HEIGHT)))
        if self.rect.bottom<0:
            self.kill()

class animatedexplosion(pygame.sprite.Sprite):
    def __init__(self,frames,pos,groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image=self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        explosion_sound.play()

    def update(self, dt):
        self.frame_index+=20*dt
        if self.frame_index<len(self.frames):
            self.image=self.frames[int(self.frame_index)]# % len(self.frames)]
        else:
            self.kill
            
class meteor(pygame.sprite.Sprite):
    def __init__(self,surf,pos, groups):
        super().__init__(groups)
        self.original_surf=surf
        self.image=self.original_surf
        self.rect=self.image.get_rect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 7000
        self.direction= pygame.Vector2(random.uniform(-0.5,0.5),1)
        self.speed=random.randint(900,1000)
        self.rotationspeed=random.randint(40,80)
        self.rotation=0
        #self.mask = pygame.mask.from_surface(self.image)
    def update(self,dt):
        self.rect.center+=self.direction
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()  
        if score == 33:
            self.speed=self.speed*2 
        #continuous rotation
        self.rotation+=self.rotationspeed*dt
        self.image = pygame.transform.rotozoom(self.original_surf,self.rotation,1)
        self.rect=self.image.get_rect(center=self.rect.center)#new rectangle with same center position as the last one
                            
class laser(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.image=surf
        self.rect = self.image.get_rect(midbottom = pos)
        #self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.rect.centery-=200*dt
        if self.rect.bottom<0:
            self.kill()

class Plane(pygame.sprite.Sprite):
    def __init__(self,groups):
        global score
        score=0
        #plane display through sprite
        super().__init__(groups)
        self.image=pygame.image.load("E:/Game file/images/Ships.png").convert_alpha()
        self.rect=self.image.get_rect(center=(WINDOW_WIDTH/2,Window_HEIGHT/2)).inflate(0,-90)#decrease hit zone
        self.direct=pygame.Vector2( )
        self.speed=250
        
        #cooldown
        self.can_shoot=True
        self.laser_shoot_timer = 0
        self.cooldown_duration=400

        # masking for collisions
        self.mask = pygame.mask.from_surface(self.image)
        #mask_surf = mask.to_surface()
        #mask_surf.set_colorkey((0,0,0))
        #self.image = mask_surf
        
    def laser_timer(self):
        if not self.can_shoot:
            current_time=pygame.time.get_ticks()
            if current_time-self.laser_shoot_time >=self.cooldown_duration:
                self.can_shoot = True
    
    def update(self,dt):
        #input fot keyboard
        keys=pygame.key.get_pressed()
        
        self.direct.x=int(keys[pygame.K_RIGHT])-int(keys[pygame.K_LEFT])
              
        self.direct.y=int(keys[pygame.K_DOWN])-int(keys[pygame.K_UP])

        self.direct=self.direct.normalize() if self.direct else self.direct 
        recent_key= pygame.key.get_pressed()
        if plane.rect.right!=1280 or plane.rect.left!=0:
            self.rect.center += self.direct * self.speed * dt
        
        #controler movements
        if joysticks:  # Check if a controller is connected
            joystick = joysticks[0]  # Use the first joystick
            hat_x, hat_y = joystick.get_hat(0)  # Read D-Pad input
        
            #   Apply movement based on D-Pad direction
            self.direct.x = hat_x  # Left (-1), Right (1)
            self.direct.y = -hat_y  # Up (1), Down (-1) -> Flip Y-axis
        self.rect.center += self.direct * self.speed * dt

        #controller lazer
        for joystick in joysticks:
             #shoot with buttons
             if joystick.get_button(3)and self.can_shoot: 
                #shooting
                laser(laser_surface, self.rect.midtop, (all_sprites, Laser_sprites))
                self.can_shoot=False
                self.laser_shoot_time = pygame.time.get_ticks()
                laser_sound.play()
        self.laser_timer()     
        
        if score==15:
            self.image=pygame.image.load("E:/Game file/images/Ships.png").convert_alpha()
        if score==35:
            self.image=pygame.image.load("E:/Game file/images/My one day.jpg").convert_alpha()
        
        #keyboard laser
        if recent_key[pygame.K_SPACE] and self.can_shoot: 
            laser(laser_surface,self.rect.midtop,(all_sprites,Laser_sprites))
            
            self.can_shoot=False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()
        self.laser_timer()

        
def collision():
    global running
    global score
    collided_sprites=pygame.sprite.spritecollide(plane,meteor_sprites,True,pygame.sprite.collide_mask)
    
    if collided_sprites:
       score-=5
       damage_sound.play()
       running = False
    
    if score<0:
        running=False      
    
    for Laser in Laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(Laser,meteor_sprites,True)

        if collided_sprites:
            score+=5
            Laser.kill() 
            animatedexplosion(explosion_frames, Laser.rect.midtop,all_sprites)
            

def Numbers_font():
      
    #score
    score_surf=Score_font.render(str(score), True,(222,222,222))
    score_rect=score_surf.get_rect(midbottom = (WINDOW_WIDTH-80,Window_HEIGHT-50))
    display_surface.blit(score_surf,score_rect)
    
    #word
    word_surf=text_font.render("Shots on target", True,(222,222,222))
    word_rect=word_surf.get_rect(midtop = (WINDOW_WIDTH-80,Window_HEIGHT-50))
    display_surface.blit(word_surf,word_rect)
    #time
    current_timer=pygame.time.get_ticks()//10
    text_surf=time_font.render(str(current_timer), True,(222,222,222))
    text_rect=text_surf.get_rect(midbottom = (WINDOW_WIDTH/2,Window_HEIGHT-50))
    display_surface.blit(text_surf,text_rect)
    #distance
    Distance_surf=Dist_font.render("Distance", True,(222,222,222))
    Distance_rect=Distance_surf.get_rect(midbottom = (WINDOW_WIDTH/2,Window_HEIGHT-20))
    display_surface.blit(Distance_surf,Distance_rect)
    #borders
    pygame.draw.rect(display_surface,(222,222,222),text_rect.inflate(20,10).move(0,-8),5,15)
    
#background  
display_surface =pygame.display.set_mode((WINDOW_WIDTH, Window_HEIGHT),pygame.RESIZABLE)
surface=pygame.Surface((100,200))
running = True

#imports
star_surf = pygame.image.load("E:/Game file/images/star.png").convert_alpha()

Meteor =pygame.image.load("E:/Game file/images/meteor.png").convert_alpha()

laser_surface=pygame.image.load("E:/Game file/images/laser.png").convert_alpha()

explosion_frames=[pygame.image.load(join("E:/","Game file","images","explosion",f"{i}.png")).convert_alpha() for i in range (21)]

laser_sound=pygame.mixer.Sound(join("E:/","Game file","audio","laser.wav"))
laser_sound.set_volume(0.3)

explosion_sound=pygame.mixer.Sound(join("E:/","Game file","audio","explosion.wav"))
explosion_sound.set_volume(0.3)

damage_sound = pygame.mixer.Sound(join("E:/","Game file","audio","damage.wav"))
damage_sound.set_volume(0.3)

game_music =pygame.mixer.Sound(join("E:/","Game file","audio","xo.mp3"))
game_music.set_volume(0.5)
game_music.play(loops=-1)

#font
time_font=pygame.font.Font("E:/Game file/images/almonte/almonte woodgrain.ttf",40)
Score_font=pygame.font.Font("E:/Game file/images/almonte/almonte snow.ttf",50)
text_font=pygame.font.Font("E:/Game file/images/almonte/almonte.ttf",20)
Dist_font=pygame.font.Font("E:/Game file/images/almonte/almonte.ttf",20)
 #sprites
all_sprites=pygame.sprite.Group()
star_sprites=pygame.sprite.Group()
meteor_sprites=pygame.sprite.Group()
Laser_sprites=pygame.sprite.Group()

#logo icon
pygame.display.set_caption("Battle front")
img = pygame.image.load("E:/Game file/images/pixil-frame-0.png")
print(img)
pygame. display. set_icon(img)

#joysticks
joysticks = []

plane=Plane(all_sprites)
for i in range(20):
    stars(star_sprites, star_surf)
speed = 500
 
#custom event -> metor
Meteor_event=pygame.event.custom_type()
pygame.time.set_timer(Meteor_event,speed)
Star_time=pygame.event.custom_type()
clock=pygame.time.Clock()

'''x=100
z=0
i=0'''

#surface with image
#Plane_surface=pygame.image.load("../images/player.png").convert_alpha()
#or Plane_surface=pygame.image.load(join("images","player.png")).convert_alpha()

#20 different random star positions with stars
#star_positions=[(random.randint(0,1280),random.randint(0,720))for i in range(20)]

#plain surface
#surface.fill("maroon")

# laser_rect=laser_surface.get_rect(center=(WINDOW_WIDTH-20,Window_HEIGHT-20))

test_rect=pygame.Rect(0,0,300,600)
#score

while running: 
    dt=clock.tick()/1000 
    #event loop to loop game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type==pygame.JOYDEVICEADDED:
           print(event)#print connection
           joy=pygame.joystick.Joystick(event.device_index)#get device number
           joysticks.append(joy)#add joystick to the array

        if event.type==Meteor_event:
            x,y=random.randint(0,WINDOW_WIDTH),random.randint(-200,-100)
            meteor(Meteor,(x,y),(all_sprites,meteor_sprites))  
              
    '''if event.type==pygame.MOUSEMOTION:
            Plane_rectangle.center= event.pos'''
    
    #fill window with blue color
    
    
    star_sprites.update()
    all_sprites.update(dt)
    
    #display_surface.blit(surface,(x,150))
    
    #Movement bounce
    '''if Plane_rectangle.right>WINDOW_WIDTH or Plane_rectangle.left<0:
        Plane_direct.x*=-1
    if Plane_rectangle.top<0 or Plane_rectangle.bottom>Window_HEIGHT:
        Plane_direct.y*=-1'''
    '''display_surface.blit(Meteor,Meteor_rect)
    display_surface.blit(laser_surface,laser_rect)'''
    collision()
    
    #draw game
    display_surface.fill((23,35,40))
    star_sprites.draw(display_surface)
    all_sprites.draw(display_surface) 
    pygame.transform.grayscale(display_surface)
    Numbers_font()
    #test collisions
    pygame.display.update()
    
pygame.quit()