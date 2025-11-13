###
### UFMT - Programacao de Computadores
### Prof Ivairton
###
### TRABALHO
### Aluno: Edilayne Ramos Sousa Silva
### Aluno: Andrielly Araujo Oliveira
###
# Biblioteca PyGame
import pygame
# Biblioteca para geracao de numeros pseudoaleatorios
import random
# Modulo da biblioteca PyGame que permite o acesso as teclas utilizadas
from pygame.locals import *
import pygame.mixer
import pygame.sprite
import sys

# Classe que representar o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25)) #Define o retangulo que representa o player
        mut = pygame.image.load('mutano_d.png')
        scaled_mut = pygame.transform.scale(mut, (mut.get_width() / 4, mut.get_height() / 6))
        self.surf = mut
        self.rect = self.surf.get_rect()

    # Determina acao de movimento conforme teclas pressionadas
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)

        # Mantem o jogador nos limites da tela do jogo
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 500:
            self.rect.bottom = 500

# Classe que representa os inimigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self, dificult):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10)) #Definicao do retangulo
        inig = pygame.image.load('inimigoa_.png')
        scaled_inig = pygame.transform.scale(inig, (inig.get_width() / 3, inig.get_height() / 5))
        self.surf = inig
        self.rect = self.surf.get_rect( #Coloca na extrema direita (entre 820 e 900) e sorteia sua posicao em relacao a coordenada y (entre 0 e 600)
            center=(random.randint(820, 900), random.randint(0, 600))
        )
        self.clock = pygame.time.Clock()
        self.clock.tick(60)
        self.speed = random.uniform(1, 5) * dificult #Sorteia sua velocidade, entre 1 e 5

    # Funcao que atualiza a posiçao do inimigo em funcao da sua velocidade e termina com ele quando ele atinge o limite esquerdo da tela (x < 0)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
    
def menu_inicial():
    # Carregue a imagem de fundo do menu
    menu_background = pygame.image.load("inicioo.png")
    menu_background = pygame.transform.scale(menu_background, (800, 500))
    screen.blit(menu_background, (0, 0))

    pygame.display.flip()  # Atualize a tela
    
def game_over():
     # Carregue a imagem de fundo do menu
    overback = pygame.image.load("gameoverr.png")
    overback= pygame.transform.scale(overback, (800, 500)) 
    pontuacao = 0
    total_pontos_text = font.render(f"Pontuação Total: {pontos}", True, (25, 165, 0), (0, 0, 0)) #Define a cor no texto
    textRect = total_pontos_text.get_rect()
    textRect.center = (200, 300)
    screen.blit(overback, (0, 0))
    screen.blit(total_pontos_text, textRect)
    pygame.display.flip()


# Inicializa pygame
pygame.init()

dificult = 1
# Cria a tela com resolução 800x500px
screen = pygame.display.set_mode((800, 500))

# Define a musica do jogo
pygame.mixer.init()
pygame.mixer.music.set_volume (0.5)
pygame.mixer.music.load('rapjovenstitas.mp3')
pygame.mixer.music.play(-1)

# Cria um evento para adicao de inimigos
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500) #Define um intervalo para a criacao de cada inimigo (milisegundos)
ADDTIME = pygame.USEREVENT + 2
pygame.time.set_timer(ADDTIME, 1000)

player = Player()

# Define o plano de fundo, com a cor preta (RGB)
background = pygame.Surface(screen.get_size())
bg = pygame.image.load('gothan.png')
background = bg

#variavel para controlar a pontuação do jogo
pontos = 0
font = pygame.font.Font("Octopus Game.ttf", 20)  # Escolha a fonte e o tamanho desejados
total_pontos_text = font.render("Pontuação:" + str(pontos), True, (25, 165, 0))  # Renderiza o texto da pontuação
textRect = total_pontos_text.get_rect()
screen.blit(total_pontos_text, textRect)
enemies = pygame.sprite.Group() #Cria o grupo de inimigos
all_sprites = pygame.sprite.Group() #Cria o grupo de todos os Sprites
all_sprites.add(player) #Adicionar o player no grupo de todos os Sprites

running = True #Flag para controle do jogo
menu_ativo=True #Flag para controle do jogo

# Loop do menu inicial
while menu_ativo:
    menu_inicial()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            menu_ativo = False
            running = True
            

game_over_ativo = False #Definindo a flag para controle do game over
game_over_running = False

last_score_update_time = pygame.time.get_ticks()
score_update_interval = 1000  # Atualizar a pontuação a cada 1000 milissegundos (1 segundo)

while running:
    #Laco para verificacao do evento que ocorreu
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: #Verifica se a tecla ESC foi pressionada
                running = False
        elif event.type == QUIT: #Verifica se a janela foi fechada
            running = False
        elif(event.type == ADDENEMY): #Verifica se e o evento de criar um inimigo
            new_enemy = Enemy(dificult) #Cria um novo inimigo
            enemies.add(new_enemy) #Adiciona o inimigo no grupo de inimigos
            all_sprites.add(new_enemy) #Adiciona o inimigo no grupo de todos os Sprites
        elif (event.type == ADDTIME):
            pontos += 1
            dificult += 0.1
    font = pygame.font.Font("Octopus Game.ttf", 20)  # Escolha a fonte e o tamanho desejados
    total_pontos_text = font.render("Pontuação:" + str(pontos), True, (25, 165, 0))  # Renderiza o texto da pontuação
    textRect = total_pontos_text.get_rect()
    screen.blit(total_pontos_text, textRect)
    screen.blit(background, (0, 0)) #Atualiza a exibicao do plano de fundo do jogo (neste caso nao surte efeito)
    pressed_keys = pygame.key.get_pressed() #Captura as as teclas pressionadas
    screen.blit(total_pontos_text, (550, 10))  # Define a posição do texto na tela
    player.update(pressed_keys) #Atualiza a posicao do player conforme teclas usadas
    enemies.update() #Atualiza posicao dos inimigos
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect) #Atualiza a exibicao de todos os Sprites

    if pygame.sprite.spritecollideany(player, enemies): #Verifica se ocorreu a colisao do player com um dos inimigos
        collided_enemies = pygame.sprite.spritecollide(player, enemies, True)
        player.kill() #Se ocorrer a colisao, encerra o player
        game_over_ativo = True
        game_over_running = True

    #Loop para controlar a tela de game over
    while game_over_running:
        game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()# Finalize o loop de Game Over se o jogador fechar a janela
            if event.type == pygame.KEYDOWN:
                if event.key == K_r:  # Tecla "R" para reiniciar o jogo
                    game_over_ativo = False  # Defina a flag de Game Over como False para reiniciar o jogo
                    game_over_running = False  # Finalize o loop de Game Over
                    running = True
                if event.key == K_q:  # Tecla "Q" para sair do jogo
                    game_over_running = False
                    # Finalize o loop de Game Over
    pygame.display.flip() #Atualiza a projecao do jogo