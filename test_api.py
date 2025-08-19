#!/usr/bin/env python3
"""
Script de teste para a API do Fórum Hub
"""
import requests
import json
import sys

BASE_URL = "http://localhost:5001/api"

def test_api():
    print("=== Testando API do Fórum Hub ===\n")
    
    # Teste 1: Registrar usuário
    print("1. Testando registro de usuário...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=user_data, timeout=5)
        if response.status_code == 201:
            print("✓ Registro de usuário funcionando")
            data = response.json()
            token = data.get('access_token')
            print(f"  Token recebido: {token[:20]}...")
        else:
            print(f"✗ Erro no registro: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Erro na conexão: {e}")
        return False
    
    # Teste 2: Login
    print("\n2. Testando login...")
    login_data = {
        "username": "testuser",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data, timeout=5)
        if response.status_code == 200:
            print("✓ Login funcionando")
            data = response.json()
            token = data.get('access_token')
        else:
            print(f"✗ Erro no login: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Erro na conexão: {e}")
        return False
    
    # Teste 3: Listar tópicos (sem autenticação)
    print("\n3. Testando listagem de tópicos...")
    try:
        response = requests.get(f"{BASE_URL}/topicos", timeout=5)
        if response.status_code == 200:
            print("✓ Listagem de tópicos funcionando")
            topicos = response.json()
            print(f"  Número de tópicos: {len(topicos)}")
        else:
            print(f"✗ Erro na listagem: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Erro na conexão: {e}")
        return False
    
    # Teste 4: Criar tópico (com autenticação)
    print("\n4. Testando criação de tópico...")
    topico_data = {
        "titulo": "Minha primeira dúvida",
        "mensagem": "Estou com dúvida sobre como implementar autenticação JWT",
        "curso_nome": "Java"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{BASE_URL}/topicos", json=topico_data, headers=headers, timeout=5)
        if response.status_code == 201:
            print("✓ Criação de tópico funcionando")
            data = response.json()
            topico_id = data.get('topico', {}).get('id')
            print(f"  Tópico criado com ID: {topico_id}")
        else:
            print(f"✗ Erro na criação: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Erro na conexão: {e}")
        return False
    
    # Teste 5: Obter tópico específico
    print("\n5. Testando obtenção de tópico específico...")
    try:
        response = requests.get(f"{BASE_URL}/topicos/{topico_id}", timeout=5)
        if response.status_code == 200:
            print("✓ Obtenção de tópico funcionando")
            topico = response.json()
            print(f"  Título: {topico.get('titulo')}")
        else:
            print(f"✗ Erro na obtenção: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Erro na conexão: {e}")
        return False
    
    # Teste 6: Atualizar tópico
    print("\n6. Testando atualização de tópico...")
    update_data = {
        "titulo": "Dúvida resolvida!",
        "mensagem": "Consegui implementar a autenticação JWT com sucesso"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/topicos/{topico_id}", json=update_data, headers=headers, timeout=5)
        if response.status_code == 200:
            print("✓ Atualização de tópico funcionando")
        else:
            print(f"✗ Erro na atualização: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Erro na conexão: {e}")
        return False
    
    # Teste 7: Deletar tópico
    print("\n7. Testando exclusão de tópico...")
    try:
        response = requests.delete(f"{BASE_URL}/topicos/{topico_id}", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✓ Exclusão de tópico funcionando")
        else:
            print(f"✗ Erro na exclusão: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Erro na conexão: {e}")
        return False
    
    print("\n=== Todos os testes passaram! ===")
    return True

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)

