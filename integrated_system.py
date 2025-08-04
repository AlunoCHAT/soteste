import numpy as np
from src.agent import CodeLearningAgent
from src.neural_engine import (
    MicroNeuralNetwork,
    CodeEvolutionEngine,
    calculate_fitness,
)
import json
import os
import requests
import random
import logging
import base64
from datetime import datetime

API_KEYS = {
    "github": "chave_aqui"
}

class IntegratedAI:
    def __init__(self):
        self.rl_agent = CodeLearningAgent()
        self.neural_net = MicroNeuralNetwork()
        self.evolution_engine = CodeEvolutionEngine()
        self.memory_bank = []
        self.knowledge_file = "knowledge.json"
        
        self.load_knowledge()

    def load_knowledge(self):
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, 'r') as f:
                    data = json.load(f)
                    self.memory_bank = data.get('memory_bank', [])
                    logging.info(f"Conhecimento carregado. {len(self.memory_bank)} memórias recuperadas.")
            except (IOError, json.JSONDecodeError) as e:
                logging.error(f"Erro ao carregar knowledge.json: {e}. Iniciando com memórias vazias.")
        else:
            logging.info("Nenhum arquivo knowledge.json encontrado. Iniciando com memórias vazias.")

    def save_knowledge(self):
        try:
            with open(self.knowledge_file, 'w') as f:
                data = {
                    'memory_bank': self.memory_bank,
                    'timestamp': datetime.now().isoformat()
                }
                json.dump(data, f, indent=4)
                logging.info(f"Conhecimento salvo. {len(self.memory_bank)} memórias armazenadas.")
        except IOError as e:
            logging.error(f"Erro ao salvar knowledge.json: {e}")

    def learn_from_api(self, api_name, query):
        print(f"Consultando API '{api_name}' com a query: '{query}'")
        
        try:
            if api_name == "github":
                github_key = API_KEYS.get("github")
                if not github_key or github_key == "SUA_CHAVE_DO_GITHUB_AQUI":
                    print("Erro: Chave da API do GitHub não está configurada ou é inválida.")
                    return
                
                url = f"https://api.github.com/search/code?q={query}+language:python"
                headers = {
                    'Accept': 'application/vnd.github.v3+json',
                    'Authorization': f'token {github_key}'
                }
                
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                results = response.json()
                
                if results and 'items' in results:
                    print(f"Encontrei {len(results['items'])} exemplos no GitHub.")
                    for item in results['items'][:3]:
                        try:
                            file_info = requests.get(item['url'], headers=headers)
                            file_info.raise_for_status()
                            file_data = file_info.json()

                            code_content = ""
                            if file_data.get('content'):
                                code_content = base64.b64decode(
                                    file_data['content']
                                ).decode('utf-8', errors='ignore')
                            elif file_data.get('download_url'):
                                raw = requests.get(file_data['download_url'])
                                if raw.status_code == 200:
                                    code_content = raw.text

                            self.memory_bank.append({
                                'source': 'github',
                                'query': query,
                                'learning': {
                                    'url': item['html_url'],
                                    'code': code_content,
                                },
                            })
                        except Exception as e:
                            logging.error(f"Falha ao obter código do GitHub: {e}")
            
            elif api_name == "stackoverflow":
                url = f"https://api.stackexchange.com/2.3/search/advanced?q={query}&site=stackoverflow"
                response = requests.get(url)
                response.raise_for_status()
                results = response.json()
                
                if results and 'items' in results:
                    print(f"Encontrei {len(results['items'])} exemplos no StackOverflow.")
                    for item in results['items'][:3]:
                        self.memory_bank.append({
                            'source': 'stackoverflow',
                            'query': query,
                            'learning': item
                        })
                        
            elif api_name == "pypi":
                test_url = f"https://pypi.org/pypi/{query.replace(' ', '-')}/json"
                test_response = requests.get(test_url)
                
                if test_response.status_code == 200:
                    results = test_response.json()
                    print(f"Encontrei o pacote '{results['info']['name']}' no PyPI.")
                    self.memory_bank.append({
                        'source': 'pypi',
                        'query': query,
                        'learning': results
                    })
                else:
                    print(f"Nenhum pacote exato encontrado no PyPI para a query: '{query}'.")

        except requests.exceptions.HTTPError as err:
            logging.error(f"Erro na requisição para {api_name}: {err}")
            print(f"Erro na requisição para {api_name}: {err}")
        except json.JSONDecodeError as err:
            logging.error(f"Erro ao decodificar JSON para {api_name}: {err}")
            print(f"Erro ao decodificar JSON para {api_name}: {err}")
        except Exception as err:
            logging.error(f"Ocorreu um erro inesperado: {err}")
            print(f"Ocorreu um erro inesperado: {err}")
            
    def generate_solution(self, problem):
        print(f"\nPensando em: {problem}")
        
        rl_solution = self.rl_agent.generate_code(problem)
        quality = self.neural_net.predict_quality(rl_solution)
        
        if quality[0] < 0.5:
            print("Evoluindo solução...")
            evolved_solution = self.evolution_engine.evolve(
                fitness_func=calculate_fitness,
                generations=10
            )
            self.neural_net.train(codes=[evolved_solution], labels=[[1, 0, 0]], epochs=1)
            return evolved_solution
        
        return rl_solution
        
    def self_improve(self):
        if not self.memory_bank:
            return

        sample = random.choice(self.memory_bank)
        code = sample.get('learning', {}).get('code')
        if not code:
            return

        reward = self.rl_agent.evaluate_code(code)
        self.rl_agent.learn_from_code(code, reward)
        self.neural_net.train([code], [[1, 0, 0]], epochs=1)
        self.rl_agent.improve()
        logging.info("Auto aprimoramento realizado a partir de novo conhecimento.")
        
    def bootstrap(self):
        print("Bootstrapping IA...")
        
        basic_concepts = [
            "hello world", "loop", "function", "class",
            "list", "dictionary", "file read", "api call"
        ]
        
        api_sources = ["github", "stackoverflow", "pypi"]
        
        for concept in basic_concepts:
            api_name = random.choice(api_sources)
            self.learn_from_api(api_name, concept)
            
        self.self_improve()
        self.save_knowledge()
        print("Bootstrap completo!")

if __name__ == "__main__":
    print("IA Auto-Aprendente - Sistema Integrado\n")
    
    ai = IntegratedAI()
    
    if not ai.memory_bank:
        ai.bootstrap()
    
    while True:
        task = input("\nO que devo aprender/programar? (ou 'sair'): ")
        
        if task.lower() == 'sair':
            break
            
        api_sources = ["github", "stackoverflow", "pypi"]
        api_name = random.choice(api_sources)
        ai.learn_from_api(api_name, task)
        ai.save_knowledge()
        
        solution = ai.generate_solution(task)
        print(f"\nSolução:\n{solution}")
