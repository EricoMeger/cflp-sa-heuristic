class Parser():
    @staticmethod
    def parse_instance(path):
        f = open(path, "r")
        lines = f.readlines()
        f.close()

        F = None
        C = None
        P = None
        
        for line in lines:
            if "N_Clientes" in line:
                C = int(line.split("=")[1].strip())
            elif "N_Facilidades" in line:
                F = int(line.split("=")[1].strip())
            elif "P (máximo" in line:
                P = int(line.split("=")[1].strip())

        data = []
        
        for line in lines:
            line = line.strip()
            
            if not line or line.startswith("#"):
                continue
            
            if line.startswith("##"):
                continue
            
            data.append(line.split())

        idx = 0
        
        client_coords = []
        for i in range(C):
            parts = data[idx]
            client_coords.append((float(parts[1]), float(parts[2])))
            idx += 1
        
        demand = []
        for i in range(C):
            parts = data[idx]
            demand.append(float(parts[1]))
            idx += 1
        
        facility_coords = []
        for i in range(F):
            parts = data[idx]
            facility_coords.append((float(parts[1]), float(parts[2])))
            idx += 1
        
        capacity = []
        for i in range(F):
            parts = data[idx]
            capacity.append(float(parts[1]))
            idx += 1
        
        fixed_cost = []
        for i in range(F):
            parts = data[idx]
            fixed_cost.append(float(parts[1]))
            idx += 1
        
        dist = [[0.0] * F for _ in range(C)]
        for _ in range(C * F):
            parts = data[idx]
            client = int(parts[0]) - 1  
            facility = int(parts[1]) - 1
            distance = float(parts[2])
            dist[client][facility] = distance
            idx += 1
        
        return {
            "F": F,
            "C": C,
            "P": P,
            "client_coords": client_coords,
            "facility_coords": facility_coords,
            "capacity": capacity,
            "fixed_cost": fixed_cost,
            "demand": demand,
            "dist": dist
        }