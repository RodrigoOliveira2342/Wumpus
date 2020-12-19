
# coding: utf-8



import pygame
import random
clock = pygame.time.Clock()




class Coisa:
    
    def __init__(self,estado = None):
        self.estado = estado
        self.idNoTabuleiro = 0
        
    def __repr__(self):
        #representação do objeto na forma de string
        return '<{}>'.format(getattr(self, '__name__',self.__class__.__name__))
    
    def mostraEstado(self):
        return str(self.estado)
    
    def vivo(self):
        return hasattr(self, 'vivo') and self.vivo
    



class Agente(Coisa):
    
    def __init__(self,estado = None, funcaoAgente = None):
        super().__init__(estado)
        if funcaoAgente == None:
            def funcaoAgente(*entradas):
                return "Ação Default"
        self.funcaoAgente = funcaoAgente
        self.historicoPercepcoes = []
        self.x = 0
        self.y = 3
        
    def movimentacao(self,x,y):
        self.x = x
        self.y = y
        



class Jogador(Agente):
    def __init__(self,estadoInicial = None, funcaoAgente = None):
        super().__init__(estadoInicial,funcaoAgente)
        self.img = pygame.image.load('Jogador.png')
        self.idNoTabuleiro = -1

        




class PoSo(Coisa):
    def __init__(self,estado = None,x = 0, y = 0):
        super().__init__(estado)
        self.img = pygame.image.load('PoSo.png')
        self.x = x
        self.y = y
        self.idNoTabuleiro = 2
    
          
        
    



class Ouro(Coisa):
    def __init__(self,estado = None,x = 0, y = 0):
        super().__init__(estado)
        self.img = pygame.image.load('Ouro.png')
        self.x = x
        self.y = y
        self.idNoTabuleiro=1




class Wumpus(Coisa):
    def __init__(self,estado = None,x = 0, y = 0):
        super().__init__(estado)
        self.img = pygame.image.load('Wumpus.png')
        self.x = x
        self.y = y
        self.idNoTabuleiro=3




class Ambiente:
    
    def __init__(self,estadoInicial = None, gr = None):
        self.estado = estadoInicial
        self.objetosNoAmbiente = []
        self.agentes = []
        self.dest = []
        self.tabuleiro = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        
    
    def adicionaAgente(self,agente):
        self.agentes.append(agente)
        self.tabuleiro[agente.y][agente.x]=agente.idNoTabuleiro
        
    def adicionaObjeto(self,obj):
        self.objetosNoAmbiente.append(obj)
        self.tabuleiro[obj.y][obj.x]=obj.idNoTabuleiro
        
        




class Labirinto(Ambiente):
    def __init__(self,estadoInicial):
        super().__init__(estadoInicial)
        pygame.init()
        self.fim = False
        self.fechar = False
        self.cont=False

    def executaAmbiente(self):
        self.py = 3
        self.px = 0
        self.tela = pygame.display.set_mode((512,640),0,8)
        self.planoDeFundo()

        self.tela.blit(self.agentes[0].img,(self.agentes[0].x*128, self.agentes[0].y*128))
        pygame.display.update()#AT elementos no display
        Akeys = "0"
        while not self.fechar:
            keys = pygame.key.get_pressed()
            if self.fim!= True:
                if keys !=Akeys:
                    if keys[pygame.K_LEFT] and self.px>0:
                        self.px-=1
                    if keys[pygame.K_RIGHT] and self.px<3:
                        self.px+=1
                    if keys[pygame.K_UP] and self.py>0:
                        self.py-=1
                    if keys[pygame.K_DOWN] and self.py<3:
                        self.py+=1
                Akeys = keys
                self.fim , self.imgINF = self.agentes[0].funcaoAgente(self.tabuleiro,self.agentes[0].x,self.agentes[0].y)
                if keys !=0:
                    self.agentes[0].movimentacao(self.px,self.py)
                    self.planoDeFundo()
                    self.tela.blit(self.agentes[0].img,(self.agentes[0].x*128, self.agentes[0].y*128))
                    self.tela.blit(self.imgINF,(0,514))
                    pygame.time.delay(100)
            else:
                self.planoDeFundo()
                for i in range(len(self.objetosNoAmbiente)):
                        self.tela.blit(self.objetosNoAmbiente[i].img,(self.objetosNoAmbiente[i].x*128, self.objetosNoAmbiente[i].y*128))
                self.tela.blit(self.imgINF,(0,514))
                if keys[pygame.K_SPACE]:
                        self.cont=True
                        self.fechar = True
                        pygame.time.delay(100)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.fechar = True
            pygame.display.update()
            clock.tick(60)

        pygame.quit()
        return self.cont           
    def planoDeFundo(self):
        self.tela.fill((250,250,250))
        for x in range(0,512,128):
            pygame.draw.line(self.tela, (255,0,0), (x,0), (x,512))
        for y in range(0,513,128):
            pygame.draw.line(self.tela, (255,0,0), (0,y), (512,y))
            

        
        

  


# In[115]:


def encontrar (tabuleiro,x,y):
    if tabuleiro[y][x] > 1:
        img= pygame.image.load('RGO.png')
        return True , img
    elif tabuleiro[y][x] == 1:
        img = pygame.image.load('RGF.png')
        return True , img
    txt='R'
    if (x>0 and tabuleiro[y][x-1]==2) or (x<3 and tabuleiro[y][x+1]==2) or (y>0 and tabuleiro[y-1][x]==2) or (y<3 and tabuleiro[y+1][x]==2):
        txt=txt+'B'
    if (x>0 and tabuleiro[y][x-1]==3) or (x<3 and tabuleiro[y][x+1]==3) or (y>0 and tabuleiro[y-1][x]==3) or (y<3 and tabuleiro[y+1][x]==3):
        txt=txt+'F'
    if (x>0 and tabuleiro[y][x-1]==1) or (x<3 and tabuleiro[y][x+1]==1) or (y>0 and tabuleiro[y-1][x]==1) or (y<3 and tabuleiro[y+1][x]==1):
        txt=txt+'L'
    txt=txt+'.png'
    img= pygame.image.load(txt)
    return  False, img





def rxy():
    while True:
        x=random.randint(0,3)
        y=random.randint(0,3)
        if a.tabuleiro[y][x]==0:
            break
    return x,y
while True:
    a = Labirinto([])
    j = Jogador([],encontrar)
    a.adicionaAgente(j)

    x,y = rxy()
    o = Ouro(0,x,y)
    a.adicionaObjeto(o)

    x,y = rxy()
    w = Wumpus(0,x,y)
    a.adicionaObjeto(w)

    x,y = rxy()
    p1 = PoSo(0,x,y)
    a.adicionaObjeto(p1)

    x,y = rxy()
    p2 = PoSo(0,x,y)
    a.adicionaObjeto(p2)

    cont = a.executaAmbiente()
    if cont == False:
        break

