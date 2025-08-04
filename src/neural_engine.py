import numpy as np
import json
import random
import ast
import re

def calculate_fitness(code):
    score = 0
    try:
        tree = ast.parse(code)
        score += 50
        
        lines_of_code = len(code.split('\n'))
        if lines_of_code < 50:
            score += 20
        
        patterns = {
            'functions': re.findall(r'def\s+(\w+)\s*\([^)]*\):', code),
            'classes': re.findall(r'class\s+(\w+)', code)
        }
        
        if patterns['functions'] or patterns['classes']:
            score += 30

    except SyntaxError:
        score = 0
        
    return score / 100.0

class MicroNeuralNetwork:
    def __init__(self, input_size=12, hidden_size=6, output_size=3):
        self.weights1 = np.random.randn(input_size, hidden_size) * 0.1
        self.weights2 = np.random.randn(hidden_size, output_size) * 0.1
        self.learning_rate = 0.01
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def encode_code(self, code_text):
        features = [
            len(code_text),
            code_text.count('def'),
            code_text.count('class'),
            code_text.count('if'),
            code_text.count('for'),
            code_text.count('while'),
            code_text.count('try'),
            code_text.count('import'),
            code_text.count('\n'),
            len(code_text.split()),
            code_text.count('('),
            code_text.count('{')
        ]
        return np.array(features[:12])
    
    def forward(self, X):
        X = np.reshape(X, (1, -1))
        self.layer1 = self.sigmoid(np.dot(X, self.weights1))
        self.output = self.sigmoid(np.dot(self.layer1, self.weights2))
        return self.output.flatten()
    
    def train(self, codes, labels, epochs):
        for epoch in range(epochs):
            for code, label in zip(codes, labels):
                X = self.encode_code(code)
                y = np.array(label)
                
                output = self.forward(X)
                
                error = y - output
                d_output = error * self.sigmoid_derivative(output)
                
                error_hidden = np.dot(d_output, self.weights2.T)
                d_hidden = error_hidden * self.sigmoid_derivative(self.layer1.flatten())
                
                self.weights2 += self.learning_rate * np.dot(self.layer1.T, d_output.reshape(-1, 1))
                self.weights1 += self.learning_rate * np.dot(X.reshape(-1, 1), d_hidden.reshape(1, -1))
                
    def predict_quality(self, code):
        X = self.encode_code(code)
        return self.forward(X)

class CodeEvolutionEngine:
    def __init__(self):
        self.population = []
        self.population_size = 100
        self.mutation_rate = 0.1
        self.elite_percentage = 0.1
    
    def create_random_individual(self):
        func_name = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=5))
        return f"def {func_name}():\n    pass"

    def mutate(self, code):
        if random.random() < self.mutation_rate:
            lines = code.split('\n')
            if len(lines) > 1:
                line_index = random.randint(1, len(lines) - 1)
                
                mutation_types = [
                    lambda l: f"    # Mutação: {l.strip()}",
                    lambda l: f"    print('mutado')",
                    lambda l: f"    {l.strip()}",
                ]
                
                mutated_line = random.choice(mutation_types)(lines[line_index])
                lines[line_index] = mutated_line
                
                for i in range(1, len(lines)):
                    if not lines[i].startswith('    '):
                        lines[i] = '    ' + lines[i].strip()
                
                return '\n'.join(lines)
        return code
    
    def crossover(self, parent1, parent2):
        lines1 = parent1.split('\n')
        lines2 = parent2.split('\n')
        
        crossover_point = random.randint(1, min(len(lines1), len(lines2)) -1)
        
        child_lines = lines1[:crossover_point] + lines2[crossover_point:]
        return '\n'.join(child_lines)
    
    def evolve(self, fitness_func=calculate_fitness, generations=10):
        if not self.population:
            self.population = [self.create_random_individual() for _ in range(self.population_size)]
        
        for gen in range(generations):
            fitness_scores = [fitness_func(code) for code in self.population]
            
            num_elite = int(self.population_size * self.elite_percentage)
            elite_indices = np.argsort(fitness_scores)[-num_elite:]
            survivors = [self.population[i] for i in elite_indices]
            
            new_population = survivors.copy()
            
            attempts = 0
            max_attempts = self.population_size * 10
            
            while len(new_population) < self.population_size and attempts < max_attempts:
                parent1 = random.choice(survivors)
                parent2 = random.choice(survivors)
                
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                
                try:
                    ast.parse(child)
                    new_population.append(child)
                except SyntaxError:
                    pass
                
                attempts += 1

            self.population = new_population
        
        best_code = self.population[0]
        best_score = fitness_func(best_code)
        for code in self.population:
            score = fitness_func(code)
            if score > best_score:
                best_code = code
                best_score = score
                
        return best_code