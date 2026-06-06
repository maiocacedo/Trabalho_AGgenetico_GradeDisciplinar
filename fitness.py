from dados import aulas, disciplinas

PESO_HARD = 100
PESO_SOFT = 10

def calcular_fitness(cromossomo):
    penalidades = 0
    prof_horarios = {}
    periodo_horarios = {}
    disciplina_horarios = {}

    for idx, horario in enumerate(cromossomo):
        aula = aulas[idx]
        prof = aula.professor
        periodo = aula.disciplina.periodo
        disc_code = aula.disciplina.codigo

        if disc_code not in disciplina_horarios:
            disciplina_horarios[disc_code] = []
        disciplina_horarios[disc_code].append(horario)

        if prof:
            if horario not in prof.disponibilidade:
                penalidades += PESO_HARD

            if horario not in prof_horarios:
                prof_horarios[horario] = []
            prof_horarios[horario].append(prof.nome)

        if horario not in periodo_horarios:
            periodo_horarios[horario] = []
        periodo_horarios[horario].append(aula.disciplina)

    for horario, profs in prof_horarios.items():
        counts = {}
        for p in profs:
            counts[p] = counts.get(p, 0) + 1
        for p, count in counts.items():
            if count > 1:
                penalidades += (count - 1) * PESO_HARD


    for horario, discs in periodo_horarios.items():
        period_discs = {}
        for d in discs:
            if d.periodo not in period_discs:
                period_discs[d.periodo] = []
            period_discs[d.periodo].append(d)
        for p, group in period_discs.items():
            if len(group) > 1:
                cores = [d for d in group if not d.optativa]
                opts = [d for d in group if d.optativa]
                if len(cores) > 1:
                    penalidades += (len(cores) - 1) * PESO_HARD
                    if opts:
                        penalidades += len(opts) * PESO_HARD
                elif len(cores) == 1:
                    if opts:
                        penalidades += len(opts) * PESO_HARD

    for disc_code, horarios_lst in disciplina_horarios.items():
        disc = disciplinas[disc_code]
        for req_code in disc.requisitos:
            if req_code in disciplina_horarios:
                req_horarios = disciplina_horarios[req_code]
                intersection = set(horarios_lst).intersection(set(req_horarios))
                if intersection:
                    penalidades += len(intersection) * PESO_HARD

    for horario in cromossomo:
        if (horario % 10) >= 5:
            penalidades += PESO_SOFT

    prof_day_horarios = {}
    for idx, horario in enumerate(cromossomo):
        aula = aulas[idx]
        prof = aula.professor
        if prof:
            day = horario // 10
            turn = 0 if (horario % 10 < 5) else 1
            key = (prof.nome, day, turn)
            if key not in prof_day_horarios:
                prof_day_horarios[key] = set()
            prof_day_horarios[key].add(horario)

    for (prof_name, day, turn), horarios_set in prof_day_horarios.items():
        if len(horarios_set) > 1:
            min_h = min(horarios_set)
            max_h = max(horarios_set)
            for h in range(min_h + 1, max_h):
                if h not in horarios_set:
                    penalidades += PESO_SOFT

    period_day_counts = {}
    for idx, horario in enumerate(cromossomo):
        aula = aulas[idx]
        periodo = aula.disciplina.periodo
        day = horario // 10
        key = (periodo, day)
        period_day_counts[key] = period_day_counts.get(key, 0) + 1


    for p in range(1, 5):
        for day in range(5):
            if period_day_counts.get((p, day), 0) == 0:
                penalidades += PESO_SOFT

    return 100 / (100 + penalidades)
