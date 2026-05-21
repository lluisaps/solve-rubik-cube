# Solucionador de Cubo Mágico

**PROJETO EM GRUPO – Aplicação Prática de Algoritmos em Python (P2) - UNISAGRADO**

### Integrantes do Grupo

- Amanda Santos
- Luísa Prado
- Eduardo Pontes
- Willian Miranda

---

O programa resolve um Cubo Mágico embaralhado e mostra a solução passo a passo
com uma interface gráfica feita em **Tkinter**.

---

## Como instalar e executar

**1. Instale a dependência:**
```bash
pip install RubikTwoPhase
```

**2. Execute o programa:**
```bash
python main.py
```
---

## Como usar

| Botão / Ação       | O que faz                                         |
|--------------------|---------------------------------------------------|
| **Embaralhar**     | Aplica 20 movimentos aleatórios no cubo           |
| **Resolver**       | Calcula e anima a sequência de solução            |
| **Resetar**        | Volta o cubo ao estado inicial (resolvido)        |
| Controle deslizante| Ajusta a velocidade da animação (ms por movimento)|

---

## Conceitos de algoritmos aplicados

### Entrada e saída
- **Entrada:** cliques nos botões (Embaralhar, Resolver, Resetar) e controle de velocidade
- **Saída:** cubo desenhado no canvas, lista de movimentos e mensagem de status

### Estruturas de repetição
- `for i in range(9)` — percorre as 9 células de cada face para desenhá-las (`main.py`)
- `for _ in range(moves)` — repete o embaralhamento por N movimentos (`cube.py`)
- `for _ in range(turns)` — repete giros da mesma face (ex: move duplo) (`cube.py`)
- `for face in FACES` — verifica se todas as faces estão resolvidas (`cube.py`)

### Estruturas de decisão
- `if / elif / else` — escolhe qual face está sendo girada (`cube.py`, método `_turn`)
- `if indice >= len(movimentos)` — detecta o fim da animação (`main.py`)
- `if self.cubo.is_solved()` — verifica se o cubo já está resolvido (`main.py`)

### Vetores e matrizes
- O cubo é armazenado como um **dicionário de 6 listas** (6 faces × 9 stickers),
  formando uma **matriz 6 × 9** (`cube.py`, atributo `state`)
- Cada lista de 9 elementos representa uma face como **vetor** de stickers
- O índice de cada sticker é calculado com `linha = i // 3` e `coluna = i % 3`
  (divisão inteira e resto), mapeando o vetor em uma grade 3 × 3

---

## Estrutura do projeto

```
main.py          — interface gráfica (Tkinter) e animação
cube.py          — modelo do cubo: estado, movimentos e embaralhamento
requirements.txt — dependência externa (solver)
```

---

## Explicação do funcionamento

1. O cubo é representado por 6 faces (`U`, `R`, `F`, `D`, `L`, `B`), cada uma
   com uma lista de 9 stickers (letras que indicam a cor original).
2. Ao embaralhar, o programa escolhe faces aleatoriamente e aplica giros,
   guardando a sequência em uma lista.
3. Ao resolver, o estado atual do cubo é convertido numa string de 54 caracteres
   e enviado à biblioteca **RubikTwoPhase**, que retorna a sequência mínima de movimentos.
4. A animação executa cada movimento com um atraso configurável usando `janela.after()`,
   redesenhando o cubo a cada passo.
