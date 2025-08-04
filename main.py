import time
import os
from agent import CodeLearningAgent
import requests
import json
from collections import defaultdict

class SelfLearningSystem:
    def __init__(self):
        self.agent = CodeLearningAgent()
        self.training_history = []
        self.api_sources = [
            "https://api.github.com/search/code",
            "https://api.stackexchange.com/2.3/search"
        ]
        
    def autonomous_learning_cycle(self):
        """Ciclo de aprendizado autônomo"""
        programming_topics = [
            "sort algorithm", "data structure", "api request",
            "file handling", "error handling", "database connection",
            "web scraping", "json parsing", "list comprehension"
        ]
        
        for topic in programming_topics:
            print(f"\n🔍 Pesquisando sobre: {topic}")
            
            # Busca exemplos
            examples = self.search_code_examples(topic)
            
            # Aprende com exemplos
            for example in examples[:5]:  # Limita para não sobrecarregar
                if example:
                    # Gera código baseado no aprendizado
                    generated = self.agent.generate_code(topic)
                    
                    # Auto-avalia
                    score = self.agent.evaluate_code(generated)
                    
                    # Aprende com o resultado
                    self.agent.learn_from_code(example, score)
                    
                    self.training_history.append({
                        'topic': topic,
                        'score': score,
                        'timestamp': time.time()
                    })
            
            # Auto-melhoria
            self.agent.improve()
            
            # Salva progresso
            self.save_progress()
            
            time.sleep(1)  # Evita rate limiting
    
    def search_code_examples(self, topic):
        """Busca exemplos de código em APIs"""
        examples = []
        
        # GitHub API
        try:
            response = requests.get(
                f"https://api.github.com/search/code?q={topic}+language:python",
                headers={'Accept': 'application/vnd.github.v3+json'}
            )
            if response.status_code == 200:
                items = response.json().get('items', [])
                for item in items[:3]:
                    # Simulação - em produção, buscaríamos o conteúdo real
                    examples.append(f"def {topic.replace(' ', '_')}():\n    # Implementation\n    pass")
        except:
            pass
            
        return examples
    
    def interactive_mode(self):
        """Modo interativo para testar a IA"""
        print("\n🤖 Sistema de IA Auto-Aprendente Iniciado!")
        print("Digite 'sair' para encerrar\n")
        
        while True:
            task = input("📝 O que você quer que eu programe? ")
            
            if task.lower() == 'sair':
                break
                
            # Gera código
            code = self.agent.generate_code(task)
            print(f"\n💻 Código gerado:\n{code}")
            
            # Auto-avalia
            score = self.agent.evaluate_code(code)
            print(f"\n📊 Auto-avaliação: {score:.2%}")
            
            # Feedback do usuário
            feedback = input("\n👍 O código está bom? (s/n): ")
            reward = 1.0 if feedback.lower() == 's' else 0.0
            
            # Aprende com feedback
            self.agent.learn_from_code(code, reward)
            self.agent.improve()
            
            print("✅ Aprendizado registrado!\n")
    
    def save_progress(self):
        """Salva progresso do aprendizado"""
        self.agent.save_knowledge(
            "C:\\Users\\elien\\Desktop\\Programação\\Criando_IA_Inteligente\\knowledge.json"
        )
        
        with open("C:\\Users\\elien\\Desktop\\Programação\\Criando_IA_Inteligente\\history.json", 'w') as f:
            json.dump(self.training_history, f, indent=2)
    
    def load_progress(self):
        """Carrega conhecimento anterior"""
        knowledge_path = "C:\\Users\\elien\\Desktop\\Programação\\Criando_IA_Inteligente\\knowledge.json"
        if os.path.exists(knowledge_path):
            with open(knowledge_path, 'r') as f:
                data = json.load(f)
                self.agent.q_table = defaultdict(lambda: defaultdict(float), data['q_table'])
                self.agent.knowledge_base = data['knowledge_base']
                self.agent.exploration_rate = data['exploration_rate']

if __name__ == "__main__":
    system = SelfLearningSystem()
    
    # Carrega conhecimento anterior se existir
    system.load_progress()
    
    # Menu principal
    print("🚀 IA Auto-Aprendente - MVP")
    print("1. Modo Interativo")
    print("2. Aprendizado Autônomo")
    print("3. Sair")
    
    choice = input("\nEscolha: ")
    
    if choice == "1":
        system.interactive_mode()
    elif choice == "2":
        system.autonomous_learning_cycle()
    
    # Salva antes de sair
    system.save_progress()
    print("\n💾 Conhecimento salvo!")
