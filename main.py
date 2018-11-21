import pygame
from pygame.locals import *

LARGURA = 550
ALTURA = 250
#CORES
AZUL = (100,100,255)
BRANCO = (255,255,255)
VERMELHO = (255,0,0)
VERDE = (34,139,34)
AMARELO = (228,252,18)

class Bola(object):
    def __init__(self, screensize):
        self.screensize = screensize #Pegando o tamanho da tela
        self.centrox = int(screensize[0]*0.5)
        self.centroy = int(screensize[1]*0.5)
        self.tamanho = 6
        self.retang = pygame.Rect(self.centrox-self.tamanho,
                                  self.centroy-self.tamanho,
                                  self.tamanho*2, self.tamanho*2) #esquerda, topo, largura, altura
        self.cor = AMARELO
        self.direcao = [1,1]
        self.velocidadex = 3
        self.velocidadey = 2
        self.colisao_esq = False #checa se bateu na parede da esquerda ou direita
        self.colisao_dir = False
    def update(self, raqt_player, raqt_bot):

        self.centrox += self.direcao[0]*self.velocidadex
        self.centroy += self.direcao[1]*self.velocidadey

        self.retang.center = (self.centrox, self.centroy)

        if self.retang.top <= 0:
            self.direcao[1] = 1 #se bater no topo, volta para baixo
        elif self.retang.bottom >=self.screensize[1]-1:
            self.direcao[1] = -1 #se bater no chao, volta para cima
        if self.retang.right >= self.screensize[0]-1:
            self.colisao_dir = True
        elif self.retang.left <= 0:
            self.colisao_esq = True
        if self.retang.colliderect(raqt_player.retang):
            self.direcao[0] = -1
        if self.retang.colliderect(raqt_bot.retang):
            self.direcao[0] = 1

    def renderizar(self, tela):
        pygame.draw.circle(tela, self.cor, self.retang.center, self.tamanho, 0)
        pygame.draw.circle(tela, BRANCO, self.retang.center, self.tamanho, 2)


class BotRaqt(object):
    def __init__(self, screensize):
        self.screensize = screensize
        self.centrox = 5
        self.centroy = int(screensize[1]*0.5)
        self.altura = 60
        self.largura = 8
        self.score = 0
        self.retang = pygame.Rect(0,self.centroy-int(self.altura*0.5), self.largura, self.altura)
        self.cor = VERMELHO

        self.vel = 5

    def update(self, bola):
        if bola.retang.top < self.retang.top:  # Verifica se a bola esta acima
            self.centroy -= self.vel
        elif bola.retang.bottom > self.retang.bottom:  # abaixo
            self.centroy += self.vel
        self.retang.center = (self.centrox, self.centroy)


    def renderizar(self, tela):
        pygame.draw.rect(tela, self.cor, self.retang, 0)
        pygame.draw.rect(tela, BRANCO, self.retang, 2)



class PlayerRaqt(object):
    def __init__(self, screensize):
        self.screensize = screensize
        self.centrox = screensize[0]-5
        self.centroy = int(screensize[1]*0.5)
        self.altura = 60
        self.largura = 8
        self.score = 0
        self.retang = pygame.Rect(0,self.centroy-int(self.altura*0.5), self.largura, self.altura)
        self.cor = VERDE

        self.vel = 4
        self.direcao = 0
    def update(self):
        self.centroy += self.direcao*self.vel
        self.retang.center = (self.centrox, self.centroy)

        if self.retang.top < 0:
            self.retang.top = 0
        if self.retang.bottom > self.screensize[1]-1:
            self.retang.bottom = self.screensize[1]-1

    def renderizar(self, tela):
        pygame.draw.rect(tela, self.cor, self.retang, 0)
        pygame.draw.rect(tela, BRANCO, self.retang, 2)

def doRectsOverlap(rect1, rect2):
    for a,b in [(rect1, rect2), (rect2,rect1)]:
        if((isPointInsideRect(a.left, a.top,b)) or
		   (isPointInsideRect(a.left, a.bottom,b)) or
		   (isPointInsideRect(a.right, a.bottom,b))):
            return True
    return False

def isPointInsideRect(x,y,rect):
    if(x>rect.left) and (x<rect.right) and (y > rect.top) and (y<rect.bottom):
        return True
    else:
        return False

def ScoreBot(score, fonte2, tela):
    botzera = fonte2.render("BOT: " + str(score), True, VERMELHO)
    tela.blit(botzera, [50, 0])

def ScorePlayer(score, fonte2, tela):
    player = fonte2.render("Player1 : " + str(score), True, VERDE)
    tela.blit(player, [450, 0])

def main():
    pygame.init()
    screensize = (LARGURA,ALTURA)
    tela = pygame.display.set_mode(screensize)
    clock = pygame.time.Clock() #Clock eh um objeto e nao uma funcao - sera usado para controlar e limitar o FPS do jogo
    fonte = pygame.font.SysFont("Verdana", 20 )
    fonte2 = pygame.font.SysFont("Verdana", 15)
    texto1 = fonte.render("PONG PONG", True, BRANCO)
    texto2 = fonte.render("DO KING KONG", True, BRANCO)

    bola = Bola(screensize)
    raqt_bot = BotRaqt(screensize)
    raqt_player = PlayerRaqt(screensize)


    rodando = True

    while rodando:
        #lidando com o FPS
        clock.tick(75)

        #verificacao de eventos
        for event in pygame.event.get(): #event.get pega todos os inputs (clicks de mouse, teclado)
            if event.type == QUIT:
                rodando = False
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    raqt_player.direcao = -1
                elif event.key == K_DOWN:
                    raqt_player.direcao = 1
            if event.type == KEYUP:
                if event.key == K_UP and raqt_player.direcao == -1:
                    raqt_player.direcao = 0
                elif event.key == K_DOWN and raqt_player.direcao == 1:
                    raqt_player.direcao = 0

        #atualizando os objetos

        raqt_bot.update(bola)
        raqt_player.update()
        bola.update(raqt_player, raqt_bot)
        checaBot = doRectsOverlap(raqt_bot.retang, bola.retang)
        checaPlayer = doRectsOverlap(raqt_player.retang, bola.retang)

        if bola.colisao_esq:
            rodando = False
            main()
        elif bola.colisao_dir:
            rodando = False
            main()
        if checaBot == True:
            raqt_bot.score += 1
        if checaPlayer == True:
            raqt_player.score += 1

        #renderizando
        tela.fill((0,0,0)) #deixando a tela preta
        tela.blit(texto1, (LARGURA / 2 - texto1.get_rect().width / 2, ALTURA / 2 - 30))
        tela.blit(texto2, (LARGURA / 2 - texto2.get_rect().width / 2, ALTURA / 2 - 10 ))
        ScoreBot(raqt_bot.score,fonte2,tela)
        ScorePlayer(raqt_player.score,fonte2,tela)
        raqt_bot.renderizar(tela)
        raqt_player.renderizar(tela)
        bola.renderizar(tela)
        pygame.display.flip() #atualiza as telas


main()
pygame.quit()
