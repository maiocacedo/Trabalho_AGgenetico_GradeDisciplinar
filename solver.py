import random
import matplotlib.pyplot as plt
from algoritmo_genetico import GeneticAlgorithm
from dados import aulas, inicializar_individuo, disciplinas
from fitness import calcular_fitness

def mutacao(individuo, taxa_mutacao):
    novo_ind = individuo.copy()
    for i in range(len(novo_ind)):
        if random.random() < taxa_mutacao:
            aula = aulas[i]
            if aula.professor and aula.professor.disponibilidade:
                novo_ind[i] = random.choice(aula.professor.disponibilidade)
            else:
                novo_ind[i] = random.randint(0, 49)
    return novo_ind

def main():
    ga = GeneticAlgorithm(
        pop_size=200,
        crossover_rate=0.75,
        mutation_rate=0.05,
        generations=800,
        elitism_size=2
    )

    melhor_ind, melhor_fit, historico = ga.run(
        initialize_fn=inicializar_individuo,
        fitness_fn=calcular_fitness,
        mutate_fn=mutacao,
        select_type="tournament",
        crossover_type="one_point"
    )

    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    horarios_nomes = [
        "07:30 - 08:20",
        "08:20 - 09:10",
        "09:10 - 10:00",
        "10:20 - 11:10",
        "11:10 - 12:00",
        "13:00 - 13:50",
        "13:50 - 14:40",
        "14:40 - 15:30",
        "15:50 - 16:40",
        "16:40 - 17:30"
    ]

    relatorio_linhas = []

    def registrar(texto):
        print(texto)
        relatorio_linhas.append(texto)

    registrar("=== RESULTADO DA OTIMIZAÇÃO ===")
    registrar(f"Melhor Fitness Alcançado: {melhor_fit:.6f}")
    registrar(f"Gerações Executadas: {len(historico)}")
    registrar("")

    for p in range(1, 5):
        registrar(f"--- GRADE HORÁRIA - PERÍODO {p} ---")
        grade = [["---" for _ in range(5)] for _ in range(10)]
        
        for idx, horario in enumerate(melhor_ind):
            aula = aulas[idx]
            if aula.disciplina.periodo == p:
                dia_idx = horario // 10
                horario_idx = horario % 10
                prof_nome = aula.professor.nome.split()[0] if aula.professor else "SemProf"
                val = f"{aula.disciplina.codigo}({prof_nome})"
                if grade[horario_idx][dia_idx] == "---":
                    grade[horario_idx][dia_idx] = val
                else:
                    grade[horario_idx][dia_idx] += f" / {val}"

        header = f"{'Horário':<15} | " + " | ".join(f"{dias[d]:<17}" for d in range(5))
        registrar(header)
        registrar("-" * len(header))
        for h_idx, h_str in enumerate(horarios_nomes):
            row_str = f"{h_str:<15} | " + " | ".join(f"{grade[h_idx][d]:<17}" for d in range(5))
            registrar(row_str)
        registrar("")

    with open("relatorio_grade.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(relatorio_linhas))

    plt.figure(figsize=(10, 5))
    plt.plot(historico)
    plt.title("Evolução do Fitness")
    plt.xlabel("Geração")
    plt.ylabel("Fitness do Melhor Indivíduo")
    plt.grid(True)
    plt.savefig("grafico_evolucao.png")

if __name__ == "__main__":
    main()
