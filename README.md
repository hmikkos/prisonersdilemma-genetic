# Axelrod's Tournament Simulation

This repository contains a Python script that simulates Axelrod's Tournament using Genetic Algorithms. Axelrod's Tournament is a classic simulation in game theory, where different strategies compete in a prisoner's dilemma scenario.

## Description

In this project, we have implemented different strategies like 'Cooperation', 'Agression', 'Tit for Tat', 'Two Tits for Tat' and 'Tit for Two Tats'. Each prisoner uses a strategy and plays against others in multiple rounds of the game. 

Prisoners can also evolve their strategies over time by using genetic algorithm principles - they can breed, creating new strategies, and occasionally mutate. The script simulates the evolution of these strategies over multiple generations.

## How to Run

1. Clone the repository to your local machine.
2. Make sure Python 3.x and necessary libraries (numpy, matplotlib, seaborn) are installed.
3. Run the script `python3 project.py`.

The simulation's parameters, such as the number of generations to run and the initial number of each type of prisoner, can be adjusted in the `axelrod_tournament()` function at the bottom of the script.

## Output

The script outputs a series of plots showing how the population's composition changes over time and how aggressive behavior evolves. The agressivity score is a count of the number of times a prisoner betrayed their accomplice, and it will be plotted at each generation.

## Note

This simulation is a simplified version of Axelrod's original tournament, it can be extended or modified to include more sophisticated strategies or a more complex game environment.


