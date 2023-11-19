import numpy as np
import random

from objects.sudoku import Sudoku

# population_size: (int) kich co quan the cua the he dau tien
# values_to_set: Gia tri chung ta can khoi tao cho Sudoku
# return: (array) mang cac ca the duoc tao ra ngau nhien, mang nay co chinh xac <population_size> ca the
def create_generation(population_size, values_to_set): # Tao ra the he dau tien
    population = []
    for i in range(population_size):
        population.append(Sudoku(values_to_set).fill_random())
    return population

# return: (list) danh sach cac ca the da duoc danh gia duoc sap xep theo thu tu tang dan
def rank_population(population): # Danh gia tung ca the trong 1 quan the theo thang diem fitness (so lan lap lai cua tung gia tri trong Sudoku)
    individuals_and_score = {}
    for individual in population:
        individuals_and_score[individual] = individual.fitness()
    return sorted(individuals_and_score, key = individuals_and_score.get)

#return: (array) cac phan tu da duoc lua chon tu 1 quan the da duoc danh gia
def pick_from_population(ranked_population, selection_rate, random_selection_rate):
    '''
    Chon ngau nhien cac phan tu tot nhat trong 1 quan the da duoc danh gia dua vao ty le lua chon + chon ngau nhien 1 vai phan tu khac
    '''
    next_breeders = []

    nb_best_to_select = int(len(ranked_population) * selection_rate)
    nb_random_to_select = int(len(ranked_population) * random_selection_rate)

    # Giu n phan tu tot nhat trong quan the + 1 vai phan tu khac
    for i in range(nb_best_to_select):
        next_breeders.append(ranked_population[i])
    for i in range(nb_random_to_select):
        next_breeders.append(random.choice(ranked_population))

    # Tron moi thu ngau nhien de tranh truong hop chi co nhung phan tu tot nhat o dau danh sach
    np.random.shuffle(next_breeders)
    return next_breeders

# nb_children: (int) so luong con duoc tao ra tu moi cap bo me
# return: (array) danh sach cac con cua the he ke tiep
def create_children(next_breeders, nb_children): # Tao ra con (the he ke tiep) tu nhung phan tu da duoc chon
    next_population = []
    # Chia ra 2 tap bo va me
    for i in range(int(len(next_breeders)/2)):
        for j in range(nb_children):
            # De bo o dau va me o cuoi
            next_population.append(create_one_child(next_breeders[i], next_breeders[len(next_breeders) - 1 - i], next_breeders[i].get_initial_values()))
    return next_population

def create_children_random_parents(next_breeders, nb_children):
    next_population = []
    # Chon ngau nhien 1 bo va 1 me de tao con den khi quan the thuoc the he ke tiep duoc lap day
    range_val = int(len(next_breeders)/2) * nb_children
    for _ in range(range_val):
        father = random.choice(next_breeders)
        mother = random.choice(next_breeders)
        next_population.append(create_one_child_random_elements(father, mother, father.get_initial_values()))
    return next_population

def create_one_child(father, mother, values_to_set):
    '''
    Chon ngau nhien 1 grid (3x3) tu cha hoac me de tao ra con
    '''
    # Tranh viec tat ca grid duoc chon chi den tu bo hoac me
    sudoku_size = father.size()
    crossover_point = np.random.randint(1, sudoku_size)

    child_grids = []
    for i in range(sudoku_size):
        if i < crossover_point:
            child_grids.append(father.grids()[i])
        else:
            child_grids.append(mother.grids()[i])
    return Sudoku(values_to_set).fill_with_grids(child_grids)

def create_one_child_random_elements(father, mother, values_to_set):
    '''
    Chon ngau nhien 1 grid (3x3) tu cha hoac me de tao ra con
    '''
    # Tranh viec tat ca grid duoc chon chi den tu bo hoac me
    sudoku_size = father.size()
    elements_from_mother = np.random.randint(0, sudoku_size, np.random.randint(1, sudoku_size - 1))

    child_grids = []
    for i in range(sudoku_size):
        if i in elements_from_mother:
            child_grids.append(mother.grids()[i])
        else:
            child_grids.append(father.grids()[i])
    return Sudoku(values_to_set).fill_with_grids(child_grids)

# return: (array) 1 quan the moi voi 1 vai phan tu da duoc dot bien
def mutate_population(population, mutation_rate): # Ngau nhien dot bien vai phan tu trong quan the duoc cho dua tren ty le dot bien
    population_with_mutation = []
    for individual in population:
        if np.random.random() < mutation_rate:
            individual = individual.swap_2_values()
        population_with_mutation.append(individual)
    return population_with_mutation