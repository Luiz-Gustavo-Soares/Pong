import pygame
from pygame.locals import *
from controller.objetos import *


class Game:
    def __init__(self, config): 
        pygame.init()
        pygame.display.set_caption('Pong')
        self.config = config

        self.clock = pygame.time.Clock()
        self.tela = pygame.display.set_mode((self.config.LARGURA, self.config.ALTURA))

        self.player1 = Player(posicao=[8, self.config.ALTURA/2], tamanho_tela=(self.config.LARGURA, self.config.ALTURA))
        self.player2 = Player(posicao=[self.config.LARGURA-24, self.config.ALTURA/2], tamanho_tela=(self.config.LARGURA, self.config.ALTURA))
        self.bola = Bola([self.config.LARGURA/2, self.config.ALTURA/2], tamanho_tela=(self.config.LARGURA, self.config.ALTURA), velocidade=self.config.VELOCIDADE_BOLA)

    def controle_players(self):
        keys = pygame.key.get_pressed()

        if keys [K_UP]:
            self.player2.move_top()
        
        elif keys [K_DOWN]:
            self.player2.move_down()
        
        if keys [K_w]:
            self.player1.move_top()
        
        elif keys [K_s]:
            self.player1.move_down()

    def iniciar_game(self):
        while True:
            self.clock.tick(60)
            self.tela.fill((0,0,0))
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()  

            self.controle_players()

            self.bola.calcular_posicao((self.player1.get_local(), self.player2.get_local()))
            
            self.bola.desenhar(self.tela)
            self.player1.desenhar(self.tela)
            self.player2.desenhar(self.tela)

            pygame.display.update()