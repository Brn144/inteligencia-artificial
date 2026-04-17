import numpy as np
import time
import tracemalloc
import heapq
import random
from collections import deque


def busca_largura(jogo, tab_inicial): # Busca em largura
    fila = deque([(tab_inicial, [])])
    visitados = {jogo.tabuleiro_para_tupla(tab_inicial)}
   
    while fila: 
        tab, acoes = fila.popleft()
        if jogo.eh_objetivo(tab): return acoes
       
        for l in range(jogo.n):
            for c in range(jogo.n):
                novo_tab = jogo.clicar(tab, l, c)
                estado = jogo.tabuleiro_para_tupla(novo_tab)
                if estado not in visitados:
                    visitados.add(estado)
                    fila.append((novo_tab, acoes + [(l, c)]))
    return None
 
def busca_profundidade(jogo, tab_inicial, prof_max=20): # Busca em profundidade
    pilha = [(tab_inicial, [], 0)]
    visitados = {jogo.tabuleiro_para_tupla(tab_inicial)}
   
    while pilha:
        tab, acoes, prof = pilha.pop()
        if jogo.eh_objetivo(tab): return acoes
        if prof >= prof_max: continue
       
        for l in range(jogo.n):
            for c in range(jogo.n):
                novo_tab = jogo.clicar(tab, l, c)
                estado = jogo.tabuleiro_para_tupla(novo_tab)
                if estado not in visitados:
                    visitados.add(estado)
                    pilha.append((novo_tab, acoes + [(l, c)], prof + 1))
    return None
 
def busca_gulosa(jogo, tab_inicial): # Busca gulosa
    heap = [(jogo.heuristica(tab_inicial), 0, tab_inicial, [])]
    visitados = {jogo.tabuleiro_para_tupla(tab_inicial)}
    contador = 0
   
    while heap:
        _, _, tab, acoes = heapq.heappop(heap)
        if jogo.eh_objetivo(tab): return acoes
       
        for l in range(jogo.n):
            for c in range(jogo.n):
                novo_tab = jogo.clicar(tab, l, c)
                estado = jogo.tabuleiro_para_tupla(novo_tab)
                if estado not in visitados:
                    visitados.add(estado)
                    contador += 1
                    heapq.heappush(heap, (jogo.heuristica(novo_tab), contador, novo_tab, acoes + [(l, c)]))
    return None
 
def busca_a_estrela(jogo, tab_inicial): # Busca A*
    contador = 0
    heap = [(jogo.heuristica(tab_inicial), contador, 0, tab_inicial, [])]
    melhor_g = {jogo.tabuleiro_para_tupla(tab_inicial): 0}
   
    while heap:
        _, _, g, tab, acoes = heapq.heappop(heap)
        if jogo.eh_objetivo(tab): return acoes
        if g > melhor_g.get(jogo.tabuleiro_para_tupla(tab), float('inf')): continue
       
        for l in range(jogo.n):
            for c in range(jogo.n):
                novo_tab = jogo.clicar(tab, l, c)
                novo_g = g + 1
                estado = jogo.tabuleiro_para_tupla(novo_tab)
               
                if novo_g < melhor_g.get(estado, float('inf')):
                    melhor_g[estado] = novo_g
                    contador += 1
                    heapq.heappush(heap, (novo_g + jogo.heuristica(novo_tab), contador, novo_g, novo_tab, acoes + [(l, c)]))
    return None
 
def subida_encosta(jogo, tab_inicial, iteracoes_max=5000, reinicios=10): # Subida da encosta
    melhor_solucao = None
   
    for tentativa in range(reinicios):
        tab = tab_inicial.copy() if tentativa == 0 else jogo.gerar_tabuleiro_aleatorio()
        acoes = []
        h_atual = jogo.heuristica(tab)
       
        for _ in range(iteracoes_max):
            if jogo.eh_objetivo(tab): return acoes
           
            melhor_vizinho, melhor_h, melhor_acao = None, h_atual, None
            for l in range(jogo.n):
                for c in range(jogo.n):
                    novo_tab = jogo.clicar(tab, l, c)
                    h = jogo.heuristica(novo_tab)
                    if h < melhor_h:
                        melhor_h, melhor_vizinho, melhor_acao = h, novo_tab, (l, c)
           
            if melhor_vizinho is None: break
           
            tab, h_atual = melhor_vizinho, melhor_h
            acoes.append(melhor_acao)
           
        if melhor_solucao is None or h_atual < jogo.heuristica(tab_inicial):
            melhor_solucao = acoes if jogo.eh_objetivo(tab) else None
           
    return melhor_solucao
 
