#!/usr/bin/env python3
import os
import sys
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    clear_screen()
    print("=" * 50)
    print("   🧠 IA AUTO-EVOLUTIVA - MENU PRINCIPAL")
    print("=" * 50)
    print("\n1. 💬 Chat Interativo (Conversar com a IA)")
    print("2. 🔄 Evolução Autônoma (Rodar 24/7)")
    print("3. 🖥️  Sistema Integrado (Terminal)")
    print("4. 📊 Ver Dashboard (Navegador)")
    print("5. 📦 Instalar Dependências")
    print("6. 🔍 Testar Dependências")
    print("7. 📖 Ler Documentação")
    print("8. ❌ Sair")
    print("\n" + "=" * 50)

def main():
    while True:
        show_menu()
        choice = input("\n➤ Digite sua escolha (1-8): ").strip()
        
        if choice == '1':
            print("\n🚀 Iniciando Chat Interativo...")
            subprocess.run([sys.executable, "chat_system.py"])
            
        elif choice == '2':
            print("\n🚀 Iniciando Evolução Autônoma...")
            print("⚠️  Este modo roda indefinidamente. Use Ctrl+C para parar.")
            input("\nPressione ENTER para continuar...")
            subprocess.run([sys.executable, "autonomous_evolution.py"])
            
        elif choice == '3':
            print("\n🚀 Iniciando Sistema Integrado...")
            subprocess.run([sys.executable, "integrated_system.py"])
            
        elif choice == '4':
            print("\n📊 Abrindo Dashboard...")
            if os.path.exists("dashboard.html"):
                os.startfile("dashboard.html")
            else:
                print("❌ Dashboard ainda não foi gerado. Execute primeiro o modo autônomo.")
            input("\nPressione ENTER para continuar...")
            
        elif choice == '5':
            print("\n📦 Escolha o método de instalação:")
            print("1. Instalação padrão (requirements.txt)")
            print("2. Instalação mínima (sem versões específicas)")
            print("3. Instalador interativo (recomendado se houver erros)")
            
            install_choice = input("\nEscolha (1-3): ").strip()
            
            if install_choice == '1':
                print("\n📦 Instalando com requirements.txt...")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            elif install_choice == '2':
                print("\n📦 Instalando versão mínima...")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_minimal.txt"])
            elif install_choice == '3':
                print("\n📦 Iniciando instalador interativo...")
                subprocess.run([sys.executable, "instalar_dependencias.py"])
            else:
                print("\n❌ Opção inválida!")
                
            input("\nPressione ENTER para continuar...")
            
        elif choice == '6':
            print("\n🔍 Testando dependências...")
            subprocess.run([sys.executable, "testar_dependencias.py"])
            
        elif choice == '7':
            print("\n📖 Abrindo documentação...")
            if os.path.exists("GUIA_COMPLETO.md"):
                with open("GUIA_COMPLETO.md", "r", encoding="utf-8") as f:
                    content = f.read()
                print(content[:2000] + "\n...\n")
                print("\n📄 Para ler completo, abra GUIA_COMPLETO.md")
            input("\nPressione ENTER para continuar...")
            
        elif choice == '8':
            print("\n👋 Obrigado por usar a IA Auto-Evolutiva!")
            sys.exit(0)
            
        else:
            print("\n❌ Opção inválida!")
            input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    # Verifica se está no diretório correto
    if not os.path.exists("requirements.txt"):
        print("❌ Erro: Execute este script do diretório do projeto!")
        sys.exit(1)
    
    main()
