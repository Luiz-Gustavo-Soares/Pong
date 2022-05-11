from numpy import place
import pygame


class Player:
    def __init__(self, posicao=list, tamanho=(16, 80), tamanho_tela=tuple, cor=(255,255,255), velocidade_p=8):
        self.posicao = posicao
        self.tamanho = tamanho
        self.cor = cor
        self.velocidade = 0
        self.velocidade_p = velocidade_p
        self.tamanho_tela = tamanho_tela

    def get_local(self):
        '''
        -> Obter o valor da posicao do player.
        :return: A posição referente ao eixo X, a posição referente ao eixo Y
        '''
        return (self.posicao[0], self.posicao[0] + self.tamanho[0]), (self.posicao[1], self.posicao[1] + self.tamanho[1])

    def move_top(self):
        '''
        -> Move o player para cima, o impedindo de sair da tela.
        '''
        if self.posicao[1] >= 0:  
            self.velocidade = self.velocidade_p * -1
        else: 
            self.velocidade = 0
    
    def move_down(self):
        '''
        -> Move o player para baixo, o impedindo de sair da tela.
        '''
        if self.posicao[1] + self.tamanho[1] <= self.tamanho_tela[1]:
            self.velocidade = self.velocidade_p
        else: 
            self.velocidade = 0
        
    def saiu_tela(self):
        '''
        -> Verifica se o player saiu da tela.
        :return: True se saiu da tela, False se não saiu.
        '''
        if self.posicao[1] <= 0:
            return True
        elif self.posicao[1] + self.tamanho[1] >= self.tamanho_tela[1]:
            return True
        else:
            return False

    def calcular_posicao(self):
        '''
        -> Calcula a nova posição do player
        '''
        self.posicao[1] += self.velocidade
        self.velocidade = 0

    def desenhar(self, tela):
        '''
        -> Desenha o player na tela
        :param tela: tela a ser desenhada
        '''
        self.calcular_posicao()

        pygame.draw.rect(tela, self.cor, pygame.Rect(self.posicao[0], self.posicao[1], self.tamanho[0], self.tamanho[1]))


class Bola:
    def __init__(self, posicao=list, tamanho_tela=tuple, raio=10, cor=[255,255,255], velocidade=[5, 5]):
        self.posicao = posicao
        self.raio = raio
        self.cor = cor
        self.tamanho_tela = tamanho_tela
        self.velocidade = velocidade

    def colisao_cima_baixo(self):
        '''
        -> Verifica se o objeto teve uma colisão com a parte superior ou inferior da tela
        :return: True se teve colisão
        '''
        if self.posicao[1] <= 0 + self.raio or self.posicao[1] + self.raio >= self.tamanho_tela[1]:
            return True
        else:
            return False

    def posicao_real_relativa_a_velocida(self):
        '''
        -> Calcula a posição do objeto dependendo da sua velocidade
        :return: posição X/Y
        '''
        if self.velocidade[0] > 0:
            posicao_bola_x = self.posicao[0] + self.raio
        else:
            posicao_bola_x = self.posicao[0] - self.raio
        
        if self.velocidade[1] > 0:
            posicao_bola_y = self.posicao[1] + self.raio
        else:
            posicao_bola_y = self.posicao[1] - self.raio

        return posicao_bola_x, posicao_bola_y

    def colisao_player(self, p):
        '''
        -> verifica se o objeto teve colisão com o player.
        :param p: player a ser verificado.
        :return: True se teve colisão.
        '''

        posicao_bola_x, posicao_bola_y = self.posicao_real_relativa_a_velocida()

        if p[0][0] <= posicao_bola_x <= p[0][1] and p[1][0] <= posicao_bola_y <= p[1][1]:
                print(True)
                return True

        return False

    def calcular_posicao(self, players):
        if self.colisao_cima_baixo():
            self.velocidade[1] *= -1
        
        for player in players:
            if self.colisao_player(player):
                self.velocidade[0] *= -1

        self.posicao[0] += self.velocidade[0]
        self.posicao[1] += self.velocidade[1]

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, self.posicao, self.raio, 0)
