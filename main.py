import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import math
import numpy

class Game:
    def __init__(self):
        pygame.init()
        self.largura = 800
        self.altura = 600

        self.posicao = [-19, 1, -19]  # Posição inicial da câmera
        self.rotacao = [0, 0]  # Rotação inicial da câmera

        self.cont = 0
        self.flag = True
        self.tamanho_cena = 20

        # Variáveis para controle do mouse
        self.ultima_posicao_mouse = None
        self.mouse_na_janela = False
        self.is_running = True

        self.camera_width = 0.5
        self.camera_height = 0.5
        self.camera_depth = 0.5

        #Contador para setar mouse inicialmente inativo
        self.MouseCount = 0


        self.novos_retangulos = []
        self.retangulos =[]

        # Definindo as dimensões do retângulo a ser adicionado (seu tamanho fixo)
        self.largura_retangulo = 1
        self.altura_retangulo = 4
        self.profundidade_retangulo = 1

        self.paredes = \
            [
                # Paredes laterais
                ((-1*self.tamanho_cena, -1, -1*self.tamanho_cena), (-1*self.tamanho_cena, -1, 1*self.tamanho_cena)),
                ((1*self.tamanho_cena, -1, -1*self.tamanho_cena), (1*self.tamanho_cena, -1, 1*self.tamanho_cena)),
                # Paredes frontal e traseira
                ((-1*self.tamanho_cena, -1, -1*self.tamanho_cena), (1*self.tamanho_cena, -1, -1*self.tamanho_cena)),
                ((-1*self.tamanho_cena, -1, 1*self.tamanho_cena), (1*self.tamanho_cena, -1, 1*self.tamanho_cena)),

            ]

    def setup(self):
        pygame.display.set_mode((self.largura, self.largura), DOUBLEBUF | OPENGL)
        self.load_textures()
        self.desenhar_paredes()


    def desenhar_paredes(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textura_id_parede)

        # Definir a repetição de textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        for parede in self.paredes:
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

    def desenhar_plano(self, z, texture, repeat,size):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)

        # Definir a repetição de textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glBegin(GL_QUADS)
        glColor3f(1, 1, 1)

        # Coordenadas de textura normalizadas
        glTexCoord2f(0, 0)
        glVertex3f(-1*size, z, -1*size)
        glTexCoord2f(repeat, 0)  # Aumente o valor do primeiro argumento para repetir a textura mais vezes na direção X
        glVertex3f(1*size, z, -1*size)
        glTexCoord2f(repeat, repeat)  # Aumente o valor de ambos os argumentos para repetir a textura mais vezes em ambas as direções
        glVertex3f(1*size, z, 1*size)
        glTexCoord2f(0, repeat)  # Aumente o valor do segundo argumento para repetir a textura mais vezes na direção Y
        glVertex3f(-1*size, z, 1*size)

        glEnd()

    def desenhar_retangulo_3d(self,posicao, largura, altura, profundidade):
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
        glBindTexture(GL_TEXTURE_2D, self.textura_id_obj)

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


    def load_textures(self):
        # Carregue suas texturas aqui
        self.imagem_binaria = Image.open('dots.png').convert('L')
        pixels = self.imagem_binaria.load()
        self.textura_chao = pygame.image.load('ground.jpg')
        self.textura_parede = pygame.image.load('wall.png')
        self.textura_obj = pygame.image.load('stone_bricks.png')
        self.textura_teto = pygame.image.load('plank.jpg')
        glEnable(GL_TEXTURE_2D)
        self.textura_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textura_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.textura_chao.get_width(), self.textura_chao.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(self.textura_chao, 'RGBA'))

        glEnable(GL_TEXTURE_2D)
        self.textura_id_parede = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textura_id_parede)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.textura_parede.get_width(), self.textura_parede.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(self.textura_parede, 'RGBA'))

        self.textura_id_obj = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textura_id_obj)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.textura_obj.get_width(), self.textura_obj.get_height(), 0, GL_RGB,GL_UNSIGNED_BYTE, pygame.image.tostring(self.textura_obj, "RGB", 1))

        self.textura_id_teto = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textura_id_teto)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.textura_teto.get_width(), self.textura_teto.get_height(), 0, GL_RGB,GL_UNSIGNED_BYTE, pygame.image.tostring(self.textura_teto, "RGB", 1))

        for x in range(self.imagem_binaria.width):
            for z in range(self.imagem_binaria.height):
                # Se o pixel é preto (valor 0), adicionamos o retângulo na posição correspondente
                if pixels[x, z] == 0:
                    novo_retangulo = {
                        'posicao': [x-self.tamanho_cena, 1, z-self.tamanho_cena],
                        'largura': self.largura_retangulo,
                        'altura': self.altura_retangulo,
                        'profundidade': self.profundidade_retangulo
                    }
                    self.novos_retangulos.append(novo_retangulo)



        self.retangulos.extend(self.novos_retangulos)

    def capturar_movimento_mouse(self):
        posicao_mouse_atual = pygame.mouse.get_pos()

        if self.ultima_posicao_mouse is not None and self.mouse_na_janela:
            delta_mouse = (
                posicao_mouse_atual[0] - self.ultima_posicao_mouse[0],
                posicao_mouse_atual[1] - self.ultima_posicao_mouse[1]
            )

            sensibilidade_mouse = 0.1
            self.rotacao[0] -= delta_mouse[1] * sensibilidade_mouse
            self.rotacao[1] -= delta_mouse[0] * sensibilidade_mouse

            if self.rotacao[0] > 90:
                self.rotacao[0] = 90
            elif self.rotacao[0] < -90:
                self.rotacao[0] = -90
    
        self.ultima_posicao_mouse = posicao_mouse_atual

    def colisao(self,pos):
        if (pos[0] <= self.tamanho_cena - 0.2 and pos[2] <= self.tamanho_cena - 0.2 and pos[0] >= -self.tamanho_cena + 0.2 and pos[2] >= -self.tamanho_cena + 0.2):
            return True
        else:
            return False


    def colisao_obj(self,camera_position, camera_width, camera_height, camera_depth, rectangles):
        if not self.colisao(camera_position):
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

    def handle_events(self):
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
                    self.mouse_na_janela = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_na_janela = False

        self.capturar_movimento_mouse()

        # Captura das teclas pressionadas para movimentação do personagem
        teclas = pygame.key.get_pressed()
        velocidade = 0.05 #0.07
        proxima_posicao = self.posicao.copy()
        if self.colisao(proxima_posicao):
            if teclas[pygame.K_w]:
                proxima_posicao[0] += velocidade * math.sin(self.rotacao[1] * math.pi / 180.0)
                proxima_posicao[2] -= velocidade * math.cos(self.rotacao[1] * math.pi / 180.0)
                #Modifica a altura da câmera para simular o movimento de um personagem
                if proxima_posicao[1] < 1.5 and self.flag:
                    proxima_posicao[1] += 0.01

                else:
                    self.flag = False
                    if proxima_posicao[1] > 1:
                        proxima_posicao[1] -= 0.01
                    else:
                        self.flag = True

            if teclas[pygame.K_s]:
                proxima_posicao[0] -= velocidade * math.sin(self.rotacao[1] * math.pi / 180.0)
                proxima_posicao[2] += velocidade * math.cos(self.rotacao[1] * math.pi / 180.0)
                if proxima_posicao[1] < 1.5 and self.flag:
                    proxima_posicao[1] += 0.01

                else:
                    self.flag = False
                    if proxima_posicao[1] > 1:
                        proxima_posicao[1] -= 0.01
                    else:
                        self.flag = True


            if teclas[pygame.K_a]:
                proxima_posicao[0] -= velocidade * math.cos(self.rotacao[1] * math.pi / 180.0)
                proxima_posicao[2] -= velocidade * math.sin(self.rotacao[1] * math.pi / 180.0)
            if teclas[pygame.K_d]:
                proxima_posicao[0] += velocidade * math.cos(self.rotacao[1] * math.pi / 180.0)
                proxima_posicao[2] += velocidade * math.sin(self.rotacao[1] * math.pi / 180.0)

            #Caso a camera não se movimente nem para frente nem para trás, a altura é setada para a inical
            if(teclas[pygame.K_w] == False and teclas[pygame.K_s] == False):
                proxima_posicao[1] = 1


        # Captura das teclas pressionadas para rotacionar a câmera
        if teclas[pygame.K_LEFT]:
            self.rotacao[1] -= 1  # Girar para a esquerda
        if teclas[pygame.K_RIGHT]:
            self.rotacao[1] += 1  # Girar para a direita
        if teclas[pygame.K_UP]:
            self.rotacao[0] -= 1  # Olhar para cima
        if teclas[pygame.K_DOWN]:
            self.rotacao[0] += 1  # Olhar para baixo

        if self.colisao_obj(proxima_posicao, self.camera_width, self.camera_height,self.camera_depth, self.retangulos):
            print("Houve uma colisão!")
        else:
            self.posicao = proxima_posicao



    def update(self):
        glLoadIdentity()
        glRotatef(self.rotacao[0], 1, 0, 0)
        glRotatef(self.rotacao[1], 0, 1, 0)
        glTranslatef(-self.posicao[0], -self.posicao[1], -self.posicao[2])


    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.largura / self.altura), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        self.update()

        # Desenho do ambiente
        self.desenhar_paredes()
        self.desenhar_plano(-1, self.textura_id, 16, self.tamanho_cena) #Chao
        self.desenhar_plano(6,  self.textura_id, 16, self.tamanho_cena) #teto

        for retangulo in self.retangulos:
         self.desenhar_retangulo_3d(retangulo['posicao'], retangulo['largura'], retangulo['altura'], retangulo['profundidade'])

        # Desativa a textura após desenhar o chão
        glDisable(GL_TEXTURE_2D)
        pygame.display.flip()
        pygame.time.wait(1)

    def run(self,debug = False):
        self.setup()

        while self.is_running:
            self.handle_events()
            self.update()
            self.render()

            if debug:
                print(f'Posicao da camera: {self.posicao}\n,  raotação camera: {self.rotacao} , mouse: {self.ultima_posicao_mouse}' )
                           
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run(debug=True)