#!/usr/bin/env python3
import random
import math

from llmtest.explorers import Explorer
from llmtest.techniques import Technique
from llmtest.transforms import Transform

class SimulatedAnnealing(Explorer):
    def __init__(self, techniques: list[Technique]) -> None:
        self.transform_length = 3
        self.scores: list[tuple[Technique, float]] = []

        # Cooling schedule stuff
        self.start_temperature = 1
        self.base_temperature = self.start_temperature

        # Iteration stuff
        self.current_iteration = -1
        self.max_iterations = 100
        self.current_transform = None # This is the current state
        self.current_score = 0.0 # This is the current "energy"

        # Restart stuff
        self.best_transform = None # Used for restarts, if no better one has been found in a while
        self.best_score = 0.0 # Used for restarts.
        self.last_reset = 0
        self.max_bad_steps = min(round(self.max_iterations * 0.1), 10) # Take 10% of max_iterations but max 10

        self.stop_score = 1 # The satisfying score to end the process, if found before max_iterations

        super().__init__(techniques)

    def __len__(self) -> int:
        return self.max_iterations

    def generateInitialTransforms(self) -> list[Transform]:
        """
        Generates the initial starting transform randomly
        """                                                  
        return [ self.__generateRandomTransform() ]


    def __generateRandomTransform(self) -> Transform:
        return Transform(list(random.sample(self.techniques, min(self.transform_length, len(self.techniques)))))


    def seedScore(self, result: float) -> None:
        self.__handleIteration(result)


    def __handleIteration(self, score: float) -> None:
        self.current_iteration += 1
        if score >= self.stop_score:
            self._setMessage("Found satisfying score, terminating early")
            return
        if self.current_iteration == self.max_iterations:
            return
        
        temperature = self.__temperature()
        new_transform = self.transforms[self.current_iteration]
        # Special case of first run
        if self.current_iteration == 0:
            self.current_score = score
            self.current_transform = new_transform
            self.best_score = score
            self.best_transform = self.current_transform
            self.last_reset = self.current_iteration
        # Handle all other runs
        else:
            delta_score = score - self.current_score
            if self.__accept(delta_score, temperature):
                self.current_score = score
                self.current_transform = new_transform

                # Handle restart logic
                if score >= self.best_score:
                    if score > self.best_score:
                        self._setMessage(f"Found new best score: {score*100:.2f} %")
                    self.best_score = score
                    self.best_transform = new_transform
                    self.last_reset = self.current_iteration
                else:
                    if self.current_iteration - self.last_reset > self.max_bad_steps:
                        self.__restart()
        # Choose new state for next iteration
        self.transforms.append(self.__chooseNeighbour(temperature, self.current_transform))


    def __temperature(self) -> float:
        return self.base_temperature * (1 - (self.current_iteration / self.max_iterations))
    
    
    def __accept(self, delta_score: float, temperature: float) -> bool:
        if delta_score > 0:
            # Auto accept, if the new state is better
            return True
        else:
            prob = math.exp(delta_score/temperature)
            return prob >= random.random()
        
    
    def __reheat(self, target_fraction: float = 0.6):
        target_temp = self.start_temperature * target_fraction
        required_base = target_temp / (1 - (self.current_iteration / self.max_iterations))
        self.base_temperature = required_base


    def __restart(self) -> None:
        if random.random() < 0.3: # 30 % chance of restarting from a completely random transform
            self.current_transform = self.__generateRandomTransform()
        # If it has not gotten better for the past max_bad_steps iterations, restart from best transform
        else:
            self.current_score = self.best_score
            self.current_transform = self.best_transform
            # Reheat, but only if cold
            if self.__temperature() < self.start_temperature * 0.65:
                self.__reheat(0.65)
        self.last_reset = self.current_iteration


    def __chooseNeighbour(self, temperature: float, transform) -> Transform:
        """
        Choose one of the 4 defined changes to the current transform. 
        At low temperatures only small changes are allowed.
        """
        # Take a sample and scale it down with the temperature "progress"
        sample = random.random() * (temperature/self.start_temperature) 
        # The probabilities of doing the transforms in order: Swap cons, Swap non cons, Exchange in class, Exchange outside class
        probabilities = [0.05, 0.15, 0.35, 0.45]
        if sample > sum(probabilities[:3]):
            # Exchange a random technique, with one from another class
            new_transform = self.__exchangeFromOutsideClass(transform)
        elif sample > sum(probabilities[:2]):
            # Exchange a random technique, with one from same class
            new_transform = self.__exchangeFromClass(transform)
        elif sample > probabilities[0]:
            # Swap two random, non consecutive techniques
            new_transform = self.__swapNonConsecutive(transform)
        else:
            # Swap two consecutive techniques
            new_transform = self.__swapConsecutive(transform)

        return new_transform
    
    
    def __exchangeFromOutsideClass(self, transform: Transform) -> Transform:
        """
        The highest distance change, that changes a random technique with one from a different class
        """
        transform_techniques = transform.getTechniques().copy()
        # Choose random index
        index = random.randint(0, len(transform_techniques) - 1)
        tech_class = transform_techniques[index].getTechniqueClass()
        # Select a random new technique, from techniques
        new_technique = random.choice(list(filter(lambda x: x.getTechniqueClass() != tech_class and x not in transform_techniques, self.techniques)))
        # Overwrite the new technique at index
        transform_techniques[index] = new_technique
        return Transform(transform_techniques)
    
    
    def __exchangeFromClass(self, transform: Transform) -> Transform:
        """
        The second highest distance change, that changes a random technique with one from the same class that is not already included
        """
        transform_techniques = transform.getTechniques().copy()
        # Construct a dictionary, with a list of all possibly swaps keyed by index in transform technique list.
        possible_moves = { 
            index:list(filter(
                lambda tech: tech.getTechniqueClass() == technique.getTechniqueClass() and tech not in transform_techniques, 
                self.techniques
            )) 
            for (index, technique) in enumerate(transform_techniques) 
        }
        # Filter away all indexes, with no possible swaps
        possible_moves = dict(filter(lambda pair: len(pair[1]) > 0, possible_moves.items()))

        # If possible, make a swap
        if len(possible_moves.keys()) > 0:
            index = random.choice(list(possible_moves.keys()))
            transform_techniques[index] = random.choice(possible_moves[index])
        
        return Transform(transform_techniques)

    
    def __swapNonConsecutive(self, transform: Transform) -> Transform:
        """
        The second smallest distance change, that swaps the order of any two non consecutive techniques in the transform
        """
        transform_techniques = transform.getTechniques().copy()
        # If there is only two techniques, swap them. If there is one, do nothing
        if len(transform_techniques) <= 2:
            return self.__swapConsecutive(transform)
        else:
            indexes = list(range(len(transform_techniques)))
            # Construct of dictionairy, with keys as indexes and values as a list of valid index swaps for key index
            possible_moves = {
                index:list(filter(
                    lambda i: i < index -1 or i > index + 1,
                    indexes
                ))
                for index in indexes
            }
            possible_moves = dict(filter(lambda pair: len(pair[1]) > 0, possible_moves.items()))
            a = random.choice(list(possible_moves.keys()))
            b = random.choice(possible_moves[a])
            transform_techniques[a], transform_techniques[b] = transform_techniques[b], transform_techniques[a]
            return Transform(transform_techniques)

    
    def __swapConsecutive(self, transform: Transform) -> Transform:
        """
        The smallest distance change, that swaps the order of two consecutive techniques in the transform
        """
        transform_techniques = transform.getTechniques().copy()
        if len(transform_techniques) > 1:
            index = random.randint(0, len(transform_techniques) - 2) # Don't include the last index, since we can not swap later than the end
            # Swap the two values
            transform_techniques[index], transform_techniques[index + 1] = transform_techniques[index + 1], transform_techniques[index]

        return Transform(transform_techniques)
