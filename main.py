import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import math
import numpy as np

class Game:
    def __init__(self):
        pygame.init()
        self.largura = 800
        self.altura = 600

        self.clock = pygame.time.Clock()
        self.fps = 120  # Defina a taxa de quadros por segundo desejada

        self.posicao = [-19, 1, -19]  # Posição inicial da câmera
        self.rotacao = [0, 90]  # Rotação inicial da câmera

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
        self.init_rect_vbo()


    def init_rect_vbo(self):
        # Create VBOs for rectangle vertices and indices
        self.rect_vertex_vbo = glGenBuffers(1)
        self.rect_index_vbo = glGenBuffers(1)

        # Create and bind the VAO (Vertex Array Object) for rectangles
        self.rect_vao = glGenVertexArrays(1)
        glBindVertexArray(self.rect_vao)

        # Bind the vertex VBO and buffer data
        glBindBuffer(GL_ARRAY_BUFFER, self.rect_vertex_vbo)
        glBufferData(GL_ARRAY_BUFFER, np.array(self.get_rect_vertices(), dtype=np.float32), GL_STATIC_DRAW)

        # Bind the index VBO and buffer data
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.rect_index_vbo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, np.array(self.get_rect_indices(), dtype=np.uint32), GL_STATIC_DRAW)

        # Define the vertex attributes
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        # Unbind VAO
        glBindVertexArray(0)

    def get_rect_vertices(self):
        vertices = [
            (-self.largura_retangulo/2, -self.altura_retangulo/2, -self.profundidade_retangulo/2),
            (-self.largura_retangulo/2, self.altura_retangulo/2, -self.profundidade_retangulo/2),
            (self.largura_retangulo/2, self.altura_retangulo/2, -self.profundidade_retangulo/2),
            (self.largura_retangulo/2, -self.altura_retangulo/2, -self.profundidade_retangulo/2),
            (-self.largura_retangulo/2, -self.altura_retangulo/2, self.profundidade_retangulo/2),
            (-self.largura_retangulo/2, self.altura_retangulo/2, self.profundidade_retangulo/2),
            (self.largura_retangulo/2, self.altura_retangulo/2, self.profundidade_retangulo/2),
            (self.largura_retangulo/2, -self.altura_retangulo/2, self.profundidade_retangulo/2)
        ]
        return vertices

    def get_rect_indices(self):
        indices = [
            0, 1, 2, 3,
            4, 5, 6, 7,
            0, 1, 5, 4,
            2, 3, 7, 6,
            0, 3, 7, 4,
            1, 2, 6, 5
        ]
        return indices


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

    def desenhar_retangulo_3d(self,posicao, largura, altura, profundidade, cor):
        vertices = np.array([
            # Frente
            [posicao[0] - largura / 2, posicao[1] - altura / 2, posicao[2] + profundidade / 2],
            [posicao[0] + largura / 2, posicao[1] - altura / 2, posicao[2] + profundidade / 2],
            [posicao[0] + largura / 2, posicao[1] + altura / 2, posicao[2] + profundidade / 2],
            [posicao[0] - largura / 2, posicao[1] + altura / 2, posicao[2] + profundidade / 2],

            # Trás
            [posicao[0] - largura / 2, posicao[1] - altura / 2, posicao[2] - profundidade / 2],
            [posicao[0] + largura / 2, posicao[1] - altura / 2, posicao[2] - profundidade / 2],
            [posicao[0] + largura / 2, posicao[1] + altura / 2, posicao[2] - profundidade / 2],
            [posicao[0] - largura / 2, posicao[1] + altura / 2, posicao[2] - profundidade / 2],
        ], dtype=np.float32)

        indices = np.array([
            # Frente
            0, 1, 2,
            2, 3, 0,

            # Topo
            3, 2, 6,
            6, 7, 3,

            # Trás
            7, 6, 5,
            5, 4, 7,

            # Base
            4, 0, 3,
            3, 7, 4,

            # Lado direito
            1, 5, 6,
            6, 2, 1,

            # Lado esquerdo
            4, 5, 1,
            1, 0, 4,
        ], dtype=np.uint32)

        # Criação do VBO para os vértices
        vbo_vertices = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Criação do VBO para os índices
        vbo_indices = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbo_indices)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        # Desenhar o retângulo usando VBOs
        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
        glVertexPointer(3, GL_FLOAT, 0, None)

        if(cor == "preto"):
            glColor3f(0.392, 0.392, 0.392)
        if(cor == "verde"):
            glColor3f(0.0, 1.0, 0.0)
        if(cor == "vermelho"):
            glColor3f(1.0, 0.0, 0.0)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbo_indices)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glDisableClientState(GL_VERTEX_ARRAY)

        # Liberação dos VBOs
        glDeleteBuffers(1, [vbo_vertices, vbo_indices])


    def carregar_textura(self,textura, filtro_min, filtro_mag):
        glEnable(GL_TEXTURE_2D)
        textura_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textura_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, filtro_min)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filtro_mag)

        if textura.get_alpha():
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textura.get_width(), textura.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(textura, 'RGBA'))
        else:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, textura.get_width(), textura.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, pygame.image.tostring(textura, 'RGB'))

        return textura_id

    def load_textures(self):
        # Carregue suas texturas aqui
        self.imagem_binaria = Image.open('maze_color.png').convert('RGB')
        pixels = self.imagem_binaria.load()
        self.textura_chao = pygame.image.load('ground.png')
        self.textura_parede = pygame.image.load('bricks_3.png')
        self.textura_obj = pygame.image.load('wall.png')
        self.textura_teto = pygame.image.load('starry-night-sky.jpg')
        glEnable(GL_TEXTURE_2D)
        self.textura_id = self.carregar_textura(self.textura_chao, GL_LINEAR, GL_LINEAR)
        self.textura_id_parede = self.carregar_textura(self.textura_parede, GL_LINEAR, GL_LINEAR)
        self.textura_id_obj = self.carregar_textura(self.textura_obj, GL_NEAREST, GL_NEAREST)
        self.textura_id_teto = self.carregar_textura(self.textura_teto, GL_NEAREST, GL_NEAREST)

        for x in range(self.imagem_binaria.width):
            for z in range(self.imagem_binaria.height):
                r, g, b = pixels[x, z]
                # Se o pixel é preto (valor 0), adicionamos o retângulo na posição correspondente
                if r == 0 and g == 0 and b == 0:
                    novo_retangulo = {
                        'posicao': [x-self.tamanho_cena, 1, z-self.tamanho_cena],
                        'largura': self.largura_retangulo,
                        'altura': self.altura_retangulo,
                        'profundidade': self.profundidade_retangulo,
                        'cor': "preto"
                    }
                    self.novos_retangulos.append(novo_retangulo)

                if g > 100 and r < 50 and b < 50: #Quando o pixel for verde, definir objeto de cor verde
                    novo_retangulo = {
                        'posicao': [x-self.tamanho_cena, 1, z-self.tamanho_cena],
                        'largura': self.largura_retangulo,
                        'altura': self.altura_retangulo - 2,
                        'profundidade': self.profundidade_retangulo,
                        'cor': "verde"
                    }

                    self.novos_retangulos.append(novo_retangulo)

                if r > 100 and g < 50 and b < 50 : #Quando o pixel for vermelho, definir posição inicial da câmera
                    self.posicao = [x-self.tamanho_cena, 1, z-self.tamanho_cena]
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
        velocidade = 0.2 #0.07
        proxima_posicao = self.posicao.copy()
        if self.colisao(proxima_posicao):
            if teclas[pygame.K_w]:
                proxima_posicao[0] += velocidade * math.sin(self.rotacao[1] * math.pi / 180.0)
                proxima_posicao[2] -= velocidade * math.cos(self.rotacao[1] * math.pi / 180.0)
                #Modifica a altura da câmera para simular o movimento de um personagem
                if proxima_posicao[1] < 1.3 and self.flag:
                    proxima_posicao[1] += 0.03

                else:
                    self.flag = False
                    if proxima_posicao[1] > 1:
                        proxima_posicao[1] -= 0.03
                    else:
                        self.flag = True

            if teclas[pygame.K_s]:
                proxima_posicao[0] -= velocidade * math.sin(self.rotacao[1] * math.pi / 180.0)
                proxima_posicao[2] += velocidade * math.cos(self.rotacao[1] * math.pi / 180.0)
                if proxima_posicao[1] < 1.3 and self.flag:
                    proxima_posicao[1] += 0.03

                else:
                    self.flag = False
                    if proxima_posicao[1] > 1:
                        proxima_posicao[1] -= 0.03
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
            self.rotacao[1] -= 3  # Girar para a esquerda
        if teclas[pygame.K_RIGHT]:
            self.rotacao[1] += 3  # Girar para a direita
        if teclas[pygame.K_UP]:
            self.rotacao[0] -= 3  # Olhar para cima
        if teclas[pygame.K_DOWN]:
            self.rotacao[0] += 3  # Olhar para baixo

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
        gluPerspective(45, (self.largura / self.altura), 0.1, 150.0)
        glMatrixMode(GL_MODELVIEW)
        self.update()

        glEnable(GL_CULL_FACE)
        for retangulo in self.retangulos:
            self.desenhar_retangulo_3d(retangulo['posicao'], retangulo['largura'], retangulo['altura'], retangulo['profundidade'],retangulo['cor'])

        glDisable(GL_CULL_FACE)
        # Desenho do ambiente
        self.desenhar_paredes()
        self.desenhar_plano(-1, self.textura_id, 16, self.tamanho_cena) #Chao
        glEnable(GL_DEPTH_TEST)
        self.desenhar_plano(15,  self.textura_id_teto, 16, self.tamanho_cena*10) #teto




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

        # if debug:
        #print(f'Posicao da camera: {self.posicao}\n,  raotação camera: {self.rotacao} , mouse: {self.ultima_posicao_mouse}' )

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run(debug=True)
