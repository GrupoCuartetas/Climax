import datetime

import re
import secrets
from flask import Flask, redirect, request, render_template, session, url_for
import requests

api_key = "bdf79b2f2d5637450827abd057f7c1d1"

grados = "metric"
ciudad = ""
temperatura = ""
min_temp = ""
max_temp = ""
pais=""



# #-----------------------------------------------------------------------------------------------------------------# 
# def ugradual():
#     global grados
#     print("Ingrese si quiere la medida en sistema metrico o imperial:")
#     med = input().lower()
#     if med == "metrico" or med == "metric":
#         grados = "metric"
#         print("Sistema elegido: métrico")
#     elif med == "imperial":
#         grados = "imperial"
#         print("Sistema elegido: imperial")
#     else:
#         print("Opción no válida, se continuará en el sistema que estaba antes.")


# #-----------------------------------------------------------------------------------------------------------------# 
# def menu():
#     while True:
#         print("Seleccione una opción")
#         print("1) Temperatura")
#         print("2) Elegir medida de temperatura")
#         print("3) Pronóstico de los próximos días")
#         print("4) Mostrar historial de consultas")
#         opcion = input()
#         if opcion == "1":
#             tempminymax()
#         elif opcion == "2":
#             ugradual()    
#         elif opcion == "3":
#             pronosticoDias()
#         elif opcion=="4":
#             mostrarHistorial()    
#         else:
#             print("Opción no válida. Saliendo del programa.")
#             break


# #-----------------------------------------------------------------------------------------------------------------#         
# def guardar_solicitud(consulta, resultado):
#     with open("Historial.txt", "a") as f:
#         f.write(f"Consulta: {consulta} - {resultado}\n")

# #-----------------------------------------------------------------------------------------------------------------#         
# def borrarCaractes(palabra):
#     return re.sub(r'[^a-zA-Z]', '', palabra)

# #-----------------------------------------------------------------------------------------------------------------#        
# def tempminymax():
#     Urlciudad = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units={grados}"
    
#     try:
#         info = requests.get(Urlciudad)
#         info.raise_for_status()  # Lanza un error si la respuesta fue un error HTTP
#         infojson = info.json()
        
#         temp = infojson["main"]["temp"]
#         min_temp = infojson["main"]["temp_min"]
#         max_temp = infojson["main"]["temp_max"]
        
#         print(f"La temperatura en {ciudad} es de {temp}")
#         print(f"La temperatura mínima es de {min_temp}")
#         print(f"La temperatura máxima es de {max_temp}")

#         guardar_solicitud(ciudad, temp)
        
#     except requests.exceptions.HTTPError as http_err:
#         print(f"Error HTTP: {http_err}")
    
#     print("Desea volver al menú? escribiendo 'si', volverá, de lo contrario saldrá del programa")
#     volver = input().lower()
#     if volver == "si":
#         menu()
#     else:
#         exit()



# #------------------------------------------------------------------------------------------------#   
# def pronosticoDias():
#    while True:
#         Urlciudad = f"https://api.openweathermap.org/data/2.5/forecast?q={ciudad}&appid={api_key}&units={grados}"
#         guardar_solicitud(ciudad, "")
#         try:
#             info = requests.get(Urlciudad)
#             info.raise_for_status()  # Lanza un error si la respuesta fue un error HTTP
#             infojson = info.json()
        
#             for forecast in infojson['list']:
#                 date = forecast['dt_txt']  
#                 temperature = forecast['main']['temp']
#                 description = forecast['weather'][0]['description']
#                 if date.endswith('12:00:00'):
#                     print(f"{date}: {temperature}°C, {description}")
#             break  
#         except requests.exceptions.HTTPError as http_err:
#             print(f"Error HTTP: {http_err}")
       


# #------------------------------------------------------------------------------------------------#      
# def mostrarHistorial():
#     try:
#         with open("Historial.txt", "r") as f:
#             historial = f.readlines()
#             if historial:
#                 print("\nHistorial de Consultas:")
#                 for linea in historial:
#                     print(linea.strip() + "°C")
#             else:
#                 print("El historial está vacío.")
#     except FileNotFoundError:
#         print("No se encontró el archivo de historial.")


# ciudad=""
# while not ciudad:
#     print("Ingrese una ciudad")
#     ciudad=borrarCaractes(input())
#     if not ciudad:
#         print("Debe ingresar una ciudad sin numeros ni caracteres especiales")
#     elif():
#         break


# menu()
app=Flask(__name__)
app.secret_key = secrets.token_hex(16)
historial = []
pronosticos = {}


codigoPaises = {
    "AR": "Argentina",
    "AU": "Australia",
    "AT": "Austria",
    "BR": "Brasil",
    "BG": "Bulgaria",
    "CA": "Canadá",
    "CL": "Chile",
    "CN": "China",
    "CO": "Colombia",
    "CR": "Costa Rica",
    "DK": "Dinamarca",
    "DO": "República Dominicana",
    "EG": "Egipto",
    "FR": "Francia",
    "DE": "Alemania",
    "GR": "Grecia",
    "HK": "Hong Kong",
    "HU": "Hungría",
    "ID": "Indonesia",
    "IN": "India",
    "IE": "Irlanda",
    "IL": "Israel",
    "IT": "Italia",
    "JP": "Japón",
    "KR": "Corea del Sur",
    "MX": "México",
    "MY": "Malasia",
    "NL": "Países Bajos",
    "NZ": "Nueva Zelanda",
    "NO": "Noruega",
    "PE": "Perú",
    "PH": "Filipinas",
    "PL": "Polonia",
    "PT": "Portugal",
    "RO": "Rumania",
    "RU": "Rusia",
    "SG": "Singapur",
    "ZA": "Sudáfrica",
    "ES": "España",
    "SE": "Suecia",
    "CH": "Suiza",
    "TH": "Tailandia",
    "TR": "Turquía",
    "UA": "Ucrania",
    "GB": "Reino Unido",
    "US": "Estados Unidos",
    "VE": "Venezuela",
    "VN": "Vietnam"
}
dias = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

def borrarCaractes(palabra):
    return re.sub(r'[^a-zA-Z]', '', palabra)

def nombrePais(codigo):
    return codigoPaises.get(codigo,"")

def gradosEnAbreviatura(grados):
    abreviatura=""
    if(grados=="metric"):
        abreviatura="°C"
    elif(grados=="imperial"):
        abreviatura="°F"
    return abreviatura        

@app.route("/", methods=["GET", "POST"])
def home():
    global grados, historial, ciudad, temperatura, max_temp, min_temp, pais
    
    ciudad = request.args.get("ciudad", "")
    temperatura = request.args.get("temperatura", "")
    max_temp = request.args.get("max_temp", "")
    min_temp = request.args.get("min_temp", "")
    pais = request.args.get("pais", "")
    
    if request.method == "POST":
        if request.form.get("grados"):
                grados = request.form.get("grados")  
        else:
                ciudad = borrarCaractes(request.form.get("ciudad"))
        if ciudad:
            Urlciudad = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units={grados}"
            try:
                info = requests.get(Urlciudad)
                info.raise_for_status()
                infojson = info.json()

                temperatura = infojson["main"]["temp"]
                min_temp = infojson["main"]["temp_min"]
                max_temp = infojson["main"]["temp_max"]
                codigoPais = infojson["sys"]["country"]
                pais=nombrePais(codigoPais)

                consulta = {
                        "fecha": datetime.datetime.now().strftime("%d/%m/%Y"),
                        "hora" : datetime.datetime.now().strftime("%H:%M"),
                        "pais": pais.upper(),
                        "ciudad": ciudad.upper(),
                        "temp": f"{temperatura}{gradosEnAbreviatura(grados)}"
                    }

                historial = session.get('historial', [])
                historial.append(consulta) 
                session['historial'] = historial 

                return redirect(url_for('temp', ciudad=ciudad, temperatura=temperatura, pais=pais, max_temp=max_temp, min_temp=min_temp))
            except requests.exceptions.HTTPError as http_err:
                    print("No se encontro ciudad")

    return render_template("index.html", ciudad=ciudad, temperatura=temperatura, min_temp=min_temp, max_temp=max_temp, historial=historial, pais=pais)

@app.route("/clima")
def temp():
    ciudad = request.args.get("ciudad", "")
    temperatura = request.args.get("temperatura", "")
    pais = request.args.get("pais", "")
    maxtemp = request.args.get("max_temp", "")
    mintemp = request.args.get("min_temp","")
    gradosAb = gradosEnAbreviatura(grados) 
    return render_template("clima.html", ciudad=ciudad.upper(), temperatura=temperatura, pais=pais, maxtemp=maxtemp, mintemp=mintemp, grados=gradosAb)

@app.route("/cambiar_unidad", methods=["POST"])
def cambiar_unidad():
    global grados,historial, ciudad, temperatura, max_temp, min_temp, pais  
    grados = request.form.get("grados")
    Urlciudad = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units={grados}"
    info = requests.get(Urlciudad)
    infojson = info.json()
    
    temperatura = infojson["main"]["temp"]
    min_temp = infojson["main"]["temp_min"]
    max_temp = infojson["main"]["temp_max"]
    
    return redirect(url_for('temp', ciudad=ciudad.upper(), temperatura=temperatura, pais=pais, max_temp=max_temp, min_temp=min_temp, grados=gradosEnAbreviatura(grados)))

@app.route('/historial')
def mostrar_historial():
    global historial, ciudad, temperatura, max_temp, min_temp, pais  
    return render_template("historial.html", historial=historial, ciudad=ciudad.upper(), temperatura=temperatura, pais=pais, max_temp=max_temp, min_temp=min_temp)

@app.route('/pronosticos')
def mostrar_pronosticos():
    global pronosticos, grados, historial, ciudad, temperatura, max_temp, min_temp, pais
    ciudad = request.args.get("ciudad", "")
    Urlciudad = f"https://api.openweathermap.org/data/2.5/forecast?q={ciudad}&appid={api_key}&units={grados}"
    
    try:
        info = requests.get(Urlciudad)
        info.raise_for_status()
        infojson = info.json()

        pronosticos[ciudad] = []
        
        for forecast in infojson['list']:
            date = forecast['dt_txt']
            fecha = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            dia_ingles = fecha.strftime('%A')
            dia = dias[dia_ingles]
            temperature = forecast['main']['temp']
            min_temp=forecast['main']['temp_min']
            max_temp=forecast['main']['temp_max']
            description = forecast['weather'][0]['description']
            if date.endswith('12:00:00'):
                pronosticos[ciudad].append({
                    'date': dia,
                    'temperature': temperature,
                    'min_temp':min_temp,
                    'max_temp':max_temp,
                    'description': description
                })
        
        return render_template('pronostico.html', ciudad=ciudad, pronosticos=pronosticos[ciudad], temperatura=temperatura, pais=pais, max_temp=max_temp, min_temp=min_temp, grados=gradosEnAbreviatura(grados))
    except requests.exceptions.HTTPError as http_err:
        return f"Error HTTP: {http_err}"
     
if __name__ == "__main__":
    app.run(debug=True)