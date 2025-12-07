import random


class Neighborhoods:

    @staticmethod
    def swap(open_fac):
        """Fecha uma facility aberta e abre uma fechada."""
        F = len(open_fac)
        new = open_fac[:]

        open_list = [f for f in range(F) if new[f] == 1]
        closed_list = [f for f in range(F) if new[f] == 0]

        if not open_list or not closed_list:
            return new  # fallback

        f_open = random.choice(open_list)
        f_closed = random.choice(closed_list)

        new[f_open] = 0
        new[f_closed] = 1

        return new

    @staticmethod
    def add(open_fac, P=None):
        """Abre facility apenas se não violar P"""
        if P is not None and sum(open_fac) >= P:
            return open_fac[:]
        
        F = len(open_fac)
        new = open_fac[:]

        closed_list = [f for f in range(F) if new[f] == 0]
        if not closed_list:
            return new

        f = random.choice(closed_list)
        new[f] = 1

        return new

    @staticmethod
    def remove(open_fac):
        """Fecha uma facility aberta (se houver mais de uma aberta)."""
        F = len(open_fac)
        new = open_fac[:]

        open_list = [f for f in range(F) if new[f] == 1]
        if len(open_list) <= 1:
            return new

        f = random.choice(open_list)
        new[f] = 0

        return new

    @staticmethod
    def hybrid(open_fac, P):
        """Vizinhança híbrida respeitando limite P"""
        r = random.random()
        num_open = sum(open_fac)
        
        if num_open >= P:
            if r < 0.80:
                return Neighborhoods.swap(open_fac)
            else:
                return Neighborhoods.remove(open_fac)
        elif num_open == 1:
            if r < 0.50:
                return Neighborhoods.add(open_fac, P)
            else:
                return Neighborhoods.swap(open_fac)
        else:
            if r < 0.70:
                return Neighborhoods.swap(open_fac)
            elif r < 0.85:
                return Neighborhoods.add(open_fac, P)
            else:
                return Neighborhoods.remove(open_fac)
