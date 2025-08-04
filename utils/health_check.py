#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de verificação de saúde para o sistema de IA auto-evolutiva.
Este script checa o estado dos processos, o progresso da evolução em 'evolution_log.json'
e as mensagens de erro nos logs de atividade.

Para funcionar corretamente, os seguintes pacotes são necessários:
pip install psutil python-dateutil
"""

import os
import json
import time
from datetime import datetime, timezone
from dateutil.parser import parse  # Usa a função parse, mais flexível que isoparse
 
# --- Configuração ---
LOG_FILE = "evolution.log"
EVOLUTION_FILE = "evolution_log.json"
PROCESS_NAME_FRAGMENT = "autonomous_evolution.py"
STALL_THRESHOLD_SECONDS = 3600  # 1 hora

def check_psutil():
    """
    Verifica se o psutil está instalado e o retorna.
    A instalação de 'psutil' permite verificar os processos do sistema.
    """
    try:
        import psutil
        return psutil
    except ImportError:
        print("Aviso: `psutil` não está instalado. Não é possível verificar processos.")
        print("   Para uma verificação completa, instale com: pip install psutil")
        return None

def check_running_processes(psutil):
    """
    Verifica se o processo principal de evolução está rodando e se há duplicatas.
    
    Args:
        psutil: O módulo psutil, se estiver disponível.
        
    Returns:
        Um status (str) e uma mensagem (str) sobre os processos.
    """
    if not psutil:
        return "desconhecido", "Não foi possível verificar os processos."

    processes = []
    # Itera sobre todos os processos para encontrar o de evolução
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
        try:
            if proc.info['cmdline'] and any(PROCESS_NAME_FRAGMENT in arg for arg in proc.info['cmdline']):
                processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Ignora processos que não podem ser acessados ou que já morreram
            continue

    if not processes:
        return "parado", f"ERRO: Nenhum processo '{PROCESS_NAME_FRAGMENT}' encontrado. O sistema não está rodando."
    
    if len(processes) > 1:
        processes.sort(key=lambda p: p.info['create_time'])
        pids = [p.pid for p in processes]
        return "conflito", f"Aviso: Múltiplos processos encontrados (PIDs: {pids}). Isso pode causar conflitos. Considere parar todos e reiniciar."

    return "rodando", f"OK: Um processo está rodando corretamente (PID: {processes[0].pid})."

def check_evolution_progress():
    """
    Verifica o arquivo 'evolution_log.json' para progresso recente.
    
    Returns:
        Um status (str) e uma mensagem (str) sobre o progresso.
    """
    if not os.path.exists(EVOLUTION_FILE):
        return "parado", f"ERRO: Arquivo de log de evolução '{EVOLUTION_FILE}' não encontrado."

    try:
        with open(EVOLUTION_FILE, "r") as f:
            data = json.load(f)
        
        checkpoints = data.get("checkpoints")
        if not checkpoints:
            return "parado", "Aviso: O log de evolução está vazio. Nenhuma geração foi completada ainda."

        last_checkpoint = checkpoints[-1]
        timestamp_str = last_checkpoint.get("timestamp")
        generation = last_checkpoint.get("generation", "N/A")
        
        if not timestamp_str:
            return "erro", "ERRO: Último checkpoint no log não tem timestamp."

        # Aprimoramento da lógica para garantir que a data seja ciente de fuso horário (aware)
        parsed_time = parse(timestamp_str)
        if parsed_time.tzinfo is None:
            # Se a string não contiver fuso horário, assumimos UTC e forçamos
            last_update_time = parsed_time.replace(tzinfo=timezone.utc)
        else:
            # Se já for ciente de fuso horário, apenas convertemos para UTC
            last_update_time = parsed_time.astimezone(timezone.utc)
        
        now_utc = datetime.now(timezone.utc)
        
        # O erro 'TypeError' não ocorrerá mais, pois ambos são 'aware'
        time_since_update = now_utc - last_update_time

        if time_since_update.total_seconds() > STALL_THRESHOLD_SECONDS:
            minutes_stalled = time_since_update.total_seconds() / 60
            return "travado", f"ALERTA: Sistema parece travado! Última atualização há {minutes_stalled:.1f} minutos. (Geração {generation})"
        
        minutes_since_update = time_since_update.total_seconds() / 60
        return "ativo", f"OK: Progresso recente detectado. Última atualização há {minutes_since_update:.1f} minutos. (Geração {generation})"

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        return "erro", f"ERRO: Erro ao ler ou processar '{EVOLUTION_FILE}': {e}"

def check_activity_log():
    """
    Verifica o arquivo 'evolution.log' para entradas recentes e erros.
    
    Returns:
        Um status (str) e uma mensagem (str) sobre o log.
    """
    if not os.path.exists(LOG_FILE):
        return "desconhecido", f"INFO: Arquivo de log de atividade '{LOG_FILE}' não encontrado."

    lines = []
    try:
        # Tenta com UTF-8 primeiro, que é o padrão ideal
        with open(LOG_FILE, "r", encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # Se falhar, tenta com uma codificação de fallback (latin-1 é seguro)
        try:
            with open(LOG_FILE, "r", encoding='latin-1') as f:
                lines = f.readlines()
            print(f"   (Aviso: O arquivo de log '{LOG_FILE}' não é UTF-8. Lendo com codificação de fallback.)")
        except Exception as e:
            return "erro", f"ERRO: Erro ao ler '{LOG_FILE}' com múltiplas codificações: {e}"
    except Exception as e:
        return "erro", f"ERRO: Erro inesperado ao ler '{LOG_FILE}': {e}"

    if not lines:
        return "inativo", "INFO: O log de atividade está vazio."

    last_line = lines[-1].strip()
    error_lines = [line for line in lines[-50:] if "ERROR" in line or "Exception" in line]

    if error_lines:
        return "erro", f"ERRO: Erros recentes detectados no log! Último erro: {error_lines[-1].strip()}"
    
    return "ativo", f"OK: Nenhuma mensagem de erro recente. Última linha do log: {last_line}"

def main():
    """
    Executa a verificação de saúde completa.
    """
    print("="*50 + "\nVERIFICAÇÃO DE SAÚDE - IA AUTO-EVOLUTIVA\n" + "="*50)
    
    # 1. Verificação de Processos
    psutil = check_psutil()
    print("\n--- 1. Verificação de Processos ---")
    process_status, process_msg = check_running_processes(psutil)
    print(process_msg)

    # 2. Verificação de Progresso
    print("\n--- 2. Verificação de Progresso da Evolução ---")
    progress_status, progress_msg = check_evolution_progress()
    print(progress_msg)

    # 3. Verificação do Log de Atividade
    print("\n--- 3. Verificação do Log de Atividade ---")
    log_status, log_msg = check_activity_log()
    print(log_msg)

    # 4. Diagnóstico Final
    print("\n" + "="*50 + "\nDIAGNÓSTICO FINAL\n" + "="*50)
    if "erro" in [progress_status, log_status] or "conflito" in process_status:
        print("ESTADO: ERRO CRÍTICO. Ações recomendadas:")
        if "conflito" in process_status:
            print("   - Pare todos os processos 'autonomous_evolution.py' manualmente (Gerenciador de Tarefas).")
        if "erro" in log_status:
            print(f"   - Verifique o erro no arquivo '{LOG_FILE}'.")
        if "erro" in progress_status:
            print(f"   - Verifique a formatação do arquivo '{EVOLUTION_FILE}'.")
    elif "travado" in progress_status:
        print("ESTADO: POSSIVELMENTE TRAVADO. O processo está rodando, mas sem progresso recente.")
        print("   - Considere parar o processo e reiniciar. Verifique o log para ver a última atividade.")
    elif "parado" in process_status:
        print("ESTADO: INATIVO. Execute `python autonomous_evolution.py` para iniciar.")
    elif "rodando" in process_status and "ativo" in progress_status:
        print("ESTADO: SAUDÁVEL. O sistema parece estar rodando e evoluindo corretamente.")
    else:
        print("ESTADO: INDETERMINADO. Analise os detalhes. Pode estar no primeiro ciclo.")

if __name__ == "__main__":
    main()