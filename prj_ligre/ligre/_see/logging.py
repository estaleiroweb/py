import http.server
import logging

# Configuração do log
logging.basicConfig(filename="servidor.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        """Redireciona logs do servidor para o arquivo de log"""
        # logging.info("%s - %s" % (self.client_address[0], format % args))
        logging.info("%s - %s" % (self.address_string(), format % args))
    def log_error(self, format, *args):
        logging.error("%s - %s" % (self.client_address[0], format % args))

    def do_GET(self):
        """Log para requisições GET"""
        logging.info(f"Requisição GET recebida de {self.client_address}")
        super().do_GET()  # Chama o comportamento padrão

    def do_POST(self):
        """Log para requisições POST"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        logging.info(f"Requisição POST recebida de {self.client_address} com corpo: {post_data}")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"POST recebido!")

# Iniciar o servidor HTTP
if __name__ == "__main__":
    server_address = ("", 8080)  # Servindo na porta 8080
    httpd = http.server.HTTPServer(server_address, CustomHandler)
    print("Servidor rodando em http://localhost:8080")
    httpd.serve_forever()


########################################
quit()
# Exibir logs no console e salvar no arquivo
import http.server
import logging

# Configuração do log
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("servidor.log")
console_handler = logging.StreamHandler()

# Define formato do log
formatter = logging.Formatter("%(asctime)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Adiciona handlers ao logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        """Loga tanto no console quanto no arquivo"""
        log_msg = "%s - %s" % (self.client_address[0], format % args)
        logger.info(log_msg)

# Inicia o servidor
PORT = 8080
server = http.server.HTTPServer(("", PORT), CustomHandler)
print(f"Servidor rodando na porta {PORT}")
server.serve_forever()
