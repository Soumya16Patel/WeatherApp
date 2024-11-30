
import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather",self)
        self.temperature_lable = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()#QVBoxLayout is a layout manager that arranges widgets vertically (in a column)

        vbox.addWidget(self.city_label) # Providing the distance among the widgets
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_lable)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter) #For the alignment of the widget
        self.temperature_lable.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_lable") # used to assign a unique name to a widget.This name allows you to easily identify and style specific widgets, especially useful for applying custom stylesheets and debugging complex interfaces.
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_lable.setObjectName("temperature_lable")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLable, QPushButton{
                font-family: Helvetica;
            }
            QLabel#city_lable{
                font-size: 50px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
                
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
                
            }
            QLabel#temperature_lable{
                font-size: 65px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;
                
            }
        
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "8bde5b2077ad55fbec123ce3a57b7f54"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()#checks whether an HTTP request was successful or not.
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
           match response.status_code:
               case 400:
                   self.display_error("Bad request:\nPlease check your input")
               case 401:
                   self.display_error("Unauthorized:\nInvalid API key")
               case 403:
                   self.display_error("Forbidden:\nAccess is denied")
               case 404:
                   self.display_error("Not Found:\nCity not found")
               case 500:
                   self.display_error("Internal Server Error:\nPlease try again later")
               case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
               case 503:
                   self.display_error("Service Unavailable:\nServer is down")
               case 504:
                   self.display_error("Gateway Timeout:\nNo response from the server")
               case _:
                self.display_error("HTTP error occurred:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\n Check your internet connection ")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")



    def display_error(self, message):
        self.temperature_lable.setStyleSheet("font-size: 30px;")
        self.temperature_lable.setText(message)
        self.description_label.clear()
        self.emoji_label.clear()

    def display_weather(self, data):
        self.temperature_lable.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67
        weather_description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        self.temperature_lable.setText(f"{temperature_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
    @staticmethod
    def get_weather_emoji(weather_id):

        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌥️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 700 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return " "





if __name__ == "__main__":

    app = QApplication(sys.argv)#initializes the PyQt application and prepares it to handle GUI interactions.
    weather_app = WeatherApp()
    weather_app.show() #displays the window on the screen.
    sys.exit(app.exec_()) #starts the application’s main event loop and waits for user interactions. When the application is closed, app.exec_() returns, and sys.exit() ensures a clean exit.


