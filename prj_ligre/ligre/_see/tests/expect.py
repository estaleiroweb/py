import pexpect


def executar_conexao(tipo_conexao, ip, porta, usuario, senha, prompt, comandos):
    try:
        # Determinar o comando inicial com base no tipo de conexão
        if tipo_conexao == 'ssh':
            conn = pexpect.spawn(f'ssh {usuario}@{ip} -p {porta}')
        elif tipo_conexao == 'telnet':
            conn = pexpect.spawn(f'telnet {ip} {porta}')
        elif tipo_conexao == 'ftp':
            conn = pexpect.spawn(f'ftp {ip}')
        elif tipo_conexao == 'sftp':
            conn = pexpect.spawn(f'sftp -P {porta} {usuario}@{ip}')
        else:
            print("Tipo de conexão inválido!")
            return

        # Tratamento de login e senha
        conn.expect(['password:', 'Password:', 'senha:',
                    pexpect.EOF, pexpect.TIMEOUT])
        conn.sendline(senha)

        # Esperar pelo prompt para confirmar login bem-sucedido
        conn.expect(prompt)

        # Executar comandos fornecidos
        for cmd, esperado in comandos.items():
            print(f'Executando: {cmd}')
            conn.sendline(cmd)
            conn.expect(prompt)
            resultado = conn.before.decode(
                'utf-8', errors='ignore') if conn.before else None
            print(f'Resultado: {resultado}')

            # Validar se o resultado esperado está presente
            if esperado and esperado not in resultado:
                print(
                    f"Aviso: O resultado esperado '{esperado}' não foi encontrado!")

        conn.sendline('exit')  # Encerra a sessão
        conn.close()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


# Exemplo de uso
if __name__ == '__main__':
    tipo_conexao = 'ssh'  # Opções: ssh, telnet, ftp, sftp
    ip = '192.168.1.100'
    porta = 22
    usuario = 'seu_usuario'
    senha = 'sua_senha'
    prompt = r'\$ '  # Ajuste para o prompt esperado (ex: '#' para root)

    # Comandos em um dicionário: {comando: resultado esperado}
    comandos = {
        'ls -la': 'total',
        'uname -a': 'Linux',
    }

    executar_conexao(tipo_conexao, ip, porta, usuario, senha, prompt, comandos)
