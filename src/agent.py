import json
import random
import numpy as np
from collections import defaultdict
import requests
import ast
import re

class CodeLearningAgent:
    """
    Agente de Aprendizado por Reforço que busca e aprende com código.
    """
    def __init__(self):
        # Tabela Q para aprendizado por reforço
        self.q_table = defaultdict(lambda: defaultdict(float))
        # Base de conhecimento para armazenar padrões e snippets
        self.knowledge_base = {
            'functions': {},
            'patterns': {},
            'apis': {}
        }
        self.learning_rate = 0.1
        self.exploration_rate = 0.3
        self.discount_factor = 0.95
    
    def extract_patterns(self, code):
        """
        Extrai padrões de código, como funções e imports.
        """
        patterns = {
            'functions': re.findall(r'def\s+(\w+)\s*\([^)]*\):', code),
            'imports': re.findall(r'import\s+(\w+)|from\s+(\w+)', code),
            'classes': re.findall(r'class\s+(\w+)', code)
        }
        return patterns
    
    def learn_from_code(self, code, reward):
        """
        Atualiza a base de conhecimento e a tabela Q com um novo código.
        """
        # Esta é uma implementação conceitual. A lógica real de RL seria mais complexa.
        patterns = self.extract_patterns(code)
        
        # Simula a atualização da base de conhecimento
        for func in patterns['functions']:
            self.knowledge_base['functions'][func] = code
        
        # Simula o aprendizado da tabela Q
        # state = hash do problema, action = hash do código
        state = hash("some_state")
        action = hash(code)
        
        old_value = self.q_table[state][action]
        next_max = max(self.q_table[action].values()) if self.q_table[action] else 0
        new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (reward + self.discount_factor * next_max)
        self.q_table[state][action] = new_value

    def generate_code(self, task):
        """
        Gera um snippet de código para a tarefa.
        """
        # Usa um mix de exploração e padrões aprendidos
        if random.random() < self.exploration_rate:
            # Exploração: Cria uma solução nova
            return self._explore_new_solution(task)
        else:
            # Explotação: Usa um padrão conhecido
            return self._use_learned_patterns(task)

    def _explore_new_solution(self, task):
        """
        Cria uma solução aleatória baseada em templates simples.
        """
        templates = [
            f"def {task.replace(' ', '')}():\n    # Implementar lógica para {task}\n    pass",
            f"class {task.replace(' ', '')}():\n    def __init__(self):\\n        pass"
        ]
        return random.choice(templates)
    
    def _use_learned_patterns(self, task):
        """
        Usa padrões aprendidos da base de conhecimento.
        """
        if self.knowledge_base['functions']:
            func_name, func_code = random.choice(list(self.knowledge_base['functions'].items()))
            return func_code
        return self._explore_new_solution(task)
    
    def evaluate_code(self, code):
        """
        Auto-avalia o código gerado.
        """
        score = 0
        try:
            # Verifica a sintaxe, que é um requisito básico
            ast.parse(code)
            score += 50
            
            # Verifica se o código contém funções ou classes
            patterns = self.extract_patterns(code)
            if patterns['functions'] or patterns['classes']:
                score += 30
            if patterns['imports']:
                score += 20
                
        except SyntaxError:
            score = 0
            
        return score / 100.0  # Retorna um score entre 0 e 1
    
    def improve(self):
        """
        Melhora o agente ao reduzir a taxa de exploração.
        """
        self.exploration_rate *= 0.99
        self.exploration_rate = max(0.01, self.exploration_rate)
        
    def save_knowledge(self, filepath):
        """
        Salva o conhecimento aprendido.
        """
        knowledge_to_save = {
            'q_table': {str(k): dict(v) for k, v in self.q_table.items()},
            'knowledge_base': self.knowledge_base,
            'exploration_rate': self.exploration_rate
        }
        with open(filepath, 'w') as f:
            json.dump(knowledge_to_save, f, indent=4)