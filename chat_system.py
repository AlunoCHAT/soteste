import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import time
import json
from datetime import datetime
from integrated_system import IntegratedAI
import queue
import webbrowser
import random

class AIChat:
    def __init__(self):
        self.ai = IntegratedAI()
        self.ai.bootstrap()
        self.message_queue = queue.Queue()
        
        # Interface
        self.window = tk.Tk()
        self.window.title("🤖 IA Auto-Evolutiva - Chat")
        self.window.geometry("800x600")
        
        # Fontes de API para seleção aleatória
        self.api_sources = ["github", "stackoverflow", "pypi"]
        
        self.setup_ui()
        self.evolution_thread = threading.Thread(target=self.background_evolution, daemon=True)
        self.evolution_thread.start()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Área de chat
        self.chat_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=20, width=70)
        self.chat_area.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar tags para cores
        self.chat_area.tag_config("user", foreground="blue")
        self.chat_area.tag_config("ai", foreground="green")
        self.chat_area.tag_config("system", foreground="orange")
        
        # Caixa de entrada do usuário
        self.user_input = ttk.Entry(main_frame, width=60)
        self.user_input.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        self.user_input.bind("<Return>", self.process_message)
        
        # Botão de enviar
        send_button = ttk.Button(main_frame, text="Enviar", command=self.process_message)
        send_button.grid(row=1, column=1, sticky=tk.W, pady=10)
        
        # Botões de controle
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        save_button = ttk.Button(control_frame, text="💾 Salvar Estado", command=self.save_state)
        save_button.pack(side=tk.LEFT, padx=5)
        
        evolve_button = ttk.Button(control_frame, text="🧬 Forçar Evolução", command=self.force_evolution)
        evolve_button.pack(side=tk.LEFT, padx=5)

        dashboard_button = ttk.Button(control_frame, text="📊 Dashboard", command=self.show_dashboard)
        dashboard_button.pack(side=tk.LEFT, padx=5)

        # Labels de status
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.status_labels = {
            'population': ttk.Label(status_frame, text="🧬 População: 0"),
            'learning': ttk.Label(status_frame, text="📈 Taxa de Exploração: 0%"),
            'memory': ttk.Label(status_frame, text="🧠 Memórias: 0")
        }
        
        self.status_labels['population'].pack(side=tk.LEFT, padx=5)
        self.status_labels['learning'].pack(side=tk.LEFT, padx=5)
        self.status_labels['memory'].pack(side=tk.LEFT, padx=5)
        
        self.update_status_labels()
        
    def add_message(self, sender, message, tag):
        """Adiciona mensagem na área de chat"""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"[{sender}]: {message}\n", tag)
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
        
    def process_message(self, event=None):
        """Processa a mensagem do usuário"""
        message = self.user_input.get()
        if not message:
            return
            
        self.add_message("Você", message, "user")
        self.user_input.delete(0, tk.END)
        
        # Adiciona a mensagem à fila para processamento em segundo plano
        self.message_queue.put(message)

        # Processamento em uma thread separada para não travar a UI
        threading.Thread(target=self._process_message_thread, args=(message,), daemon=True).start()

    def _process_message_thread(self, message):
        """Lógica de processamento em uma thread separada"""
        
        # 1. Busca conhecimento na API (agora de forma aleatória)
        api_name = random.choice(self.api_sources)
        self.ai.learn_from_api(api_name, message)

        # 2. Gera uma solução
        solution = self.ai.generate_solution(message)
        self.add_message("IA", f"Solução: {solution}", "ai")
        
        # 3. Melhora a si mesma
        self.ai.self_improve()
        self.update_status_labels()

    def background_evolution(self):
        """Loop de evolução em segundo plano"""
        while True:
            # Seleciona uma API aleatória para buscar tópicos para auto-evolução
            api_name = random.choice(self.api_sources)
            topic = random.choice(["python", "javascript", "code patterns", "algorithms"]) # Exemplo
            
            self.ai.learn_from_api(api_name, topic)
            self.ai.self_improve()
            self.update_status_labels()
            time.sleep(600) # Evolui a cada 10 minutos
            
    def update_status_labels(self):
        """Atualiza os rótulos de status na UI"""
        try:
            self.status_labels['population'].config(
                text=f"🧬 População: {len(self.ai.evolution_engine.population)}")
            self.status_labels['learning'].config(
                text=f"📈 Taxa de Exploração: {self.ai.rl_agent.exploration_rate:.1%}")
            self.status_labels['memory'].config(
                text=f"🧠 Memórias: {len(self.ai.memory_bank)}")
        except:
            pass
    
    def force_evolution(self):
        """Força ciclo de evolução"""
        self.add_message("Sistema", "🧬 Forçando evolução...", "system")
        threading.Thread(target=self._do_evolution, daemon=True).start()
        
    def _do_evolution(self):
        self.ai.self_improve()
        best = self.ai.evolution_engine.evolve(
            lambda c: self.ai.rl_agent.evaluate_code(c), 
            generations=5
        )
        self.add_message("Sistema", f"✅ Evolução completa! Melhor indivíduo:\n{best}", "system")
    
    def save_state(self):
        """Salva estado atual"""
        # A lógica de salvar o estado do RL Agent e da neural net precisaria ser implementada
        # Atualmente apenas simula
        with open("knowledge.json", 'w') as f:
            json.dump(self.ai.memory_bank, f, indent=4)

        self.add_message("Sistema", "💾 Estado salvo com sucesso!", "system")
    
    def show_dashboard(self):
        """Gera e abre um dashboard HTML com as métricas atuais"""
        self.add_message("Sistema", "📊 Gerando dashboard...", "system")

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard IA Auto-Evolutiva</title>
            <style>
                body {{ font-family: sans-serif; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; }}
                h1 {{ color: #007bff; }}
                .metric {{ background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Dashboard da IA</h1>
                <p>Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <div class="metric">
                    <h3>Memórias (Base de Conhecimento)</h3>
                    <p>Total de memórias: <strong>{len(self.ai.memory_bank)}</strong></p>
                </div>
                <div class="metric">
                    <h3>Ciclo de Evolução</h3>
                    <p>População atual: <strong>{len(self.ai.evolution_engine.population)}</strong></p>
                    <p>Taxa de Exploração: <strong>{self.ai.rl_agent.exploration_rate:.1%}</strong></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        dashboard_file = "dashboard.html"
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        webbrowser.open_new_tab(f"file://{os.path.abspath(dashboard_file)}")
        self.add_message("Sistema", "✅ Dashboard aberto no navegador.", "system")

if __name__ == "__main__":
    chat = AIChat()
    chat.window.mainloop()