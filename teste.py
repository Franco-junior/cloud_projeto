import requests
from time import sleep
# Teste do endpoint /registrar
print("Teste 1: Registrando usuário")
try:
    response = requests.post(
        "http://localhost:8080/registrar",
        json={"nome": "Disciplina Cloud", "email": "cloud@insper.edu.br", "senha": "cloud0"}
    )
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    jwt_token = response.json().get("jwt")
    
except Exception as e:
    print(f"Erro ao registrar: {e}")
    jwt_token = None

sleep(3)
# Teste do endpoint /login
print("\nTeste 2: Login do usuário")
try:
    response = requests.post(
        "http://localhost:8080/login",
        json={"email": "cloud@insper.edu.br", "senha": "cloud0"}
    )
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    jwt_token = response.json().get("jwt")
    
except Exception as e:
    print(f"Erro ao fazer login: {e}")
    if jwt_token is None:  # Se o teste anterior falhou, não temos token
        jwt_token = "token_inválido_para_teste"

sleep(3)
# Teste do endpoint /consultar (requer autenticação)
print("\nTeste 3: Consultando dados (com autenticação)")
try:
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(
        "http://localhost:8080/consultar", 
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()[:2]}...")  # Mostra apenas os 2 primeiros registros
    
    # Teste opcional: formato CSV
    print("\nTeste 4: Consultando dados no formato CSV")
    response_csv = requests.get(
        "http://localhost:8080/consultar?format=csv", 
        headers=headers
    )
    print(f"Status: {response_csv.status_code}")
    print(f"Primeiras linhas do CSV:")
    # Mostrar apenas as primeiras linhas do CSV para não sobrecarregar o output
    csv_text = response_csv.text.strip()
    print(csv_text.split('\n')[0])  # Cabeçalho
    print(csv_text.split('\n')[1] if '\n' in csv_text else "Formato não contém quebras de linha")
    
except Exception as e:
    print(f"Erro ao consultar: {e}")

# Teste de acesso sem autenticação (deve falhar)
print("\nTeste 5: Consultando sem autenticação (deve falhar)")
try:
    response = requests.get("http://localhost:8080/consultar")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.text}")
except Exception as e:
    print(f"Erro esperado: {e}")