class Runner:
    def run(self, class_name, duration, n_replicates):
        pass


class SerialRunner(Runner):
    def __init__(self, class_name, duration, n_replicates):
        self.class_name = class_name
        self.duration = duration
        self.n_replicates = n_replicates

    def run(self):
        return [self.new_sim().run_simulation() for x in range(self.n_replicates)]

    def new_sim(self):
        constructor = globals()[self.class_name]
        sim = constructor()
        sim.duration = self.duration
        return sim

    with open('hama_vs_sav_compar.csv', 'w') as csvfile:
        pass
