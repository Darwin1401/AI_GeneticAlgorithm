import matplotlib.pyplot as plt

# Su dung thu vien matplotlib de ve 1 so do don gian de hien thi viec tim kiem ket qua tot nhat so voi nhung lan tim kiem ket qua te nhat
def draw_best_worst_fitness_scores(best_data, worst_data):
    plt.figure(figsize = (8, 6), dpi = 80)
    plt.plot(best_data, label = "Best solution score", color="blue", linewidth = 1.0, linestyle = "-")
    plt.plot(worst_data, label = "Worst solution score", color="red", linewidth = 1.0, linestyle = "-")
    plt.ylabel('Fitness funtion value evaluation')
    plt.xlabel('Number of generations')
    plt.ylim(0, worst_data[0])
    plt.xlim(0, len(best_data))
    plt.legend()
    plt.show()