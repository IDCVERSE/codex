def ler_instancia_pt(path):
    """Lê arquivos no formato '[PT=...]'."""
    with open(path, "r", encoding="utf-8") as f:
        for linha in f:
            if linha.startswith("[PT=") and linha.endswith("]"):
                conteudo = linha[4:-1]
                return [
                    list(map(int, job.split(",")))
                    for job in conteudo.split(";")
                    if job.strip()
                ]
    raise ValueError("Instância mal formatada")


def ler_instancia_alt(path):
    """Lê arquivos no formato alternativo utilizado na descrição da tarefa."""
    with open(path, "r", encoding="utf-8") as f:
        linhas = [l.strip() for l in f if l.strip()]

    try:
        idx = next(
            i
            for i, l in enumerate(linhas)
            if "tempos de processamento" in l.lower()
        )
    except StopIteration as e:
        raise ValueError("Cabeçalho 'tempos de processamento' não encontrado") from e

    matriz = [list(map(int, linhas[idx + i + 1].split())) for i in range(5)]

    if any(len(l) != len(matriz[0]) for l in matriz):
        raise ValueError("Linhas de processamento com tamanhos diferentes")

    # transposição: linhas representam máquinas, colunas representam trabalhos
    return [list(t) for t in zip(*matriz)]


def ler_instancia(path):
    """Tenta ler o arquivo em qualquer um dos formatos suportados."""
    try:
        return ler_instancia_pt(path)
    except Exception:
        return ler_instancia_alt(path)

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

