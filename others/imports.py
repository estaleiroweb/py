"""_summary_
    
# Estrutura:
    /
        pasta/
            meu_script.py
            subpasta/
                file_import.py
                __pycache__/
                    file_import.cpython-38.pyc

    
``
    
# Passos para Importar o Arquivo Compilado

1. Certifique-se de que o arquivo compilado .pyc esteja no formato correto:
   - O arquivo .pyc deve estar dentro do diretório __pycache__ e deve seguir a convenção de nomeação, como file_import.cpython-38.pyc para Python 3.8. Se você compilou manualmente e moveu o arquivo .pyc, renomeie-o corretamente ou ajuste a estrutura conforme necessário.
2. Atualize o Caminho de Importação:
   - Para importar o arquivo .pyc de uma subpasta, você pode adicionar o caminho da subpasta ao sys.path ou usar um pacote relativo se a estrutura do projeto suportar isso.
3. Criação de um arquivo .py correspondente:
   - Para importar diretamente, o Python procura um arquivo .py correspondente. Para facilitar, você pode criar um arquivo file_import.py vazio ou com a mesma estrutura de nome do arquivo .pyc dentro da subpasta.

# Considerações Importantes

- Portabilidade: Certifique-se de que o arquivo .pyc é compatível com a versão do Python que você está utilizando.
- Estrutura de Diretórios: A estrutura de diretórios e convenções de nomeação são importantes para que o Python possa localizar e importar o módulo corretamente.
- Mantenha os Arquivos Consistentes: Se você fizer mudanças no código-fonte, recompile os arquivos .pyc para garantir que eles estejam atualizados.

"""


# importação direta
from subpasta.file_import import class_or_fn # type: ignore

class_or_fn()

# ------------------------------------------------------------------------------------------------------------------------------

import sys
import os

# Adicione o caminho da subpasta ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'subpasta'))

# Se não quiser criar um arquivo file_import.py vazio, você pode adicionar o caminho do __pycache__ diretamente ao sys.path e importar o módulo compilado. Aqui está um exemplo:
sys.path.append(os.path.join(os.path.dirname(__file__), 'subpasta', '__pycache__'))

# Agora importe o módulo normalmente
import file_import # type: ignore

# Utilize as funções ou classes do módulo importado
file_import.class_or_fn()

# ------------------------------------------------------------------------------------------------------------------------------

import sys
import os
import importlib.util

# Caminho absoluto para o módulo .pyc
module_path = '/pasta/subpasta/file_import.pyc'

# Nome do módulo que será usado internamente
# module_name = 'file_import'
module_name = os.path.splitext(os.path.basename(module_path))[0]
module_name = module_name.split('.')[0]

# Carregar o módulo a partir do caminho
spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module) # type: ignore

module.class_or_fn()
