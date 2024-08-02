#!/usr/bin/python3

import subprocess
import requests

def get_installed_extensions():
    # Executa o comando para listar as extensões instaladas
    result = subprocess.run(['code', '--list-extensions'], stdout=subprocess.PIPE)
    # Decodifica e divide a saída para criar uma lista das extensões
    return result.stdout.decode().splitlines()

def get_extension_details(extension_name):
    # Faz uma solicitação para a API do Visual Studio Marketplace
    url = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"
    payload = {
        "filters": [{
            "criteria": [{
                "filterType": 7,
                "value": extension_name
            }]
        }],
        "flags": 103
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;api-version=3.0-preview.1"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        extension = data['results'][0]['extensions'][0]
        return {
            "name": extension['displayName'],
            "author": extension['publisher']['displayName'],
            "description": extension.get('shortDescription', 'Sem descrição'),
            "image": next((file['source'] for file in extension['versions'][0]['files'] if file['assetType'] == 'Microsoft.VisualStudio.Services.Icons.Default'), None),
            "link": f"https://marketplace.visualstudio.com/items?itemName={extension['publisher']['publisherName']}.{extension['extensionName']}"
        }
    return None

extensions = get_installed_extensions()
print(extensions)

details = get_extension_details(extensions[0])
print(details)
quit()


for ext in extensions:
    details = get_extension_details(ext)
    if details:
        print(f'''[<img src='{details['image']}' /> {details['name']}]({details['link']}): Autor: {details['author']}<pre>\n{details['description']}\n</pre>''')
