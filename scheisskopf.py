import experiment as ex

# Main method used for testing.
if __name__ == '__main__':

	experiment = ex.Experiment(1, "RANDOM", "HEURISTIC")
	experiment.run()

	#experiment = ex.Experiment(10000, "RANDOM", "HEURISTIC")
	#experiment.run()

	#experiment = ex.Experiment(10000, "GREEDY", "HEURISTIC")
	#experiment.run()