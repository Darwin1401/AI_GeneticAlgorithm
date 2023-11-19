# Tham khao code cua https://github.com/nidragedd

from objects.sudoku_genetics import SudokuGA

if __name__ == '__main__':

    population_size = 5000
    selection_rate = 0.25
    random_selection_rate = 0.25
    nb_children = 4
    mutation_rate = 0.25
    max_nb_generations = 100
    presolving = False
    model_to_solve = "3x3_easy_03"
    restart_after_n_generations_without_improvement = 30

    sga = SudokuGA(population_size, selection_rate, random_selection_rate, nb_children, max_nb_generations, mutation_rate, model_to_solve, presolving, restart_after_n_generations_without_improvement)
    sga.run()