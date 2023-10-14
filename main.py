import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("pika4all")

# Cores
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
BRANCO = (255, 255, 255)

# Carrega as imagens
inimigo = pygame.image.load("gosma.png")
inimigo = pygame.transform.scale(inimigo, (50, 50))
inimigo_rect = inimigo.get_rect()
inimigo_rect.center = (largura // 4, altura // 2)

personagem = pygame.image.load("pika.png")
personagem = pygame.transform.scale(personagem, (50, 50))
personagem_original = personagem
personagem_rect = personagem.get_rect()
personagem_rect.center = (largura // 2, altura // 2)

# Variáveis de movimento
velocidade = 3
pulando = False
pulo_duplo_disponivel = False
gravidade = 1
gravidade_pulo_duplo = 0.5
velocidade_x = 0
velocidade_y = 0
atraso_pulo_duplo = 0

# Variáveis do inimigo
velocidade_y_inimigo = 0
gravidade_inimigo = 1
pulando_inimigo = False
tempo_pulo_inimigo = 0

# Crie um retângulo para a plataforma (chão)
plataforma = pygame.Surface((largura, 20))
plataforma.fill(VERDE)
plataforma_rect = plataforma.get_rect()
plataforma_rect.topleft = (0, altura - 20)

# Crie um retângulo para a plataforma flutuante
plataforma_flutuante = pygame.Rect(300, 400, 200, 20)

# Lista de raios de Lichtenberg
raios = []
raios_ativos = False
raio_timer = 0

# Sons
som_passos = pygame.mixer.Sound("caminhar.mp3")
som_ataque1 = pygame.mixer.Sound("ataque1.mp3")
som_ataque2 = pygame.mixer.Sound("ataque2.mp3")
som_colisao_chao = pygame.mixer.Sound("pulo.mp3")
pygame.mixer.music.set_volume(0.07)
pygame.mixer.music.load("musica.mp3")
pygame.mixer.music.play(-1)

# Variável para controlar a reprodução do som de colisão no chão
colidiu_no_chao = False

# Função para criar raio de Lichtenberg
def criar_raio():
    raio_x = personagem_rect.centerx
    raio_y = personagem_rect.centery
    for _ in range(20):
        raio_x += random.randint(-20, 20)
        raio_y += random.randint(-20, 20)
        raios.append((raio_x, raio_y, 20))

# Loop principal
jogo_ativo = True
while jogo_ativo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_ativo = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_z:
                if not pulando or (pulando and atraso_pulo_duplo > 0):
                    criar_raio()
                    raios_ativos = True
                    raio_timer = 20
                    if pulando:
                        pulo_duplo_disponivel = False
                    som_ataque1.play()
            if evento.key == pygame.K_x:
                som_ataque2.play()

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        personagem = pygame.transform.flip(personagem_original, True, False)
        personagem_rect.x -= velocidade
        som_passos.play()
    elif teclas[pygame.K_RIGHT]:
        personagem = personagem_original
        personagem_rect.x += velocidade
        som_passos.play()

    # Aplicar gravidade
    if pulando and pulo_duplo_disponivel:
        velocidade_y += gravidade_pulo_duplo
    else:
        velocidade_y += gravidade

    personagem_rect.y += velocidade_y

    # Verifica colisão com a plataforma
    if personagem_rect.colliderect(plataforma_rect):
        pulando = False
        velocidade_y = 0
        personagem_rect.y = plataforma_rect.top - personagem_rect.height
        atraso_pulo_duplo = 10
        if not colidiu_no_chao:
            som_colisao_chao.play()
            colidiu_no_chao = True

    # Adicione o código para fazer o inimigo "gosma.png" pular aqui:
    if not pulando_inimigo:
        inimigo_velocidade_y = -10  # Faça o inimigo pular
        pulando_inimigo = True

    if pulando_inimigo:
        inimigo_rect.y += inimigo_velocidade_y
        inimigo_velocidade_y += gravidade

        if inimigo_rect.colliderect(plataforma_rect):
            inimigo_velocidade_y = 0
            inimigo_rect.y = plataforma_rect.top - inimigo_rect.height
            pulando_inimigo = False

    if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and not pulando:
        velocidade_y = -15
        pulo_duplo_disponivel = True
        pulando = True
        atraso_pulo_duplo = 0

    if atraso_pulo_duplo > 0:
        atraso_pulo_duplo -= 1

    tela.fill(AZUL)
    tela.blit(plataforma, plataforma_rect)
    pygame.draw.rect(tela, VERDE, plataforma_flutuante)
    tela.blit(personagem, personagem_rect)
    tela.blit(inimigo, inimigo_rect)

    # Desenha os raios de Lichtenberg
    if raios_ativos and raio_timer > 0:
        for i, (raio_x, raio_y, raio_duracao) in enumerate(raios):
            pygame.draw.line(tela, BRANCO, (personagem_rect.centerx, personagem_rect.centery), (raio_x, raio_y), 2)
            raio_duracao -= 1
            raios[i] = (raio_x, raio_y, raio_duracao)
            if raio_duracao <= 0:
                raios.pop(i)
        raio_timer -= 1
    else:
        raios_ativos = False

    pygame.display.update()

# Encerra o jogo
pygame.quit()
sys.exit()
