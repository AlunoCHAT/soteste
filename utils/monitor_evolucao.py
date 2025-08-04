#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor de Evolução da IA
Verifica se o sistema está evoluindo corretamente
"""

import os
import json
import time
from datetime import datetime, timedelta

def monitorar_evolucao():
    """Monitora a evolução do sistema em tempo real"""
    print("🧠 MONITOR DE EVOLUÇÃO DA IA")
    print("=" * 50)
    print("Pressione Ctrl+C para parar")
    print()
    
    ultima_geracao = 0
    ultima_funcoes = 0
    ultima_memoria = 0
    
    try:
        while True:
            # Verifica arquivos de estado
            if os.path.exists("evolution_log.json"):
                with open("evolution_log.json", "r") as f:
                    evolution = json.load(f)
                
                geracao_atual = evolution.get("current_generation", 0)
                checkpoints = evolution.get("checkpoints", [])
                
                if checkpoints:
                    ultimo_checkpoint = checkpoints[-1]
                    timestamp = ultimo_checkpoint.get("timestamp", "")
                    metrics = ultimo_checkpoint.get("metrics", {})
                    
                    funcoes = metrics.get("knowledge_functions", 0)
                    memoria = metrics.get("memory_size", 0)
                    exploration = metrics.get("exploration_rate", 0)
                    nivel = metrics.get("current_level", 0)
                    
                    # Verifica se houve mudança
                    mudanca = False
                    if geracao_atual != ultima_geracao:
                        print(f"🔄 NOVA GERAÇÃO: {geracao_atual} (era {ultima_geracao})")
                        mudanca = True
                        ultima_geracao = geracao_atual
                    
                    if funcoes != ultima_funcoes:
                        print(f"📚 NOVAS FUNÇÕES: {funcoes} (era {ultima_funcoes})")
                        mudanca = True
                        ultima_funcoes = funcoes
                    
                    if memoria != ultima_memoria:
                        print(f"💾 NOVA MEMÓRIA: {memoria} (era {ultima_memoria})")
                        mudanca = True
                        ultima_memoria = memoria
                    
                    if mudanca:
                        print(f"⏰ Timestamp: {timestamp}")
                        print(f"🔍 Exploração: {exploration:.2%}")
                        print(f"📊 Nível: {nivel + 1}/4")
                        print("-" * 30)
            
            # Verifica log
            if os.path.exists("evolution.log"):
                with open("evolution.log", "r") as f:
                    linhas = f.readlines()
                
                if linhas:
                    ultima_linha = linhas[-1].strip()
                    if "INFO" in ultima_linha and "Geração" in ultima_linha:
                        print(f"📝 Log: {ultima_linha}")
            
            # Verifica dashboard
            if os.path.exists("dashboard.html"):
                tamanho = os.path.getsize("dashboard.html")
                print(f"📊 Dashboard atualizado: {tamanho} bytes")
            
            # Aguarda 30 segundos
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Monitoramento interrompido")
        print("✅ Sistema continua rodando em background")

def verificar_processos_ativos():
    """Verifica se os processos estão ativos"""
    print("🔍 Verificando processos ativos...")
    
    try:
        import psutil
        
        processos_encontrados = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if 'autonomous_evolution' in cmdline:
                        processos_encontrados.append({
                            'pid': proc.info['pid'],
                            'cmdline': cmdline,
                            'status': 'running'
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if processos_encontrados:
            print("✅ Processos ativos encontrados:")
            for proc in processos_encontrados:
                print(f"  PID {proc['pid']}: {proc['cmdline']}")
        else:
            print("⚠️ Nenhum processo de evolução encontrado")
            print("💡 Execute: python autonomous_evolution.py")
        
        return len(processos_encontrados) > 0
        
    except ImportError:
        print("⚠️ psutil não instalado")
        return True

def reiniciar_sistema():
    """Reinicia o sistema se necessário"""
    print("🔄 Verificando se precisa reiniciar...")
    
    # Verifica se há processos ativos
    if not verificar_processos_ativos():
        print("🚀 Reiniciando sistema...")
        os.system("python autonomous_evolution.py &")
        print("✅ Sistema reiniciado")
    else:
        print("✅ Sistema já está rodando")

def main():
    """Menu principal"""
    print("🧠 MONITOR DE EVOLUÇÃO DA IA")
    print("=" * 50)
    print("1. Monitorar evolução em tempo real")
    print("2. Verificar processos ativos")
    print("3. Reiniciar sistema se necessário")
    print("4. Sair")
    print()
    
    while True:
        try:
            opcao = input("Escolha uma opção (1-4): ").strip()
            
            if opcao == "1":
                monitorar_evolucao()
            elif opcao == "2":
                verificar_processos_ativos()
            elif opcao == "3":
                reiniciar_sistema()
            elif opcao == "4":
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida")
                
        except KeyboardInterrupt:
            print("\n👋 Até logo!")
            break

if __name__ == "__main__":
    main() 