import random
import math
from utils import Utils
from neighborhoods import Neighborhoods


class SA:

    @staticmethod
    def run_single(inst,
                   T0=5000.0,
                   Tmin=0.0001,
                   V=3000,                 
                   reheat_threshold=500,   
                   reheat_factor=2.0):    

        open_fac, assign = Utils.generate_initial_solution(inst)
        cost = Utils.compute_cost(inst, open_fac, assign)

        best_open = open_fac[:]
        best_assign = assign[:]
        best_cost = cost

        T = T0
        no_improve_iterations = 0
        k = 1

        while T > Tmin:

            for i in range(V):

                # 1. generate hybrid neighborhood
                new_open = Neighborhoods.hybrid(open_fac, inst["P"]) 

                # 2. incremental reassignment
                new_assign = Utils.incremental_reassign(inst, open_fac, new_open, assign)

                # 3. capacity repair, if necessary
                new_open, new_assign = Utils.repair_capacity(inst, new_open, new_assign)

                # 4. cost
                new_cost = Utils.compute_cost(inst, new_open, new_assign)

                delta = new_cost - cost
                no_improve_iterations += 1

                if delta < 0:
                    open_fac = new_open
                    assign = new_assign
                    cost = new_cost

                else:
                    prob = math.exp(-delta / T)
                    if random.random() < prob:
                        open_fac = new_open
                        assign = new_assign
                        cost = new_cost

                # 5. update global best
                if cost < best_cost:
                    best_cost = cost
                    best_open = open_fac[:]
                    best_assign = assign[:]
                    no_improve_iterations = 0
                    
                    load = Utils.compute_load(best_assign, inst["demand"], inst["F"])
                    best_assign = Utils.local_search_2opt(inst, best_assign, load, best_open, max_iterations=50)
                    best_cost = Utils.compute_cost(inst, best_open, best_assign)

                # 6. reheat only if no global improvement
                if no_improve_iterations >= reheat_threshold:
                    T = T * reheat_factor
                    no_improve_iterations = 0

            # 7. cooling with vcf
            phi = (1 + (1 / (k * (V + 1))) + V) ** -1
            T = T * phi
            k += 1

        return best_open, best_assign, best_cost

    @staticmethod
    def multistart(inst, num_starts=10,
                   T0=8000.0,    
                   Tmin=0.0001,
                   V=1000,        
                   reheat_threshold=500,
                   reheat_factor=2.0):

        global_best_cost = float("inf")
        global_best_open = None
        global_best_assign = None

        for s in range(num_starts):
            print(f"Running SA {s+1}/{num_starts}...")

            open_fac, assign, cost = SA.run_single(
                inst,
                T0=T0,
                Tmin=Tmin,
                V=V,
                reheat_threshold=reheat_threshold,
                reheat_factor=reheat_factor
            )

            if cost < global_best_cost:
                global_best_cost = cost
                global_best_open = open_fac[:]
                global_best_assign = assign[:]
                print(f"  ✓ Melhor custo encontrado: {cost:.2f}")

        return global_best_open, global_best_assign, global_best_cost
