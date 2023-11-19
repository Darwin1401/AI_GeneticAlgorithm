from time import time

from objects.pencilmark import PencilMark
from objects.sudoku import Sudoku
from sudoku import ga_utils
from utils import fileloader, graphics, tools

class SudokuGA(object):
    _population_size = None
    _selection_rate = None
    _random_selection_rate = None
    _nb_children = None
    _max_nb_generations = None
    _mutation_rate = None
    _model_to_solve = None
    _presolving = None
    _restart_after_n_generations_without_improvement = None
    _start_time = None

    def __init__(self, population_size, selection_rate, random_selection_rate, nb_children, max_nb_generations, mutation_rate, model_to_solve, presolving, restart_after_n_generations_without_improvement):
        self._population_size = population_size
        self._selection_rate = selection_rate
        self._random_selection_rate = random_selection_rate
        self._nb_children = nb_children
        self._max_nb_generations = max_nb_generations
        self._mutation_rate = mutation_rate
        self._model_to_solve = model_to_solve
        self._presolving = presolving
        self._restart_after_n_generations_without_improvement = restart_after_n_generations_without_improvement

    def run(self): # Chay giai thuat di truyen de giai quyet bai toan
        values_to_set = self._load().get_initial_values()

        best_data = []
        worst_data = []
        found = False
        overall_nb_generations_done = 0
        restart_counter = 0

        while overall_nb_generations_done < self._max_nb_generations and not found:
            new_population = ga_utils.create_generation(self._population_size, values_to_set)

            nb_generations_done = 0
            remember_the_best = 0
            nb_generations_without_improvement = 0

            # Lap lai den khi dat den so luong the he toi da cho phep hoac khi da tim thay loi giai
            while nb_generations_done < self._max_nb_generations and not found:
                # Danh gia bang sudoku
                ranked_population = ga_utils.rank_population(new_population)
                best_solution = ranked_population[0]
                best_score = best_solution.fitness()
                worst_score = ranked_population[-1].fitness()
                best_data.append(best_score)
                worst_data.append(worst_score)

                # Kiem tra xem the he moi co cai thien so voi the he cu khong
                if remember_the_best == best_score:
                    nb_generations_without_improvement += 1
                else:
                    remember_the_best = best_score
                
                if 0 < self._restart_after_n_generations_without_improvement < nb_generations_without_improvement:
                    print("No improvement since {} generations, restarting the program".format(self._restart_after_n_generations_without_improvement))
                    restart_counter += 1
                    break
                
                # Kiem tra xem sudoku da duoc giai chua va in ra nhung ket qua tot nhat va te nhat
                if best_score > 0:
                    print("Problem not solved on generation {} (restarted {} times). Best solution score is {} and worst is {}".format(nb_generations_done, restart_counter, best_score, worst_score))
                    # sudoku van chua duoc giai thi se tao ra the he tiep theo 
                    next_breeders = ga_utils.pick_from_population(ranked_population, self._selection_rate, self._random_selection_rate)
                    children = ga_utils.create_children_random_parents(next_breeders, self._nb_children)
                    new_population = ga_utils.mutate_population(children, self._mutation_rate)

                    nb_generations_done += 1
                    overall_nb_generations_done += 1
                else:
                    print("Problem solved after {} generations ({} overall generations)!!! Solution found is: ".format(nb_generations_done, overall_nb_generations_done))
                    best_solution.display()
                    found = True
                    print("It took {} to solve it".format(tools.get_human_readable_time(self._start_time, time())))
        if not found:
            print("Problem not solved after {} generations. Printing best and worst results below".format(overall_nb_generations_done))
            ranked_population = ga_utils.rank_population(new_population)
            best_solution = ranked_population[0]
            worst_solution = ranked_population[-1]
            print("Best is: ")
            best_solution.display()
            print("Worst is: ")
            worst_solution.display()
        
        graphics.draw_best_worst_fitness_scores(best_data, worst_data)

    def _load(self): # Load file txt sudoku
        if ((self._selection_rate + self._random_selection_rate) / 2) * self._nb_children != 1:
            raise Exception("Either the selection rate, random selection rate or the number of children is not well adapted to fit the population")
        values_to_set = fileloader.load_file_as_values(self._model_to_solve)
        zeros_to_count = '0' if len(values_to_set) < 82 else '00'
        print("The solution we have to solve is: (nb values to find = {})".format(values_to_set.count(zeros_to_count)))

        self._start_time = time()
        s = Sudoku(values_to_set)
        s.display()

        self._run_pencil_mark(s)
        return s

    def _run_pencil_mark(self, sudoku): # Chay danh dau nhung gia tri kha thi cho tung o trong sudoku
        if self._presolving:
            print("using pencil mark to fill in some predetermined values...")
            p = PencilMark(sudoku)
            p.run()

            remaining_values_to_find = sudoku.get_initial_values().count(0)
            if remaining_values_to_find == 0:
                print("With just pencil mark, everything has been found! Solution is: ")
            else:
                print("After pencil mark, the solution we have to solve is: (nb values to find = {})".format(remaining_values_to_find))
            
            sudoku.display()
            if remaining_values_to_find == 0:
                print("It tool {} to solve it".format(tools.get_human_readable_time(self._start_time, time())))
                exit(0)