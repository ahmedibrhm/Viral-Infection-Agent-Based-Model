import random
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import copy
from IPython.display import Image
import numpy as np
from mpl_toolkits import mplot3d
import imageio
import os

class human: #initiating agents as objects with (x,y) position, status (susceptible, infected, and recovered), infection duration(if status = infected)
    def __init__(self, status, x, y):
        self.status = status
        self.x_position = x
        self.y_position = y
        self.infection_duration = 0 #initializing the value to store the duration of infection by each step
    
    def Vaccination(self): #function for applying vaccine to the human
        if self.status == "susceptible":
            self.status = "recovered"
            
def initiate_reset_world(size_y, size_x): #initiating the world
    world = [[list() for i in range(size_x)] for i in range(size_y)]
    return world

def populate(human, world): #putting agent in its place in the world
    world[human.y_position][human.x_position].append(human)
    
def remove_human(human, world): #removing agent from its place in the world
    world[human.y_position][human.x_position].remove(human)
    
def infection(human, infectious_rate): #deciding whether an agent will get infected or not according to the infectious_rate
    random_number = random.random()
    if random_number <= infectious_rate and human.status == "susceptible":
        human.status = "infected"
    return human

def infection_process(human, infection_duration): #observing the infection process for infected person. 
    #Increase the period that an agent has been infected
    if human.status == "infected":
        human.infection_duration+= 1
        #if the period became equall to the infection duration, change the agent status to recovered
        if human.infection_duration >= infection_duration:
            human.status = "recovered"
    return human

def move(human, size_x, size_y, step_size): #randomly moving agents in the world
    #size x is bigger than original matrix by 1
    move_number = random.randint(1,8)
    if move_number == 1 and human.x_position + step_size < size_x: #moving east
        human.x_position += step_size
    elif move_number == 2 and human.x_position - step_size >= 0: #moving West
        human.x_position -= step_size
    elif move_number == 3 and human.y_position + step_size < size_y: #moving North
        human.y_position += step_size
    elif move_number == 4 and human.y_position - step_size >= 0: #moving South
        human.y_position -= step_size
    elif move_number == 5 and human.y_position + step_size < size_y and human.x_position + step_size < size_x: #moving NorthEast
        human.y_position += step_size
        human.x_position += step_size
    elif move_number == 6 and human.y_position - step_size >= 0 and human.x_position - step_size >= 0: #moving SouthWest
        human.x_position -= step_size
        human.y_position -= step_size
    elif move_number == 7 and human.y_position + step_size < size_y and human.x_position - step_size >= 0: #moving NorthWest
        human.x_position -= step_size
        human.y_position += step_size
    elif move_number == 8 and human.y_position - step_size >= 0 and human.x_position + step_size < size_x: #moving SouthEast
        human.x_position += step_size
        human.y_position -= step_size
    return human

def initiate_population(population_number, size_x, size_y, initial_Infected): 
    #Initiating the population and assign them to random position in the world.
    population = list()
    for i in range(population_number):
        x= random.randint(0,size_x-1)
        y= random.randint(0,size_y-1)
        random_number = random.random()
        #initializing infected people from the beginning according to the Initially infected population percentage
        if random_number > initial_Infected:
            population.append(human("susceptible",x,y))
        else:
            population.append(human("infected",x,y))
    return population

def vaccination(human, vaccination_rate): #apply vaccination to an agent
    random_number = random.random()
    if random_number <= vaccination_rate:
        human.Vaccination()
        
def append_stats_per_step(population, i, infectedlist, recoveredlist, susceptiblelist, steps_list): 
    #appending the stats to their lists to be able to vizualize them
    infected = 0
    recovered = 0
    susceptible = 0
    steps = 0
    for q in population:
        steps += 1
        if q.status == "susceptible":
            susceptible +=1
        elif q.status == "recovered":
            recovered += 1
        elif q.status == "infected":
            infected += 1
    infectedlist.append(infected)
    recoveredlist.append(recovered)
    susceptiblelist.append(susceptible)
    steps_list.append(i)
    
def visualization(infected_list, recovered_list, susceptible_list, steps_list, steps): #creating the lineplot viz
    g = plt.figure(len(steps_list)+201)
    sns.lineplot(x=steps_list, y=infected_list, color = "red")
    sns.lineplot(x=steps_list, y=recovered_list, color = "green")
    sns.lineplot(x=steps_list, y=susceptible_list, color = "#9b870c")
    plt.legend(labels=["Infected", "Recovered", "Susceptible"])
    plt.xlim([0,steps])
    plt.ylim([0,susceptible_list[0]+recovered_list[0]+infected_list[0]])
    plt.xlabel("Days")
    plt.ylabel("Population Size")
    plt.title(f"Generation {steps_list[-1]}")
    g.show()
    plt.savefig(f'image2/{len(recovered_list)}.png')
    
def mapping(world, steps): #creating the world map
    world_copy = copy.deepcopy(world)
    f = plt.figure(steps, figsize=(6.5,6.5))
    for i in range(len(world_copy)):
        for j in range(len(world_copy[i])):
            infected = False
            recovered = False
            susceptible = False
            if len(world_copy[i][j]) == 0:
                world_copy[i][j] = 0
            else:
                for z in world_copy[i][j]:
                    if z.status == "infected":
                        infected = True
                    if z.status == "recovered":
                        recovered = True
                    if z.status == "susceptible":
                        susceptible = True
                if infected == True:
                    world_copy[i][j] = 1
                elif susceptible == True:
                    world_copy[i][j] = 3
                elif recovered == True:
                    world_copy[i][j] = 2
    my_colors = ['black', 'red', 'green', 'yellow'] # colors for 0, 1, 2 and 3
    cmap = LinearSegmentedColormap.from_list('', my_colors, len(my_colors))
    c = plt.imshow(world_copy, cmap = cmap, vmin = 0, vmax=3)
    plt.title(f"Generation {steps}")
    f.show()
    plt.savefig(f'image/{steps}.png')
    
def GIF_Maker(filenames,i): #creating GIF function
    images = list(map(lambda filename: imageio.imread(filename), filenames))
    imageio.mimsave(os.path.join(f'movie{i}.gif'), images, duration = 0.15) # modify duration as needed
    
def get_displays(n_plots, n_generations): #function for getting the number of displays. Accured from the CS51 genetic algorithm class
    displayed_plots = [1+np.floor((n_generations-1)*(i/n_plots)**2) for i in range(0, n_plots+1)]
    return displayed_plots

def phase_space(infected_list,recovered_list,susceptible_list): #creating the 3D phaseSpace
    z = [[0 for i in range(2)] for i in range(len(susceptible_list))]
    for i in range(len(susceptible_list)):
        z[i][0] = susceptible_list[i]
        z[i][1] = susceptible_list[i]
    array = np.asarray(z)
    k = plt.figure(500, figsize=(6.5,6.5))
    ax = plt.axes(projection='3d')
    ax.plot(infected_list, recovered_list, susceptible_list)
    ax.set_xlabel('Infected')
    ax.set_ylabel('Recovered')
    ax.set_zlabel('Susceptible');
    plt.savefig("test.png")
    k.show()
    
def simulation(population_number, world_x_size, world_y_size, infection_rate, #The simulation function
recovery_rate, step_size, steps, NumberOfVizList, vaccination_rate, initial_Infected):
    #initiate the population and the world
    population = initiate_population(population_number,world_x_size,world_y_size, initial_Infected)
    world = initiate_reset_world(world_y_size,world_x_size)
    #lists for tracking the numbers of the population
    infected_list, recovered_list, susceptible_list, steps_list, GIFnamesline, GIFnamesMap = list(), list(), list(), list(), list(), list()
    #looping over the number of steps that the model have to simulate (time)
    for i in range(steps):
        for j in range(population_number):
            if i != 0:
                #removing the human to be able to move it in the world
                remove_human(population[j], world)
            #move the human
            population[j] = move(population[j],world_x_size,world_y_size, step_size)
            #put the agent in the world
            populate(population[j], world)
            #apply vaccine with specific vaccination rate
            vaccination(population[j], vaccination_rate)
        for z in range(population_number):
            if population[z].status == "infected":
                #detecting people who are in the same place of infected agent
                population[z] = infection_process(population[z], recovery_rate)
                #apply infection process with infection rate
                for k in world[population[z].y_position][population[z].x_position]:
                    infection(k,infection_rate)
        #tracking the stats
        append_stats_per_step(population,i, infected_list,recovered_list,susceptible_list, steps_list)
        #creating the Vizs
        if i in NumberOfVizList or i == steps - 1:
            mapping(world,i)
            GIFnamesMap.append(f'image/{i}.png')
            GIFnamesline.append(f'image2/{len(recovered_list)}.png')
            visualization(infected_list, recovered_list, susceptible_list, steps_list, steps)
    GIF_Maker(GIFnamesMap,1)
    GIF_Maker(GIFnamesline,2)
    phase_space(infected_list,recovered_list,susceptible_list)