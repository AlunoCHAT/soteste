#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico do Sistema de IA Auto-Evolutiva
Verifica se tudo está funcionando corretamente
"""

import os
import json
import time
import sys
from datetime import datetime

def verificar_arquivos():
    """Verifica se todos os arquivos necessários existem"""
    print("🔍 Verificando arquivos do sistema...")
    
    arquivos_necessarios = [
        "knowledge.json",
        "evolution_log.json", 
        "neural_weights.npz",
        "auto_config.json",
        "dashboard.html",
        "evolution.log"
    ]
    
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            tamanho = os.path.getsize(arquivo)
            print(f"✅ {arquivo} - {tamanho} bytes")
        else:
            print(f"❌ {arquivo} - NÃO ENCONTRADO")
    
    return True

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print("\n🔍 Verificando dependências...")
    
    dependencias = [
        "requests", "numpy", "schedule", "json", "time", "threading"
    ]
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - NÃO INSTALADO")
            return False
    
    return True

def verificar_modulos():
    """Verifica se os módulos principais carregam corretamente"""
    print("\n🔍 Verificando módulos principais...")
    
    try:
        from integrated_system import IntegratedAI
        print("✅ integrated_system.py")
    except Exception as e:
        print(f"❌ integrated_system.py - ERRO: {e}")
        return False
    
    try:
        from src.agent import CodeLearningAgent
        print("✅ src/agent.py")
    except Exception as e:
        print(f"❌ src/agent.py - ERRO: {e}")
        return False
    
    try:
        from src.neural_engine import MicroNeuralNetwork, CodeEvolutionEngine
        print("✅ src/neural_engine.py")
    except Exception as e:
        print(f"❌ src/neural_engine.py - ERRO: {e}")
        return False
    
    try:
        from autonomous_evolution import AutonomousEvolution
        print("✅ autonomous_evolution.py")
    except Exception as e:
        print(f"❌ autonomous_evolution.py - ERRO: {e}")
        return False
    
    return True

def verificar_conhecimento():
    """Verifica o estado atual do conhecimento"""
    print("\n🔍 Verificando conhecimento atual...")
    
    try:
        with open("knowledge.json", "r") as f:
            knowledge = json.load(f)
        
        funcoes = len(knowledge.get("knowledge_base", {}).get("functions", {}))
        print(f"📚 Funções aprendidas: {funcoes}")
        
        exploration_rate = knowledge.get("exploration_rate", 0)
        print(f"🔍 Taxa de exploração: {exploration_rate:.2%}")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar conhecimento: {e}")
        return False

def verificar_evolucao():
    """Verifica o estado da evolução"""
    print("\n🔍 Verificando evolução...")
    
    try:
        with open("evolution_log.json", "r") as f:
            evolution = json.load(f)
        
        geracao_atual = evolution.get("current_generation", 0)
        print(f"🧬 Geração atual: {geracao_atual}")
        
        checkpoints = evolution.get("checkpoints", [])
        if checkpoints:
            ultimo_checkpoint = checkpoints[-1]
            timestamp = ultimo_checkpoint.get("timestamp", "")
            print(f"⏰ Último checkpoint: {timestamp}")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar evolução: {e}")
        return False

def verificar_log():
    """Verifica o log de evolução"""
    print("\n🔍 Verificando log de evolução...")
    
    if os.path.exists("evolution.log"):
        with open("evolution.log", "r") as f:
            linhas = f.readlines()
        
        if linhas:
            ultima_linha = linhas[-1].strip()
            print(f"📝 Última entrada no log: {ultima_linha}")
            
            # Conta entradas por tipo
            info_count = sum(1 for linha in linhas if "INFO" in linha)
            error_count = sum(1 for linha in linhas if "ERROR" in linha)
            
            print(f"ℹ️ Entradas INFO: {info_count}")
            print(f"⚠️ Entradas ERROR: {error_count}")
        
        return True
    else:
        print("❌ evolution.log não encontrado")
        return False

def testar_sistema():
    """Testa se o sistema pode ser inicializado"""
    print("\n🔍 Testando inicialização do sistema...")
    
    try:
        from autonomous_evolution import AutonomousEvolution
        
        # Cria instância (sem executar loop infinito)
        evolution = AutonomousEvolution()
        print("✅ Sistema inicializado com sucesso")
        
        # Testa um ciclo de aprendizado
        print("🧠 Testando ciclo de aprendizado...")
        evolution.autonomous_learning_cycle()
        print("✅ Ciclo de aprendizado executado")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao testar sistema: {e}")
        return False

def verificar_processos():
    """Verifica se há processos Python rodando"""
    print("\n🔍 Verificando processos Python...")
    
    try:
        import psutil
        
        processos_python = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if 'autonomous_evolution' in cmdline or 'chat_system' in cmdline:
                        processos_python.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cmdline': cmdline
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if processos_python:
            print("🔄 Processos Python ativos:")
            for proc in processos_python:
                print(f"  PID {proc['pid']}: {proc['cmdline']}")
        else:
            print("⚠️ Nenhum processo do sistema encontrado")
        
        return True
    except ImportError:
        print("⚠️ psutil não instalado - não é possível verificar processos")
        return True

def main():
    """Executa diagnóstico completo"""
    print("🧠 DIAGNÓSTICO DO SISTEMA DE IA AUTO-EVOLUTIVA")
    print("=" * 50)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    resultados = []
    
    # Executa verificações
    resultados.append(("Arquivos", verificar_arquivos()))
    resultados.append(("Dependências", verificar_dependencias()))
    resultados.append(("Módulos", verificar_modulos()))
    resultados.append(("Conhecimento", verificar_conhecimento()))
    resultados.append(("Evolução", verificar_evolucao()))
    resultados.append(("Log", verificar_log()))
    resultados.append(("Processos", verificar_processos()))
    resultados.append(("Teste Sistema", testar_sistema()))
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DO DIAGNÓSTICO")
    print("=" * 50)
    
    sucessos = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)
    
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome}: {status}")
    
    print(f"\n🎯 Resultado: {sucessos}/{total} verificações passaram")
    
    if sucessos == total:
        print("🎉 Sistema está funcionando perfeitamente!")
        print("💡 Para iniciar a evolução autônoma, execute:")
        print("   python autonomous_evolution.py")
    else:
        print("⚠️ Há problemas que precisam ser corrigidos")
        print("💡 Verifique os erros acima e corrija antes de executar")

if __name__ == "__main__":
    main() 