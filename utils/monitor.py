import time
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

class RealTimeMonitor:
    """Monitor em tempo real do progresso da IA"""
    
    def __init__(self, window_size=100):
        self.window_size = window_size
        self.metrics = {
            'knowledge': deque(maxlen=window_size),
            'quality': deque(maxlen=window_size),
            'exploration': deque(maxlen=window_size),
            'memory': deque(maxlen=window_size),
            'time': deque(maxlen=window_size)
        }
        
        # Setup do plot
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.suptitle('IA Auto-Evolutiva - Monitor em Tempo Real')
        
    def read_metrics(self):
        """Lê métricas dos arquivos"""
        try:
            # Lê knowledge.json
            if os.path.exists('knowledge.json'):
                with open('knowledge.json', 'r') as f:
                    data = json.load(f)
                    knowledge_count = len(data.get('knowledge_base', {}).get('functions', {}))
                    exploration_rate = data.get('exploration_rate', 0)
            else:
                knowledge_count = 0
                exploration_rate = 0.3
                
            # Lê evolution_log.json
            if os.path.exists('evolution_log.json'):
                with open('evolution_log.json', 'r') as f:
                    evo_data = json.load(f)
                    checkpoints = evo_data.get('checkpoints', [])
                    if checkpoints:
                        last_checkpoint = checkpoints[-1]
                        memory_size = last_checkpoint.get('metrics', {}).get('memory_size', 0)
                    else:
                        memory_size = 0
            else:
                memory_size = 0
                
            # Calcula qualidade média (simulada por enquanto)
            quality = min(1.0, knowledge_count / 100)
            
            # Adiciona aos históricos
            current_time = datetime.now()
            self.metrics['time'].append(current_time)
            self.metrics['knowledge'].append(knowledge_count)
            self.metrics['quality'].append(quality)
            self.metrics['exploration'].append(exploration_rate)
            self.metrics['memory'].append(memory_size)
            
        except Exception as e:
            print(f"Erro ao ler métricas: {e}")
    
    def update_plots(self, frame):
        """Atualiza os gráficos"""
        self.read_metrics()
        
        # Limpa axes
        for ax in self.axes.flat:
            ax.clear()
        
        # Converte tempo para segundos desde início
        if len(self.metrics['time']) > 0:
            start_time = self.metrics['time'][0]
            time_values = [(t - start_time).total_seconds() for t in self.metrics['time']]
            
            # Plot 1: Conhecimento
            self.axes[0, 0].plot(time_values, list(self.metrics['knowledge']), 'b-')
            self.axes[0, 0].set_title('📚 Funções Aprendidas')
            self.axes[0, 0].set_xlabel('Tempo (s)')
            self.axes[0, 0].set_ylabel('Quantidade')
            self.axes[0, 0].grid(True, alpha=0.3)
            
            # Plot 2: Qualidade
            self.axes[0, 1].plot(time_values, list(self.metrics['quality']), 'g-')
            self.axes[0, 1].set_title('⭐ Qualidade Média')
            self.axes[0, 1].set_xlabel('Tempo (s)')
            self.axes[0, 1].set_ylabel('Score (0-1)')
            self.axes[0, 1].set_ylim(0, 1)
            self.axes[0, 1].grid(True, alpha=0.3)
            
            # Plot 3: Taxa de Exploração
            self.axes[1, 0].plot(time_values, list(self.metrics['exploration']), 'r-')
            self.axes[1, 0].set_title('🔍 Taxa de Exploração')
            self.axes[1, 0].set_xlabel('Tempo (s)')
            self.axes[1, 0].set_ylabel('Taxa')
            self.axes[1, 0].set_ylim(0, 1)
            self.axes[1, 0].grid(True, alpha=0.3)
            
            # Plot 4: Memória
            self.axes[1, 1].plot(time_values, list(self.metrics['memory']), 'm-')
            self.axes[1, 1].set_title('🧠 Tamanho da Memória')
            self.axes[1, 1].set_xlabel('Tempo (s)')
            self.axes[1, 1].set_ylabel('Itens')
            self.axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
    def start_monitoring(self):
        """Inicia monitoramento em tempo real"""
        print("📊 Monitor em Tempo Real Iniciado")
        print("Feche a janela para parar o monitoramento")
        
        # Animação que atualiza a cada 5 segundos
        ani = animation.FuncAnimation(
            self.fig, 
            self.update_plots, 
            interval=5000,  # 5 segundos
            cache_frame_data=False
        )
        
        plt.show()

if __name__ == "__main__":
    # Verifica se matplotlib está instalado
    try:
        import matplotlib
        monitor = RealTimeMonitor()
        monitor.start_monitoring()
    except ImportError:
        print("⚠️  Matplotlib não instalado!")
        print("Para usar o monitor, instale com: pip install matplotlib")
        print("\nVocê também pode verificar o progresso em:")
        print("- dashboard.html (abra no navegador)")
        print("- evolution.log (log detalhado)")
