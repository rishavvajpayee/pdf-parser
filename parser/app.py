import falcon
from wsgiref.simple_server import make_server
from main import PdfParser

app = falcon.App()

pdf_parser = PdfParser()
app.add_route("/", pdf_parser)

if __name__ == "__main__":
    with make_server("", 9000, app) as httpd:
        print("port running on 9000")
        httpd.serve_forever()