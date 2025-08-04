import time
import json
import os
import threading
import schedule
from datetime import datetime
import random
from integrated_system import IntegratedAI
import logging

logging.basicConfig(
    filename='evolution.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AutonomousEvolution:
    def __init__(self):
        self.ai = IntegratedAI()
        self.generation = 0
        self.start_time = time.time()
        self.evolution_history = []
        self.knowledge_checkpoints = []
        
        self.config = self.load_config()
        
        self.learning_curriculum = [
            ["variable", "function", "loop", "condition", "list", "dictionary"],
            ["class", "inheritance", "exception", "file handling", "regex", "decorator"],
            ["async", "generator", "metaclass", "design pattern", "algorithm", "optimization"],
            ["machine learning", "web scraping", "api development", "database", "security", "testing"]
        ]
        self.current_level = 0
        
    def load_config(self):
        config_path = "auto_config.json"
        
        default_config = {
            "evolution": {
                "population_size": 50,
                "mutation_rate": 0.2,
                "generations_per_cycle": 5,
                "elite_percentage": 0.3
            },
            "learning": {
                "exploration_rate": 0.4,
                "learning_rate": 0.02,
                "memory_size": 5000,
                "batch_size": 16
            },
            "autonomous": {
                "cycle_minutes": 30,
                "backup_hours": 12,
                "max_api_calls_hour": 50,
                "auto_expand": True,
                "api_sources": ["github", "stackoverflow", "pypi"]
            }
        }
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            if 'api_sources' not in config['autonomous']:
                config['autonomous']['api_sources'] = default_config['autonomous']['api_sources']
            return config
        else:
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config

    def autonomous_learning_cycle(self):
        logging.info(f"Iniciando ciclo autônomo da Geração {self.generation}")
        
        topic_list = self.learning_curriculum[self.current_level]
        topic = random.choice(topic_list)
        
        api_name = random.choice(self.config['autonomous']['api_sources'])
        self.ai.learn_from_api(api_name, topic)
        
        problem_description = f"Implementar um exemplo de {topic}"
        generated_code = self.ai.generate_solution(problem_description)
        
        if generated_code:
            logging.info(f"Evoluindo a solução para o tópico: {topic}")
            self.ai.self_improve()
        
        self.generation += 1
        self.current_level = (self.current_level + 1) % len(self.learning_curriculum)
        
        self.ai.save_knowledge()
        self.save_knowledge_checkpoint()
        
    def save_knowledge_checkpoint(self):
        metrics = {
            "memory_size": len(self.ai.memory_bank),
            "knowledge_functions": len(
                self.ai.rl_agent.knowledge_base.get("functions", {})
            ),
            "exploration_rate": self.ai.rl_agent.exploration_rate,
            "current_level": self.current_level,
        }
        checkpoint = {
            "timestamp": datetime.now().isoformat(),
            "generation": self.generation,
            **metrics,
        }
        self.knowledge_checkpoints.append(checkpoint)

        with open("knowledge_checkpoints.json", "w") as f:
            json.dump(self.knowledge_checkpoints, f, indent=4)

        evo_entry = {
            "timestamp": checkpoint["timestamp"],
            "generation": self.generation,
            "metrics": metrics,
        }
        self.evolution_history.append(evo_entry)
        with open("evolution_log.json", "w") as f:
            json.dump(
                {
                    "current_generation": self.generation,
                    "checkpoints": self.evolution_history,
                },
                f,
                indent=4,
            )
            
    def run_forever(self):
        logging.info("Iniciando loop de agendamento autônomo...")
        
        schedule.every(1).minutes.do(self.autonomous_learning_cycle)
        
        schedule.every(self.config['autonomous']['backup_hours']).hours.do(self.daily_backup)
        
        if not self.ai.memory_bank:
            self.ai.bootstrap()
        
        self.autonomous_learning_cycle()
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def daily_backup(self):
        backup_dir = f"backups/{datetime.now().strftime('%Y%m%d')}"
        os.makedirs(backup_dir, exist_ok=True)
        
        import shutil
        files_to_backup = [
            "knowledge.json",
            "evolution_log.json",
            "neural_weights.npz",
            "dashboard.html"
        ]
        
        for file in files_to_backup:
            src = f"{file}"
            if os.path.exists(src):
                shutil.copy2(src, backup_dir)
        
        logging.info(f"Backup completo salvo em {backup_dir}")

if __name__ == "__main__":
    print("Iniciando Sistema de Evolução Autônoma")
    print("Este sistema rodará indefinidamente. Use Ctrl+C para parar.")
    print("-" * 50)
    
    evolution = AutonomousEvolution()
    
    try:
        evolution.run_forever()
    except KeyboardInterrupt:
        print("\n\nSistema interrompido pelo usuário.")
