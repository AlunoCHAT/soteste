import subprocess
import sys

def install_package(package):
    """Instala um pacote individualmente"""
    try:
        print(f"📦 Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado com sucesso!\n")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar {package}\n")
        return False

def main():
    print("=" * 50)
    print("🔧 INSTALADOR DE DEPENDÊNCIAS - IA AUTO-EVOLUTIVA")
    print("=" * 50)
    print()
    
    # Atualiza pip primeiro
    print("📦 Atualizando pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ Pip atualizado!\n")
    except:
        print("⚠️  Não foi possível atualizar pip, continuando...\n")
    
    # Pacotes essenciais
    essential_packages = [
        "requests",
        "numpy",
        "schedule"
    ]
    
    # Pacotes opcionais
    optional_packages = [
        "matplotlib"
    ]
    
    # Instala essenciais
    print("📋 Instalando pacotes essenciais...\n")
    failed = []
    
    for package in essential_packages:
        if not install_package(package):
            failed.append(package)
    
    # Pergunta sobre opcionais
    print("\n❓ Deseja instalar pacotes opcionais? (para monitoramento visual)")
    choice = input("Digite 's' para sim ou 'n' para não: ").lower()
    
    if choice == 's':
        for package in optional_packages:
            install_package(package)
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DA INSTALAÇÃO")
    print("=" * 50)
    
    if not failed:
        print("✅ Todos os pacotes essenciais foram instalados!")
        print("\n🚀 Você já pode executar a IA com:")
        print("   python chat_system.py")
        print("   python autonomous_evolution.py")
    else:
        print(f"❌ Falha ao instalar: {', '.join(failed)}")
        print("\n💡 Tente instalar manualmente com:")
        for pkg in failed:
            print(f"   pip install {pkg}")
    
    print("\n" + "=" * 50)
    input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    main()
