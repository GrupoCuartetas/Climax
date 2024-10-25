import datetime
import requests

api_key = "bdf79b2f2d5637450827abd057f7c1d1"
grados = "metric"


#-----------------------------------------------------------------------------------------------------------------# 
def ugradual():
    global grados
    print("Ingrese si quiere la medida en sistema metrico o imperial:")
    med = input().lower()
    if med == "metrico" or med == "metric":
        grados = "metric"
        print("Sistema elegido: métrico")
    elif med == "imperial":
        grados = "imperial"
        print("Sistema elegido: imperial")
    else:
        print("Opción no válida, se continuará en el sistema que estaba antes.")


#-----------------------------------------------------------------------------------------------------------------# 
def menu():
    while True:
        print("Seleccione una opción")
        print("1) Temperatura")
        print("2) Elegir medida de temperatura")
        print("3) Pronóstico de los próximos días")
        print("4) Mostrar historial de consultas")
        opcion = input()
        if opcion == "1":
            tempminymax()
        elif opcion == "2":
            ugradual()    
        elif opcion == "3":
            pronosticoDias()
        elif opcion=="4":
            mostrarHistorial()    
        else:
            print("Opción no válida. Saliendo del programa.")
            break


#-----------------------------------------------------------------------------------------------------------------#         
def guardar_solicitud(consulta, resultado):
    with open("Historial.txt", "a") as f:
        f.write(f"Consulta: {consulta} - {resultado}\n")


#-----------------------------------------------------------------------------------------------------------------#        
def tempminymax():
    print("Ingrese su ciudad")
    ciudad = input()
    Urlciudad = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units={grados}"
    
    try:
        info = requests.get(Urlciudad)
        info.raise_for_status()  # Lanza un error si la respuesta fue un error HTTP
        infojson = info.json()
        
        temp = infojson["main"]["temp"]
        min_temp = infojson["main"]["temp_min"]
        max_temp = infojson["main"]["temp_max"]
        
        print(f"La temperatura en {ciudad} es de {temp}")
        print(f"La temperatura mínima es de {min_temp}")
        print(f"La temperatura máxima es de {max_temp}")

        guardar_solicitud(ciudad, temp)
        
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
    
    print("Desea volver al menú? escribiendo 'si', volverá, de lo contrario saldrá del programa")
    volver = input().lower()
    if volver == "si":
        menu()
    else:
        exit()



#------------------------------------------------------------------------------------------------#   
def pronosticoDias():
   while true:
        print("Ingrese su ciudad")
        ciudad = input()
        Urlciudad = f"https://api.openweathermap.org/data/2.5/forecast?q={ciudad}&appid={api_key}&units={grados}"
        guardar_solicitud(ciudad, "")
        try:
            info = requests.get(Urlciudad)
            info.raise_for_status()  # Lanza un error si la respuesta fue un error HTTP
            infojson = info.json()
        
            for forecast in infojson['list']:
                date = forecast['dt_txt']  
                temperature = forecast['main']['temp']
                description = forecast['weather'][0]['description']
                if date.endswith('12:00:00'):
                    print(f"{date}: {temperature}°C, {description}")
             break  
        except requests.exceptions.HTTPError as http_err:
            print(f"Error HTTP: {http_err}")
       


#------------------------------------------------------------------------------------------------#      
def mostrarHistorial():
    try:
        with open("Historial.txt", "r") as f:
            historial = f.readlines()
            if historial:
                print("\nHistorial de Consultas:")
                for linea in historial:
                    print(linea.strip() + "°C")
            else:
                print("El historial está vacío.")
    except FileNotFoundError:
        print("No se encontró el archivo de historial.")

menu()
