import requests

api_key="bdf79b2f2d5637450827abd057f7c1d1"
grados= "metric"
def ugradual():
    global grados
    print("Ingrese si quiere la medida en sistema metrico o imperial:")
    med = input().lower()
    if med== "metrico" or med=="metric":
        grados= "metric"
        print("Sistema elegido:metrico")
    elif med == "imperial":
        grados = "imperial"
        print("Sistema elegido:Imperial")
    else :
        "opcion no valida, se continuara en el sistema que estaba antes"
def menu() :
    while True:
        print("Seleccione una opcion")
        print("1)temperatura")
        print("2)Elegir medida de temperatura")
        opcion=input()
        if opcion== "1":
            tempminymax()
        elif opcion== "2":
            ugradual()    
        elif opcion!= "0":
            break            
def tempminymax():
    print("Ingrese su ciudad")
    ciudad=input()
    Urlciudad=f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units={grados}"
    info=requests.get(Urlciudad)
    infojson=info.json()
    temp = infojson["main"]["temp"]
    min = infojson["main"]["temp_min"]
    max = infojson["main"]["temp_max"]
    print(f"la temperatura en {ciudad} es de {temp}")
    print(f"la temperatura minima es de {min}")
    print(f"la temperatura maxima es de {max}")
    print("Desea volver al menu? escribiendo si, volvera, de lo contrario saldra del programa")
    volver=input().lower()
    if volver == "si" :
        menu()
    else:
        exit()
menu()