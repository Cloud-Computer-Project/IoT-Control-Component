class OptimizationEngine:
    def __init__(self):
        self.scenarios = []

    def apply(self, scenario):
        print("Applying optimization scenario:", scenario)
        self.scenarios.append(scenario)
