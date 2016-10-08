import os, sys, pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]
SIZE = WIDTH, HEIGHT = 600, 700
BLACK = (0, 0, 0)
BLOOD_RED = (165, 4, 4)
GHAAS_GREEN = (4, 60, 4)
WHITE = (255,255,255)
PLACES = 1
SPEED_UPDATE_COLLISIONS = 5

def load_image(name):
    image = pygame.image.load(name).convert()
    # color = pygame.Color(255,255,255)
    color = image.get_at((0,0))    #another way to get color
    image.set_colorkey(color)
    rect = image.get_rect()
    return image, rect

def get_text_center_margin(textsurface):
    text_width = textsurface.get_width()
    center = WIDTH/2 - text_width/2
    return center

def show_game_over():
    screen = pygame.display.get_surface()
    screen.fill(BLOOD_RED)
    pygame.font.init()

    myfont = pygame.font.SysFont('Comic Sans MS', 60)
    textsurface = myfont.render('Game Over', False, (255, 255, 255))
    screen.blit(textsurface,(get_text_center_margin(textsurface), (HEIGHT/2)-50))
    
    myfont1 = pygame.font.SysFont('Comic Sans MS', 23)
    textsurface1 = myfont1.render('your ball(s) have been crushed !! Play again(y/n)?', False, (255, 255, 255))
    screen.blit(textsurface1,(get_text_center_margin(textsurface1), (HEIGHT/2)))
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.key == pygame.K_y:
                start_game()
            elif event.key == pygame.K_n:
                sys.exit()


def check_game_paused(paused):
    if paused:
        screen = pygame.display.get_surface()
        screen.fill(GHAAS_GREEN)
        pygame.font.init()

        myfont = pygame.font.SysFont('Comic Sans MS', 60)
        textsurface = myfont.render('Game Paused', False, (255, 255, 255))
        screen.blit(textsurface,(get_text_center_margin(textsurface), (HEIGHT/2)-50))

        myfont1 = pygame.font.SysFont('Comic Sans MS', 23)
        textsurface1 = myfont1.render('your ball(s) have been freezed !! Press E to exit other to unfreeze', False, (255, 255, 255))
        screen.blit(textsurface1,(get_text_center_margin(textsurface1), (HEIGHT/2)))

        pygame.display.flip()
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        sys.exit()
                    else:
                        paused = False
                        return paused
    else:
        return paused

def show_score(score):
    screen = pygame.display.get_surface()
    pygame.font.init()

    myfont1 = pygame.font.SysFont('Comic Sans MS', 23)
    textsurface1 = myfont1.render('score', False, (255, 255, 255))
    screen.blit(textsurface1,( (WIDTH - 50), 20))
    
    myfont = pygame.font.SysFont('Comic Sans MS', 40)
    textsurface = myfont.render(str(score), False, (255, 255, 255))
    screen.blit(textsurface,( (WIDTH - 35), 40))

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    try:
        sound = pygame.mixer.Sound(name)
    except pygame.error:
        print ('Cannot load sound: %s' % name)
        raise SystemExit(str(geterror()))
    return sound


class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("ball_red.png")
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.rect.inflate(-90,-90)
        self.speed = [1, 1]
        self.collisions = 0


    def move(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed[0] = -self.speed[0]

        if self.rect.top < 0:
            self.speed[1] = -self.speed[1]

        if self.rect.top > HEIGHT:
            show_game_over()

    def update_speed(self):
        new_speed = int(self.collisions / SPEED_UPDATE_COLLISIONS) + 1
        if self.speed[0] > 0:
            self.speed[0] = new_speed
        else:
            self.speed[0] = -new_speed

        if self.speed[1] > 0:
            self.speed[1] = new_speed
        else:
            self.speed[1] = -new_speed


    def bounce(self, p1):
        # L-> R : positive, R -> L :: negative
        # T -> B : posti, B -> T : negative
        if p1.handle_rect.top <= self.rect.bottom:
            if (p1.handle_rect.top + 20) <= self.rect.bottom:
                self.speed[0] = -self.speed[0]
            else:
                if self.speed[1] >= 0:
                    p1.score += 1
                    self.collisions += 1
                    if self.collisions % SPEED_UPDATE_COLLISIONS:
                        self.update_speed()
                    self.speed[1] = -self.speed[1]
                if (p1.handle_rect.left + 20) > self.rect.right:
                    if self.speed[0] >= 0:
                        self.speed[0] = -self.speed[0]

                elif (p1.handle_rect.right - 20) < self.rect.left:
                    if self.speed[0] < 0:
                        self.speed[0] = -self.speed[0]            


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        # self.handle = pygame.draw.rect(screen, WHITE, [75, 10, 50, 20])
        self.handle, self.handle_rect = load_image("blue_oval.png")
        
        self.handle = pygame.transform.scale(self.handle, (160,30))     # blue_oval.png
        self.handle_rect = self.handle_rect.inflate(-435,-110)          # blue_oval.png
        
        self.handle_rect.y = screen.get_height() - self.handle_rect.height
        self.score = 0
        
    def move_left(self, places):
        if self.handle_rect.left < 0:
            pass
        else:
            self.handle_rect = self.handle_rect.move(-places, 0)

    def move_right(self, places):
        if self.handle_rect.right > WIDTH:
            pass
        else:
            self.handle_rect = self.handle_rect.move(places, 0)

    


def start_game():
    screen = pygame.display.get_surface()
    # collision_sound = load_sound("ball_bounce.wav")
    ball = Ball()
    balls = [ball]
    
    p1 = Player()

    pressing_right = False
    pressing_left = False
    paused = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pressing_right = True
                elif event.key == pygame.K_LEFT:
                    pressing_left = True
                elif event.key == pygame.K_ESCAPE:
                    if paused:
                        paused = False
                    else:
                        paused = True
                elif event.key == pygame.K_n:
                    if len(balls) < 4:
                        new_ball = Ball()
                        balls.append(new_ball)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    pressing_right = False
                elif event.key == pygame.K_LEFT:
                    pressing_left = False

            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     new_ball = Ball()
            #     balls.append(new_ball)

        paused = check_game_paused(paused)
        
        screen.fill(BLACK)
        if pressing_right:
            p1.move_right(PLACES)
        if pressing_left:
            p1.move_left(PLACES)

        for ball in balls:
            ball.move()
            screen.blit(ball.image, ball.rect)
            screen.blit(p1.handle, p1.handle_rect)
            if ball.rect.colliderect(p1.handle_rect):
                # collision_sound.play()
                ball.bounce(p1)

        show_score(p1.score)
        # pygame.display.update()
        pygame.display.flip()


def main():
    pygame.init()
    
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('test game')

    start_game()

if __name__ == '__main__':
    main()
