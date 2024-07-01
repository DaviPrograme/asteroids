import os
import requests

def create_source_airbyte(workspace_id):
    # URL do endpoint
    url = "http://localhost:8000/api/v1/sources/create"

    auth = ('airbyte', 'password')

    # Cabeçalhos
    headers = {
        'Content-Type': 'application/json'
    }

    # Dados do corpo da requisição
    data = {
        "sourceDefinitionId": "decd338e-5647-4c0b-adf4-da0e75f5a750",
        "workspaceId": workspace_id,
        "connectionConfiguration": {
            "host": "localhost",
            "port": 9090,
            "database": "asteroid",
            "username": "postgres",
            "password": "abcXecole42"
        },
        "name": "Postgres Source",
        "syncMode": "incremental",
        "syncCatalog": "true",  
        "configuration": {
            "selected": ["incremental"],
            "xmins": "true"
        }
    }

    try:
        # Faz a requisição POST
        response = requests.post(url, auth=auth, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()

        # Imprime a resposta JSON formatada
        print(response_data)
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
    except ValueError as e:
        print(f"Erro ao processar a resposta JSON: {e}")



def create_destinations_airbyte(workspace_id):
    # URL do endpoint
    url = "http://localhost:8000/api/v1/destinations/create"

    auth = ('airbyte', 'password')

    # Cabeçalhos
    headers = {
        'content-type': 'application/json'
    }

    # Dados do corpo da requisição
    data = {
        "name":"Clickhouse",
        "destinationDefinitionId":"ce0d828e-1dc4-496c-b122-2da42e637e48",
        "workspaceId": workspace_id,
        "connectionConfiguration": {
            "ssl": False,
            "port":8123,
            "tunnel_method":{
                "tunnel_method":"NO_TUNNEL"
            },
            "host":"localhost",
            "database":"default",
            "username":"default"
        }
    }

    

    try:
        # Faz a requisição POST
        response = requests.post(url, auth=auth, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()

        # Imprime a resposta JSON formatada
        print(response_data)
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
    except ValueError as e:
        print(f"Erro ao processar a resposta JSON: {e}")



def get_workspaceid_airbyte():
    # URL do endpoint
    url = "http://localhost:8000/api/v1/workspaces/list"

    # Autenticação básica
    auth = ('airbyte', 'password')

    # Cabeçalhos
    headers = {
        'Content-Type': 'application/json'
    }

    # Dados do corpo da requisição
    data = {}
    workspace_id = None
    try:
        # Faz a requisição POST com autenticação básica
        response = requests.post(url, auth=auth, headers=headers, json=data)
        response.raise_for_status()
        data = response.json()

        # Extrai o valor de workspaceId
        workspace_id = data['workspaces'][0]['workspaceId']
        # Verifica se o valor foi extraído com sucesso
        if not workspace_id:
            print("echo 'Não foi possível extrair workspaceId'")
    except requests.exceptions.RequestException as e:
        print(f"echo 'Erro na requisição: {e}'")
    except (KeyError, IndexError) as e:
        print(f"echo 'Erro ao processar o JSON: {e}'")
    return workspace_id


if __name__ == "__main__":
    workspace_id =  get_workspaceid_airbyte()
    print(workspace_id)
    create_source_airbyte(workspace_id)
    create_destinations_airbyte(workspace_id)
