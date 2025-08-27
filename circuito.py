
class Circuito:
    def __init__(self, resistores, V):
        self.resistores = resistores
        self.V = V

    def calcular_req(self):
        raise NotImplementedError("Deve ser implementado na subclasse")

    def calcular(self):
        raise NotImplementedError("Deve ser implementado na subclasse")


class Serie(Circuito):
    def calcular_req(self):
        return sum(self.resistores)

    def calcular(self):
        Req = self.calcular_req()
        I = self.V / Req
        resultados = []
        for i, R in enumerate(self.resistores):
            Vd = I * R
            P = Vd * I
            resultados.append({
                "Resistor": f"R{i+1}",
                "Resistencia (Ω)": R,
                "Tensao (V)": Vd,
                "Corrente (A)": I,
                "Potencia (W)": P
            })
        return Req, resultados


class Paralelo(Circuito):
    def calcular_req(self):
        return 1 / sum(1/R for R in self.resistores)

    def calcular(self):
        Req = self.calcular_req()
        I_total = self.V / Req
        resultados = []
        for i, R in enumerate(self.resistores):
            I = self.V / R
            P = self.V * I
            resultados.append({
                "Resistor": f"R{i+1}",
                "Resistencia (Ω)": R,
                "Tensao (V)": self.V,
                "Corrente (A)": I,
                "Potencia (W)": P
            })
        return Req, resultados

