from parser import Parser
from sa import SA
from plotter import Plotter


def print_solution(open_fac, assign, cost):
    print("\n======================")
    print("SOLUÇÃO ENCONTRADA")
    print("======================")
    print(f"Custo total = {cost:.2f}")
    
    open_facilities = [i for i in range(len(open_fac)) if open_fac[i] == 1]
    open_facilities_1based = [f + 1 for f in open_facilities]
    print(f"Facilidades abertas: {open_facilities_1based}")
    
    for f in open_facilities:
        clients = [c + 1 for c in range(len(assign)) if assign[c] == f]
        print(f"Facility {f + 1} -> clientes: {clients}")
    
    print("======================\n")


def run_single(inst):
    print("\n=== Rodando Simulated Annealing (single start) ===")
    open_fac, assign, cost = SA.run_single(inst)
    print_solution(open_fac, assign, cost)
    Plotter.plot_solution(inst, open_fac, assign, cost)
    return open_fac, assign, cost


def run_multistart(inst, runs=10):
    print(f"\n=== Rodando SA com Multi-Start ({runs} execuções) ===")
    open_fac, assign, cost = SA.multistart(inst, runs)
    print_solution(open_fac, assign, cost)
    Plotter.plot_solution(inst, open_fac, assign, cost)
    return open_fac, assign, cost


def main():
    instance_path = "input/input3.txt" 
    print("Carregando instância:", instance_path)
    inst = Parser.parse_instance(instance_path)

    # run_single(inst)

    run_multistart(inst, runs=75)


main()
