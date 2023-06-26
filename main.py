import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy

# Inicialização do Pygame
pygame.init()

#fps
#clock = pygame.time.Clock()

# Definição das dimensões da janela
largura = 800
altura = 600

textura_chao = pygame.image.load('plank.jpg')

textura_parede = pygame.image.load('brickwall.jpg')

textura_obj = pygame.image.load('stone_bricks.png')

textura_teto = pygame.image.load('plank.jpg')

# Configuração do display do Pygame com OpenGL
pygame.display.set_mode((largura, altura), DOUBLEBUF | OPENGL)

# Definição das propriedades da câmera
posicao = [0, 1, 0]  # Posição inicial da câmera
rotacao = [0, 0]  # Rotação inicial da câmera

cont = 0
flag = True

# Variáveis para controle do mouse
ultima_posicao_mouse = None
mouse_na_janela = False

# Lista de coordenadas das paredes
paredes = [
    # Paredes laterais
    ((-20, -1, -20), (-20, -1, 20)),
    ((20, -1, -20), (20, -1, 20)),
    # Paredes frontal e traseira
    ((-20, -1, -20), (20, -1, -20)),
    ((-20, -1, 20), (20, -1, 20)),
]

#Dimensões da câmera para fins de colisão
camera_width = 0.5
camera_height = 0.5
camera_depth = 0.5

#Contador para setar mouse inicialmente inativo
MouseCount = 0;

retangulos = [
    {
        'posicao': [-16, 1, -14],
        'largura': 4,
        'altura': 4,
        'profundidade': 4
    },
    {
        'posicao': [-12, 1, -14],
        'largura': 4,
        'altura': 4,
        'profundidade': 4
    },
    {
        'posicao': [-8, 1, -14],
        'largura': 4,
        'altura': 4,
        'profundidade': 4
    },
    {
        'posicao': [-4, 1, -14],
        'largura': 4,
        'altura': 4,
        'profundidade': 4
    },
    {
        'posicao': [0, 1, -14],
        'largura': 4,
        'altura': 4,
        'profundidade': 4
    },
    {
        'posicao': [4, 1, -14],
        'largura': 4,
        'altura': 4,
        'profundidade': 4
    },
    {
        'posicao': [8, 1, -14],
        'largura': 4,
        'altura': 4,
        'profundidade': 4
    },
    {
        'posicao': [12, 1, -14],
        'largura': 4,
        'altura': 4,
        'profundidade': 4
    },
    {
        'posicao': [0, 0, -2],
        'largura': 4,
        'altura': 2,
        'profundidade': 1
    },
    {
        'posicao': [0, 0, -8],
        'largura': 2,
        'altura': 2,
        'profundidade': 1
    }
    # Adicione mais retângulos conforme necessário
]


def desenhar_retangulo_3d(posicao, largura, altura, profundidade):
    vertices = [
        (posicao[0] - largura/2, posicao[1] - altura/2, posicao[2] - profundidade/2),
        (posicao[0] - largura/2, posicao[1] + altura/2, posicao[2] - profundidade/2),
        (posicao[0] + largura/2, posicao[1] + altura/2, posicao[2] - profundidade/2),
        (posicao[0] + largura/2, posicao[1] - altura/2, posicao[2] - profundidade/2),
        (posicao[0] - largura/2, posicao[1] - altura/2, posicao[2] + profundidade/2),
        (posicao[0] - largura/2, posicao[1] + altura/2, posicao[2] + profundidade/2),
        (posicao[0] + largura/2, posicao[1] + altura/2, posicao[2] + profundidade/2),
        (posicao[0] + largura/2, posicao[1] - altura/2, posicao[2] + profundidade/2)
    ]

    faces = [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (2, 3, 7, 6),
        (0, 3, 7, 4),
        (1, 2, 6, 5)
    ]

    # Habilitar a aplicação de texturas
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

    # Desabilitar o descarte de faces
    glDisable(GL_CULL_FACE)
    glBindTexture(GL_TEXTURE_2D, textura_id_obj)

    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)
    for i, face in enumerate(faces):
        glTexCoord2f(0, 0)
        glVertex3fv(vertices[face[0]])
        glTexCoord2f(1, 0)
        glVertex3fv(vertices[face[1]])
        glTexCoord2f(1, 1)
        glVertex3fv(vertices[face[2]])
        glTexCoord2f(0, 1)
        glVertex3fv(vertices[face[3]])
    glEnd()

    # Desabilitar a aplicação de texturas

    # Habilitar o descarte de faces novamente, se necessário
    #aglEnable(GL_CULL_FACE)

    # Desabilitar o teste de profundidade
    #glDisable(GL_DEPTH_TEST)

    glDisable(GL_TEXTURE_2D)


# Função para desenhar as paredes
def desenhar_paredes():
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_id_parede)

    # Definir a repetição de textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    for parede in paredes:
        glBegin(GL_QUADS)
        glColor3f(1.0, 1.0, 1.0)  # Cor branca (se colocar outra cor, aplica um filtro a imagem original)
        glTexCoord2f(0, 8)
        glVertex3fv(parede[0])
        glTexCoord2f(1, 8)
        glVertex3f(parede[0][0], parede[0][1] + 7, parede[0][2])
        glTexCoord2f(1, 1)
        glVertex3f(parede[1][0], parede[1][1] + 7, parede[1][2])
        glTexCoord2f(0, 1)
        glVertex3fv(parede[1])
        glEnd()



def desenhar_linhas_parede():
    # Desenhar linhas verticais nos cantos do quarto
    glLineWidth(2)  # Define a largura das linhas
    glColor3f(0, 0, 0)  # Define a cor das linhas para preto

    # Canto superior esquerdo
    glBegin(GL_LINES)
    glVertex3f(-20, -1, -20)
    glVertex3f(-20, 5, -20)
    glEnd()

    # Canto superior direito
    glBegin(GL_LINES)
    glVertex3f(20, -1, -20)
    glVertex3f(20, 5, -20)
    glEnd()

    # Canto inferior esquerdo
    glBegin(GL_LINES)
    glVertex3f(-20, -1, 20)
    glVertex3f(-20, 5, 20)
    glEnd()

    # Canto inferior direito
    glBegin(GL_LINES)
    glVertex3f(20, -1, 20)
    glVertex3f(20, 5, 20)
    glEnd()


def desenhar_plano(z, texture, repeat):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    # Definir a repetição de textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)

    # Coordenadas de textura normalizadas
    glTexCoord2f(0, 0)
    glVertex3f(-20, z, -20)
    glTexCoord2f(repeat, 0)  # Aumente o valor do primeiro argumento para repetir a textura mais vezes na direção X
    glVertex3f(20, z, -20)
    glTexCoord2f(repeat, repeat)  # Aumente o valor de ambos os argumentos para repetir a textura mais vezes em ambas as direções
    glVertex3f(20, z, 20)
    glTexCoord2f(0, repeat)  # Aumente o valor do segundo argumento para repetir a textura mais vezes na direção Y
    glVertex3f(-20, z, 20)

    glEnd()




# # Função para desenhar o chão quadriculado
# def desenhar_plano():
#     for i in range(-20, 20):
#         for j in range(-20, 20):
#             if (i + j) % 2 == 0:
#                 cor = (1, 1, 1)  # Quadrados brancos
#             else:
#                 cor = (0, 0, 0)  # Quadrados pretos
#
#             glBegin(GL_QUADS)
#             glColor3fv(cor)
#             glVertex3fv((i, -1, j))
#             glVertex3fv((i + 1, -1, j))
#             glVertex3fv((i + 1, -1, j + 1))
#             glVertex3fv((i, -1, j + 1))
#             glEnd()

# Função para atualizar a visão da câmera
def atualizar_camera():
    glLoadIdentity()
    glRotatef(rotacao[0], 1, 0, 0)
    glRotatef(rotacao[1], 0, 1, 0)
    glTranslatef(-posicao[0], -posicao[1], -posicao[2])

# Captura do movimento do mouse
def capturar_movimento_mouse():
    global rotacao, ultima_posicao_mouse

    posicao_mouse_atual = pygame.mouse.get_pos()

    if ultima_posicao_mouse is not None:
        if mouse_na_janela:
            delta_mouse = (
                posicao_mouse_atual[0] - ultima_posicao_mouse[0],
                posicao_mouse_atual[1] - ultima_posicao_mouse[1]
            )

            sensibilidade_mouse = 0.1
            rotacao[0] -= delta_mouse[1] * sensibilidade_mouse
            rotacao[1] -= delta_mouse[0] * sensibilidade_mouse

            if rotacao[0] > 90:
                rotacao[0] = 90
            elif rotacao[0] < -90:
                rotacao[0] = -90

    ultima_posicao_mouse = posicao_mouse_atual

# Posiciona o cursor do mouse no centro da tela
#pygame.mouse.set_pos(largura // 2, altura // 2)

#Função para detectar colisão

def colisao(pos):
    if (pos[0] <= 19.8 and pos[2] <= 19.8 and pos[0] >= -19.8 and pos[2] >= -19.8):
        return True
    else:
        return False


def colisao_obj(camera_position, camera_width, camera_height, camera_depth, rectangles):
    if not colisao(camera_position):
        return True

    camera_x, camera_y, camera_z = camera_position
    camera_left = camera_x - camera_width/2
    camera_right = camera_x + camera_width/2
    camera_top = camera_y - camera_height/2
    camera_bottom = camera_y + camera_height/2
    camera_front = camera_z - camera_depth/2
    camera_back = camera_z + camera_depth/2

    for rectangle in rectangles:
        rect_x, rect_y, rect_z = rectangle['posicao']
        rect_width = rectangle['largura']
        rect_height = rectangle['altura']
        rect_depth = rectangle['profundidade']

        rect_left = rect_x - rect_width/2
        rect_right = rect_x + rect_width/2
        rect_top = rect_y - rect_height/2
        rect_bottom = rect_y + rect_height/2
        rect_front = rect_z - rect_depth/2
        rect_back = rect_z + rect_depth/2

        if (rect_left < camera_right and
                rect_right > camera_left and
                rect_top < camera_bottom and
                rect_bottom > camera_top and
                rect_front < camera_back and
                rect_back > camera_front):
            return True

    return False

# Configuração da textura do chão
glEnable(GL_TEXTURE_2D)
textura_id = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, textura_id)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, textura_chao.get_width(), textura_chao.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(textura_chao, 'RGBA'))

glEnable(GL_TEXTURE_2D)
textura_id_parede = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, textura_id_parede)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, textura_parede.get_width(), textura_parede.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(textura_parede, 'RGBA'))

textura_id_obj = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, textura_id_obj)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, textura_obj.get_width(), textura_obj.get_height(), 0, GL_RGB,GL_UNSIGNED_BYTE, pygame.image.tostring(textura_obj, "RGB", 1))

textura_id_teto = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, textura_id_teto)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, textura_teto.get_width(), textura_teto.get_height(), 0, GL_RGB,GL_UNSIGNED_BYTE, pygame.image.tostring(textura_teto, "RGB", 1))



# Loop principal do jogo
while True:

    #pygame.mouse.set_pos(largura // 2, altura // 2)

    # Calcula o FPS
    #fps = clock.get_fps()

    # Atualiza o título da janela com o FPS
    #pygame.display.set_caption(f"The Room - FPS: {int(fps)}")

    # Atualização do display
    #pygame.display.flip()

    # Limita a taxa de quadros (FPS) para 60
    # clock.tick(60)


    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         pygame.quit()
    #         quit()
    #     elif event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_ESCAPE:
    #             pygame.quit()
    #             quit()
    #     elif event.type == pygame.MOUSEBUTTONDOWN:
    #         MouseCount = MouseCount + 1;
    #         print(MouseCount)
    #         if MouseCount%2!=0:
    #             mouse_na_janela = True
    #         else:
    #             mouse_na_janela = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_na_janela = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_na_janela = False

    # Captura do movimento do mouse
    capturar_movimento_mouse()

    # Captura das teclas pressionadas para movimentação do personagem
    teclas = pygame.key.get_pressed()
    velocidade = 0.05 #0.07
    proxima_posicao = posicao.copy()
    if colisao(proxima_posicao):
        if teclas[pygame.K_w]:
            proxima_posicao[0] += velocidade * math.sin(rotacao[1] * math.pi / 180.0)
            proxima_posicao[2] -= velocidade * math.cos(rotacao[1] * math.pi / 180.0)
            #Modifica a altura da câmera para simular o movimento de um personagem
            if proxima_posicao[1] < 1.5 and flag:
                proxima_posicao[1] += 0.01

            else:
                flag = False
                if proxima_posicao[1] > 1:
                    proxima_posicao[1] -= 0.01
                else:
                    flag = True

        if teclas[pygame.K_s]:
            proxima_posicao[0] -= velocidade * math.sin(rotacao[1] * math.pi / 180.0)
            proxima_posicao[2] += velocidade * math.cos(rotacao[1] * math.pi / 180.0)
            if proxima_posicao[1] < 1.5 and flag:
                proxima_posicao[1] += 0.01

            else:
                flag = False
                if proxima_posicao[1] > 1:
                    proxima_posicao[1] -= 0.01
                else:
                    flag = True


        if teclas[pygame.K_a]:
            proxima_posicao[0] -= velocidade * math.cos(rotacao[1] * math.pi / 180.0)
            proxima_posicao[2] -= velocidade * math.sin(rotacao[1] * math.pi / 180.0)
        if teclas[pygame.K_d]:
            proxima_posicao[0] += velocidade * math.cos(rotacao[1] * math.pi / 180.0)
            proxima_posicao[2] += velocidade * math.sin(rotacao[1] * math.pi / 180.0)

        #Caso a camera não se movimente nem para frente nem para trás, a altura é setada para a inical
        if(teclas[pygame.K_w] == False and teclas[pygame.K_s] == False):
            proxima_posicao[1] = 1


    # Captura das teclas pressionadas para rotacionar a câmera
    if teclas[pygame.K_LEFT]:
        rotacao[1] -= 1  # Girar para a esquerda
    if teclas[pygame.K_RIGHT]:
        rotacao[1] += 1  # Girar para a direita
    if teclas[pygame.K_UP]:
        rotacao[0] -= 1  # Olhar para cima
    if teclas[pygame.K_DOWN]:
        rotacao[0] += 1  # Olhar para baixo

    # Atualização da posição da câmera

    #print(teclas[pygame.K_s])

    if colisao_obj(proxima_posicao, camera_width, camera_height, camera_depth, retangulos):
        print("Houve uma colisão!")
    else:
        posicao = proxima_posicao

    # Configuração do OpenGL
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (largura / altura), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    atualizar_camera()

    # Desenho do ambiente
    desenhar_paredes()
    desenhar_plano(-1,textura_id,16) #Chao
    desenhar_plano(6,textura_id,16) #teto
    desenhar_linhas_parede()

    # Desativa a textura após desenhar o chão
    glDisable(GL_TEXTURE_2D)
    # Dentro do loop principal do jogow



    # ...

    # Desenhar um retângulo 3D em uma posição específica
    # posicao_retangulo = [0, 0, -5]  # Exemplo de posição
    # largura_retangulo = 4
    # altura_retangulo = 2
    # profundidade_retangulo = 1
    # desenhar_retangulo_3d(posicao_retangulo, largura_retangulo, altura_retangulo, profundidade_retangulo)

    for retangulo in retangulos:
        desenhar_retangulo_3d(retangulo['posicao'], retangulo['largura'], retangulo['altura'], retangulo['profundidade'])


    # Atualização do display
    pygame.display.flip()
    pygame.time.wait(1)
