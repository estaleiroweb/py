"""
```bash
# compilar para executável

pip install pyinstaller
pyinstaller --onefile meu_script.py

## Adicionar Ícone ao Executável
pyinstaller --onefile --icon=meu_icone.ico meu_script.py

## Especificar um Nome para o Executável
pyinstaller --onefile --name meu_executavel meu_script.py

# compilar para bytecode
python -m py_compile meu_script.py
python __pycache__/meu_script.cpython-38.pyc


para alterar a senha renomear o arquivo para db_config.py, criar o .pyc
    Renomear o arquivo para db_config_source.pyc e apagar a senha
```
"""

# Automação da Compilação
import compileall

# Compilar todos os arquivos Python no diretório atual
compileall.compile_dir('.', force=True)
