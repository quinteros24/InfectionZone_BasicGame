from typing import Pattern
import pygame
import random

from pygame.constants import QUIT

ROJO = [255,0,0]
VERDE = [103,148,12]
VERDE_S = [0,255,0]
AZUL = [0,0,255]
AZUL_FONDO = [115,215,245]
BLANCO = [255,255,255]
GRIS = [245,245,245]
GRIS_CLARO = [225,200,200]
GRIS_CLARO_CLARO = [197,197,197]
NEGRO = [0,0,0]
AMARILLO = [255,255,0]
PURPURA = [128,0,128]
NARANJA = [255,165,0]
NARANJA_CLARO = [255,170,156]
NARANJA_CLARO_CLARO = [255,230,190]
ROSA = [255,40,210]
ROSA_CLARO = [255,108,160]
ROSA_CLARO_CLARO = [255,205,250]

ANCHO_VENTANA = 1400
ALTO_VENTANA = 700

#Variable que permite que el jugador se mueva por el mapa
moverse = True


class jugador(pygame.sprite.Sprite):
    #Creamos el constructor
    def __init__(self,matriz):
        pygame.sprite.Sprite.__init__(self)
        self.matriz = matriz
        self.col = 0
        self.fil = 0
        self.image = self.matriz[self.fil][self.col]
        #La posicion esta controlada por rect
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 500
        self.velx = 0
        self.vely = 0
        self.bloques = pygame.sprite.Group()
        self.modificadores = pygame.sprite.Group()
        self.puntos = 0
        self.salud = 100
        self.liminf = 0
        self.limsup = 0
        self.arma = True
        self.resistencia = False
        self.poder = False
    def update(self):
        #Limites para la colision zombie
        self.liminf = self.rect.bottom-20
        self.limsup = self.rect.bottom+40
        if self.velx != self.vely:
            self.image = self.matriz[self.fil][self.col]
            #print('fila ',self.fil,'   col ',self.col)
            if self.col<3:
                self.col += 1
            else:
                self.col = 0
        self.rect.x += self.velx
        ls_col=pygame.sprite.spritecollide(self, self.bloques, False)
        for b in ls_col:
            if self.velx > 0:
                if self.rect.right > b.rect.left:
                    self.rect.right = b.rect.left
                    self.velx = 0
            else:
                if self.rect.left < b.rect.right:
                    self.rect.left = b.rect.right
                    self.velx = 0
        self.rect.y += self.vely
        ls_col=pygame.sprite.spritecollide(self, self.bloques, False)
        for b in ls_col:
            if self.vely > 0:
                if self.rect.bottom > b.rect.top:
                    self.rect.bottom = b.rect.top
                    self.vely = 0
            else:
                if self.rect.top < b.rect.bottom:
                    self.rect.top = b.rect.bottom
                    self.vely = 0
        #Si hay zombies no se va a poder mover por el mapa
        #hasta que los mate a todos
        if not moverse:
            if self.rect.right > ANCHO_VENTANA:
                self.rect.right = ANCHO_VENTANA
                self.velx = 0
            if self.rect.left < 0:
                self.rect.left = 0
                self.velx = 0
            if self.rect.bottom > ALTO_VENTANA:
                self.rect.bottom = ALTO_VENTANA
                self.vely = 0
            if self.rect.top < 0:
                self.rect.top = 0
                self.vely = 0

class bloque(pygame.sprite.Sprite):
    #Creamos el constructor
    def __init__(self,dimensiones, posicion, col=ROJO):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dimensiones)
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.x = posicion[0]
        self.rect.y = posicion[1]

class bala(pygame.sprite.Sprite):
    #Creamos el constructor
    def __init__(self, pos, imbala, boton, vel):
        pygame.sprite.Sprite.__init__(self)
        self.imbala = imbala
        self.vel = vel
        self.image = self.imbala
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vely = 0
        self.velx = 0
        self.boton = boton
    def update(self):
        if self.boton == 1:
            self.velx = 15+self.vel
        elif self.boton == 2:
            self.velx = -15+(self.vel*-1)
        elif self.boton == 3:
            self.vely = -15+(self.vel*-1)
        elif self.boton == 4 or self.boton == 0:
            self.vely = 15+self.vel
        self.rect.x += self.velx
        self.rect.y += self.vely

class generadorZombies(pygame.sprite.Sprite):
    #Entidad que genera nuevos sprites
    def __init__(self, pos, dimensiones):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([dimensiones[0],dimensiones[1]])
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class generadorojo(pygame.sprite.Sprite):
    def __init__(self, pos, lista):
        pygame.sprite.Sprite.__init__(self)
        self.lista = lista
        self.col = 0
        self.image = self.lista[self.col]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.salud = 100
        self.temp=random.randrange(30,70)
    def update(self):
        self.temp -= 1
        self.image = self.lista[self.col]
        if self.col<5:
            self.col += 1
        else:
            self.col = 0

class zombie(pygame.sprite.Sprite):
    #Entidad que genera nuevos sprites
    def __init__(self, pos, matriz):
        pygame.sprite.Sprite.__init__(self)
        self.matriz = matriz
        self.col = 0
        self.fil = 0
        self.image = self.matriz[self.fil][self.col]
        self.rect = self.image.get_rect()
        self.velx = 0
        self.vely = 0
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.salud = 100
    def update(self):
        self.image = self.matriz[self.fil][self.col]
        if self.col<2:
            self.col += 1
        else:
            self.col = 0
        self.rect.x += self.velx
        self.rect.y += self.vely

class modificador(pygame.sprite.Sprite):
    def __init__(self, pos, lista, col):
        pygame.sprite.Sprite.__init__(self)
        self.lista = lista
        self.col = col
        self.image = self.lista[self.col]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class portal(pygame.sprite.Sprite):
    def __init__(self, pos, lista):
        pygame.sprite.Sprite.__init__(self)
        self.lista = lista
        self.col = 0
        self.image = self.lista[self.col]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    def update(self):
        self.image = self.lista[self.col]
        if self.col<3:
            self.col += 1
        else:
            self.col = 0

class sangre(pygame.sprite.Sprite):
    #Creamos el constructor
    def __init__(self, pos, lista):
        pygame.sprite.Sprite.__init__(self)
        self.lista = lista
        self.col = 0
        self.image = self.lista[self.col]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    def update(self):
        self.image = self.lista[self.col]
        if self.col<3:
            self.col += 1
        else:
            self.col = 0

class fantasma(pygame.sprite.Sprite):
    #Creamos el constructor
    def __init__(self, pos, imiz, imde):
        pygame.sprite.Sprite.__init__(self)
        self.imiz = imiz
        self.imde = imde
        self.image = self.imiz
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vely = 0
        self.velx = 0
        self.salud = 100
    def update(self):
        if self.image == self.imde:
            self.image = self.imiz
        else:
            self.image = self.imde
        self.rect.x += self.velx
        self.rect.y += self.vely

class ojo(pygame.sprite.Sprite):
    #Creamos el constructor
    def __init__(self, pos,left_view,right_view,bottom_view,top_view):
        pygame.sprite.Sprite.__init__(self)
        self.left_view = left_view
        self.right_view = right_view
        self.top_view = top_view
        self.bottom_view = bottom_view
        self.lista = self.top_view
        self.col = 0
        self.image = self.lista[self.col]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vely = 0
        self.velx = 0
        self.salud = 300
        self.right_limit = 1670
        self.left_limit = 32
        self.top_limit = 1312
        self.bottom_limit = 2944
    def update(self):
        self.image = self.lista[self.col]
        if self.col<5:
            self.col += 1
        else:
            self.col = 0
        self.rect.x += self.velx
        self.rect.y += self.vely

class generadoresqueleto(pygame.sprite.Sprite):
    def __init__(self, pos, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.salud = 100
        self.temp=100
    def update(self):
        self.temp -= 1

class balaesqueleto(pygame.sprite.Sprite):
    #Creamos el constructor
    def __init__(self, pos, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vely = 0
        self.velx = 0
    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely

if __name__ == '__main__':
    #Inicialización del juego
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])
    Fuente = pygame.font.Font(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\upheavtt.ttf', 50) #Fuente del mensaje que arroja 
    texto = "FIN DEL JUEGO..."
    ubicacion_mensaje = [500,350]
    #------------------------------------------------------------------------------------------------------------------FONDO
    fondo = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\terreno.png')
    info_fondo = fondo.get_rect()

    ancho_fondo = info_fondo[2]
    alto_fondo = info_fondo[3]

    #------------------------------------------------------------------------------------------------------------------MODIFICADORES
    #Modificadores bala
    alcance_bala = 300
    velmod = 0

    #modificacion jugador
    velocidadjug = 50
    mod_arma = 2


    #------------------------------------------------------------------------------------------------------------------RECORTE PERSONAJE
    img_bala = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\punto.png')

    img_bala2 = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\bola2.png')

    linea = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\linea.png')

    fantiz = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\fantaiz.png')

    fander = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\fantader.png')

    imesq = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\generador.png')

    balaiz = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\balaizq.png')

    balader = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\balader.png')

    balaarriba = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\balatop.png')

    balabajo = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\baladown.png')
    #______________________________________

    im_jug = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\calvo.png')
    info_img = im_jug.get_rect()

    ancho_img = info_img[2]
    alto_img = info_img[3]

    matriz = []
    #Cuantos recortes hay a lo ancho y a lo alto
    sp_ancho = 4
    sp_alto = 4
    desplazamiento_x = 79.25
    desplazamiento_y = 96
    for i in range(sp_alto):
        aux = []
        for j in range(sp_ancho):
            cuadro = im_jug.subsurface(desplazamiento_x*j,desplazamiento_y*i,desplazamiento_x,desplazamiento_y)
            aux.append(cuadro)
        matriz.append(aux)
    #------------------------------------------------------------------------------------------------------------------RECORTE ZOMBIE INICIO
    im_zoini = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\zombieinicio.png')
    info_img = im_zoini.get_rect()

    ancho_img = info_img[2]
    alto_img = info_img[3]

    list_zom = []
    #Cuantos recortes hay a lo ancho y a lo alto
    sp_ancho = 8
    desplazamiento_x = 102
    for i in range(sp_ancho):
        cuadro = im_zoini.subsurface(desplazamiento_x*i,0,desplazamiento_x,120)
        list_zom.append(cuadro)

    #------------------------------------------------------------------------------------------------------------------RECORTE ZOMBIE
    im_zomb = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\zombie.png')
    info_img = im_zomb.get_rect()

    ancho_img = info_img[2]
    alto_img = info_img[3]

    matrizzomb = []
    #Cuantos recortes hay a lo ancho y a lo alto
    sp_ancho = 3
    sp_alto = 4
    desplazamiento_x = 100
    desplazamiento_y = 100
    for i in range(sp_alto):
        aux = []
        for j in range(sp_ancho):
            cuadro = im_zomb.subsurface(desplazamiento_x*j,desplazamiento_y*i,desplazamiento_x,desplazamiento_y)
            aux.append(cuadro)
        matrizzomb.append(aux)

    #------------------------------------------------------------------------------------------------------------------RECORTE MODIFICADORES
    im_mod = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\mods.png')
    info_img = im_mod.get_rect()

    ancho_img = info_img[2]
    alto_img = info_img[3]

    matrizmod = []
    #Cuantos recortes hay a lo ancho y a lo alto
    sp_ancho = 4
    desplazamiento_x = 32
    for i in range(sp_ancho):
        cuadro = im_mod.subsurface(desplazamiento_x*i,0,desplazamiento_x,64)
        matrizmod.append(cuadro)

    im_mod_no = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\saturado.png')
    info_img = im_mod_no.get_rect()

    ancho_img = info_img[2]
    alto_img = info_img[3]

    lista_mod = []
    #Cuantos recortes hay a lo ancho y a lo alto
    sp_ancho = 4
    desplazamiento_x = 32
    for i in range(sp_ancho):
        cuadro = im_mod_no.subsurface(desplazamiento_x*i,0,desplazamiento_x,65)
        lista_mod.append(cuadro)

    #------------------------------------------------------------------------------------------------------------------RECORTE PORTAL
    im_portal = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\portal.png')
    info_img = im_portal.get_rect()

    ancho_img = info_img[2]
    alto_img = info_img[3]

    lista_portal = []
    #Cuantos recortes hay a lo ancho y a lo alto
    sp_ancho = 4
    desplazamiento_x = 70
    for i in range(sp_ancho):
        cuadro = im_portal.subsurface(desplazamiento_x*i,0,desplazamiento_x,166)
        lista_portal.append(cuadro)

    #------------------------------------------------------------------------------------------------------------------RECORTE OJO
    im_ojo = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\ojo.png')
    info_img = im_ojo.get_rect()

    ancho_img = info_img[2]
    alto_img = info_img[3]

    lista_ojo = []
    #Cuantos recortes hay a lo ancho y a lo alto
    sp_alto = 6
    desplazamiento_y = 378
    for i in range(sp_alto):
        cuadro = im_ojo.subsurface(0,desplazamiento_y*i,250,desplazamiento_y)
        lista_ojo.append(cuadro)

    
    im_ojohor = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\ojohorizontal.png')
    info_img = im_ojohor.get_rect()

    ancho_img = info_img[2]
    alto_img = info_img[3]

    lista_ojohor = []
    #Cuantos recortes hay a lo ancho y a lo alto
    sp_ancho = 6
    desplazamiento_x = 378
    for i in range(sp_ancho):
        cuadro = im_ojohor.subsurface(desplazamiento_x*i,0,desplazamiento_x,250)
        lista_ojohor.append(cuadro)


    im_ojohorder = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\ojohorizontalder.png')
    info_img = im_ojohorder.get_rect()

    ancho_img = info_img[2]
    alto_img = info_img[3]

    lista_ojohorder = []
    #Cuantos recortes hay a lo ancho y a lo alto
    sp_ancho = 6
    desplazamiento_x = 378
    for i in range(sp_ancho):
        cuadro = im_ojohorder.subsurface(desplazamiento_x*i,0,desplazamiento_x,250)
        lista_ojohorder.append(cuadro)


    im_ojoabajo = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\ojoabajo.png')
    info_img = im_ojoabajo.get_rect()

    ancho_img = info_img[2]
    alto_img = info_img[3]

    lista_ojoabajo = []
    #Cuantos recortes hay a lo ancho y a lo alto
    sp_alto = 6
    desplazamiento_y = 378
    for i in range(sp_alto):
        cuadro = im_ojoabajo.subsurface(0,desplazamiento_y*i,250,desplazamiento_y)
        lista_ojoabajo.append(cuadro)

    #------------------------------------------------------------------------------------------------------------------RECORTE SANGRE
    im_sangre = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\sangre_j1.png')
    info_img = im_sangre.get_rect()

    ancho_img = info_img[2]
    alto_img = info_img[3]

    lista_sangre = []
    #Cuantos recortes hay a lo ancho y a lo alto
    sp_ancho = 4
    desplazamiento_x = 100
    for i in range(sp_ancho):
        cuadro = im_sangre.subsurface(desplazamiento_x*i,0,desplazamiento_x,126)
        lista_sangre.append(cuadro)
    #------------------------------------------------------------------------------------------------------------------INFO FONDO
    
    infoimag = fondo.get_rect()
    ancho_fondo = infoimag[2] #Para saber cuando acaba
    alto_fondo = infoimag[3]

    #------------------------------------------------------------------------------------------------------------------CREACION MODIFICADORES
    #Primer Arma
    modificadores=pygame.sprite.Group()
    mod1=modificador([960,1056],matrizmod,2)
    modificadores.add(mod1)

    #Resistencia
    mod_res = modificador([2240,96],matrizmod,3)
    modificadores.add(mod_res)

    #Armamento pesado
    mod2 = modificador([5248,1504],matrizmod,1)
    modificadores.add(mod2)

    #------------------------------------------------------------------------------------------------------------------INICIALIZACION
    stage = 1
    boton = 0
    
    jugadores=pygame.sprite.Group()
    j1=jugador(matriz)
    jugadores.add(j1)

    #--------------------------------------------------------------COLISIONES
    bloques=pygame.sprite.Group()
    #Stage 1
    capilla=bloque([100,128], [1696,32])
    bloques.add(capilla)
    arbustos1 = bloque([128,384],[32,804])
    bloques.add(arbustos1)
    arbustos2 = bloque([1664,96],[160,1120])
    bloques.add(arbustos2)
    #Stage 2
    casas1 = bloque([3072,96],[2112,224])
    bloques.add(casas1)
    casas2 = bloque([416,73],[2112,800])
    bloques.add(casas2)
    casas3 = bloque([352,96],[2112,1120])
    bloques.add(casas3)
    casas4 = bloque([960,192],[2112,1408])
    bloques.add(casas4)
    iglesia1 = bloque([96,192],[2720,928])
    bloques.add(iglesia1)
    iglesia2 = bloque([224,96],[2656,1024])
    bloques.add(iglesia2)
    casas5 = bloque([576,106],[3072,800])
    bloques.add(casas5)
    casas6 = bloque([544,96],[3104,1152])
    bloques.add(casas6)
    arboles1 = bloque([160,960],[3488,800])
    bloques.add(arboles1)
    arboles2 = bloque([160,960],[4032,800])
    bloques.add(arboles2)
    arboles3 = bloque([64,64],[4384,864])
    bloques.add(arboles3)
    arboles4 = bloque([64,64],[5024,864])
    bloques.add(arboles4)
    arboles5 = bloque([64,64],[4384,1440])
    bloques.add(arboles5)
    arboles6 = bloque([64,64],[5024,1440])
    bloques.add(arboles6)
    casas7 = bloque([192,128],[4352,1088])
    bloques.add(casas7)
    casas8 = bloque([192,128],[4896,1088])
    bloques.add(casas8)
    casas9 = bloque([160,128],[4640,896])
    bloques.add(casas9)
    casas10 = bloque([160,128],[4640,1280])
    bloques.add(casas10)
    carros1 = bloque([576,128],[4864,1632])
    bloques.add(carros1)
    carros2 = bloque([128,448],[5344,800])
    bloques.add(carros2)
    #Stage 3
    arboles7 = bloque([96,64],[4256,2240])
    bloques.add(arboles7)
    arboles8 = bloque([96,96],[3296,1952])
    bloques.add(arboles8)
    arboles9 = bloque([96,96],[4576,1984])
    bloques.add(arboles9)
    arboles10 = bloque([96,96],[4480,2400])
    bloques.add(arboles10)
    arboles11 = bloque([96,96],[3168,2432])
    bloques.add(arboles11)
    arboles12 = bloque([96,96],[2464,2400])
    bloques.add(arboles12)
    #Stage 4
    arboles13 = bloque([1024,32],[256,1888])
    bloques.add(arboles13)

    #------------------------------------------------------------------------------------------------------------------CREACION GENERADORES
    generadores = pygame.sprite.Group()
    g1 = generadorZombies([1920,600],[80,80])
    generadores.add(g1)
    g2 = generadorZombies([3392,480],[32,256])
    generadores.add(g2)

    fantasmas = pygame.sprite.Group()

    generadores_ojos = pygame.sprite.Group()
    g_o = generadorojo([3744,1440],lista_ojo)
    generadores_ojos.add(g_o)
    g_o = generadorojo([5120,448],lista_ojohor)
    generadores_ojos.add(g_o)
    

    balas_esqueletos = pygame.sprite.Group()

    generadores_esqueletos = pygame.sprite.Group()
    ge = generadoresqueleto([(85*32),(65*32)],imesq)
    generadores_esqueletos.add(ge)
    # ge = generadoresqueleto([(32*148),(32*75)],imesq)
    # generadores_esqueletos.add(ge)


    ojos = pygame.sprite.Group()
    o = ojo([1664,2912],lista_ojohor,lista_ojohorder,lista_ojoabajo,lista_ojo)
    ojos.add(o)


    portales = pygame.sprite.Group()
    pos_portal1 = [1800,400]
    pos_portal2 = [3744,1440]
    pos_portal3 = [70*32,64*32]
    crear_portal1 = False
    crear_portal2 = False
    crear_portal3 = False

    sangres = pygame.sprite.Group()
    mostrar_sangre = False

    zombies=pygame.sprite.Group()
    balas=pygame.sprite.Group()

    j1.bloques = bloques
    j1.modificadores = modificadores

    #Organizo el fondo antes de empezar
    f_posx = 0
    f_posy = 0
    f_vel = -10 #Se desplaza hacia la izquierda
    entra = False
    f_posx_anterior = 0
    f_posy_anterior = 0
    entra_por1 = False
    entra_por2 = False
    entra_por3 = False
    auxiliar_portal1 = 1
    auxiliar_portal2 = 1
    auxiliar_portal3 = 1
    aceptar_tecla = True #Acepta instrucciones
    guillermo = 10 #Lo que baja de salud
    limite_fantasmas_hor = (66*32)
    limite_fantasmas_ver = 32
    limite_bala_izq = (66*32)
    limite_bala_der = ancho_fondo-32
    limite_bala_arriba = 1856
    limite_bala_abajo = alto_fondo - 32
    x = 1
    s=0

    '''------------------------------------------------------------------------------------------------------------------CICLO DEL JUEGO'''
    
    reloj=pygame.time.Clock()
    fin = False
    fin_juego = False
    
    while (not fin) and (not fin_juego):
        #tener en cuenta que la sala podria ser mas pequeña
    #------------------------------------------------------------------------------------------------------------------STAGES
        if not entra:
            if stage == 1:
                oleadas = 1
                #Modo creativo
                limite_ventanaxder = -6000
                limite_ventanaxizq = 6000
                limite_ventanayabajo = -6000
                limite_ventanayarriba = 6000
                #limites para el stage 1
                # limite_ventanaxder = ANCHO_VENTANA - (66*32)
                # limite_ventanaxizq = 0
                # limite_ventanayabajo = ALTO_VENTANA - 1280
                # limite_ventanayarriba = 0
                #limites movimiento stage 1
                lim_right = ANCHO_VENTANA - (6*32)
                lim_left = 32
                lim_top = 32
                lim_bottom = ALTO_VENTANA - (2*32)
            elif stage == 1.5:
                #Quitamos los límites de la pantalla
                #print("Entré")
                limite_ventanaxder = -6000
                limite_ventanaxizq = 6000
                limite_ventanayabajo = -6000
                limite_ventanayarriba = 6000
            elif stage == 2:
                oleadas = 1
                #limites para el stage 2
                limite_ventanaxder = -1*(ancho_fondo-ANCHO_VENTANA-10)
                limite_ventanaxizq = -1920
                limite_ventanayabajo = -1152
                limite_ventanayarriba = 0
                #limites movimiento stage 2
                lim_right = ANCHO_VENTANA - 32
                lim_left = (6*32)
                lim_top = 32
                lim_bottom = ALTO_VENTANA - (3*32)
            elif stage == 3:
                limite_ventanaxder = -1*(ancho_fondo-ANCHO_VENTANA-10)
                limite_ventanaxizq = -1920
                limite_ventanayabajo = -2510
                limite_ventanayarriba = -1760
                #limites movimiento stage 3
                lim_right = ANCHO_VENTANA - 32
                lim_left = (32*6)
                lim_top = (32*3)
                lim_bottom = ALTO_VENTANA - 32
            elif stage == 4:
                oleadas = 1
                limite_ventanaxder = -710
                limite_ventanaxizq = 0
                limite_ventanayabajo = -2500
                limite_ventanayarriba = -1210
                #limites movimiento stage 3
                lim_right = ANCHO_VENTANA - (32*6)
                lim_left = 32
                lim_top = (32*2)
                lim_bottom = ALTO_VENTANA - 32
            entra = True

        #print('[',j1.rect.x,',',j1.rect.y,']')
    
    #------------------------------------------------------------------------------------------------------------------EVENTOS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if aceptar_tecla:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        j1.fil = 3
                        j1.velx = 10+velocidadjug
                        j1.vely = 0
                        boton = 1
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        j1.fil = 2
                        j1.velx = -10+(velocidadjug*-1)
                        j1.vely = 0
                        boton = 2
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        j1.fil = 1
                        j1.vely = -10+(velocidadjug*-1)
                        j1.velx = 0
                        boton = 3
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        j1.fil = 0
                        j1.vely = 10+velocidadjug
                        j1.velx = 0
                        boton = 4
                    if event.key == pygame.K_SPACE:
                        if mod_arma == 1:
                            posbala = j1.rect.midtop
                            bu=bala(posbala,img_bala, boton, velmod)
                            balas.add(bu)
                        elif mod_arma == 2:
                            posbala = j1.rect.midtop
                            bu=bala(posbala,img_bala2, boton, velmod)
                            balas.add(bu)
                if event.type == pygame.KEYUP:
                    j1.velx = 0
                    j1.vely = 0

    #------------------------------------------------------------------------------------------------------------------SUCESOS
        if stage == 1 and oleadas > 0 and len(zombies)==0 and mod_arma == 1:
            for i in range(1):
                posy = random.randrange(100,580)
                z = zombie([g1.rect.x,posy],matrizzomb)
                z.fil = 1
                z.velx = random.randrange(-12,-2)
                zombies.add(z)
            oleadas -= 1
            auxuliar = 1
        
        #print(f_posx,'  ',j1.rect.x)
        if stage == 2 and oleadas > 0 and len(zombies)==0:
            if f_posx < -1910:
                for i in range(40):
                    posy = random.randrange(j1.rect.y-50,j1.rect.y+50)
                    z = zombie([g2.rect.x,posy],matrizzomb)
                    z.fil = 1
                    z.velx = random.randrange(-12,-2)
                    zombies.add(z)
                oleadas -= 1

        
        if stage == 4 and oleadas > 0:
            #print('entre')
            if o.velx == o.vely and x==1:
                o.vely = -20
                x=0
            if o.top_limit > o.rect.top:
                print([o.rect.x,o.rect.y],' izaq: ',o.left_limit,' der: ',o.right_limit,' arriba: ',o.top_limit,' abajo: ',o.bottom_limit,' stage:',stage,' oleadas:',oleadas)
                o.vely = 0
                o.velx = -20
                o.lista = o.left_view
            if o.left_limit > o.rect.x:
                o.velx = 0
                o.vely = 20
                o.lista = o.bottom_view
            if o.bottom_limit < o.rect.y:
                o.vely = 0
                o.velx = 20
                o.lista = o.right_view
            if o.right_limit < o.rect.x:
                o.velx = 0
                o.vely = -20
                o.lista = o.top_view

        
        if oleadas == 0 and len(zombies) == 0:
            crear_portal1 = True

    #------------------------------------------------------------------------------------------------------------------CONTROL MODIFICADORES
        lista_colision = pygame.sprite.spritecollide(j1, modificadores, False)
        if len(lista_colision) > 0:
            for m in lista_colision:
                #Para el mod de salud
                if m.col == 0 and j1.salud < 100:
                    modificadores.remove(m)
                    j1.salud += 5
                if m.col == 1:
                    j1.poder = True
                    modificadores.remove(m)
                    mod_arma = 2
                    alcance_bala = 500
                    velmod = 10
                #Para el de el arma inicial
                if m.col == 2:
                    j1.arma = True
                    modificadores.remove(mod1)
                    mod_arma = 1
                if m.col == 3:
                    j1.resistencia = True
                    modificadores.remove(mod_res)
                    guillermo = 5 #Menos daño
        
        reloj.tick(12)
   
    #------------------------------------------------------------------------------------------------------------------LIMITES JUGADOR
        #print(f_posx)
        if len(zombies) == 0:
            moverse = True
            if j1.rect.right > lim_right:
                j1.rect.right = lim_right
                #print("fposx=",f_posx,"  limiteder=",limite_ventanaxder)
                if f_posx > limite_ventanaxder:
                    f_posx += f_vel
                    for b in bloques:
                        b.rect.x += f_vel
                    #Para que no se teletransporte
                    ls_col=pygame.sprite.spritecollide(j1, j1.bloques, False)
                    if len(ls_col) > 0:
                        for b in ls_col:
                            if j1.rect.right > b.rect.left:
                                j1.rect.right = b.rect.left
                                j1.velx = 0
                                j1.rect.y+= f_vel
                    for m in modificadores:
                        m.rect.x += f_vel
                    for g in generadores:
                        g.rect.x += f_vel
                    for g in generadores_ojos:
                        g.rect.x += f_vel
                    for p in portales:
                        p.rect.x += f_vel
                    for f in fantasmas:
                        f.rect.x += f_vel
                    for g in generadores_esqueletos:
                        g.rect.x += f_vel
                    for b in balas_esqueletos:
                        b.rect.x += f_vel
                    for o in ojos:
                        o.rect.x += f_vel
                    pos_portal1[0] += f_vel
                    pos_portal2[0] += f_vel
                    pos_portal3[0] += f_vel
                    limite_fantasmas_hor += f_vel
                    limite_bala_der += f_vel
                    limite_bala_izq += f_vel
                    o.right_limit += f_vel
                    o.left_limit += f_vel
            if j1.rect.left < lim_left:
                j1.rect.left = lim_left
                #Recordar que la posicion es negativa// EX: mirar la pos inicial del fondo
                #print("fposx=",f_posx,"  limiteiz=",limite_ventanaxizq)
                if f_posx < limite_ventanaxizq:
                    f_posx += -1*f_vel
                    for b in bloques:
                        b.rect.x += -1*f_vel
                    #Para que no se teletransporte
                    ls_col=pygame.sprite.spritecollide(j1, j1.bloques, False)
                    if len(ls_col) > 0:
                        for b in ls_col:
                            if j1.rect.left < b.rect.right:
                                j1.rect.left = b.rect.right
                                j1.velx = 0
                                j1.rect.y+= -1*f_vel
                    for m in modificadores:
                        m.rect.x += -1*f_vel
                    for g in generadores:
                        g.rect.x += -1*f_vel
                    for g in generadores_ojos:
                        g.rect.x += -1*f_vel
                    for p in portales:
                        p.rect.x += -1*f_vel
                    for f in fantasmas:
                        f.rect.x += -1*f_vel
                    for g in generadores_esqueletos:
                        g.rect.x += -1*f_vel
                    for b in balas_esqueletos:
                        b.rect.x += -1*f_vel
                    for o in ojos:
                        o.rect.x += -1*f_vel
                    pos_portal1[0] += -1*f_vel
                    pos_portal2[0] += -1*f_vel
                    pos_portal3[0] += -1*f_vel
                    limite_fantasmas_hor += -1*f_vel
                    limite_bala_izq += -1*f_vel
                    limite_bala_der += -1*f_vel
                    o.right_limit += -1*f_vel
                    o.left_limit += -1*f_vel
            if j1.rect.top < lim_top:
                j1.rect.top = lim_top
                #print("fposy=",f_posy,"  limiteiz=",limite_ventanayarriba)
                if f_posy < limite_ventanayarriba:
                    f_posy += -1*f_vel
                    for b in bloques:
                        b.rect.y += -1*f_vel
                    #Para que no se teletransporte
                    ls_col=pygame.sprite.spritecollide(j1, j1.bloques, False)
                    if len(ls_col) > 0:
                        for b in ls_col:
                            if j1.rect.top < b.rect.bottom:
                                j1.rect.top = b.rect.bottom
                                j1.vely = 0
                                j1.rect.y+= -1*f_vel
                    for m in modificadores:
                        m.rect.y += -1*f_vel
                    for g in generadores:
                        g.rect.y += -1*f_vel
                    for g in generadores_ojos:
                        g.rect.y += -1*f_vel
                    for p in portales:
                        p.rect.y += -1*f_vel
                    for f in fantasmas:
                        f.rect.y += -1*f_vel
                    for g in generadores_esqueletos:
                        g.rect.y += -1*f_vel
                    for b in balas_esqueletos:
                        b.rect.y += -1*f_vel
                    for o in ojos:
                        o.rect.y += -1*f_vel
                    pos_portal1[1] += -1*f_vel
                    pos_portal2[1] += -1*f_vel
                    pos_portal3[1] += -1*f_vel
                    limite_fantasmas_ver += -1*f_vel
                    limite_bala_arriba += -1*f_vel
                    limite_bala_abajo += -1*f_vel
                    o.top_limit += -1*f_vel
                    o.bottom_limit += -1*f_vel
            if j1.rect.bottom > lim_bottom:
                j1.rect.bottom = lim_bottom
                #print("fposy=",f_posy,"  limiteiz=",limite_ventanayabajo)
                if f_posy > limite_ventanayabajo:
                    f_posy += f_vel
                    for b in bloques:
                        b.rect.y += f_vel
                    #Para que no se teletransporte
                    ls_col=pygame.sprite.spritecollide(j1, j1.bloques, False)
                    if len(ls_col) > 0:
                        for b in ls_col:
                            if j1.rect.bottom > b.rect.top:
                                j1.rect.bottom = b.rect.top
                                j1.vely = 0
                                j1.rect.y+= f_vel
                    for m in modificadores:
                        m.rect.y += f_vel
                    for g in generadores:
                        g.rect.y += f_vel
                    for g in generadores_ojos:
                        g.rect.y += f_vel
                    for p in portales:
                        p.rect.y += f_vel
                    for f in fantasmas:
                        f.rect.y += f_vel
                    for g in generadores_esqueletos:
                        g.rect.y += f_vel
                    for b in balas_esqueletos:
                        b.rect.y += f_vel
                    for o in ojos:
                        o.rect.y += f_vel
                    pos_portal1[1] += f_vel
                    pos_portal2[1] += f_vel
                    pos_portal3[1] += f_vel
                    limite_fantasmas_ver += f_vel
                    limite_bala_abajo += f_vel
                    limite_bala_arriba += f_vel
                    o.top_limit += f_vel
                    o.bottom_limit += f_vel
        else:
            moverse = False

    #------------------------------------------------------------------------------------------------------------------LIMITES ZOMBIES
        #Control ventana
        for i in zombies:
            if i.rect.left < lim_left:
                if i.velx < 0:
                    i.velx = i.velx*(-1)
                    i.fil = 2
            if i.rect.right > lim_right:
                if i.velx > 0:
                    i.velx = i.velx*(-1)
                    i.fil = 1

    #------------------------------------------------------------------------------------------------------------------ATAQUE ZOMBIES
        for z in zombies:  
            lista_colision = pygame.sprite.spritecollide(z, jugadores, False)
            if len(lista_colision) > 0:
                if z.rect.bottom > j1.liminf and z.rect.bottom < j1.limsup:
                    j1.salud -= guillermo #Guillermo es lo que le baja de salud
                    z.velx = -1*z.velx
                    if z.fil == 1:
                        z.fil = 2
                        z.rect.x += 20
                    else:
                        z.fil = 1
                        z.rect.x -= 20
            ls_col = pygame.sprite.spritecollide(z,balas, True)
            if len(ls_col) > 0:
                z.salud -= 50
                if z.salud == 0:
                    dado = random.randrange(100)
                    if dado > 70:
                        m = modificador([z.rect.x,z.rect.y],matrizmod,0)
                        modificadores.add(m)
                    zombies.remove(z)
    
    #------------------------------------------------------------------------------------------------------------------CONTROL PORTALES
        if crear_portal1 == True and auxiliar_portal1 == 1:
            port1 = portal(pos_portal1,lista_portal)
            portales.add(port1)
            auxiliar_portal1 = 0
            entra_por1 = True
            print("portal creado")

        if crear_portal2:
            port2 = portal(pos_portal2,lista_portal)
            portales.add(port2)
            entra_por2 = True
            crear_portal2 = False
            auxiliar_portal2 = 0
            print("portal creado")

        if crear_portal3:
            port3 = portal(pos_portal3,lista_portal)
            portales.add(port3)
            entra_por3 = True
            crear_portal3 = False
            auxiliar_portal3 = 0
            print("portal creado")
        
        if entra_por1:
            Paso_s1_s2 = pygame.sprite.spritecollide(port1, jugadores, False)
            if len(Paso_s1_s2) > 0:
                portales.remove(port1)
                entra = False
                stage = 1.5
                j1.vely = 0
                j1.fil = 3
                j1.velx = 20
                aceptar_tecla = False
            if f_posx < (-1*(60*32)):
                aceptar_tecla = True
                j1.velx = 0
                entra = False #Me deja entrar a los stages
                stage = 2
                entra_por1 = False

        if entra_por2:
            Paso_s2_s3 = pygame.sprite.spritecollide(port2, jugadores, False)
            if len(Paso_s2_s3) > 0:
                portales.remove(port2)
                entra = False
                stage = 1.5
                j1.velx = 0
                j1.fil = 0
                j1.vely = 20
                aceptar_tecla = False
            if f_posy < (-1760):
                aceptar_tecla = True
                j1.vely = 0
                entra = False #Me deja entrar a los stages
                stage = 3
                entra_por2 = False
        #print('f_posx=',f_posx,'  f_posy =',f_posy)

        if entra_por3:
            Paso_s3_s4 = pygame.sprite.spritecollide(port3, jugadores, False)
            if len(Paso_s3_s4) > 0:
                portales.remove(port3)
                entra = False
                stage = 1.5
                j1.vely = 0
                j1.fil = 2
                j1.velx = -20
                aceptar_tecla = False
            if f_posx > -710:
                print('a\na\na\na\na\na\na\na\na')
                aceptar_tecla = True
                j1.velx = 0
                entra = False #Me deja entrar a los stages
                stage = 4
                entra_por3 = False
        
    #------------------------------------------------------------------------------------------------------------------CONTROL BALAS
        for i in balas:
            #El alcance es el que define cuando muere la bala
            if i.boton == 1: #la variable boton es para saber pa donde disparar
                if i.rect.x > j1.rect.x + alcance_bala:
                    balas.remove(i)
            if i.boton == 2:
                if i.rect.x < j1.rect.x - alcance_bala:
                    balas.remove(i)
            if i.boton == 3:
                if i.rect.y < j1.rect.y - alcance_bala:
                    balas.remove(i)
            if i.boton == 4:
                if i.rect.y > j1.rect.y + alcance_bala:
                    balas.remove(i)

    #------------------------------------------------------------------------------------------------------------------CONTROL GEN OJOS
        if len(generadores_ojos) == 1 and auxiliar_portal2 == 1:
            crear_portal2 = True
            
        
        if len(fantasmas) > 0 and stage == 1:
            for f in fantasmas:
                fantasmas.remove(f)

        
        for g in generadores_ojos:
            if g.col == 2 and g.temp < 0:
                f = fantasma([g.rect.x,g.rect.y], fantiz, fander)
                if g.lista == lista_ojohor:
                    f.velx = -7
                else:
                    f.vely = -7
                fantasmas.add(f)
                g.temp = random.randrange(30,60)
            ls_col = pygame.sprite.spritecollide(g,jugadores, False)
            if len(ls_col) > 0:
                if j1.resistencia:
                    j1.salud -= 15
                else:
                    j1.salud -= 25
                if g.lista == lista_ojohor:
                    j1.rect.x -= 550
                else:
                    j1.rect.y -= 300
            ls_col = pygame.sprite.spritecollide(g,balas, True)
            if len(ls_col) > 0:
                if g.salud < 1:
                    m = modificador(g.rect.center,matrizmod,0)
                    modificadores.add(m)
                    generadores_ojos.remove(g)
                g.salud -= 10
        
        for f in fantasmas:
            ls_col = pygame.sprite.spritecollide(f,jugadores, False)
            if len(ls_col) > 0:
                if j1.resistencia:
                    j1.salud -= 5
                else:
                    j1.salud -= 10
                fantasmas.remove(f)
            if mod_arma == 2: #unica forma de que el fantasma muera
                ls_col = pygame.sprite.spritecollide(f,balas, True)
                if len(ls_col) > 0:
                    fantasmas.remove(f)
            if f.rect.x < limite_fantasmas_hor or f.rect.y < limite_fantasmas_ver:
                fantasmas.remove(f)

    #------------------------------------------------------------------------------------------------------------------CONTROL GEN ESQUELETOS
        if len(generadores_esqueletos) == 0 and auxiliar_portal3 == 1:
            crear_portal3 = True
        
        for g in generadores_esqueletos:
            if g.temp < 0:
                pos = g.rect.midright
                b = balaesqueleto([pos[0]-(32*2),pos[1]-(32)],balader)
                b.velx = 10
                balas_esqueletos.add(b)
                pos = g.rect.midleft
                b = balaesqueleto([pos[0]-(32*2),pos[1]],balaiz)
                b.velx = -10
                balas_esqueletos.add(b)
                pos = g.rect.midtop
                b = balaesqueleto([pos[0]-(32),pos[1]],balaarriba)
                b.vely = -10
                balas_esqueletos.add(b)
                pos = g.rect.midbottom
                b = balaesqueleto([pos[0]-(32),pos[1]-(32*3)],balabajo)
                b.vely = 10
                balas_esqueletos.add(b)
                g.temp = random.randrange(30,60)
            ls_col = pygame.sprite.spritecollide(g,jugadores, False)
            if len(ls_col) > 0:
                if j1.resistencia:
                    j1.salud -= 15
                else:
                    j1.salud -= 25
                if g.rect.right > j1.rect.left:
                    j1.rect.x += 100
                elif g.rect.left < j1.rect.right:
                    j1.rect.x -= 100
                elif g.rect.bottom > j1.rect.top:
                    j1.rect.y += 100
                elif g.rect.top < j1.rect.bottom:
                    j1.rect.y -= 100
            ls_col = pygame.sprite.spritecollide(g,balas, True)
            if len(ls_col) > 0:
                if g.salud < 1:
                    m = modificador(g.rect.center,matrizmod,0)
                    modificadores.add(m)
                    generadores_esqueletos.remove(g)
                g.salud -= 10
        
        for b in balas_esqueletos:
            ls_col = pygame.sprite.spritecollide(b,jugadores, False)
            if len(ls_col) > 0:
                if j1.resistencia:
                    j1.salud -= 10
                else:
                    j1.salud -= 15
                balas_esqueletos.remove(b)
            if b.rect.left < limite_bala_izq or b.rect.right > limite_bala_der or b.rect.top < limite_bala_arriba or b.rect.bottom >limite_bala_abajo:
                balas_esqueletos.remove(b)

    #------------------------------------------------------------------------------------------------------------------CONTROL VIDA JUGADOR

        if j1.salud < 1:
            s1=sangre([j1.rect.x,j1.rect.y],lista_sangre)
            sangres.add(s1)
            j1.salud = 0
            j1.kill()
            mostrar_sangre = True

    #------------------------------------------------------------------------------------------------------------------CONTROL OBJETOS
        jugadores.update()
        balas.update()
        generadores.update()
        zombies.update()
        sangres.update()
        portales.update()
        modificadores.update()
        generadores_ojos.update()
        fantasmas.update()
        generadores_esqueletos.update()
        balas_esqueletos.update()
        ojos.update()
        pantalla.fill(VERDE)
        pantalla.blit(fondo, [f_posx,f_posy])
    
    #------------------------------------------------------------------------------------------------------------------DIBUJAR OBJETOS
        #bloques.draw(pantalla)
        generadores.draw(pantalla)
        balas.draw(pantalla)
        modificadores.draw(pantalla)
        zombies.draw(pantalla)
        jugadores.draw(pantalla)
        fantasmas.draw(pantalla)
        generadores_ojos.draw(pantalla)
        portales.draw(pantalla)
        balas_esqueletos.draw(pantalla)
        generadores_esqueletos.draw(pantalla)
        ojos.draw(pantalla)
        
        #Perspectiva para que no pasen por encima de los otros
        ls_col = pygame.sprite.spritecollide(j1,zombies,False)
        for z in ls_col:            
            if j1.rect.bottom > z.rect.bottom:
                zombies.draw(pantalla)
                jugadores.draw(pantalla)
            else:
                jugadores.draw(pantalla)
                zombies.draw(pantalla)
        if mostrar_sangre:
            sangres.draw(pantalla)

    #------------------------------------------------------------------------------------------------------------------MENSAJES
        #Salud
        pantalla.blit(linea, [0,0])
        info = "SALUD: " + str(j1.salud)
        color_salud = VERDE_S
        if j1.salud <= 60:
            color_salud = NARANJA
        if j1.salud <= 40:
            color_salud = ROJO
        txt_info = Fuente.render(info, True, color_salud)
        pantalla.blit(txt_info, [50,60])
        #Posiones activas
        info = "POSIONES ACTIVAS: "
        color_posiones = NARANJA
        txt_info = Fuente.render(info, True, color_posiones)
        pantalla.blit(txt_info, [50,20])
        if j1.arma:
            pantalla.blit(matrizmod[2], [540,0])
        else:
            pantalla.blit(lista_mod[2], [540,0])
        if j1.poder:
            pantalla.blit(matrizmod[1], [580,0])
        else:
            pantalla.blit(lista_mod[1], [580,0])
        if j1.resistencia:
            pantalla.blit(matrizmod[3], [620,0])
        else:
            pantalla.blit(lista_mod[3], [620,0])
   
    #------------------------------------------------------------------------------------------------------------------MENSAJE FIN DEL JUEGO

        # if len(rivales) == 0:
        #     if oleada == 2:
        #         fin_juego = True
        #         ubicacion_mensaje = [300,300]
        #         texto = "FIN DEL JUEGO: ERES EL GANADOR =)"
        #     else:
        #         rivales = Crear_Oleada(8)
        #         oleada += 1
                
        if len(jugadores) == 0:
            #fin_juego = True
            #pantalla.fill(NEGRO)
            ubicacion_mensaje = [250,350]
            texto = "FIN DEL JUEGO: ERES EL PERDEDOR =("
            img_texto = Fuente.render(texto,True, BLANCO)
            pantalla.blit(img_texto, ubicacion_mensaje)
    
        pygame.display.flip()

    #------------------------------------------------------------------------------------------------------------------FIN
    pygame.quit()
    print('Fin del programa')
