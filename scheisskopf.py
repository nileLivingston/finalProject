import experiment as ex
import graphics as gr

# Main method used for testing.
if __name__ == '__main__':

	theGraphics = gr.Graphics() 
	experiment = ex.Experiment(1, "GREEDY", "RANDOM", False, theGraphics)
	experiment.run()

