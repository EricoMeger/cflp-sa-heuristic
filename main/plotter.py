import matplotlib.pyplot as plt
import os

class Plotter:
    @staticmethod
    def plot_solution(inst, open_fac, assign, cost):
        client_coords = inst["client_coords"]
        facility_coords = inst["facility_coords"]

        C = inst["C"]
        F = inst["F"]

        # separa coords
        cli_x = [c[0] for c in client_coords]
        cli_y = [c[1] for c in client_coords]

        fac_x = [f[0] for f in facility_coords]
        fac_y = [f[1] for f in facility_coords]

        plt.figure(figsize=(10, 10))

        plt.scatter(cli_x, cli_y, c="black", s=20, label="Clientes")

        plt.scatter(fac_x, fac_y, c="blue", s=120, marker="s", label="Facilities")

        open_indices = [i for i in range(F) if open_fac[i] == 1]
        open_x = [fac_x[i] for i in open_indices]
        open_y = [fac_y[i] for i in open_indices]
        plt.scatter(open_x, open_y, c="red", s=200, marker="s", label="Abertas")

        for c in range(C):
            f = assign[c]
            plt.plot(
                [cli_x[c], fac_x[f]],
                [cli_y[c], fac_y[f]],
                c="gray",
                linewidth=0.5
            )

        plt.title(f"Cost = {cost:.2f}")
        plt.legend()
        plt.grid(True)
        
        results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
        os.makedirs(results_dir, exist_ok=True)
        
        filepath = os.path.join(results_dir, f"solution_cost_{cost:.2f}.png")
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"image saved in: {filepath}")
        
        plt.show()
