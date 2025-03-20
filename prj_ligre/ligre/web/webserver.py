import os
import ssl
from http.server import SimpleHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
import socketserver
from ..core.conf import Conf


class WebServer:
    def __init__(self,
                 port: int = 80,
                 bind: str = '',
                 https: bool = False,
                 socket: bool = False,
                 keyfile: bool = None,
                 certfile: bool = None,
                 handler: SimpleHTTPRequestHandler = SimpleHTTPRequestHandler
                 ):
        self.bind: str = bind
        self.keyfile: str = keyfile
        self.certfile: str = certfile
        self.socket: bool = socket
        self.https: bool = https\
            and self.keyfile \
            and self.certfile \
            and os.path.exists(self.keyfile) \
            and os.path.exists(self.certfile)
        self.port: int = port
        self.handler = handler
        self.httpd: 'socketserver.TCPServer|HTTPServer' = None
        if https == self.https:
            self.start()

    def start(self, https=False):
        """Inicia o servidor HTTP"""
        if https and not self.https:
            return

        if self.socket:
            with socketserver.TCPServer(
                (self.bind, self.port),
                self.handler
            ) as self.httpd:
                self.send()
        else:
            self.httpd = HTTPServer(
                (self.bind, self.port),
                self.handler
            )
            self.send()

    def send(self):
        if self.https:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(
                certfile=self.certfile,
                keyfile=self.keyfile
            )
            self.httpd.socket = context.wrap_socket(
                self.httpd.socket,
                server_side=True
            )

        print(
            "Web Server running " +
            ('HTTPS' if self.https else 'HTTP') +
            f"://{self.bind}:{self.port}"
        )

        self.httpd.serve_forever()


class HttpHandler_Redirect(SimpleHTTPRequestHandler):
    REDIRECT_PORT = 443

    def do_GET(self):
        """Responde às requisições GET e gerencia a sessão."""
        if self.server.server_port != self.REDIRECT_PORT:  # Se acessado via HTTP
            host = self.headers['Host'].split(':')[0]
            https_url = f"https://{host}:{self.REDIRECT_PORT}{self.path}"
            self.send_response(301)
            self.send_header("Location", https_url)
            self.end_headers()
            return True
        return False

    def do_POST(self):
        self.do_GET()


class HttpHandler(SimpleHTTPRequestHandler):
    encoding = "utf-8"

    def __init__(self, *args, **kwds):
        self.id:str = self._get_id()
        super().__init__(*args, **kwds)

    def _get_id(self) -> str:
        """Carrega a sessão do usuário ou cria uma nova."""

        self.id = None
        # Check cookie
        if "Cookie" in self.headers:
            cookies = SimpleCookie(self.headers["Cookie"])
            if "session_id" in cookies:
                self.id = cookies["session_id"].value
        if not self.id:
            import uuid
            self.id = uuid.uuid4()
        return id

    def do_GET(self):
        """Responde às requisições GET e gerencia a sessão."""
        # Config HTTP response
        self.send_response(200)
        self.send_header("Content-type", f"text/html; charset={self.encoding}")
        # self.send_header("Set-Cookie", f"session_id={oSess}; Path=/")
        # self.send_header("Set-Cookie", f"session_id={self.__id}; Path=/; Max-Age=3600; HttpOnly")
        self.send_header("Set-Cookie", f"session_id={self.id}; Path=/; HttpOnly")
        self.end_headers()
        content_length = int(self.headers.get('Content-Length', 0))
        payload = self.rfile.read(content_length) if content_length else None

        # Show info
        resposta = f"""
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Título da Página</title>
            <meta name="description" content="Descrição da página para SEO.">
            <meta name="keywords" content="palavras-chave, para, SEO">
            <!-- 
            <meta charset="{self.encoding}">
            <link rel="icon" href="favicon.ico" type="image/x-icon">
            <link rel="stylesheet" href="style.css">
            <script src="script.js" defer></script>
            -->
        </head>
        <body>
            <h1>Servidor HTTP com Sessão</h1>
            <p>Seu ID de sessão: <b>{self.id}</b></p>
            <ul>
                <li><b>server</b>: {self.server}</li>
                <li><b>client_address</b>: {self.client_address}</li>
                <li><b>command</b>: {self.command}</li>
                <li><b>path</b>: {self.path}</li>
                <li><b>headers</b>: <pre>{self.headers}</pre></li>
                <li><b>rfile</b>: {self.rfile}</li>
                <li><b>wfile</b>: {self.wfile}</li>
                <li><b>protocol_version</b>: {self.protocol_version}</li>
                <li><b>request_version</b>: {self.request_version}</li>
                <li><b>close_connection</b>: {self.close_connection}</li>
                <li><b>timeout</b>: {self.timeout}</li>
                <li><b>requestline</b>: {self.requestline}</li>
                <li><b>content_length</b>: {content_length}</li>
                <li><b>payload</b>: <pre>{payload}</pre></li>
            </ul>
            <a href='/aaaa'>Clique aqui</a>
        </body>
        </html>
        """
        self.wfile.write(
            resposta.encode(self.encoding)
        )

    def do_POST(self):
        self.do_GET()

    def do_PUT(self):
        self.do_GET()

    def do_DELETE(self):
        self.do_GET()

    def do_HEAD(self):
        self.do_GET()

    def do_OPTIONS(self):
        self.do_GET()

def start():
    cnf:dict=Conf('settings.json').get('webserver',{})
    for i in cnf:
        print(i,cnf[i])
    # print(WebServer.)

start()
