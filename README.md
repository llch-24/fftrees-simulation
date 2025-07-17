# FFTrees Simulation

This project uses simulated gamble data to explore decision-making using Fast-and-Frugal Trees (FFTrees).

- Python files simulate coin toss and Copenhagen-style gamble choices.
- The simulations generate CSV files representing gamble options and outcomes.
- These CSVs are imported into R, where we:
  - Generate binary cues (e.g., max, min, count of positives)
  - Train FFTrees to classify which gamble should be chosen under different decision frameworks

The goal is to test whether simple heuristics can approximate complex models like Expected Utility Theory (EUT) and Ergodicity Economics (EE).

Files to run:
- cues.R
- fftrees.R
- eut_fftrees.R

If you want to rerun the simulations, run simulations.py

Make sure you have the following installed:
In R:
- tidyverse
- marcusbuckmann/ffcr (if installing ffcr, install devtools first)

In Python:
- pandas
- numpy
- matplotlib
