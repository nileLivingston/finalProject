import experiment as ex

# Main method used for testing.
if __name__ == '__main__':

	experiment = ex.Experiment(100, "GREEDY", "RANDOM", False)
	experiment.run()
