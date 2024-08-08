import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



SIZE = 300  # x/y dimensions of the field
WRAP = True  # fence; when moving beyond the border
R_OFFSPRING = 2  # num of rabbit offsprings when reproduce
F_OFFSPRING = 1 # num of fox offsprings when reproduce
GRASS_RATE = 0.1  # prof of grass growing at any given loc
INIT_RABBITS = 10  # num of starting rabbits
INIT_FOXES = 2  # num of starting foxes
SPEED = 1  # num of generation per frame



class Animal:
    def __init__(self, species):
        self.species = species
        # x, y = coordinate
        self.x = random.randrange(0, SIZE)
        self.y = random.randrange(0, SIZE)

        # type of species
        if species == 'rabbit':
            # amount of grass eaten
            self.eaten = 0
        elif species == 'fox':
            # level of hunger - how long has the fox gone without eating (default max 10)
            self.hunger = 10

    def reproduce(self):
        """ after reproduce, both species hunger goes back to 0"""
        if self.species == 'rabbit':
            self.eaten = 0
        elif self.species == 'fox':
            self.hunger = 10
        return copy.deepcopy(self)

    def eat(self, amount):
        # rabbit's eaten level --> fed
        if self.species == 'rabbit':
            self.eaten += amount
        # fox's hunger resets
        elif self.species == 'fox':
            self.hunger = 0

    def move(self):
        if self.species == 'rabbit':
            max_move = 1
        elif self.species == 'fox':
            max_move = 2
  

        if WRAP:
            self.x = (self.x + random.choice([-max_move, 0, max_move])) % SIZE
            self.y = (self.y + random.choice([-max_move, 0, max_move])) % SIZE
        else:
            self.x = min(SIZE - 1, max(0, (self.x + random.choice([-max_move, 0, max_move]))))
            self.y = min(SIZE - 1, max(0, (self.y + random.choice([-max_move, 0, max_move]))))

        # every time a fox moves, it gets hungrier
        if self.species == 'fox':
            self.hunger += 1

    def can_eat(self, other):
        if self.species == 'fox' and other.species == 'rabbit':
            return self.x == other.x and self.y == other.y


class Field:
    """Field is a patch of grass with 0 or more rabbits hopping around in search of grass"""

    def __init__(self):
        self.rabbits = []
        self.foxes = []
        self.field = np.ones(shape=(SIZE, SIZE), dtype=int)

    def add_animal(self, animal):
        if animal.species == 'rabbit':
            self.rabbits.append(animal)
        elif animal.species == 'fox':
            self.foxes.append(animal)

    def move(self):
        for rabbit in self.rabbits:
            rabbit.move()
        for fox in self.foxes:
            fox.move()

    def eat(self):
        for fox in self.foxes:
            for rabbit in self.rabbits:
                if fox.can_eat(rabbit):
                    self.rabbits.remove(rabbit)
                    fox.eat(-1)  # Increase fox's hunger after eating a rabbit
                    break
            fox.eat(self.field[fox.x, fox.y])
            self.field[fox.x, fox.y] = 0
        
        for rabbit in self.rabbits:
            rabbit.eat(self.field[rabbit.x, rabbit.y])
            self.field[rabbit.x, rabbit.y] = 0

    def survive(self):
        self.rabbits = [rabbit for rabbit in self.rabbits if rabbit.eaten > 0]
        self.foxes = [fox for fox in self.foxes if fox.hunger < 10]

    def reproduce(self):
        new_rabbits = []
        for rabbit in self.rabbits:
            for _ in range(random.randint(0, R_OFFSPRING)):
                new_rabbit = rabbit.reproduce()
                new_rabbits.append(new_rabbit)
        self.rabbits += new_rabbits

        new_foxes = []
        for fox in self.foxes:
            for _ in range(random.randint(0, F_OFFSPRING)):
                new_fox = fox.reproduce()
                new_foxes.append(new_fox)
        self.foxes += new_foxes

    def grow(self):
        growloc = (np.random.rand(SIZE, SIZE) < GRASS_RATE) * 1
        self.field = np.maximum(self.field, growloc)

    def generation(self):
        self.move()
        self.eat()
        self.survive()
        self.reproduce()
        self.grow()

def animate(i, field, im):
    for _ in range(SPEED):
        field.generation()

    # Create an empty image array
    im_array = np.zeros((SIZE, SIZE, 3))  # RGB image array

    # Set the color for grass
    for x in range(SIZE):
        for y in range(SIZE):
            if field.field[x, y] == 0:  # Grass eaten
                im_array[x, y] = [0.8, 0.6, 0.4]  # Tan color
            else:
                im_array[x, y] = [160/255, 215/255, 180/255]  # Light green color

    # Set the positions and colors for rabbits
    for rabbit in field.rabbits:
        x, y = rabbit.x, rabbit.y
        im_array[x, y] = [1, 0, 0]  # Rabbit color (red)

    # Set the positions and colors for foxes
    for fox in field.foxes:
        x, y = fox.x, fox.y
        im_array[x, y] = [0, 0, 1]  # Fox color (blue)

    # Update the image array
    im.set_array(im_array)

    # Update the title with generation and population information
    plt.title('Generation: ' + str(i * SPEED) + ' Rabbits: ' + str(len(field.rabbits)) + ' Foxes: ' + str(len(field.foxes)))

    return im,



def main():
    field = Field()

    # Initialize with some rabbits
    for _ in range(INIT_RABBITS):
        field.add_animal(Animal('rabbit'))

    # Initialize with some foxes
    for _ in range(INIT_FOXES):
        field.add_animal(Animal('fox'))

    array = np.zeros(shape=(SIZE, SIZE), dtype=int)
    fig = plt.figure(figsize=(10, 10))
    im = plt.imshow(array, cmap='YlGnBu', interpolation='hamming', aspect='auto',
                    vmin=0, vmax=1)

    anim = animation.FuncAnimation(fig, animate, fargs=(field, im), frames=10**100, interval=1)
    plt.show()


if __name__ == '__main__':
    main()
