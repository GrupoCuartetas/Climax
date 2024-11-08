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
mensaje=""

app=Flask(__name__)
app.secret_key = secrets.token_hex(16)
historial = []
pronosticos = {}
DatosCiudad = []


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

def borrarCaractes(ciudad):
    ciudad = re.sub(r'[^a-zA-Z ]', '', ciudad)
    ciudad= ciudad.strip()
    if ciudad:
        return ciudad

# def fueConsultada(ciudad):
#     DatosCiudad=session.get('Ciudad')
#     posicion=0
#     if DatosCiudad:
#         for consulta in DatosCiudad:
#                 if consulta[posicion]['ciudad']==ciudad:
#                     return True, posicion
#                     break
#                 posicion+=1
#     return False, -2
    

# def obtenerDatosCiudad(ciudad):
    
#     ciudades_guardadas = session.get('Ciudad', [])
    
    
#     for ciudad_guardada in ciudades_guardadas:
#         if ciudad_guardada['ciudad'].lower() == ciudad.lower():  
#             return ciudad_guardada
#         else:
#             return False

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
def inicio():
    global temperatura, ciudad, pais, max_temp, min_temp, grados, historial, DatosCiudad
    
    ciudad = request.args.get("ciudad")
    fue=request.args.get("fueConsultada")
    grados=request.args.get("grados", "metric")

    
    
    if ciudad and fue:
        DatosCiudad=session.get('Ciudad')
        posicion=int(request.args.get("posicion"))
        ciudad=ciudad
        temperatura=DatosCiudad[posicion]['temperatura']
        pais=DatosCiudad[posicion]['pais']
        max_temp=DatosCiudad[posicion]['max_temp']
        min_temp=DatosCiudad[posicion]['min_temp']
        gradosAb=DatosCiudad[posicion]['gradosAb']
        return redirect(url_for('temp', ciudad=ciudad, temperatura=temperatura, pais=pais, max_temp=max_temp, min_temp=min_temp, gradosAb=gradosAb, DatosCiudad=DatosCiudad))

    elif ciudad:
        url=f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units={grados}"
        try:
            info = requests.get(url)
            info.raise_for_status()
            infojson=info.json()


            # ciudad = ciudad.lower()
            # temperatura = infojson['main']['temp']
            # min_temp = infojson['main']['temp_min']
            # max_temp = infojson['main']['temp_max']
            # sensacionTermica=infojson['main']['feels_like']
            # nubosidad= infojson['weather'][0]['main']
            # codigoPais = infojson['sys']['country']
            # pais=nombrePais(codigoPais)
            # grados=grados
            # gradosAb=gradosEnAbreviatura(grados)
            DatosCiudad=session.get('Ciudad', [])
            datos={
                "ciudad": ciudad,
                "temperatura": f"{infojson['main']['temp']:.0f}",
                "max_temp": f"{infojson['main']['temp_max']:.0f}",
                "min_temp": f"{infojson['main']['temp_min']:.0f}",
                "nubosidad": infojson['weather'][0]['main'],
                "sensacionTermica": infojson['main']['feels_like'],
                "humedad":infojson['main']['humidity'],
                "codigoPais": infojson['sys']['country'],
                "pais": nombrePais(infojson['sys']['country']),
                "grados": grados,
                "gradosAb": gradosEnAbreviatura(grados)
            }

            DatosCiudad.append(datos)
            session['Ciudad'] = DatosCiudad


            historial = session.get('historial', [])
            consulta = {
                "fecha": datetime.datetime.now().strftime("%d/%m/%Y"),
                "hora" : datetime.datetime.now().strftime("%H:%M"),
                "pais": pais.upper(),
                "ciudad": ciudad.upper(),
                "temp": f"{datos['temperatura']}{gradosEnAbreviatura(grados)}"
            }

            historial.append(consulta) 
            session['historial'] = historial
            return redirect(url_for('temp', ciudad=datos['ciudad'], temperatura=datos['temperatura'], pais=datos['pais'], max_temp=datos['max_temp'], min_temp=datos['min_temp'], gradosAb=datos['gradosAb'], grados=datos['grados'], DatosCiudad=DatosCiudad, nubosidad=datos['nubosidad'], humedad=datos['humedad'], sensacionT=datos['sensacionTermica']))
        except requests.exceptions.RequestException as e:
            
            return render_template("index.html", mensaje="Ciudad no encontrada")
        except KeyError as e:
            
            return render_template("index.html", mensaje="No se encontró la información completa de la ciudad")
        except Exception as e:

            return render_template("index.html", mensaje="Ocurrió un error inesperado")
    return render_template("index.html")

@app.route("/validacion", methods=["POST"])
def validarCiudad():
    
    ciudad = request.form.get("ciudad").lower()
    ciudad = borrarCaractes(ciudad)
    

    if ciudad:
            return redirect (url_for('inicio', ciudad=ciudad))
    else:
        return render_template("index.html", mensaje="Ciudad invalida")


@app.route("/clima")
def temp():




    ciudad = request.args.get('ciudad')
    temperatura = request.args.get('temperatura')
    pais = request.args.get('pais')
    maxtemp = request.args.get('max_temp')
    mintemp = request.args.get('min_temp')
    gradosAb = request.args.get('gradosAb')
    nubosidad = request.args.get('nubosidad')
    humedad=request.args.get('humedad')
    sensacionT=request.args.get('sensacionT')
   
    return render_template("clima.html", ciudad=ciudad.upper(), temperatura=temperatura, pais=pais, maxtemp=maxtemp, mintemp=mintemp, gradosAb=gradosAb, nubosidad=nubosidad, humedad=humedad, sensacionT=sensacionT)

@app.route("/cambiar_unidad", methods=["POST"])
def cambiar_unidad(): 
    global grados, DatosCiudad
    DatosCiudad=session.get('Ciudad')
    gradosActual = DatosCiudad[-1]['grados']
    grados = request.form.get("grados")
    temperatura=float(DatosCiudad[-1]['temperatura'])
    ciudad=DatosCiudad[-1]['ciudad']
    pais=DatosCiudad[-1]['pais']
    min_temp=float(DatosCiudad[-1]['max_temp'])
    max_temp=float(DatosCiudad[-1]['min_temp'])
    humedad=DatosCiudad[-1]['humedad']
    nubosidad=DatosCiudad[-1]['nubosidad']
    sensacionT=float(DatosCiudad[-1]['sensacionTermica'])
    

    if grados=="metric" and gradosActual!="metric":
         temperatura=(temperatura-32)*5/9
         min_temp=(min_temp-32)*5/9
         max_temp=(max_temp-32)*5/9
         sensacionT=(sensacionT-32)*5/9
    elif grados=="imperial" and gradosActual!="imperial":
        temperatura = (temperatura*9/5)+32
        min_temp = (min_temp*9/5)+32
        max_temp = (max_temp*9/5)+32
        sensacionT=(sensacionT*9/5)+32
    
    DatosCiudad[-1]['grados']=grados
    DatosCiudad[-1]['temperatura']=temperatura
    DatosCiudad[-1]['max_temp']=max_temp
    DatosCiudad[-1]['min_temp']=min_temp
    DatosCiudad[-1]['sensacionTermica']=sensacionT

    temperatura=f"{temperatura:.0f}"
    max_temp=f"{max_temp:.0f}"
    min_temp=f"{min_temp:.0f}"
    sensacionT=f"{sensacionT:.2f}"

    return redirect(url_for('temp', ciudad=ciudad.upper(), pais=pais, temperatura=temperatura,max_temp=max_temp, min_temp=min_temp, gradosAb=gradosEnAbreviatura(grados), nubosidad=nubosidad, humedad=humedad, sensacionT=sensacionT))

@app.route('/historial')
def mostrar_historial():
    global historial, ciudad, temperatura, max_temp, min_temp, pais  
    return render_template("historial.html", historial=historial)


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
            temperature = f"{forecast['main']['temp']:.0f}"
            min_temp=f"{forecast['main']['temp_min']:.0f}"
            max_temp=f"{forecast['main']['temp_max']:.0f}"
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
    app.run(host="0.0.0.0", port=5000, debug=True)
