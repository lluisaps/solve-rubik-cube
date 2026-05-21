import random

FACES = ['U', 'R', 'F', 'D', 'L', 'B']

COLOR_BY_FACE = {
    'U': (1.0, 1.0, 1.0),  # branco
    'R': (1.0, 0.0, 0.0),  # vermelho
    'F': (0.0, 0.7, 0.0),  # verde
    'D': (1.0, 1.0, 0.0),  # amarelo
    'L': (1.0, 0.5, 0.0),  # laranja
    'B': (0.0, 0.3, 1.0),  # azul
}


def _girar_horario(face):
    
    return [face[6], face[3], face[0],
            face[7], face[4], face[1],
            face[8], face[5], face[2]]


class Cube:
    def __init__(self):
        self.state = {face: [face] * 9 for face in FACES}

    def to_solver_string(self):
        resultado = ''
        for face in ['U', 'R', 'F', 'D', 'L', 'B']:
            for sticker in self.state[face]:
                resultado += sticker
        return resultado

    def is_solved(self):
    #Retorna True se o cubo estiver completamente resolvido.
        for face in FACES:
            for sticker in self.state[face]:
                if sticker != face:   
                    return False
        return True

    def apply_move(self, move):
        # Movimentos possíveis
        #   R  -> giro simples (90 graus horário)
        #   R'  -> giro inverso (90 graus anti-horário)
        #   R2  -> 2 giros simples
        #   R1 / 'R3' -> equivalente a R / R'
        
        face = move[0]
        sufixo = move[1:] if len(move) > 1 else ''

        if sufixo == '2':
            repeticoes = 2
        elif sufixo == "'" or sufixo == '3':     
            repeticoes = 3
        else:                                   
            repeticoes = 1
        for _ in range(repeticoes):
            self._girar(face)

    def _girar(self, face):
        s = self.state

        s[face] = _girar_horario(s[face])

        if face == 'U':
            f, r, b, l = s['F'], s['R'], s['B'], s['L']
            f[0], f[1], f[2], r[0], r[1], r[2], b[0], b[1], b[2], l[0], l[1], l[2] = (
                r[0], r[1], r[2], b[0], b[1], b[2], l[0], l[1], l[2], f[0], f[1], f[2]
            )
        elif face == 'D':
            f, r, b, l = s['F'], s['R'], s['B'], s['L']
            f[6], f[7], f[8], r[6], r[7], r[8], b[6], b[7], b[8], l[6], l[7], l[8] = (
                l[6], l[7], l[8], f[6], f[7], f[8], r[6], r[7], r[8], b[6], b[7], b[8]
            )
        elif face == 'F':
            u, r, d, l = s['U'], s['R'], s['D'], s['L']
            salvo = (u[6], u[7], u[8])    
            u[6], u[7], u[8] = l[8], l[5], l[2]
            l[2], l[5], l[8] = d[0], d[1], d[2]
            d[0], d[1], d[2] = r[6], r[3], r[0]
            r[0], r[3], r[6] = salvo
        elif face == 'B':
            u, r, d, l = s['U'], s['R'], s['D'], s['L']
            salvo = (u[0], u[1], u[2])  
            u[0], u[1], u[2] = r[2], r[5], r[8]
            r[2], r[5], r[8] = d[8], d[7], d[6]
            d[6], d[7], d[8] = l[0], l[3], l[6]
            l[0], l[3], l[6] = salvo[2], salvo[1], salvo[0]
        elif face == 'R':
            u, f, d, b = s['U'], s['F'], s['D'], s['B']
            salvo = (u[2], u[5], u[8])  
            u[2], u[5], u[8] = f[2], f[5], f[8]
            f[2], f[5], f[8] = d[2], d[5], d[8]
            d[2], d[5], d[8] = b[6], b[3], b[0]
            b[0], b[3], b[6] = salvo[2], salvo[1], salvo[0]
        elif face == 'L':
            u, f, d, b = s['U'], s['F'], s['D'], s['B']
            salvo = (u[0], u[3], u[6])   
            u[0], u[3], u[6] = b[8], b[5], b[2]
            b[2], b[5], b[8] = d[6], d[3], d[0]
            d[0], d[3], d[6] = f[0], f[3], f[6]
            f[0], f[3], f[6] = salvo

    def scramble(self, moves=20, seed=None):
        rng = random.Random(seed)
        ultima_face = None
        sequencia = []

        for _ in range(moves):
            # Uma face dif da anterior
            face = rng.choice(FACES)
            while face == ultima_face:
                face = rng.choice(FACES)

            sufixo = rng.choice(['', "'", '2'])
            movimento = face + sufixo

            sequencia.append(movimento)
            self.apply_move(movimento)
            ultima_face = face

        return sequencia
