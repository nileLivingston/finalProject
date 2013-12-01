import experiment as ex

# Main method used for testing.
if __name__ == '__main__':

	experiment = ex.Experiment(1, "HUMAN", "RANDOM")
	experiment.run()

	#experiment = ex.Experiment(5000, "RANDOM", "GREEDY")
	#experiment.run()

	#experiment = ex.Experiment(10000, "GREEDY", "HEURISTIC")
	#experiment.run()