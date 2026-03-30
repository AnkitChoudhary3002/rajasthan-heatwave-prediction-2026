import requests

class HeatwaveService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def predict_heatwave(self, data: dict):
        response = requests.post(f"{self.base_url}/predict", json=data)
        return self._handle_response(response)

    def calculate_heat_index(self, data: dict):
        response = requests.post(f"{self.base_url}/heat_index_calculator", json=data)
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code == 200:
            return response.json(), None
        return None, response.text