from util import calcular_makespan
import random
import math
import time

def _inserir(sequencia, i, j):
    if i == j: return list(sequencia)
    temp = list(sequencia)
    job = temp.pop(i)
    temp.insert(j, job)
    return temp

def _trocar(sequencia, i, j):
    if i == j: return list(sequencia)
    temp = list(sequencia)
    temp[i], temp[j] = temp[j], temp[i]
    return temp

def _inverter(sequencia, i, j):
    temp = list(sequencia)
    temp[i:j+1] = temp[i:j+1][::-1]
    return temp

def neh(tempos):
    ordem = sorted(range(len(tempos)), key=lambda j: -sum(tempos[j]))
    seq = [ordem[0]]
    for k in range(1, len(ordem)):
        job = ordem[k]
        melhor = float('inf')
        melhor_seq = []
        for i in range(len(seq) + 1):
            temp_seq = seq[:i] + [job] + seq[i:]
            mk = calcular_makespan(temp_seq, tempos)
            if mk < melhor:
                melhor = mk
                melhor_seq = temp_seq
        seq = melhor_seq
    return seq

def rvnd(seq_ini, tempos):
    seq = list(seq_ini)
    mk = calcular_makespan(seq, tempos)
    vizinhancas = [("insercao", _inserir), ("swap", _trocar), ("inversao", _inverter)]
    while True:
        random.shuffle(vizinhancas)
        melhora = False
        for nome, op in vizinhancas:
            for i in range(len(seq)):
                for j in range(len(seq)):
                    if i == j: continue
                    nova = op(seq, i, j)
                    mk_nova = calcular_makespan(nova, tempos)
                    if mk_nova < mk:
                        seq = nova
                        mk = mk_nova
                        melhora = True
                        break
                if melhora: break
            if melhora: break
        if not melhora: break
    return seq

def destruir_reconstruir(seq, tempos, pct=0.3):
    r = max(1, int(len(seq)*pct))
    rem = random.sample(seq, r)
    base = [j for j in seq if j not in rem]
    for j in rem:
        melhor = float('inf')
        best = []
        for i in range(len(base)+1):
            nova = base[:i] + [j] + base[i:]
            mk = calcular_makespan(nova, tempos)
            if mk < melhor:
                melhor = mk
                best = nova
        base = best
    return base

def aceitar_solucao(novo, atual, temp):
    if novo < atual: return True
    if temp <= 0: return False
    delta = novo - atual
    return random.random() < math.exp(-delta / temp)

def iterated_greedy(tempos, limite=600, destr=0.3, temp_ini=0.05):
    sol = rvnd(neh(tempos), tempos)
    mk_atual = calcular_makespan(sol, tempos)
    melhor_sol, melhor_mk = list(sol), mk_atual
    inicio = time.time()
    while time.time() - inicio < limite:
        pert = destruir_reconstruir(sol, tempos, destr)
        cand = rvnd(pert, tempos)
        mk_cand = calcular_makespan(cand, tempos)
        if aceitar_solucao(mk_cand, mk_atual, temp_ini):
            sol, mk_atual = list(cand), mk_cand
        if mk_atual < melhor_mk:
            melhor_sol, melhor_mk = list(sol), mk_atual
    return melhor_sol
