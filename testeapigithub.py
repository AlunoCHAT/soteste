import requests

def testar_chave_github(chave_api):
    """
    Função para testar se a chave da API do GitHub é válida.
    """
    if not chave_api or chave_api == "ghp_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":
        print("Erro: A chave da API não foi fornecida.")
        return False

    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {chave_api }'
    }

    # Faz uma requisição simples para o seu perfil. Isso requer autenticação.
    url = "https://api.github.com/user"
    
    try:
        response = requests.get(url, headers=headers)
        
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Sucesso! A sua chave de API do GitHub está funcionando.")
            print(f"Nome de usuário: {user_data.get('login')}")
            print(f"URL do perfil: {user_data.get('html_url')}")
            return True
        elif response.status_code == 401:
            print("❌ Erro 401: Chave de API inválida ou expirada.")
            print("Por favor, verifique se a chave está correta e tem as permissões necessárias (scopes).")
            print("Link de ajuda: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token")
            return False
        else:
            print(f"❌ Erro na requisição: Status {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return False

if __name__ == "__main__":
    print("--- Testador de Chave da API do GitHub ---")
    chave_api = input("Por favor, cole a sua chave de API do GitHub aqui: ").strip()
    
    if testar_chave_github(chave_api):
        print("\nA chave está funcionando. Agora você pode colocá-la no arquivo 'integrated_system.py'.")
    else:
        print("\nOcorreu um problema com a sua chave. Por favor, verifique-a e tente novamente.")