"""multiprocessing cria um processo totalmente separado do principal, garantindo isolamento e limpeza automática da memória quando o processo termina."""
import multiprocessing
import pickle

class classe_parametro:
    def __init__(self):
        self.valor = "Este é um parâmetro"

class classe_exemplo:
    def __init__(self, obj):
        print(f"Processo filho iniciado com: {obj.valor}")

def executar_classe(obj_serializado):
    """Função executada no subprocesso"""
    obj = pickle.loads(obj_serializado)  # Desserializa o objeto
    classe_exemplo(obj)

if __name__ == "__main__":
    obj = classe_parametro()  # Criando o objeto
    obj_serializado = pickle.dumps(obj)  # Serializando o objeto para passar ao subprocesso

    # Criando um processo separado
    p = multiprocessing.Process(target=executar_classe, args=(obj_serializado,))
    p.start()  # Inicia o subprocesso
    p.join()   # Aguarda a conclusão do subprocesso

    print("Subprocesso finalizado, memória liberada!")
