#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correção e Otimização do Sistema de IA Auto-Evolutiva
Identifica e corrige problemas que podem impedir a evolução contínua
"""

import os
import json
import time
import subprocess
import signal
from datetime import datetime

def verificar_problemas():
    """Identifica possíveis problemas no sistema"""
    print("🔍 Verificando problemas potenciais...")
    
    problemas = []
    
    # 1. Verifica se há exceções não tratadas
    if os.path.exists("evolution.log"):
        with open("evolution.log", "r") as f:
            linhas = f.readlines()
        
        erros = [linha for linha in linhas if "ERROR" in linha or "Exception" in linha]
        if erros:
            problemas.append(f"❌ {len(erros)} erros encontrados no log")
    
    # 2. Verifica se o sistema está travado
    if os.path.exists("evolution_log.json"):
        with open("evolution_log.json", "r") as f:
            evolution = json.load(f)
        
        checkpoints = evolution.get("checkpoints", [])
        if checkpoints:
            ultimo_checkpoint = checkpoints[-1]
            timestamp = ultimo_checkpoint.get("timestamp", "")
            
            # Verifica se o último checkpoint é muito antigo
            try:
                from datetime import datetime
                ultima_atualizacao = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                agora = datetime.now()
                diferenca = agora - ultima_atualizacao
                
                if diferenca.total_seconds() > 3600:  # Mais de 1 hora
                    problemas.append(f"⚠️ Sistema pode estar travado - último update há {diferenca.total_seconds()/3600:.1f} horas")
            except:
                pass
    
    # 3. Verifica se há processos órfãos
    try:
        import psutil
        processos_autonomous = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if 'autonomous_evolution' in cmdline:
                        processos_autonomous.append(proc.info['pid'])
            except:
                pass
        
        if len(processos_autonomous) > 2:
            problemas.append(f"⚠️ Múltiplos processos autonomous_evolution detectados: {len(processos_autonomous)}")
    except ImportError:
        pass
    
    return problemas

def corrigir_problemas():
    """Corrige problemas identificados"""
    print("🔧 Aplicando correções...")
    
    # 1. Limpa processos duplicados
    try:
        import psutil
        processos_para_terminar = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if 'autonomous_evolution' in cmdline:
                        processos_para_terminar.append(proc.info['pid'])
            except:
                pass
        
        # Mantém apenas o processo mais recente
        if len(processos_para_terminar) > 1:
            print(f"🔄 Terminando {len(processos_para_terminar)-1} processos duplicados...")
            for pid in processos_para_terminar[1:]:
                try:
                    psutil.Process(pid).terminate()
                    time.sleep(1)
                except:
                    pass
    except ImportError:
        pass
    
    # 2. Corrige configurações se necessário
    if os.path.exists("auto_config.json"):
        with open("auto_config.json", "r") as f:
            config = json.load(f)
        
        # Ajusta configurações para melhor performance
        config['autonomous']['cycle_minutes'] = 30  # Ciclos mais frequentes
        config['learning']['exploration_rate'] = 0.4  # Mais exploração
        config['evolution']['mutation_rate'] = 0.15  # Mais mutação
        
        with open("auto_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("✅ Configurações otimizadas")
    
    # 3. Limpa logs antigos se muito grandes
    if os.path.exists("evolution.log"):
        tamanho = os.path.getsize("evolution.log")
        if tamanho > 1024 * 1024:  # Mais de 1MB
            print("🧹 Limpando log antigo...")
            with open("evolution.log", "w") as f:
                f.write(f"# Log limpo em {datetime.now()}\n")
    
    print("✅ Correções aplicadas")

def reiniciar_sistema():
    """Reinicia o sistema de forma limpa"""
    print("🚀 Reiniciando sistema...")
    
    # 1. Para processos existentes
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if 'autonomous_evolution' in cmdline:
                        print(f"🛑 Terminando processo {proc.info['pid']}")
                        proc.terminate()
                        time.sleep(2)
            except:
                pass
    except ImportError:
        pass
    
    # 2. Inicia novo processo
    print("🔄 Iniciando novo processo...")
    subprocess.Popen([
        "python", "autonomous_evolution.py"
    ], cwd=os.getcwd())
    
    print("✅ Sistema reiniciado")

def otimizar_configuracao():
    """Otimiza configurações para melhor evolução"""
    print("⚙️ Otimizando configurações...")
    
    config_otimizada = {
        "evolution": {
            "population_size": 50,  # Reduzido para melhor performance
            "mutation_rate": 0.2,   # Mais mutação
            "generations_per_cycle": 5,  # Ciclos mais rápidos
            "elite_percentage": 0.3
        },
        "learning": {
            "exploration_rate": 0.4,  # Mais exploração
            "learning_rate": 0.02,    # Aprendizado mais rápido
            "memory_size": 5000,      # Memória otimizada
            "batch_size": 16
        },
        "autonomous": {
            "cycle_minutes": 30,      # Ciclos mais frequentes
            "backup_hours": 12,       # Backup mais frequente
            "max_api_calls_hour": 50, # Menos chamadas para evitar rate limits
            "auto_expand": True
        }
    }
    
    with open("auto_config.json", "w") as f:
        json.dump(config_otimizada, f, indent=2)
    
    print("✅ Configurações otimizadas para evolução mais rápida")

def verificar_conectividade():
    """Verifica se as APIs estão funcionando"""
    print("🌐 Verificando conectividade...")
    
    try:
        import requests
        
        # Testa GitHub API
        response = requests.get(
            "https://api.github.com/search/code?q=python+function&per_page=1",
            headers={'Accept': 'application/vnd.github.v3+json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ GitHub API funcionando")
        else:
            print(f"⚠️ GitHub API retornou status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro de conectividade: {e}")

def main():
    """Menu principal de correção"""
    print("🔧 CORREÇÃO E OTIMIZAÇÃO DO SISTEMA")
    print("=" * 50)
    
    # Verifica problemas
    problemas = verificar_problemas()
    
    if problemas:
        print("⚠️ Problemas identificados:")
        for problema in problemas:
            print(f"  {problema}")
        
        print("\n🔧 Aplicando correções automáticas...")
        corrigir_problemas()
        reiniciar_sistema()
    else:
        print("✅ Nenhum problema crítico identificado")
    
    # Otimizações
    print("\n⚡ Aplicando otimizações...")
    otimizar_configuracao()
    verificar_conectividade()
    
    print("\n🎯 Sistema otimizado e pronto para evolução!")
    print("💡 O sistema agora deve evoluir mais rapidamente")
    print("📊 Monitore o progresso com: python monitor_evolucao.py")

if __name__ == "__main__":
    main() 