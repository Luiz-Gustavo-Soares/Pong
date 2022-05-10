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
        return (self.posicao[0], self.posicao[0] + self.tamanho[0]), (self.posicao[1], self.posicao[1] + self.tamanho[1])

    def move_top(self):
        if self.posicao[1] >= 0:  
            self.velocidade = self.velocidade_p * -1
        else: 
            self.velocidade = 0
    
    def move_down(self):
        if self.posicao[1] + self.tamanho[1] <= self.tamanho_tela[1]:
            self.velocidade = self.velocidade_p
        else: 
            self.velocidade = 0
        
    def saiu_tela(self):
        if self.posicao[1] <= 0:
            return True
        elif self.posicao[1] + self.tamanho[1] >= self.tamanho_tela[1]:
            return True
        else:
            return False

    def calcular_posicao(self):
        self.posicao[1] += self.velocidade
        self.velocidade = 0

    def desenhar(self, tela):
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
        if self.posicao[1] <= 0 + self.raio:
            return True
        
        elif self.posicao[1] + self.raio >= self.tamanho_tela[1]:
            return True

        else:
            return False

    def colisao_player(self, p):

        if self.posicao[0] - self.raio <= p[0][0][1] and self.posicao[1] > p[0][1][0] and self.posicao[1] < p[0][1][1]:
            return True

        if self.posicao[0] + self.raio >= p[1][0][0] and self.posicao[1] > p[1][1][0] and self.posicao[1] < p[1][1][1]:
            return True
        
        return False

    def calcular_posicao(self, players):
        if self.colisao_cima_baixo():
            self.velocidade[1] *= -1
        
        if self.colisao_player(players):
            self.velocidade[0] *= -1

        self.posicao[0] += self.velocidade[0]
        self.posicao[1] += self.velocidade[1]

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, self.posicao, self.raio, 0)
