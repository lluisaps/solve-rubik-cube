import tkinter as tk
from tkinter import messagebox

from cube import Cube

CORES = {
    'U': '#ffffff',
    'R': '#ff2200',
    'F': '#00aa00',
    'D': '#ffdd00',
    'L': '#ff8800',
    'B': '#0044ff'
}

TAMANHO_CELULA = 56
MARGEM = 4

# Variáveis globais da interface
janela = None
canvas = None
lista = None
lbl_status = None
velocidade = None
btn_embaralhar = None
btn_resolver = None
btn_resetar = None
cubo = Cube()


def posicao_face(face):
    passo = TAMANHO_CELULA + MARGEM
    grade = {
        'U': (3, 0),
        'L': (0, 3),
        'F': (3, 3),
        'R': (6, 3),
        'B': (9, 3),
        'D': (3, 6),
    }
    col, lin = grade[face]
    return MARGEM + col * passo, MARGEM + lin * passo


def desenhar_cubo():
    canvas.delete('all')
    passo = TAMANHO_CELULA + MARGEM

    for face, stickers in cubo.state.items():
        x0, y0 = posicao_face(face)

        for i in range(9):
            linha = i // 3
            coluna = i % 3
            x = x0 + coluna * passo
            y = y0 + linha * passo
            cor = CORES[stickers[i]]
            canvas.create_rectangle(x, y, x + TAMANHO_CELULA, y + TAMANHO_CELULA,
                                    fill=cor, outline='#111111', width=2)

        centro_x = x0 + (3 * passo - MARGEM) // 2
        canvas.create_text(centro_x, y0 - 2, text=face,
                           fill='#aabbff', font=('Arial', 9, 'bold'), anchor='s')


def definir_botoes(ativo):
    if ativo:
        estado = tk.NORMAL
    else:
        estado = tk.DISABLED
    btn_embaralhar.config(state=estado)
    btn_resolver.config(state=estado)
    btn_resetar.config(state=estado)


def executar_passo(movimentos, titulo, indice):
    if indice >= len(movimentos):
        if cubo.is_solved():
            lbl_status.config(text="Resolvido!", fg='#55ff88')
        else:
            lbl_status.config(text="Pronto", fg='#88ccff')
        definir_botoes(True)
        return

    cubo.apply_move(movimentos[indice])
    desenhar_cubo()

    lista.selection_clear(0, tk.END)
    lista.selection_set(indice)
    lista.see(indice)
    lbl_status.config(text=f"{titulo}: {indice + 1}/{len(movimentos)}", fg='#ffdd88')

    janela.after(velocidade.get(), executar_passo, movimentos, titulo, indice + 1)


def animar_sequencia(movimentos, titulo):
    definir_botoes(False)
    lista.delete(0, tk.END)
    for i in range(len(movimentos)):
        lista.insert(tk.END, f"  {i + 1}. {movimentos[i]}")
    executar_passo(movimentos, titulo, 0)


def embaralhar():
    global cubo
    cubo = Cube()
    sequencia = cubo.scramble(moves=20)
    cubo = Cube()
    lbl_status.config(text="Embaralhando...", fg='#ffdd88')
    animar_sequencia(sequencia, "Embaralhando")


def resolver():
    if cubo.is_solved():
        lbl_status.config(text="Já está resolvido!", fg='#55ff88')
        return

    lbl_status.config(text="Calculando solução...", fg='#ffdd88')
    janela.update()

    try:
        import twophase.solver as solver
    except ImportError:
        messagebox.showerror("Erro", "Execute: pip install RubikTwoPhase")
        lbl_status.config(text="Erro de instalação", fg='#ff6666')
        return

    estado = cubo.to_solver_string()
    resultado = solver.solve(estado, 0, 5.0)

    if not resultado or 'error' in resultado.lower():
        lbl_status.config(text="Erro no solver", fg='#ff6666')
        return

    movimentos = []
    for t in resultado.split():
        if t and not t.startswith('('):
            movimentos.append(t)

    if not movimentos:
        lbl_status.config(text="Já está resolvido!", fg='#55ff88')
        return

    animar_sequencia(movimentos, "Resolvendo")


def resetar():
    global cubo
    cubo = Cube()
    lista.delete(0, tk.END)
    lbl_status.config(text="Resetado", fg='#88ccff')
    desenhar_cubo()


def criar_interface():
    global canvas, lista, lbl_status, velocidade
    global btn_embaralhar, btn_resolver, btn_resetar

    janela.title("Solucionador de Cubo Mágico")
    janela.resizable(False, False)
    janela.configure(bg='#1a1a2e')

    tk.Label(janela, text="Solucionador de Cubo Mágico",
             font=('Arial', 17, 'bold'), bg='#1a1a2e', fg='white').pack(pady=(12, 4))

    frame_central = tk.Frame(janela, bg='#1a1a2e')
    frame_central.pack(padx=14, pady=6)

    passo = TAMANHO_CELULA + MARGEM
    canvas = tk.Canvas(frame_central,
                       width=MARGEM + 12 * passo,
                       height=MARGEM + 9 * passo,
                       bg='#2d2d44', highlightthickness=0)
    canvas.pack(side=tk.LEFT, padx=(0, 12))

    frame_lado = tk.Frame(frame_central, bg='#1a1a2e')
    frame_lado.pack(side=tk.LEFT, fill=tk.Y)

    tk.Label(frame_lado, text="Sequência de movimentos",
             font=('Arial', 11, 'bold'), bg='#1a1a2e', fg='#aabbff').pack(anchor='w')

    frame_lista = tk.Frame(frame_lado, bg='#1a1a2e')
    frame_lista.pack(fill=tk.BOTH, expand=True)

    scroll = tk.Scrollbar(frame_lista)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    lista = tk.Listbox(frame_lista, yscrollcommand=scroll.set,
                       font=('Consolas', 12), bg='#16213e', fg='#dddddd',
                       selectbackground='#304d8a', activestyle='none',
                       width=13, height=18, bd=0)
    lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll.config(command=lista.yview)

    lbl_status = tk.Label(frame_lado, text="Pronto",
                          font=('Arial', 11), bg='#1a1a2e', fg='#88ccff', anchor='w')
    lbl_status.pack(fill=tk.X, pady=(6, 0))

    frame_botoes = tk.Frame(janela, bg='#1a1a2e')
    frame_botoes.pack(pady=8)

    btn_embaralhar = tk.Button(frame_botoes, text="Embaralhar",
                               font=('Arial', 12, 'bold'), width=12, relief=tk.FLAT,
                               cursor='hand2', pady=5, bg='#c0392b', fg='white',
                               command=embaralhar)
    btn_embaralhar.pack(side=tk.LEFT, padx=6)

    btn_resolver = tk.Button(frame_botoes, text="Resolver",
                             font=('Arial', 12, 'bold'), width=12, relief=tk.FLAT,
                             cursor='hand2', pady=5, bg='#1a5276', fg='white',
                             command=resolver)
    btn_resolver.pack(side=tk.LEFT, padx=6)

    btn_resetar = tk.Button(frame_botoes, text="Resetar",
                            font=('Arial', 12, 'bold'), width=12, relief=tk.FLAT,
                            cursor='hand2', pady=5, bg='#6c3483', fg='white',
                            command=resetar)
    btn_resetar.pack(side=tk.LEFT, padx=6)

    frame_vel = tk.Frame(janela, bg='#1a1a2e')
    frame_vel.pack(pady=(0, 12))

    tk.Label(frame_vel, text="Velocidade:", bg='#1a1a2e',
             fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 6))

    velocidade = tk.IntVar(value=250)
    tk.Scale(frame_vel, from_=50, to=700, orient=tk.HORIZONTAL,
             variable=velocidade, bg='#1a1a2e', fg='white',
             troughcolor='#304d8a', highlightthickness=0,
             length=180, label="ms entre movimentos").pack(side=tk.LEFT)


janela = tk.Tk()
criar_interface()
desenhar_cubo()
janela.mainloop()
