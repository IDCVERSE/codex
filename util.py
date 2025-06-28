def ler_instancia_pt(path):
    with open(path, 'r', encoding='utf-8') as f:
        for linha in f:
            if linha.startswith('[PT=') and linha.endswith(']'):
                conteudo = linha[4:-1]
                return [list(map(int, job.split(','))) for job in conteudo.split(';') if job.strip()]
    raise ValueError("Instância mal formatada")

def calcular_makespan(seq, tempos):
    m = len(tempos[0])
    n = len(seq)
    C = [[0] * m for _ in range(n)]
    C[0][0] = tempos[seq[0]][0]
    for j in range(1, m):
        C[0][j] = C[0][j-1] + tempos[seq[0]][j]
    for i in range(1, n):
        C[i][0] = C[i-1][0] + tempos[seq[i]][0]
        for j in range(1, m):
            C[i][j] = max(C[i-1][j], C[i][j-1]) + tempos[seq[i]][j]
    return C[-1][-1]
