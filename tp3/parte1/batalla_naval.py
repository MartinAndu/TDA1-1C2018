

class Estrategia:
    """ Clase base para las estrategias. """

    def siguiente_turno(self, tablero, lanzaderos, barcos):
        """
        Este método debe ejecutar un turno, basandose en los datos del tablero,
        lanzaderos y barcos actuales.

        Parametros:

        - tablero es un diccionario que tiene como clave el número de línea (o
          número de barco, que es lo mismo) y como valores una lista con las
          los números de daño de cada celda. Por ejemplo:

          {1: [10, 20, 30, 10]}

        - lanzaderos es el número de lanzaderos

        - barcos es un diccionario que tiene como claves números de barco, y
          como valores un diccionario con sus puntos de vida y su posición en el
          tablero. Por ejemplo:

          {1: {'vida': 50, 'posicion': 0}}

        Una estrategia de barcos debe devolver el número de barco a avanzar en
        el turno actual.

        Una estrategia de lanzaderos debe devolver una lista con los números de
        barcos a los que disparar (el tamaño de la lista debe ser igual a la
        cantidad de lanzaderos)
        """
        pass


class NaiveBarcos(Estrategia):

    def siguiente_turno(self, tablero, lanzaderos, barcos):
        """
        Estrategia naive que devuelve el primer barco con vida que encuentra
        """
        for i, barco in barcos.items():
            if barco['vida'] > 0:
                return i


class NaiveLanzaderos(Estrategia):

    def siguiente_turno(self, tablero, lanzaderos, barcos):
        """
        Estrategia naive que dispara todos los misiles al primer barco con vida
        que encuentra
        """
        for i, barco in barcos.items():
            if barco['vida'] > 0:
                return [i] * lanzaderos


class Juego:

    def __init__(self, tablero_file, lanzaderos, estrategia_barcos,
                 estrategia_lanzaderos):
        self.tablero_file = tablero_file
        self.tablero = {}
        self.lanzaderos = lanzaderos
        self.barcos = {}
        self.estrategia_barcos = estrategia_barcos
        self.estrategia_lanzaderos = estrategia_lanzaderos

    def parsear_tablero(self):
        with open(self.tablero_file) as f:
            for i, line in enumerate(f):
                splits = list(map(int, line.split()))
                self.barcos[i] = {
                    'posicion': 0,
                    'vida': splits[0]
                }
                self.tablero[i] = splits[1:]

    def cantidad_barcos_vivos(self):
        return len([x for x in self.barcos.values() if x['vida'] > 0])

    def mover_barco(self, barco):
        self.barcos[barco]['posicion'] += 1
        if self.barcos[barco]['posicion'] >= len(self.tablero[barco]):
            self.barcos[barco]['posicion'] = 0

    def disparar_misiles(self, misiles):
        for misil in misiles:
            barco = self.barcos[misil]
            danio = self.tablero[misil][barco['posicion']]
            self.barcos[misil]['vida'] -= danio

    def imprimir_turno(self, turno, puntos):
        print('Turno actual: {}, puntos acumulados: {}. Barcos disponibles:'
              .format(turno, puntos))
        for i, barco in self.barcos.items():
            if barco['vida'] > 0:
                pos = barco['posicion']
                print('Barco {}. Vida: {}, posición: {}, daño potencial: {}'
                      .format(i, barco['vida'], pos, self.tablero[i][pos]))
        print('-' * 40)

    def imprimir_misiles(self, misiles_disparados):
        mensajes = ['Lanzadero {} al barco {}'.format(i, k)
                    for i, k in enumerate(misiles_disparados)]
        print('Misiles lanzados: ' + ', '.join(mensajes))
        print('-' * 40)

    def imprimir_final(self, turno, puntos):
        print('Juego finalizado! Cantidad de turnos: {}. Puntos acumulados: {}'
              .format(turno, puntos))

    def jugar(self):
        self.parsear_tablero()
        args = (self.tablero, self.lanzaderos, self.barcos)

        turno = 0
        puntos = 0
        print('Inicio del juego!')
        self.imprimir_turno(turno, puntos)

        while True:
            turno += 1
            barco_a_mover = self.estrategia_barcos.siguiente_turno(*args)
            self.mover_barco(barco_a_mover)
            self.imprimir_turno(turno, puntos)

            misiles_disparados = self.estrategia_lanzaderos.siguiente_turno(*args)
            self.disparar_misiles(misiles_disparados)
            self.imprimir_misiles(misiles_disparados)

            barcos_vivos = self.cantidad_barcos_vivos()
            if barcos_vivos == 0:
                break

            puntos += barcos_vivos

        self.imprimir_final(turno, puntos)


if __name__ == '__main__':
    estrategia_barcos = NaiveBarcos()
    estrategia_lanzaderos = NaiveLanzaderos()
    Juego(tablero_file='tablero', lanzaderos=2,
          estrategia_barcos=estrategia_barcos,
          estrategia_lanzaderos=estrategia_lanzaderos).jugar()
