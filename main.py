import os
import pandas as pd
from heuristicas import iterated_greedy
from util import ler_instancia, calcular_makespan

def main():
    pasta = "data"
    resultados = []
    for nome in sorted(os.listdir(pasta)):
        if nome.endswith(".txt") and nome.startswith("P"):
            caminho = os.path.join(pasta, nome)
            print(f"Processando {nome}...")
            try:
                tempos = ler_instancia(caminho)
                seq = iterated_greedy(tempos, limite=600)
                mk = calcular_makespan(seq, tempos)
                resultados.append({"Instância": nome, "Makespan": mk, "Sequência": seq})
            except Exception as e:
                print(f"Erro na instância {nome}: {e}")
    df = pd.DataFrame(resultados)
    os.makedirs("resultados", exist_ok=True)
    df.to_csv("resultados/resultados_iterated_greedy.csv", index=False)
    print("Resultados salvos em: resultados/resultados_iterated_greedy.csv")

if __name__ == "__main__":
    main()
