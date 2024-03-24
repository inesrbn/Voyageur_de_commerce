import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import tkinter as tk

class GraphWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Graph Visualization")

        self.num_cities = tk.IntVar()
        self.min_coord = tk.DoubleVar()
        self.max_coord = tk.DoubleVar()

        self.num_cities.set(5)  # Valeur par défaut
        self.min_coord.set(0)
        self.max_coord.set(100)

        self.canvas = None
        self.graph_figure = None

        self.create_widgets()

    def create_widgets(self):
        label_num_cities = tk.Label(self.master, text="Number of Cities:")
        label_num_cities.grid(row=0, column=0, sticky=tk.E)
        entry_num_cities = tk.Entry(self.master, textvariable=self.num_cities)
        entry_num_cities.grid(row=0, column=1)

        label_min_coord = tk.Label(self.master, text="Minimum Coordinate:")
        label_min_coord.grid(row=1, column=0, sticky=tk.E)
        entry_min_coord = tk.Entry(self.master, textvariable=self.min_coord)
        entry_min_coord.grid(row=1, column=1)

        label_max_coord = tk.Label(self.master, text="Maximum Coordinate:")
        label_max_coord.grid(row=2, column=0, sticky=tk.E)
        entry_max_coord = tk.Entry(self.master, textvariable=self.max_coord)
        entry_max_coord.grid(row=2, column=1)

        btn_generate = tk.Button(self.master, text="Generate Graph", command=self.generate_graph)
        btn_generate.grid(row=3, columnspan=2)

        self.graph_figure = plt.figure(figsize=(7, 7))
        self.canvas = FigureCanvasTkAgg(self.graph_figure, master=self.master)
        self.canvas.get_tk_widget().grid(row=4, columnspan=2)


    def coordonees_random(self, num_cities, min_coord, max_coord):
        cities = {}
        for i in range(num_cities):
            city_name = f"v{i+1}"
            while True:
                x = random.uniform(min_coord, max_coord)
                y = random.uniform(min_coord, max_coord)
                if (x, y) not in cities.values():
                    cities[city_name] = (x, y)
                    break
        return cities

    def parcours_longueur(self, parcours, cities):
        total_distance = 0
        for i in range(len(parcours) - 1):
            city1 = parcours[i]
            city2 = parcours[i + 1]
            total_distance += self.distance_villes(cities[city1], cities[city2])
        total_distance += self.distance_villes(cities[parcours[-1]], cities[parcours[0]])
        return total_distance

    def distance_villes(self, city1, city2):
        return ((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)**0.5
    

    def tab_plus_court_chemin(self, best_solution, cities):
        print("Plus Court Chemin:")
        print("City \t Next City \t Distance")
        
        for i in range(len(best_solution)):
            city = best_solution[i]
            next_city = best_solution[(i + 1) % len(best_solution)]
            distance = self.distance_villes(cities[city], cities[next_city])
            print(f"{city} \t {next_city} \t {distance:.2f}")

    def generate_graph(self):
        self.graph_figure.clear()
        num_cities = self.num_cities.get()
        min_coord = self.min_coord.get()
        max_coord = self.max_coord.get()



        # Appel de la fonction pour générer le chemin le plus court
        best_solution, best_longueur = self.graphe(num_cities, min_coord, max_coord)

        cities = self.coordonees_random(num_cities, min_coord, max_coord)
        G = nx.DiGraph()
        G.add_nodes_from(cities.keys())
        pos = nx.random_layout(G)  # Récupérer les positions des noeuds

        # Ajouter les arêtes pour le chemin le plus court
        for i in range(len(best_solution) - 1):
            G.add_edge(best_solution[i], best_solution[i+1])
        G.add_edge(best_solution[-1], best_solution[0])  # Boucle

        # Dessiner le graphe
        nx.draw(G, pos, with_labels=True, ax=self.graph_figure.gca())
        self.graph_figure.gca().set_title(f"Shortest Path: {best_longueur:.2f}")
        self.canvas.draw()

        # Afficher les détails du chemin le plus court dans le terminal
        self.tab_plus_court_chemin(best_solution, cities)


    def eval_solution(self, solution, cities):
        return self.parcours_longueur(solution, cities)

    def selection_parents(self, population):
        return random.sample(population, 2)

    def recombinaison(self, parents):
        pivot = random.randint(0, len(parents[0]) - 1)
        child1 = parents[0][:pivot] + [city for city in parents[1] if city not in parents[0][:pivot]]
        child2 = parents[1][:pivot] + [city for city in parents[0] if city not in parents[1][:pivot]]
        return child1, child2

    def mutation(self, indiv1):
        x = random.randint(0, 100)
        if x <= 2:
            index1, index2 = random.sample(range(len(indiv1)), 2)
            indiv1[index1], indiv1[index2] = indiv1[index2], indiv1[index1]
        return indiv1

    def formation(self, indiv1, indiv2):
        new_population = indiv1 + indiv2
        return new_population

    def graphe(self, num_cities, min_cord, max_coord):
        cities = self.coordonees_random(num_cities,min_cord, max_coord)

        population_size = 10
        population = [list(cities.keys()) for _ in range(population_size)]

        iterations = 100
        for _ in range(iterations):
            parents = self.selection_parents(population)
            enfants = self.recombinaison(parents)
            enfants = [self.mutation(child) for child in enfants]
            population = self.formation(population, enfants)

        best_solution = min(population, key=lambda x: self.eval_solution(x, cities))
        best_longueur = self.eval_solution(best_solution, cities)
        print("Meilleure solution:", best_solution)
        print("Longueur de la meilleure solution:", best_longueur)

        return best_solution, best_longueur
    



def main():
    root = tk.Tk()
    app = GraphWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
