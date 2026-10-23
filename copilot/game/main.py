import math
import random
import sys

import pygame

# Dimensiones de la ventana y ritmo de actualización.
ANCHO = 800
ALTO = 600
FPS = 60

# Ajustá estos valores para cambiar la dificultad y la velocidad del juego.
VELOCIDAD_NAVE = 420
INTERVALO_METEORITOS_INICIAL = 0.9
INTERVALO_METEORITOS_MINIMO = 0.22
AUMENTO_DIFICULTAD_POR_SEGUNDO = 0.018
VELOCIDAD_METEORITO_MINIMA = 150
VELOCIDAD_METEORITO_MAXIMA = 270
PROBABILIDAD_METEORITO_RAPIDO = 0.15
MULTIPLICADOR_METEORITO_RAPIDO = 1.7

COLOR_FONDO = (7, 10, 30)
COLOR_TEXTO = (240, 245, 255)


class Nave:
    """Nave del jugador, dibujada con figuras geométricas."""

    def __init__(self):
        self.ancho = 48
        self.alto = 54
        self.x = ANCHO / 2
        self.y = ALTO - 75
        self.velocidad = VELOCIDAD_NAVE
        self.rectangulo = pygame.Rect(0, 0, self.ancho, self.alto)
        self.rectangulo.center = (round(self.x), round(self.y))

    def actualizar(self, teclas, delta_tiempo):
        """Mueve la nave con las flechas o con A y D."""
        direccion = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            direccion -= 1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            direccion += 1

        self.x += direccion * self.velocidad * delta_tiempo
        mitad_ancho = self.ancho / 2
        self.x = max(mitad_ancho, min(ANCHO - mitad_ancho, self.x))
        self.rectangulo.center = (round(self.x), round(self.y))

    def dibujar(self, pantalla):
        """Dibuja el cuerpo, las alas y la cabina de la nave."""
        centro_x = self.rectangulo.centerx
        centro_y = self.rectangulo.centery
        puntos_cuerpo = [
            (centro_x, centro_y - self.alto // 2),
            (centro_x + self.ancho // 2, centro_y + self.alto // 2),
            (centro_x, centro_y + self.alto // 3),
            (centro_x - self.ancho // 2, centro_y + self.alto // 2),
        ]
        pygame.draw.polygon(pantalla, (90, 210, 255), puntos_cuerpo)
        pygame.draw.polygon(pantalla, (220, 250, 255), puntos_cuerpo, 2)
        pygame.draw.ellipse(
            pantalla,
            (255, 190, 90),
            (centro_x - 5, centro_y + 12, 10, 15),
        )
        pygame.draw.ellipse(
            pantalla,
            (190, 240, 255),
            (centro_x - 6, centro_y - 8, 12, 17),
        )


class Meteorito:
    """Meteorito de forma irregular que cae hacia la parte inferior."""

    def __init__(self, velocidad_extra):
        self.radio = random.randint(17, 34)
        self.x = random.randint(self.radio, ANCHO - self.radio)
        self.y = -self.radio
        self.velocidad = random.uniform(VELOCIDAD_METEORITO_MINIMA, VELOCIDAD_METEORITO_MAXIMA)
        self.velocidad += velocidad_extra
        # De vez en cuando aparece uno más rápido y de color más claro.
        self.es_rapido = random.random() < PROBABILIDAD_METEORITO_RAPIDO
        if self.es_rapido:
            self.velocidad *= MULTIPLICADOR_METEORITO_RAPIDO
        self.angulo = random.uniform(0, math.tau)
        self.giro = random.uniform(-1.2, 1.2)
        self.color = (
            (245, 45, 190)
            if self.es_rapido
            else random.choice([(137, 91, 83), (158, 105, 91), (120, 102, 112)])
        )
        self.puntos = []
        cantidad_puntas = random.randint(8, 11)
        for indice in range(cantidad_puntas):
            angulo = math.tau * indice / cantidad_puntas
            distancia = self.radio * random.uniform(0.78, 1.12)
            self.puntos.append((math.cos(angulo) * distancia, math.sin(angulo) * distancia))

    def actualizar(self, delta_tiempo):
        self.y += self.velocidad * delta_tiempo
        self.angulo += self.giro * delta_tiempo

    def dibujar(self, pantalla):
        puntos_rotados = []
        for punto_x, punto_y in self.puntos:
            x_rotado = punto_x * math.cos(self.angulo) - punto_y * math.sin(self.angulo)
            y_rotado = punto_x * math.sin(self.angulo) + punto_y * math.cos(self.angulo)
            puntos_rotados.append((round(self.x + x_rotado), round(self.y + y_rotado)))

        pygame.draw.polygon(pantalla, self.color, puntos_rotados)
        color_borde = (255, 235, 90) if self.es_rapido else (205, 160, 145)
        pygame.draw.polygon(pantalla, color_borde, puntos_rotados, 2)
        # Cráteres pequeños para dar textura sin usar imágenes.
        pygame.draw.circle(
            pantalla,
            (94, 72, 76),
            (round(self.x - self.radio * 0.25), round(self.y - self.radio * 0.1)),
            max(3, self.radio // 6),
        )
        pygame.draw.circle(
            pantalla,
            (94, 72, 76),
            (round(self.x + self.radio * 0.3), round(self.y + self.radio * 0.25)),
            max(2, self.radio // 8),
        )

    def choca_con(self, nave):
        """Comprueba la colisión usando una distancia entre centros."""
        distancia = math.hypot(self.x - nave.x, self.y - nave.y)
        return distancia < self.radio + 19


class Estrella:
    """Estrella de fondo que se desplaza lentamente hacia abajo."""

    def __init__(self, aleatoria=True):
        self.x = random.randrange(ANCHO)
        self.y = random.randrange(ALTO) if aleatoria else random.randrange(-ALTO, 0)
        self.velocidad = random.uniform(18, 75)
        self.radio = random.choice((1, 1, 2))
        self.brillo = random.randint(115, 235)

    def actualizar(self, delta_tiempo):
        self.y += self.velocidad * delta_tiempo
        if self.y > ALTO:
            self.y = 0
            self.x = random.randrange(ANCHO)

    def dibujar(self, pantalla):
        pygame.draw.circle(
            pantalla,
            (self.brillo, self.brillo, min(255, self.brillo + 20)),
            (self.x, round(self.y)),
            self.radio,
        )


def dibujar_texto(pantalla, fuente, texto, color, centro):
    """Dibuja texto centrado en la posición indicada."""
    superficie = fuente.render(texto, True, color)
    pantalla.blit(superficie, superficie.get_rect(center=centro))


def crear_partida():
    """Crea los objetos y valores iniciales para una partida nueva."""
    return {
        "nave": Nave(),
        "meteoritos": [],
        "tiempo": 0.0,
        "tiempo_hasta_meteorito": 0.0,
        "terminada": False,
    }


def ejecutar_juego():
    pygame.init()
    pygame.display.set_caption("Esquiva Meteoritos")
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 36)
    fuente_grande = pygame.font.Font(None, 76)
    fuente_chica = pygame.font.Font(None, 28)

    estrellas = [Estrella() for _ in range(100)]
    partida = crear_partida()
    ejecutando = True

    while ejecutando:
        # Limitar FPS y convertir milisegundos a segundos para el delta time.
        delta_tiempo = min(reloj.tick(FPS) / 1000.0, 0.05)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_r and partida["terminada"]:
                    partida = crear_partida()

        teclas = pygame.key.get_pressed()
        for estrella in estrellas:
            estrella.actualizar(delta_tiempo)

        if not partida["terminada"]:
            partida["tiempo"] += delta_tiempo
            nivel_dificultad = partida["tiempo"] * AUMENTO_DIFICULTAD_POR_SEGUNDO
            intervalo = max(
                INTERVALO_METEORITOS_MINIMO,
                INTERVALO_METEORITOS_INICIAL / (1 + nivel_dificultad),
            )
            velocidad_extra = min(240, partida["tiempo"] * 2.5)

            partida["tiempo_hasta_meteorito"] -= delta_tiempo
            if partida["tiempo_hasta_meteorito"] <= 0:
                partida["meteoritos"].append(Meteorito(velocidad_extra))
                partida["tiempo_hasta_meteorito"] = intervalo

            partida["nave"].actualizar(teclas, delta_tiempo)
            for meteorito in partida["meteoritos"]:
                meteorito.actualizar(delta_tiempo)
                if meteorito.choca_con(partida["nave"]):
                    partida["terminada"] = True

            # Quitar meteoritos que ya salieron de la ventana.
            partida["meteoritos"] = [
                meteorito
                for meteorito in partida["meteoritos"]
                if meteorito.y - meteorito.radio < ALTO
            ]

        pantalla.fill(COLOR_FONDO)
        for estrella in estrellas:
            estrella.dibujar(pantalla)
        for meteorito in partida["meteoritos"]:
            meteorito.dibujar(pantalla)
        partida["nave"].dibujar(pantalla)

        puntaje = int(partida["tiempo"])
        texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, COLOR_TEXTO)
        pantalla.blit(texto_puntaje, (20, 18))

        if partida["terminada"]:
            # Una capa oscura resalta el mensaje final sin ocultar el juego.
            capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            capa.fill((0, 0, 0, 175))
            pantalla.blit(capa, (0, 0))
            dibujar_texto(pantalla, fuente_grande, "GAME OVER", (255, 105, 105), (ANCHO // 2, 235))
            dibujar_texto(
                pantalla,
                fuente,
                f"Puntaje final: {puntaje}",
                COLOR_TEXTO,
                (ANCHO // 2, 300),
            )
            dibujar_texto(
                pantalla,
                fuente_chica,
                "Presioná R para volver a jugar",
                COLOR_TEXTO,
                (ANCHO // 2, 365),
            )
            dibujar_texto(
                pantalla,
                fuente_chica,
                "Presioná Escape para salir",
                COLOR_TEXTO,
                (ANCHO // 2, 400),
            )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    ejecutar_juego()
