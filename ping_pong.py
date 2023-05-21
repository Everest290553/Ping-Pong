import pygame
pygame.init()

win_width = 900
win_height = 700
FPS = 60

score_l = 0
score_r = 0

round = 1

ask_check = False

window = pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption('Ping Pong Game')
background = pygame.image.load('table.png')
clock = pygame.time.Clock()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))
        self.speed = speed
        self.width = width
        self.height = height
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update_L(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 30:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < 430:
            self.rect.y += self.speed
    def update_R(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 30:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < 430:
            self.rect.y += self.speed

racket_L = Player('racket.png', 20, 250, 80, 240, 3)
racket_R = Player('racket.png', 800, 250, 80, 240, 3)

ball = GameSprite('ball.png', 425, 325, 50, 50, 3)
speed_x = 3
speed_y = 3

def l_win():
    text = pygame.font.Font(None, 100).render('Гравець 1 вийграв!', True, (0,0,255))
    window.blit(text, (125,325))
    global label1, label2
    label1 = pygame.font.Font(None,50).render('Гравець1', True, (0,255,0))
    label2 = pygame.font.Font(None,50).render('Гравець2', True, (255,0,0))
def r_win():
    text = pygame.font.Font(None, 100).render('Гравець 2 вийграв!', True, (0,0,255))
    window.blit(text, (125,325))
    global label1, label2
    label1 = pygame.font.Font(None,50).render('Гравець1', True, (255,0,0))
    label2 = pygame.font.Font(None,50).render('Гравець2', True, (0,255,0))

label1 = pygame.font.Font(None,50).render('Гравець1', True, (0,0,255))
label2 = pygame.font.Font(None,50).render('Гравець2', True, (0,0,255))

score_l_label = pygame.font.Font(None,50).render(str(score_l), True, (0,0,255))
score_r_label = pygame.font.Font(None,50).render(str(score_r), True, (0,0,255))

round_label = pygame.font.Font(None, 50).render('Раунд '+str(round), True, (0,0,255))

ask_continue_label = pygame.font.Font(None, 50).render('Продовжити', True, (0,0,255))
ask_restart_label = pygame.font.Font(None,50).render('Зіграти знову', True, (0,0,255))
end_label = pygame.font.Font(None, 50).render('Вийти', True, (255,0,0))

hit = pygame.mixer.Sound('hit.mp3')

update = True
game = True
while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
        if e.type == pygame.MOUSEBUTTONDOWN and ask_check == True:
            pos = pygame.mouse.get_pos()
            if 330 < pos[0] < 550 and 450 < pos[1] < 480:
                ask_check = False
                round += 1
                label1 = pygame.font.Font(None,50).render('Гравець1', True, (0,0,255))
                label2 = pygame.font.Font(None,50).render('Гравець2', True, (0,0,255))
                ball.rect.x = 425
                ball.rect.y = 325
                racket_L.rect.x = 20
                racket_L.rect.y = 250
                racket_R.rect.x = 800
                racket_R.rect.y = 250
                update = True
            if 325 < pos[0] < 550 and 550 < pos[1] < 580:
                ask_check = False
                round = 1
                score_l = 0
                score_r = 0
                label1 = pygame.font.Font(None,50).render('Гравець1', True, (0,0,255))
                label2 = pygame.font.Font(None,50).render('Гравець2', True, (0,0,255))
                ball.rect.x = 425
                ball.rect.y = 325
                racket_L.rect.x = 20
                racket_L.rect.y = 250
                racket_R.rect.x = 800
                racket_R.rect.y = 250
                update = True
            if 395 < pos[0] < 500 and 600 < pos[1] < 630:
                game = False
    pygame.display.update()
    clock.tick(FPS)

    window.blit(background, (0,0))
    racket_L.reset()
    racket_R.reset()
    ball.reset()

    score_l_label = pygame.font.Font(None,50).render(str(score_l), True, (0,0,255))
    score_r_label = pygame.font.Font(None,50).render(str(score_r), True, (0,0,255))
    round_label = pygame.font.Font(None, 50).render('Раунд '+str(round), True, (0,0,255))

    window.blit(label1, (60,60))
    window.blit(label2, (680,60))
    window.blit(score_l_label, (330,60))
    window.blit(score_r_label, (550,60))
    window.blit(round_label, (385,60))

    if ball.rect.x > 850:
        l_win()
    if ball.rect.x < 0:
        r_win()

    if ask_check == True:
        window.blit(ask_continue_label, (330,450))
        window.blit(ask_restart_label, (325, 550))
        window.blit(end_label, (395,600))

    if update:
        racket_L.update_L()
        racket_R.update_R()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if pygame.sprite.collide_rect(ball, racket_L) or pygame.sprite.collide_rect(ball, racket_R):
            speed_x *= -1
            hit.play()
        if ball.rect.y < 50:
            speed_y *= -1
            hit.play()
        if ball.rect.y > 600:
            speed_y *= -1
            hit.play()

        if ball.rect.x > 850:
            score_l += 1
            update = False
            ask_check = True
        if ball.rect.x < 0:
            score_r += 1
            update = False
            ask_check = True
