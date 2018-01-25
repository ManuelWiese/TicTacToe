import math
import copy
import random
import pickle
import datetime
import pygame

#
POPULATION = 150
DELTA_DISJOINT = 2.0
DELTA_WEIGHTS = 0.4
DELTA_THRESHOLD = 1.0
WEIGHT_RANGE = 2.0
BIAS_RANGE = 1.0
#
STALE_SPECIES = 15
#
PERTUBCHANCE = 0.90
CROSSOVER_CHANCE = 0.75
LINK_MUTATION_CHANCE = 2.0
NODE_MUTATION_CHANCE = 0.50
BIAS_MUTATION_CHANCE = 1.00
WEIGHT_MUTATION_CHANCE = 1.00
TRANSFER_MUTATION_CHANCE = 0.5
STEPSIZE = 0.1
DISBALE_MUTATION_CHANCE = 0.4
ENABLE_MUTATION_CHANCE = 0.2

MAX_NODES = 10000

SAVEPATH = "./save/"


class Gene:
    def __init__(self, object=None):
        if not object:
            self.into = 0
            self.out = 0
            self.weight = 0.0
            self.enabled = True
            self.innovation = 0
        else:
            self.into = object.into
            self.out = object.out
            self.weight = object.weight
            self.enabled = object.enabled
            self.innovation = object.innovation

    def print(self):
        print(self.__repr__())
        print("into: ", self.into)
        print("out: ", self.out)
        print("weight: ", self.weight)
        print("enabled: ", self.enabled)
        print("innovation: ", self.innovation)


class Neuron:
    def sigmoid(x):
        try:
            return 1.0 / (1.0 + math.exp(-1.0 * x)) - 0.0
        except OverflowError:
            if x > 0:
                return 1.0
            return 0.0

    def step(x):
        if x >= 0.0:
            return 1.0
        return 0.0

    def slope(x):
        if x >= 0.5:
            return 1.0
        if x < -0.5:
            return 0.0
        return (x + 0.5)

    def id(x):
        return x

    def __init__(self):
        self.incoming = []
        self.value = 0.0
        self.depth = -1
        self.calculated = False
        self.transfer = Neuron.sigmoid
        self.bias = 0.0

    def addIncoming(self, gene):
        self.incoming.append(gene)

    def removeIncoming(self, gene):
        if gene in self.incoming:
            self.incoming.remove(gene)
            return True
        print("Could not remove ")
        gene.print()
        for inGene in self.incoming:
            if gene.innovation == inGene.innovation:
                inGene.print()
        return False


class Genome:
    def __init__(self, object=None, pool=None):
        if not object:
            self.genes = []
            self.fitness = 0
            self.maxneuron = 0
            self.globalRank = 0
            self.mutationRates = {"weight": WEIGHT_MUTATION_CHANCE,
                                  "link": LINK_MUTATION_CHANCE,
                                  "bias": BIAS_MUTATION_CHANCE,
                                  "node": NODE_MUTATION_CHANCE,
                                  "enable": ENABLE_MUTATION_CHANCE,
                                  "disable": DISBALE_MUTATION_CHANCE,
                                  "transfer": TRANSFER_MUTATION_CHANCE,
                                  "step": STEPSIZE}
            self.pool = pool
            self.checkedLinks = {}

            self.neurons = {}
            for i in range(self.pool.inputs):
                self.neurons[i] = Neuron()

            for i in range(self.pool.outputs):
                self.neurons[MAX_NODES - self.pool.outputs + i] = Neuron()
        else:
            self.genes = copy.deepcopy(object.genes)
            self.fitness = 0
            self.maxneuron = object.maxneuron
            self.globalRank = object.globalRank
            self.mutationRates = copy.deepcopy(object.mutationRates)
            self.mutationRates["step"] = STEPSIZE
            self.pool = object.pool
            self.checkedLinks = copy.deepcopy(object.checkedLinks)
            self.neurons = {i: Neuron() for i in object.neurons}

            for i in object.neurons:
                self.neurons[i].transfer = object.neurons[i].transfer
                self.neurons[i].bias = object.neurons[i].bias

            for gene in self.genes:
                if gene.enabled:
                    self.neurons[gene.out].addIncoming(gene)

    def calculateNeuron(self, neuronNumber):
        neuron = self.neurons[neuronNumber]

        if neuron.calculated:
            return neuron.value

        tmpSum = 0.0
        for gene in neuron.incoming:
            tmpSum += gene.weight * self.calculateNeuron(gene.into)
        tmpSum += neuron.bias
        neuron.value = neuron.transfer(tmpSum)
        neuron.calculated = True
        return neuron.value

    def evaluate(self, inputs):

        for neuron in self.neurons:
            self.neurons[neuron].calculated = False

        for i in range(self.pool.inputs):
            self.neurons[i].value = inputs[i]
            self.neurons[i].calculated = True

        output = []

        for i in range(self.pool.outputs):
            self.neurons[MAX_NODES - self.pool.outputs + i].calculated = False
            self.calculateNeuron(MAX_NODES - self.pool.outputs + i)
            output.append(self.neurons[MAX_NODES
                                       - self.pool.outputs + i].value)
        return output

    def calculateNeuronDepth(self, neuronNumber):
        neuron = self.neurons[neuronNumber]

        if neuron.depth != -1:
            return neuron.depth

        for gene in neuron.incoming:
            previousDepth = self.calculateNeuronDepth(gene.into)
            if previousDepth == -1:
                continue
            if neuron.depth < previousDepth + 1:
                neuron.depth = previousDepth + 1
        return neuron.depth

    def computeDepth(self):
        for neuron in self.neurons:
            if self.neurons[neuron] is not None:
                self.neurons[neuron].depth = -1

        for i in range(self.pool.inputs):
            self.neurons[i].depth = 0

        maxDepth = 0

        for i in range(MAX_NODES - self.pool.outputs, MAX_NODES):
            self.calculateNeuronDepth(i)
            if maxDepth < self.neurons[i].depth:
                maxDepth = self.neurons[i].depth

        for i in range(MAX_NODES - self.pool.outputs, MAX_NODES):
            self.neurons[i].depth = maxDepth

        return maxDepth

    def countLayers(self):
        maxDepth = self.computeDepth()
        layer = [[] for i in range(maxDepth + 1)]

        for i in self.neurons:
            if self.neurons[i] is not None and self.neurons[i].depth != -1:
                layer[self.neurons[i].depth].append(i)

        return layer

    def plotNetwork(self):
        DISPLAY_WIDTH = 1280
        DISPLAY_HEIGHT = 800
        DISPLAY_SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

        pygame.init()
        screen = pygame.display.set_mode(DISPLAY_SIZE)
        screen.fill((255, 255, 255))

        layers = self.countLayers()

        width = len(layers)
        height = max([len(element) for element in layers])

        layerDist = DISPLAY_WIDTH/width

        neuronWidth = 0.4 * DISPLAY_WIDTH / width
        neuronHeight = 0.4 * DISPLAY_HEIGHT / height

        neuronSize = min(neuronHeight, neuronWidth)
        neuronDist = neuronSize

        for i, layer in enumerate(layers):
            x = i * layerDist
            y = DISPLAY_HEIGHT/2 + (neuronSize + neuronDist) * len(layer)/2
            for neuron in layer:
                if self.neurons[neuron].transfer == Neuron.sigmoid:
                    pygame.draw.rect(screen, (255, 0, 0), [x, y, neuronSize,
                                                           neuronSize], 1)
                elif self.neurons[neuron].transfer == Neuron.id:
                    pygame.draw.rect(screen, (0, 255, 0), [x, y, neuronSize,
                                                           neuronSize], 1)
                elif self.neurons[neuron].transfer == Neuron.step:
                    pygame.draw.rect(screen, (0, 0, 255), [x, y, neuronSize,
                                                           neuronSize], 1)
                elif self.neurons[neuron].transfer == Neuron.slope:
                    pygame.draw.rect(screen, (255, 255, 0), [x, y, neuronSize,
                                                             neuronSize], 1)
                for gene in self.neurons[neuron].incoming:
                    intoNeuron = self.neurons[gene.into]
                    index_x = intoNeuron.depth
                    if index_x == -1:
                        continue
                    index_y = layers[intoNeuron.depth].index(gene.into)
                    x1 = index_x * layerDist
                    y1 = (DISPLAY_HEIGHT/2 +
                          (neuronSize + neuronDist) *
                          (len(layers[intoNeuron.depth])/2 - index_y))
                    if gene.enabled:
                        pygame.draw.line(screen,
                                         (0, 0, 0),
                                         [x1 + neuronSize, y1+neuronSize/2],
                                         [x, y+neuronSize/2], 1)

                    else:
                        pygame.draw.line(screen,
                                         (255, 0, 0),
                                         [x1 + neuronSize,
                                          y1 + neuronSize/2],
                                         [x, y+neuronSize/2], 1)
                        gene.print()
                y -= (neuronSize + neuronDist)

        pygame.display.flip()

    def basicGenome(pool):
        genome = Genome(pool=pool)
        genome.maxneuron = pool.inputs - 1
        genome.mutate()

        return genome

    def containsGene(self, gene):
        for tmpGene in self.genes:
            if tmpGene.into == gene.into and tmpGene.out == gene.out:
                return True
        return False

    def randomNeuron(self, includeInput):
        if includeInput:
            possible = (list(range(self.pool.inputs)) +
                        list(range(self.pool.inputs, self.maxneuron + 1)) +
                        list(range(MAX_NODES - self.pool.outputs, MAX_NODES)))
        else:
            possible = (list(range(self.pool.inputs, self.maxneuron + 1)) +
                        list(range(MAX_NODES - self.pool.outputs, MAX_NODES)))

        return random.choice(possible)

    def crossover(genome1, genome2):
        if genome2.fitness > genome1.fitness:
            genome1, genome2 = genome2, genome1

        child = Genome(pool=genome1.pool)
        child.neurons = {i: Neuron() for i in genome1.neurons}
        for i in genome1.neurons:
            child.neurons[i].transfer = genome1.neurons[i].transfer
            child.neurons[i].bias = genome1.neurons[i].bias

        innovations2 = {}
        for gene2 in genome2.genes:
            innovations2[gene2.innovation] = gene2

        for gene1 in genome1.genes:
            if gene1.innovation in innovations2:
                gene2 = innovations2[gene1.innovation]
                if gene2.enabled and random.uniform(0, 1) > 0.5:
                    copyGene = Gene(gene2)
                else:
                    copyGene = Gene(gene1)
            else:
                copyGene = Gene(gene1)
            if copyGene.enabled:
                child.neurons[copyGene.out].addIncoming(copyGene)
            child.genes.append(copyGene)
        child.maxneuron = genome1.maxneuron
        child.mutationRates = copy.deepcopy(genome1.mutationRates)
        child.checkedLinks = copy.deepcopy(genome1.checkedLinks)

        return child

    def disjoint(genome1, genome2):
        if len(genome1.genes) == 0 and len(genome2.genes) == 0:
            return 0

        innovations1 = [gene.innovation for gene in genome1.genes]

        disjointGenes = len(genome1.genes)
        for gene in genome2.genes:
            if gene.innovation in innovations1:
                disjointGenes -= 1
            else:
                disjointGenes += 1

        return disjointGenes / max(len(genome1.genes), len(genome2.genes))

    def weights(genome1, genome2):
        innovations2 = {}
        for gene in genome2.genes:
            innovations2[gene.innovation] = gene

        sum = 0
        coincident = 0

        for gene in genome1.genes:
            if gene.innovation in innovations2:
                sum += abs(gene.weight - innovations2[gene.innovation].weight)
                coincident += 1
        if coincident:
            return sum / coincident
        return 0.0

    def sameSpecies(genome1, genome2):
        dd = DELTA_DISJOINT * Genome.disjoint(genome1, genome2)
        dw = DELTA_WEIGHTS * Genome.weights(genome1, genome2)

        return dd + dw < DELTA_THRESHOLD

    def weightMutate(self):
        if not len(self.genes):
            return False

        gene = random.choice(self.genes)
        if not gene.enabled:
            return False
        if random.uniform(0.0, 1.0) < PERTUBCHANCE:
            stepsize = self.mutationRates["step"]
            gene.weight += random.uniform(-stepsize, stepsize)
        else:
            gene.weight = random.uniform(-WEIGHT_RANGE,
                                         WEIGHT_RANGE)
        return True

    def isInputNeuron(self, neuronNumber):
        return (neuronNumber >= 0 and neuronNumber < self.pool.inputs)

    def isOutputNeuron(self, neuronNumber):
        return (neuronNumber >= MAX_NODES - self.pool.outputs and
                neuronNumber < MAX_NODES)

    def areConnected(self, neuron1, neuron2):
        if self.isOutputNeuron(neuron1):
            return False
        if self.isInputNeuron(neuron2):
            return False
        if (neuron1, neuron2) in self.checkedLinks:
            return self.checkedLinks[(neuron1, neuron2)]
        for gene in self.neurons[neuron2].incoming:
            if gene.into == neuron1:
                self.checkedLinks.update({(neuron1, neuron2): True})
                return True
            if self.areConnected(neuron1, gene.into):
                self.checkedLinks.update({(neuron1, neuron2): True})
                return True
        self.checkedLinks.update({(neuron1, neuron2): False})
        return False

    def linkAllowed(self, neuron1, neuron2):
        if self.isInputNeuron(neuron2):
            return False
        if self.isOutputNeuron(neuron1):
            return False
        if neuron1 == neuron2:
            return False
        if self.areConnected(neuron2, neuron1):
            return False
        return True

    def updateCheckedLinks(self, neuron1, neuron2):
        tmpDict = {}
        self.checkedLinks.update({(neuron1, neuron2): True})
        for link1 in self.checkedLinks:
            if link1[1] == neuron1 and self.checkedLinks[link1]:
                tmpDict.update({(link1[0], neuron2): True})
                for link2 in self.checkedLinks:
                        if link2[0] == neuron2 and self.checkedLinks[link2]:
                            tmpDict.update({(neuron1, link2[1]): True})
                            tmpDict.update({(link1[0], link2[1]): True})
        self.checkedLinks.update(tmpDict)

    def linkMutate(self):
        neuron1 = self.randomNeuron(True)
        neuron2 = self.randomNeuron(False)

        if not self.linkAllowed(neuron1, neuron2):
            if self.linkAllowed(neuron2, neuron1):
                neuron1, neuron2 = neuron2, neuron1
            else:
                return False

        newGene = Gene()
        newGene.into = neuron1
        newGene.out = neuron2

        if self.containsGene(newGene):
            return False

        newGene.innovation = self.pool.newInnovation()
        newGene.weight = random.uniform(-WEIGHT_RANGE, WEIGHT_RANGE)

        self.genes.append(newGene)
        self.neurons[neuron2].addIncoming(newGene)
        self.updateCheckedLinks(neuron1, neuron2)
        return True

    def nodeMutate(self):
        if len(self.genes) == 0:
            return False

        randomIndex = random.randrange(len(self.genes))

        if not self.genes[randomIndex].enabled:
            return False

        oldGene = self.genes[randomIndex]
        self.neurons[oldGene.out].removeIncoming(oldGene)
        oldGene.enabled = False

        self.maxneuron += 1

        gene1 = Gene()
        gene1.out = self.maxneuron
        gene1.into = oldGene.into
        # TODO: why not random weight?
        gene1.weight = 1.0
        gene1.innovation = self.pool.newInnovation()
        self.genes.append(gene1)
        self.neurons[gene1.out] = Neuron()
        # TODO: why not random transfer function?
        self.neurons[gene1.out].transfer = Neuron.id
        self.neurons[gene1.out].addIncoming(gene1)

        gene2 = Gene()
        gene2.out = oldGene.out
        gene2.into = self.maxneuron
        gene2.weight = oldGene.weight
        gene2.innovation = self.pool.newInnovation()
        self.genes.append(gene2)
        self.neurons[gene2.out].addIncoming(gene2)

        tmpDict = {(self.genes[randomIndex].into, self.maxneuron): True,
                   (self.maxneuron, self.genes[randomIndex].out): True}
        for link in self.checkedLinks:
            if (link[1] == self.genes[randomIndex].into
               and self.checkedLinks[link]):
                tmpDict.update({(link[0], self.maxneuron): True})
            if (link[0] == self.genes[randomIndex].out
               and self.checkedLinks[link]):
                tmpDict.update({(self.maxneuron, link[1]): True})
        self.checkedLinks.update(tmpDict)

        return True

    def enableToDisableMutate(self):
        candidates = []
        for i, gene in enumerate(self.genes):
            if gene.enabled:
                candidates.append(i)

        if len(candidates) == 0:
            return False

        gene = self.genes[random.choice(candidates)]
        self.neurons[gene.out].removeIncoming(gene)
        gene.enabled = False

        return True

    def disableToEnableMutate(self):
        candidates = []
        for i, gene in enumerate(self.genes):
            if not gene.enabled:
                candidates.append(i)

        if len(candidates) == 0:
            return False

        gene = self.genes[random.choice(candidates)]
        gene.enabled = True
        self.neurons[gene.out].addIncoming(gene)

        return True

    def transferMutate(self):
        neuron = self.randomNeuron(False)
        self.neurons[neuron].transfer = random.choice([Neuron.sigmoid,
                                                      Neuron.id,
                                                      Neuron.step,
                                                      Neuron.slope])

    def biasMutate(self):
        neuron = self.randomNeuron(False)
        if random.uniform(0.0, 1.0) < PERTUBCHANCE:
            stepsize = self.mutationRates["step"]
            self.neurons[neuron].bias += random.uniform(-stepsize, stepsize)
        else:
            self.neurons[neuron].bias = random.uniform(-BIAS_RANGE,
                                                       BIAS_RANGE)
        return True

    def mutate(self):
        for mutation in self.mutationRates:
            if random.uniform(0.0, 1.0) > 0.5:
                self.mutationRates[mutation] *= 0.95
            else:
                self.mutationRates[mutation] /= 0.95

        for mutation in ["weight", "link", "bias",
                         "node", "enable", "disable",
                         "transfer"]:
            p = self.mutationRates[mutation]
            while p > 0:
                if random.uniform(0.0, 1.0) < p:
                    if mutation == "weight":
                        self.weightMutate()
                    elif mutation == "link":
                        self.linkMutate()
                    elif mutation == "bias":
                        self.biasMutate()
                    elif mutation == "node":
                        self.nodeMutate()
                    elif mutation == "enable":
                        self.disableToEnableMutate()
                    elif mutation == "disable":
                        self.enableToDisableMutate()
                    elif mutation == "transfer":
                        self.transferMutate()
                p -= 1.0


class Species:
    def __init__(self):
        self.topFitness = 0
        self.staleness = 0
        self.genomes = []
        self.averageFitness = 0

    def calculateAverageFitness(self):
        tmpSum = 0
        for genome in self.genomes:
            tmpSum += genome.globalRank

        self.averageFitness = tmpSum / len(self.genomes)

    def breedChild(self):
        if random.uniform(0.0, 1.0) < CROSSOVER_CHANCE:
            g1 = random.choice(self.genomes)
            g2 = random.choice(self.genomes)
            child = Genome.crossover(g1, g2)
        else:
            child = Genome(object=random.choice(self.genomes))

        child.mutate()

        return child


class Pool:
    def __init__(self, inputs, outputs, filename=None, population=POPULATION):
        if filename is None:
            self.timestamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
            self.species = []
            self.generation = 0
            self.innovation = outputs
            self.currentSpecies = 0
            self.currentGenome = 0
            self.maxFitness = 0
            self.population = population
            self.inputs = inputs
            self.outputs = outputs

            for i in range(self.population):
                self.addToSpecies(Genome.basicGenome(self))

        else:
            print("Loading ", filename)
            self.load(filename)

    def save(self):
        with open(SAVEPATH + self.timestamp
                  + "_" + str(self.generation), "wb") as f:
            pickle.dump(self, f)

    def load(self, filename):
        with open(filename, "rb") as f:
            obj = pickle.load(f)

        self.timestamp = obj.timestamp
        self.species = copy.deepcopy(obj.species)
        self.generation = obj.generation
        self.innovation = obj.innovation
        self.currentSpecies = obj.currentSpecies
        self.currentGenome = obj.currentGenome
        self.maxFitness = obj.maxFitness
        self.population = obj.population
        self.inputs = obj.inputs
        self.outputs = obj.outputs

        # Both below do not work, i don't know why yet...
        # self = copy.deepcopy(obj)
        # self = obj

        self.newGeneration()

    def newInnovation(self):
        self.innovation += 1
        return self.innovation

    def rankGenomes(self):
        tmpGenomes = []
        for species in self.species:
            for genome in species.genomes:
                tmpGenomes.append(genome)
        tmpGenomes.sort(key=lambda x: x.fitness)

        for i in range(len(tmpGenomes)):
            tmpGenomes[i].globalRank = i + 1

    def getAverageFitness(self):
        tmpSum = 0
        for species in self.species:
            tmpSum += species.averageFitness

        return tmpSum / self.population

    def cullSpecies(self, cutToOne=False):
        for species in self.species:
            species.genomes.sort(key=lambda x: -x.fitness)
            if cutToOne:
                remaining = 1
            else:
                remaining = math.ceil(len(species.genomes) / 2)
            species.genomes = species.genomes[:remaining]

    def removeStaleSpecies(self):
        survived = []
        for index, species in enumerate(self.species):
            species.genomes.sort(key=lambda x: - x.fitness)

            if species.genomes[0].fitness > species.topFitness:
                species.topFitness = species.genomes[0].fitness
                species.staleness = 0
            else:
                species.staleness += 1

            if (species.staleness < STALE_SPECIES or
               species.topFitness >= self.maxFitness):
                survived.append(species)

        if not len(survived):
            self.species.sort(key=lambda x: -x.topFitness)
            survived.append(self.species[0])

        self.species = survived

    def removeWeakSpecies(self):
        survived = []
        tmpSum = self.getAverageFitness()
        for species in self.species:
            if math.floor(species.averageFitness / tmpSum) >= 1:
                survived.append(species)
        self.species = survived

    def addToSpecies(self, child):
        for species in self.species:
            if Genome.sameSpecies(species.genomes[0], child):
                species.genomes.append(child)
                break
        else:
            newSpecies = Species()
            newSpecies.genomes.append(child)
            self.species.append(newSpecies)

    def newGeneration(self):
        self.cullSpecies()
        self.rankGenomes()
        self.removeStaleSpecies()
        self.rankGenomes()

        for species in self.species:
            species.calculateAverageFitness()

        self.removeWeakSpecies()
        avgFitness = self.getAverageFitness()

        children = []

        for species in self.species:
            breed = math.floor(species.averageFitness / avgFitness) - 1
            for i in range(breed):
                children.append(species.breedChild())

        self.cullSpecies(True)

        while len(children) + len(self.species) < self.population:
            children.append(random.choice(self.species).breedChild())

        for child in children:
            self.addToSpecies(child)

        self.generation += 1

    def nextGenome(self):
        currentGenomes = self.species[self.currentSpecies].genomes
        print(self.currentSpecies, self.currentGenome,
              currentGenomes[self.currentGenome].fitness, self.maxFitness)
        self.currentGenome += 1
        if self.currentGenome >= len(currentGenomes):
            self.currentGenome = 0
            self.currentSpecies += 1
            if self.currentSpecies >= len(self.species):
                self.currentSpecies = 0
                if self.generation % 10 == 0:
                    self.save()
                self.newGeneration()
