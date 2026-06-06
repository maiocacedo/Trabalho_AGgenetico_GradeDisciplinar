import json
import random

class Disciplina:
    def __init__(self, codigo, nome, periodo, creditos, horarios, requisitos, optativa):
        self.codigo = codigo
        self.nome = nome
        self.periodo = periodo
        self.creditos = creditos
        self.horarios = horarios
        self.requisitos = requisitos
        self.optativa = optativa

class Professor:
    def __init__(self, nome, disponibilidade, disciplinas):
        self.nome = nome
        self.disponibilidade = disponibilidade
        self.disciplinas = disciplinas

class Aula:
    def __init__(self, disciplina, indice_aula, professor):
        self.disciplina = disciplina
        self.indice_aula = indice_aula
        self.professor = professor

with open("grade_curricular.json", "r", encoding="utf-8") as f:
    grade_data = json.load(f)
with open("professores.json", "r", encoding="utf-8") as f:
    prof_data = json.load(f)

disciplinas = {}
for item in grade_data:
    disc = Disciplina(
        item["codigo"],
        item["nome"],
        item["periodo"],
        item["aulas_semanais"],
        item["horarios"],
        item["requisitos"],
        item["optativa"]
    )
    disciplinas[disc.codigo] = disc

professores = []
disciplina_para_professor = {}
for item in prof_data:
    prof = Professor(
        item["nome"],
        item["disponibilidade"],
        item["disciplinas"]
    )
    professores.append(prof)
    for disc_code in prof.disciplinas:
        disciplina_para_professor[disc_code] = prof

aulas = []
for disc_code, disc in disciplinas.items():
    prof = disciplina_para_professor.get(disc_code)
    for i in range(disc.horarios):
        aulas.append(Aula(disc, i, prof))

def inicializar_individuo():
    ind = []
    for aula in aulas:
        if aula.professor and aula.professor.disponibilidade:
            ind.append(random.choice(aula.professor.disponibilidade))
        else:
            ind.append(random.randint(0, 49))
    return ind

