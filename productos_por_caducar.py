import requests

def send_request():
    url = "http://127.0.0.1:5000/producto-por-caducar"
    response = requests.post(url)
    if response.status_code == 200:
        print("Correos enviados con éxito")
    else:
        print("Error al enviar la solicitud")


if __name__ == "__main__":
    send_request()