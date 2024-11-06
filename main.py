import sys
import random
import regex as re

p_tlf = re.compile(r"(\d{3}) (\d{3}) (\d{3})")
p_nif = re.compile(r"([XYZ\d])(\d{7})((?![ÑIOU])[A-Z])")
p_fecha = re.compile(r"((?P<anyo>\d{4})-(?P<mes>\d{2})-(?P<dia>\d{2}) +(?P<hora>\d{2}):(?P<min>\d{2}))|((?i)(?P<mes>(j(anuary|une|uly)|february|m(arch|ay)|a(pril|ugust)|september|october|november|december)) +(?P<dia>\d{2}), +(?P<anyo>\d{1,4}) +(?P<hora>\d{1,2}):(?P<min>\d{2}) (?P<letras>AM|PM))|((?P<hora>\d{2}):(?P<min>\d{2}):(?P<seg>\d{2}) +(?P<dia>\d{2})/(?P<mes>\d{2})/(?P<anyo>\d{4}))")
p_coord = re.compile(r"((\+{0,1}|-)(?P<grados1>\d{1,2}\.\d{1,}) *, *(\+{0,1}|-)(?P<grados2>\d{1,3}\.\d{1,}))|((?P<grados1>\d{1,2})º *(?P<minutos1>\d{1,2})' *(?P<segundos1>\d{1,2}.\d{4})\" *(?P<letra1>[NS]) *, *(?P<grados2>\d{1,2,3})º *(?P<minutos2>\d{1,2})' *(?P<segundos2>\d{1,2}.\d{4})\" *(?P<letra2>[EW]))|((?P<grados1>(\d{3}))(?P<minutos1>\d{2})(?P<segundos1>\d{2}.\d{4})(?P<letra1>[NS])(?P<grados2>\d{3})(?P<minutos2>\d{2})(?P<segundos2>\d{2}.\d{4})(?P<letra2>[EW]))")
d_mes = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}
d_numMes = {"1": "January", "2": "February", "3": "March", "4": "April", "5": "May", "6": "June", "7": "July", "8": "August", "9": "September", "10": "October", "11": "November", "12": "December"}


# SESION 1 :
# EJERCICIO 1 :
def bisiesto(anyo):
    return anyo % 4 == 0 and (anyo % 400 == 0 or anyo % 100 != 0)

# EJERCICIO 2 :
def verificarfecha(anyo, mes, dia):
    if mes == 2:
        if bisiesto(anyo):
            return 0 < dia <= 29           # Comparaciones concadenadas. Pág : 21
        else:
            return 0 < dia <= 28
    elif mes in [4, 6, 9, 11]:           # Meses con 30 días
        return 0 < dia <= 30
    elif mes in [1, 3, 5, 7, 8, 10, 12]:                               # Meses con 31 días
        return 0 < dia <= 31
    return 0

# EJERCICIO 3 :
def verificarhora(horas,minutos,segundos):
    return 0 <= horas <= 23 and 0 <= minutos <= 59 and 0 <= segundos <= 59

# EJERCICIO 4 :
def compararfechas(anyo1, mes1, dia1, hora1, minuto1, segundo1, anyo2, mes2, dia2, hora2, minuto2, segundo2):
    if (anyo1, mes1, dia1) < (anyo2, mes2, dia2):
        return -1
    elif (anyo1, mes1, dia1) > (anyo2, mes2, dia2):
        return 1
    # Si las fechas son iguales, comparamos la hora
    elif (hora1, minuto1, segundo1) < (hora2, minuto2, segundo2):
        return -1
    elif (hora1, minuto1, segundo1) > (hora2, minuto2, segundo2):
        return 1
    else:
        return 0


# SESIÓN 2 :
# EJERCICIO 1 :
def letraDNI(dni):
     lista = 'TRWAGMYFPDXBNJZSQVHLCKE'
     numero =dni % 23
     return "%s" % lista[numero]

# EJERCICIO 2 :
def nifValido(dni):
    if dni[0] == 'X':
        numero = int("0" + dni[1:8])
    elif dni[0] == 'Y':
        numero = int("1" + dni[1:8])
    elif dni[0] == 'Z':
        numero = int("2" + dni[1:8])
    else:
        numero = int(dni[0:8])

    return dni[-1] == letraDNI(numero)


def coordenadaValida(grados1, minutos1, segundos1, grados2, minutos2, segundos2):
    return abs(grados1) >= 0 and abs(grados1) < 90 and minutos1 >= 0 and minutos1 < 60 and segundos1 >= 0 and segundos1 < 60 and abs(grados2) >= 0 and abs(grados2) < 180 and minutos2 >= 0 and minutos2 < 60 and segundos2 >= 0 and segundos2 < 60

 # EJERCICIO 3 :
def generarListaDNI(tamano):
    lista = []
    while len(lista) < tamano:
        dni = random.randint(0,99999999)
        letra = letraDNI(dni)
        dniFinal = str(dni) + letra

        if dniFinal not in lista:
           lista.append(dniFinal)

    return lista

# SESION 3 :

formatosTotales = [
    "Formato1",  # "YYYY-MM-DD HH:MM"   // DECIMAL
    "Formato2",  # "Month D, Y HH:MM AM/PM" // SEXAGESIMAL
    "Formato3"  # "HH:MM:SS DD/MM/YYYY"  // GPS
]

def generaTelefonos():
    return "%03d %03d %03d" % (random.randint(0, 999), random.randint(0, 999), random.randint(0, 999))

def generar_nif():
    letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
    numero = random.randint(0, 99999999)
    letra = letras[numero % 23]
    return "%08d%s" % (numero, letra)

def generar_nie():
    letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
    numero = random.randint(0, 999999)
    prefijo = random.choice(['X', 'Y', 'Z'])
    numero_final = 0

    if prefijo == 'X':
        numero_final = int("0" + str(numero))
    elif prefijo[0] == 'Y':
        numero_final = int("1" + str(numero))
    elif prefijo[0] == 'Z':
        numero_final = int("2" + str(numero))

    letra = letras[numero_final % 23]
    return "%s%07d%s" % (prefijo, numero_final, letra)

def generar_fechas():

    anyo = random.randint(1900,2024)
    mes = random.randint(1,12)

    if mes == 2:
        if bisiesto(anyo):
           dia = random.randint(1,29)
        else:
           dia = random.randint(1,28)
    elif mes in [4, 6, 9, 11]:
        dia = random.randint(1,30)
    else:
        dia = random.randint(1,31)

    hora = random.randint(0, 23)
    min = random.randint(0, 59)
    seg = random.randint(0, 59)

    formato = random.choice(formatosTotales)

    if formato == "Formato1":
        fecha = "%d-%02d-%02d %02d:%02d" % (anyo, mes, dia, hora, min)
    elif formato == "Formato2":
        meses = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                 "November", "December"]
        mes = meses[mes-1]

        if hora < 12:
            am_pm = "AM"
        else:
            am_pm = "PM"

        hora = hora % 12

        fecha = "%s %d, %d %d:%d %s" % (mes, dia, anyo, hora, min, am_pm)

    else:
        fecha = "%02d:%02d:%02d %02d/%02d/%d" % (hora, min, seg, dia, mes, anyo)

    return fecha

''' Se podría implementar para simplificar cálculos
def calculoGradosMinSeg(coordenada):
    grados = int(abs(coordenada))
    minutos_decimal = (abs(coordenada) - grados) * 60
    minutos = int(minutos_decimal)
    segundos = (minutos_decimal - minutos) * 60
    return grados, minutos, segundos
'''

def generar_coordenadas():
    latitud = random.uniform(-90.0, 90.0)
    longitud = random.uniform(-180.0, 180.0)

    formato = random.choice(formatosTotales)

    if formato == "Formato1":
        coordenadas = "%lf,%lf" % (latitud, longitud)
        return coordenadas

    elif formato == "Formato2":
        # Latitud :
        latitud_grados = int(abs(latitud))      # Si el número es 23.5, se quedaría en 23.
        latitud_grados_a_minutos = (latitud - latitud_grados) * 60  # Se obtiene la parte decimal y se convierte a minutos.
        latitud_minutos = int(abs(latitud_grados_a_minutos))
        latitud_minutos_a_segundos = (latitud_grados_a_minutos -latitud_minutos) * 60
        latitud_segundos = int(abs(latitud_minutos_a_segundos))

        # Cálculo letra en latitud :
        if latitud_grados >= 0:
            latitud_letra = "N"
        else:
            latitud_letra = "S"

        latitud_final = "%dº %d' %d'' %s" %(abs(latitud),latitud_minutos,latitud_segundos,latitud_letra)

        # Longitud :
        longitud_grados = int(abs(longitud))
        longitud_grados_a_minutos = (longitud - longitud_grados) * 60
        longitud_minutos = int(longitud_grados_a_minutos)
        longitud_minutos_a_segundos = (longitud_grados_a_minutos - longitud_minutos) * 60
        longitud_segundos = int(longitud_minutos_a_segundos)

        # Cálculo letra en longitud :
        if longitud_grados >= 0:
            longitud_letra = "E"
        else:
            longitud_letra = "W"

        longitud_final = "%dº %d' %d'' %s " % (abs(longitud),longitud_minutos,longitud_segundos,longitud_letra)
        coordenadas = "%s, %s" %(latitud_final,longitud_final)
        return coordenadas

    else:
        # LATITUD :
        latitud_grados = int(abs(latitud))
        latitud_grados_a_minutos = (latitud - latitud_grados) * 60
        latitud_minutos = int(latitud_grados_a_minutos)
        latitud_minutos_a_segundos = (latitud_grados_a_minutos - latitud_minutos) * 60
        latitud_segundos = int(latitud_minutos_a_segundos)

        if latitud_grados >= 0:
            latitud_letra = "N"
        else:
            latitud_letra = "S"

        latitud_final = "%03d%02d%07.4f%s" %(abs(latitud),latitud_minutos,latitud_segundos,latitud_letra)

        # Longitud :
        longitud_grados = int(abs(longitud))
        longitud_grados_a_minutos = (longitud - longitud_grados) * 60
        longitud_minutos = int(longitud_grados_a_minutos)
        longitud_minutos_a_segundos = (longitud_grados_a_minutos - longitud_minutos) * 60
        longitud_segundos = int(longitud_minutos_a_segundos)

        if longitud_grados >= 0:
            longitud_letra = "E"
        else:
            longitud_letra = "W"

        longitud_final = "%03d%02d%07.4f%s" % (abs(longitud),longitud_minutos,longitud_segundos,longitud_letra)
        coordenadas = "%s%s" % (latitud_final,longitud_final)
        return coordenadas

def generar_producto():
    productos = ["Tablet", "Auriculares", "Teléfono", "Ordenador", "Portátil"]
    return random.choice(productos)

def generar_precio():
    return "%d%s" % (random.randint(100, 5000), '€')

def generar_Formato(tamano):
    lista = []
    contador = 0
    while contador < tamano:
        tlf = generaTelefonos()
        nif = random.choice([generar_nif(), generar_nie()])
        fecha = generar_fechas()
        coordenadas = generar_coordenadas()
        producto = generar_producto()
        precio = generar_precio()

        linea = "%s ; %s ; %s ; %s ; %s ; %s" % (tlf,nif,fecha,coordenadas,producto,precio)
        lista.append(linea)
        contador = contador + 1

    return lista

def verifica_Telefono(texto):
    m = p_tlf.fullmatch(texto)
    if m:
        return {"Telefono": m[0]}
    else:
        return None

def verifica_nif(dni):
    d = p_nif.fullmatch(dni)
    if d:
        if d[1] in ["X","Y","Z"] and nifValido(dni):
            return {"NIF": d[0]}
        else:
            return None
    else:
        return None

def verifica_fecha(fecha):
    f = p_fecha.fullmatch(fecha)
    if f:
        if not f["mes"].isnumeric():
            m = f["mes"].lower()
            mes = d_mes[m]
        else:
            mes = int(f["mes"])

        if f["seg"]:
            seg = f["seg"]
        else:
            seg = "00"

        if verificarhora(int(f["hora"]), int(f["min"]), int(seg)) and verificarfecha(int(f["anyo"]), mes, int(f["dia"])):
            return {
                "dia": f["dia"],
                "mes": str(mes),
                "año": f["anyo"],
                "hora": f["hora"],
                "min": f["min"],
                "seg": str(seg),
                "letras": f["letras"]
            }
        else:
            return None
    else:
        return None


def verifica_coord(coordenadas):
    c = p_coord.fullmatch(coordenadas)
    if c:
        if c["minutos1"]:
            minutos1 = c["minutos1"]
        else:
            minutos1 = 0

        if c["minutos2"]:
            minutos2 = c["minutos2"]
        else:
            minutos2 = 0

        if c["segundos1"]:
            segundos1 = c["segundos1"]
        else:
            segundos1 = 0

        if c["segundos2"]:
            segundos2 = c["segundos2"]
        else:
            segundos2 = 0

        if coordenadaValida(float(c["grados1"]), float(minutos1), float(segundos1), float(c["grados2"]), float(minutos2), float(segundos2)):
            return {
                "grados1": c["grados1"],
                "minutos1": str(minutos1),
                "segundos1": str(segundos1),
                "grados2": c["grados2"],
                "minutos2": str(minutos2),
                "segundos2": str(segundos2),
                "letra1": c["letra1"],
                "letra2": c["letra2"]
            }
        else:
            return None
    else:
        return None


def escribirDiccionarios(telefono, fecha, nif, coord, formatoFecha, formatoCoordenadas):
        print(telefono["Telefono"] + ";" + nif["NIF"] + ";", end='')
        if formatoFecha == 1:
            print(fecha["año"] + "-" + fecha["mes"] + "-" + fecha["dia"] + " " + fecha["hora"] + ":" + fecha[
                "min"] + ";", end='')
        elif formatoFecha == 2:
            print(d_numMes.get(int(fecha["mes"])) + " " + fecha["dia"] + ", " + fecha["año"] + " " + fecha[
                "hora"] + ":" + fecha["min"] + " " + fecha["letras"] + ";", end='')
        else:
            print(fecha["hora"] + ":" + fecha["min"] + ":" + fecha["seg"] + " " + fecha["dia"] + "/" + fecha[
                "mes"] + "/" + fecha["año"] + ";", end='')

        if formatoCoordenadas == 1:
            print(coord["grados1"] + ", " + coord["grados2"])
        elif formatoCoordenadas == 2:
            print(coord["grados1"] + "º " + coord["minutos1"] + "' " + coord["segundos1"] + '"' + coord[
                "letra1"] + ", " + coord["grados2"] + "º " + coord["minutos2"] + "' " + coord["segundos2"] + '"' +
                  coord["letra2"])
        else:
            print(
                coord["grados1"] + coord["minutos1"] + coord["segundos1"] + coord["letra1"] + coord["grados2"] + coord[
                    "minutos2"] + coord["segundos2"] + coord["letra2"])


# EJERCICIO 5 :
def main():
    telefono = verifica_Telefono("535 434 343")
    fecha = verifica_fecha("08:15:00 06/08/1945")
    NIF = verifica_nif("X4858856Z")
    coord = verifica_coord("0250300.0000S0150722.8000E")
    if telefono and fecha and NIF and coord:
        escribirDiccionarios(telefono, fecha, NIF, coord, 2, 2)
    else:
        print("Formato incorrecto")

    #  EJERCICIO SESION 1 :
    '''

    contador = 1
    while contador <= 3:                # El número original es 100, se acorta para visualizar las otras llamadas.
        a = random.randint(0, 2024)
        m = random.randint(1, 12)
        d = random.randint(1, 31)
        h = random.randint(0, 23)
        min = random.randint(0, 59)
        s = random.randint(0, 59)
        while verificarhora(h,min,s) and verificarfecha(a,m,d):
            a = random.randint(0, 2024)
            m = random.randint(1, 12)
            d = random.randint(1, 31)
            h = random.randint(0, 23)
            min = random.randint(0, 59)
            s = random.randint(0, 59)
        print(f"{h}:{min}:{s}  {d}/{m}/{a}\n")
        # PROFESOR : Debemos retornar una lista con estos datos, no hay que imprimirlos.
        contador += 1
    

    # EJERCICIO SESION 2:
    dni = sys.argv[1]  # X2948453Z
    tamano = int(sys.argv[2])

    res2 = nifValido(dni)
    print(f'{res2}')

    res3 = generarListaDNI(tamano)
    print(f'{res3}')

    # SESIÓN 3 :
    print(generaTelefonos())
    print(random.choice([generar_nif(), generar_nie()]))
    print(generar_fechas())
    print(generar_coordenadas())
    print(generar_producto())
    print(generar_precio())
    tam = 3
    lista = generar_Formato(tam)

    for i in lista:
        print(i, end = "\n")
    '''


main()



