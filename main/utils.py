import random

class Utils():
    @staticmethod
    def generate_initial_solution(inst):
        F = inst["F"]
        C = inst["C"]
        P = inst["P"]

        open_fac = [0] * F

        k = random.randint(max(1, P - 2), P)
        opens = random.sample(range(F), min(k, F))
        for f in opens:
            open_fac[f] = 1

        assign = Utils.full_assign(inst, open_fac)
        open_fac, assign = Utils.repair_capacity(inst, open_fac, assign)
        return open_fac, assign

    @staticmethod
    def full_assign(inst, open_fac):
        C = inst["C"]
        F = inst["F"]
        dist = inst["dist"]
        demand = inst["demand"]
        capacity = inst["capacity"]

        assign = [-1] * C
        load = [0] * F

        for c in range(C):
            best_f = None
            best_cost = float("inf")
            for f in range(F):
                if open_fac[f] == 1:
                    d = dist[c][f]
                    if d < best_cost and load[f] + demand[c] <= capacity[f]:
                        best_cost = d
                        best_f = f

            if best_f is None:
                best_f = Utils.find_best_open_forced(inst, open_fac, load, c)

            assign[c] = best_f
            load[best_f] += demand[c]

        return assign

    @staticmethod
    def incremental_reassign(inst, old_open, new_open, old_assign):
        C = inst["C"]
        F = inst["F"]
        dist = inst["dist"]
        demand = inst["demand"]
        capacity = inst["capacity"]

        assign = old_assign[:]
        load = Utils.compute_load(assign, demand, F)

        for f in range(F):
            if old_open[f] == 1 and new_open[f] == 0:
                clients_to_move = [c for c in range(C) if assign[c] == f]
                clients_to_move.sort(key=lambda c: dist[c][f])

                for c in clients_to_move:
                    best_f2 = None
                    best_cost = float("inf")
                    for f2 in range(F):
                        if new_open[f2] == 1 and load[f2] + demand[c] <= capacity[f2]:
                            d = dist[c][f2]
                            if d < best_cost:
                                best_cost = d
                                best_f2 = f2

                    if best_f2 is None:
                        best_f2 = min(
                            [f2 for f2 in range(F) if new_open[f2] == 1],
                            key=lambda f2: load[f2]
                        )

                    load[f] -= demand[c]
                    load[best_f2] += demand[c]
                    assign[c] = best_f2

        for f in range(F):
            if old_open[f] == 0 and new_open[f] == 1:
                for c in range(C):
                    old_f = assign[c]
                    if dist[c][f] < dist[c][old_f] * 0.85:
                        if load[f] + demand[c] <= capacity[f]:
                            load[old_f] -= demand[c]
                            load[f] += demand[c]
                            assign[c] = f

        return assign

    @staticmethod
    def find_best_open_forced(inst, open_fac, load, c):
        F = inst["F"]
        dist = inst["dist"]
        capacity = inst["capacity"]

        best_f = None
        best_score = float("inf")

        for f in range(F):
            if open_fac[f] == 1:
                load_penalty = (load[f] / capacity[f]) ** 2 if capacity[f] > 0 else 0
                score = dist[c][f] + load_penalty * 50 
                if score < best_score:
                    best_score = score
                    best_f = f

        return best_f

    @staticmethod
    def compute_cost(inst, open_fac, assign):
        C = inst["C"]
        F = inst["F"]
        dist = inst["dist"]
        fixed = inst["fixed_cost"]

        cost = 0.0
        for f in range(F):
            if open_fac[f] == 1:
                cost += fixed[f]
        for c in range(C):
            f = assign[c]
            cost += dist[c][f]
        return cost

    @staticmethod
    def compute_load(assign, demand, F):
        load = [0] * F
        for c, f in enumerate(assign):
            load[f] += demand[c]
        return load

    @staticmethod
    def best_open_facility(inst, open_fac, load, c):
        dist = inst["dist"]
        demand = inst["demand"]
        capacity = inst["capacity"]

        best_f = None
        best_cost = float("inf")

        for f in range(inst["F"]):
            if open_fac[f] == 1 and load[f] + demand[c] <= capacity[f]:
                if dist[c][f] < best_cost:
                    best_cost = dist[c][f]
                    best_f = f

        if best_f is None:
            best_f = Utils.find_best_open_forced(inst, open_fac, load, c)
        return best_f

    @staticmethod
    def local_search_1move(inst, assign, load, open_fac):
        C = inst["C"]
        dist = inst["dist"]
        demand = inst["demand"]
        capacity = inst["capacity"]

        best_c = None
        best_f2 = None
        best_delta = 0

        for c in range(C):
            f1 = assign[c]
            for f2 in range(inst["F"]):
                if open_fac[f2] == 1 and f2 != f1:
                    if load[f2] + demand[c] <= capacity[f2]:
                        before = dist[c][f1]
                        after = dist[c][f2]
                        delta = before - after
                        if delta > best_delta:
                            best_delta = delta
                            best_c = c
                            best_f2 = f2

        if best_c is not None:
            f1 = assign[best_c]
            load[f1] -= demand[best_c]
            load[best_f2] += demand[best_c]
            assign[best_c] = best_f2

        return assign

    @staticmethod
    def local_search_2opt(inst, assign, load, open_fac, max_iterations=100):
        C = inst["C"]
        F = inst["F"]
        dist = inst["dist"]
        demand = inst["demand"]
        capacity = inst["capacity"]

        improved = True
        iterations = 0

        while improved and iterations < max_iterations:
            improved = False
            iterations += 1

            for c1 in range(C):
                for c2 in range(c1 + 1, C):
                    f1_old = assign[c1]
                    f2_old = assign[c2]

                    if f1_old != f2_old:
                        cost_before = dist[c1][f1_old] + dist[c2][f2_old]
                        cost_after = dist[c1][f2_old] + dist[c2][f1_old]

                        if cost_after < cost_before:
                            load[f1_old] -= demand[c1]
                            load[f2_old] -= demand[c2]

                            if (load[f1_old] + demand[c2] <= capacity[f1_old] and
                                load[f2_old] + demand[c1] <= capacity[f2_old]):

                                assign[c1] = f2_old
                                assign[c2] = f1_old
                                load[f1_old] += demand[c2]
                                load[f2_old] += demand[c1]
                                improved = True
                            else:
                                load[f1_old] += demand[c1]
                                load[f2_old] += demand[c2]

        return assign

    @staticmethod
    def repair_capacity(inst, open_fac, assign):
        demand = inst["demand"]
        capacity = inst["capacity"]
        F = inst["F"]
        C = inst["C"]
        P = inst["P"]

        load = Utils.compute_load(assign, demand, F)

        for f in range(F):
            while load[f] > capacity[f]:
                overflow_clients = [c for c in range(C) if assign[c] == f]
                c = random.choice(overflow_clients)

                moved = False
                for f2 in range(F):
                    if open_fac[f2] == 1 and load[f2] + demand[c] <= capacity[f2]:
                        assign[c] = f2
                        load[f] -= demand[c]
                        load[f2] += demand[c]
                        moved = True
                        break

                if not moved:
                    closed = [x for x in range(F) if open_fac[x] == 0]
                    if closed and sum(open_fac) < P:
                        f2 = random.choice(closed)
                        open_fac[f2] = 1
                        assign[c] = f2
                        load[f] -= demand[c]
                        load[f2] = demand[c]
                    else:
                        best_f2 = min(
                            [f2 for f2 in range(F) if open_fac[f2] == 1],
                            key=lambda f2: load[f2]
                        )
                        assign[c] = best_f2
                        load[f] -= demand[c]
                        load[best_f2] += demand[c]

        return open_fac, assign
