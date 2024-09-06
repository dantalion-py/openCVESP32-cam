## Instrucciones
### 1.- Instalar las dependencias de python.
```bash
pip install -r requirements.txt 
```
### 2.- Descargar las placas esp32 by Espressif Systems en arduinoIDE.
### 3.- Agregar a arduinoIDE la libreria esp32cam-main.zip.
### 4.- En el archivo camPyEsp32.ino modificar los datos correspondientes en: 
```cpp
const char* WIFI_SSID = "nombre_de_red";
const char* WIFI_PASS = "contraseña";
```
### 5.- despues de cargar el codigo a la esp32cam en el monitor serial 150000 batios aparecera la url para ver el streaming copiar la url en archivo colorDetecting_fill.py o colorDetecting.py:
```py
url = 'url_que_aparece/cam-lo.jpg'

```
## La tecla para salir de las ventanas por default es ('a')

