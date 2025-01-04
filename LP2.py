from pulp import LpProblem, LpMinimize, LpVariable, lpSum


def Vytvor_Sloty(seznam_casy, pocet_radku):
    sloty = []
    for r in range(pocet_radku):
        sloty.append([])
        for den in range(5):
            for cas in range(12):
                sloty[r].append(seznam_casy[r][den][cas])
    return sloty


def LP(pppdo, pppdv, vyucujici_casy, obory_casy, mistnosti_casy, seznam_oboru, seznam_predmetu, seznam_vyucujicich):

    num_slots = 60  # počet časových slotů
    num_teachers = len(seznam_vyucujicich)  # počet učitelů
    num_subjects = len(seznam_predmetu)  # počet předmětů
    num_fields = len(seznam_oboru)  # počet oborů
    room_slots = Vytvor_Sloty(mistnosti_casy, 1)
    teacher_slots = Vytvor_Sloty(vyucujici_casy, num_teachers)
    field_slots = Vytvor_Sloty(obory_casy, num_fields)
    room_slots = room_slots[0]

    field_subjects = pppdo
    teacher_subjects = pppdv

    model = LpProblem("Rozvrh_hodin", LpMinimize)

    # proměnné: x[subject][teacher][field][slot] je 1, pokud je předmět vyučován učitelem pro obor v daném slotu
    x = LpVariable.dicts("x",
                         ((s, t, f, sl) for s in range(num_subjects)
                          for t in range(num_teachers)
                          for f in range(num_fields)
                          for sl in range(num_slots)),  # Sloty omezeny na předposlední slot
                         cat="Binary")

    # minimalizace vzdálenosti od 8:00
    model += lpSum(sl * x[s, t, f, sl] for s in range(num_subjects)
                   for t in range(num_teachers)
                   for f in range(num_fields)
                   for sl in range(num_slots))

    # předmět může být vyučován pouze pokud je učitel dostupný v obou slotech
    for t in range(num_teachers):
        for sl in range(num_slots - 1):
            if teacher_slots[t][sl] == 0 or teacher_slots[t][sl + 1] == 0:
                for s in range(num_subjects):
                    for f in range(num_fields):
                        model += x[s, t, f, sl] == 0

    # předmět může být vyučován pouze pokud je místnost dostupná v obou slotech
    for sl in range(num_slots - 1):
        if room_slots[sl] == 0 or room_slots[sl + 1] == 0:
            for s in range(num_subjects):
                for t in range(num_teachers):
                    for f in range(num_fields):
                        model += x[s, t, f, sl] == 0

    # předmět může být vyučován pouze učitelem, který ho učí
    for t in range(num_teachers):
        for s in range(num_subjects):
            if teacher_subjects[t][s] == 0:
                for f in range(num_fields):
                    for sl in range(num_slots - 1):
                        model += x[s, t, f, sl] == 0

    # každý obor musí mít všechny své předměty
    for f in range(num_fields):
        for s in range(num_subjects):
            if field_subjects[f][s] == 1:
                model += lpSum(x[s, t, f, sl] for t in range(num_teachers) for sl in range(num_slots - 1)) == 1

    # každý učitel může vyučovat pouze jeden předmět v obou slotech
    for t in range(num_teachers):
        for sl in range(num_slots - 1):
            model += lpSum(
                x[s, t, f, sl] + x[s, t, f, sl + 1] for s in range(num_subjects) for f in range(num_fields)) <= 1

    # místnost může být použita pouze jednou během obou slotů
    for sl in range(num_slots - 1):
        model += lpSum(x[s, t, f, sl] + x[s, t, f, sl + 1] for s in range(num_subjects)
                       for t in range(num_teachers)
                       for f in range(num_fields)) <= 1

    # každý obor může mít pouze jednu přednášku v obou slotech
    for f in range(num_fields):
        for sl in range(num_slots - 1):
            model += lpSum(
                x[s, t, f, sl] + x[s, t, f, sl + 1] for s in range(num_subjects) for t in range(num_teachers)) <= 1

    model.solve()
    schedule = []
    for s in range(num_subjects):
        for t in range(num_teachers):
            for f in range(num_fields):
                for sl in range(num_slots - 1):
                    if x[s, t, f, sl].value() == 1:
                        schedule.append((seznam_predmetu[s], seznam_vyucujicich[t], seznam_oboru[f], sl, sl + 1))

    print("Rozvrh:")
    for item in schedule:
        den = ((item[3] - (item[3] % 12)) // 12) + 1
        hodina = (item[3] % 12) + 8
        print(f"Předmět: {item[0]}, Učitel: {item[1]}, Obor: {item[2]}, Slot: {item[3]}, Den: {den}, Hodina: {hodina}")
