import numpy as np
import time
import tracemalloc
import heapq
import random
from collections import deque
 
from buscas import busca_largura, busca_profundidade, busca_gulosa, busca_a_estrela, subida_encosta
 
class JogoLuzes:
    def __init__(self, n, estado=None):
        self.n = n
        self.tabuleiro = np.zeros((n, n), dtype=int) if estado is None else np.array(estado).reshape(n, n) # Matriz (NxN) preenchida com "0"
 
    def clicar(self, tabuleiro, linha, coluna): # Função inverte o bit (0 vira 1 e 1 vira 0)
        novo_tabuleiro = tabuleiro.copy() #cria uma cópia do tabuleiro e joga para essa variavel
        for l, c in [(linha, coluna), (linha-1, coluna), (linha+1, coluna), (linha, coluna-1), (linha, coluna+1)]: # Adiciona os vizinhos
            if 0 <= l < self.n and 0 <= c < self.n:
                novo_tabuleiro[l][c] ^= 1 # Aqui é onde o bit é invertido
        return novo_tabuleiro
 
    def eh_objetivo(self, tabuleiro): # Retorna se todas as celulas forem igual a 1 (Venceu)
        return np.all(tabuleiro == 1)
 
    def heuristica(self, tabuleiro): # Quanto mais luzes acesa, mais a IA pensa que está vencendo
        return int(np.sum(tabuleiro == 0))
 
    def tabuleiro_para_tupla(self, tabuleiro): # Transforma o tabuleiro em uma tupla para não revisitar estados ja visitados
        return tuple(tabuleiro.flatten())
 
    def gerar_tabuleiro_aleatorio(self): # Gera um tabuleiro aleatorio
        tabuleiro = np.ones((self.n, self.n), dtype=int)
 
        if self.n <= 2:
            tabuleiro = self.clicar(tabuleiro, 0, 0)
        else:
            for _ in range(random.randint(self.n ** 2, 2 * self.n ** 2)): # O tabuleiro começa todo aceso e vai clicando aleatoriamente
                tabuleiro = self.clicar(tabuleiro, random.randint(0, self.n - 1), random.randint(0, self.n - 1))
        return tabuleiro
 
def executar_experimento(nome, funcao, jogo, tab, **kwargs): # Executa os experimentos
    tracemalloc.start()
    inicio = time.time()
    try:
        resultado = funcao(jogo, tab, **kwargs)
    except Exception:
        resultado = None
       
    decorrido = time.time() - inicio
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
   
    return {
        "alg": nome,
        "passos": len(resultado) if resultado is not None else "N/A",
        "tempo": round(decorrido, 4),
        "mem": round(pico / 1024, 2),
        "enc": resultado is not None
    }
 
 
def main(): # Função principal
    n = int(input("Digite o tamanho do tabuleiro: "))
   
    print(f"\n{'='*40}\n Tabuleiro {n}x{n}\n{'='*40}")
    jogo = JogoLuzes(n)
    tabuleiro = jogo.gerar_tabuleiro_aleatorio()
    resultados = []
    resultados.append(executar_experimento("Largura (BFS)", busca_largura, jogo, tabuleiro))
    resultados.append(executar_experimento("Profundidade (DFS)", busca_profundidade, jogo, tabuleiro, prof_max=n*n))
    resultados.append(executar_experimento("Gulosa", busca_gulosa, jogo, tabuleiro))
    resultados.append(executar_experimento("A*", busca_a_estrela, jogo, tabuleiro))
    resultados.append(executar_experimento("Subida de Encosta", subida_encosta, jogo, tabuleiro))
    print(f"{'Algoritmo':<20} {'Enc.':<5} {'Passos':<8} {'Tempo(s)':<10} {'Mem(KB)'}")
    print("-" * 55)
    for r in resultados:
        enc_str = "SIM" if r['enc'] else "NÃO"
        print(f"{r['alg']:<20} {enc_str:<5} {str(r['passos']):<8} {str(r['tempo']):<10} {str(r['mem'])}")
 
if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
    main()