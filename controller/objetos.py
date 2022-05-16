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
    def __init__(self, posicao=list, tamanho_tela=tuple, tamanho=20, cor=[255,255,255], velocidade=5):
        self.posicao = posicao
        self.tamanho = tamanho
        self.cor = cor
        self.tamanho_tela = tamanho_tela
        self.velocidade = velocidade
        self.velocidade_bola = [self.velocidade, 0]

    def colisao_cima_baixo(self):
        '''
        -> Verifica se o objeto teve uma colisão com a parte superior ou inferior da tela
        :return: True se teve colisão
        '''
        if self.posicao[1] <= 0 or self.posicao[1] + self.tamanho >= self.tamanho_tela[1]:
            return True
        else:
            return False

    def saiu_fora_direito_esquerdo(self):
        '''
        -> Verifica se o objeto colidiu com o lado direito e esquerdo da tela
        :return: True se saiu
        '''
        if self.posicao[0] <= 0 or self.posicao[0] + self.tamanho >= self.tamanho_tela[0]:
            return True
        return False
    
    def get_local_vel(self):
        '''
        -> Obter o valor da posicao do objeto relativo a velocidade no eixo X e das duas no eio Y.
        :return: A posição referente ao eixo X e posição referente ao eixo Y
        '''

        if self.velocidade_bola[0] > 0:
            posicao_bola_x = self.posicao[0] + self.tamanho
        else:
            posicao_bola_x = self.posicao[0]
        posicao_bola_y = (self.posicao[1], self.posicao[1] + self.tamanho)

        return posicao_bola_x, posicao_bola_y

    def colisao_player(self, p):
        '''
        -> verifica se o objeto teve colisão com o player.
        :param p: player a ser verificado.
        :return: True se teve colisão.
        '''

        posicao_bola_x, posicao_bola_y = self.get_local_vel()

        if p[0][0] <= posicao_bola_x <= p[0][1] and (p[1][0] <= posicao_bola_y[0] <= p[1][1] or p[1][0] <= posicao_bola_y[1] <= p[1][1]):
                return True
        return False

    def definir_velocidade(self, p):
        '''
        -> Define a velocidade do objeto dependendo do local que colidiu com o player
        '''

        tamanho_player = p[1][1]-p[1][0]
        distancia_centro_final = (tamanho_player/2)+(self.tamanho/2)
        distencia_entre_os_centros = (self.posicao[1] + (self.tamanho/2)) - (p[1][0] + (tamanho_player/2))
        nova_velocidade_eixo_y = (distencia_entre_os_centros * self.velocidade)/distancia_centro_final

        self.velocidade_bola[1] = nova_velocidade_eixo_y

    def calcular_posicao(self, players):
        if self.colisao_cima_baixo():
            self.velocidade_bola[1] *= -1
        
        for player in players:
            if self.colisao_player(player):
                self.velocidade_bola[0] *= -1
                self.definir_velocidade(player)

        self.posicao[0] += self.velocidade_bola[0]
        self.posicao[1] += self.velocidade_bola[1]

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, pygame.Rect(self.posicao[0], self.posicao[1], self.tamanho, self.tamanho))
