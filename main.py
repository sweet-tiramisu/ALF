import sys
import regex as re
import math

# SESIONES 4,5,6:
p_tlf = re.compile(r"^((\d{3}) (\d{3}) (\d{3}))|(\+\d (\d ?){9,14})|(\+\d{2} (\d ?){8,13}|\+\d{3} (\d ?){7,12})$")
p_nif = re.compile(r"^([XYZ\d])(\d{7})((?![ÑIOU])[A-Z])$")
p_fecha = re.compile(r"^((?P<anyo>\d{4})-(?P<mes>\d{2})-(?P<dia>\d{2}) +(?P<hora>\d{2}):(?P<min>\d{2}))|((?i)("
                     r"?P<mes>(j(anuary|une|uly)|february|m(arch|ay)|a("
                     r"pril|ugust)|september|october|november|december)) +(?P<dia>\d{1,2}), +(?P<anyo>\d{1,"
                     r"4}) +(?P<hora>\d{1,2}):(?P<min>\d{2}) (?P<letras>AM|PM))|((?P<hora>\d{2}):(?P<min>\d{2}):("
                     r"?P<seg>\d{2}) +(?P<dia>\d{2})/(?P<mes>\d{2})/(?P<anyo>\d{4}))$")
p_coord = re.compile(
    r"^((?P<grados1>(\+{0,1}|-)\d{1,2}\.\d{1,}) *, *(?P<grados2>(\+{0,1}|-)\d{1,3}\.\d{1,}))|((?P<grados1>\d{1,2})º *(?P<minutos1>\d{1,2})' *(?P<segundos1>\d{1,2}\.\d{4})\" *(?P<letra1>[NS]) *, *(?P<grados2>\d{1,3})º *(?P<minutos2>\d{1,2})' *(?P<segundos2>\d{1,2}\.\d{4})\" *(?P<letra2>[EW]))|((?P<grados1>(\d{3}))(?P<minutos1>\d{2})(?P<segundos1>\d{2}.\d{4})(?P<letra1>[NS])(?P<grados2>\d{3})(?P<minutos2>\d{2})(?P<segundos2>\d{2}.\d{4})(?P<letra2>[EW]))$")
p_precio = re.compile(r"^\d+(\.\d+){0,1}€$")
p_linea = re.compile(r"^(.+);(.+);(.+);(.+);(.+);(.+)$")

d_mes = {"january": "01", "february": "02", "march": "03", "april": "04", "may": "05", "june": "06", "july": "07",
         "august": "08",
         "september": "09", "october": "10", "november": "11", "december": "12"}

productos = ["Tablet", "Auriculares", "Teléfono", "Ordenador", "Portátil"]

meses = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December"]

# SESIÓN 1
def bisiesto(anyo):
    return anyo % 4 == 0 and (anyo % 400 == 0 or anyo % 100 != 0)


def fecha_correcta(anyo, mes, dia):
    if mes == 2:
        if bisiesto(anyo):
            return 0 < dia <= 29  # Comparaciones concadenadas. Pág : 21
        else:
            return 0 < dia <= 28
    elif mes in [4, 6, 9, 11]:  # Meses con 30 días
        return 0 < dia <= 30
    elif mes in [1, 3, 5, 7, 8, 10, 12]:  # Meses con 31 días
        return 0 < dia <= 31
    return 0


def verificar_hora(horas, minutos, segundos):
    return 0 <= horas <= 23 and 0 <= minutos <= 59 and 0 <= segundos <= 59

def comparar_fechas(anyo1, mes1, dia1, hora1, minuto1, segundo1, anyo2, mes2, dia2, hora2, minuto2, segundo2):
    if (anyo1, mes1, dia1, hora1, minuto1, segundo1) < (anyo2, mes2, dia2, hora2, minuto2, segundo2):
        return -1
    elif (anyo1, mes1, dia1, hora1, minuto1, segundo1) > (anyo2, mes2, dia2, hora2, minuto2, segundo2):
        return 1
    return 0


# SESIÓN 2
def letra_dni(dni):
    lista = 'TRWAGMYFPDXBNJZSQVHLCKE'
    numero = dni % 23
    return "%s" % lista[numero]


def nif_valido(nif):
    if nif[0] == 'X':
        numero = int("0" + nif[1:8])
    elif nif[0] == 'Y':
        numero = int("1" + nif[1:8])
    elif nif[0] == 'Z':
        numero = int("2" + nif[1:8])
    else:
        numero = int(nif[0:8])
    return nif[-1] == letra_dni(numero)


# SESIÓN 6 Y 7:
def verificar_telefono(tlf):
    m = p_tlf.fullmatch(tlf)
    if m:
        return m[0]
    return None


def verificar_nif(nif):
    d = p_nif.fullmatch(nif)
    if d and nif_valido(nif):
        return d[0]
    return None


def verificar_precio(precio):
    p = p_precio.fullmatch(precio)
    if p:
        return p[0]
    return None


def verificar_fecha(fecha):
    f = p_fecha.fullmatch(fecha)
    if f:
        mes = f["mes"]
        if not f["mes"].isnumeric():  # Si se trata del segundo formato -> 'May'
            m = f["mes"].lower()  # 'May' -> 'may'
            mes = d_mes.get(m)  # 'may' -> '05'

        seg = (f["seg"] or "00")  # Si no tiene segundos (Primer formato) se establecen a 0.

        if verificar_hora(int(f["hora"]), int(f["min"]), int(seg)) and fecha_correcta(int(f["anyo"]), int(mes),
                                                                                      int(f["dia"])):
            return {
                "dia": f["dia"],
                "mes": str(mes),
                "año": f["anyo"],
                "hora": f["hora"],
                "min": f["min"],
                "seg": seg,
                "letras": f["letras"],
                "original": f[0]  # Guardamos la fecha completa para devolverla en los filtrados.
            }
    return None


def coordenada_valida(grados1, minutos1, segundos1, grados2, minutos2, segundos2):
    return 0 <= abs(grados1) < 90 and 0 <= minutos1 < 60 and 0 <= segundos1 < 60 and 0 <= abs(
        grados2) < 180 and 0 <= minutos2 < 60 and 0 <= segundos2 < 60


def verificar_coord(coordenadas):
    c = p_coord.fullmatch(coordenadas)
    if c:
        minutos1 = (c["minutos1"] or 0)  # En el caso de que c["minutos1"] no exista, se asignará un 0.
        minutos2 = (c["minutos2"] or 0)
        segundos1 = (c["segundos1"] or 0)
        segundos2 = (c["segundos2"] or 0)

        if coordenada_valida(float(c["grados1"]), float(minutos1), float(segundos1),
                             float(c["grados2"]), float(minutos2), float(segundos2)):
            return {
                "grados1": c["grados1"],
                "minutos1": str(minutos1),
                "segundos1": str(segundos1),
                "letra1": c["letra1"],
                "grados2": c["grados2"],
                "minutos2": str(minutos2),
                "segundos2": str(segundos2),
                "letra2": c["letra2"],
                "original": c[0]  # Guardamos la coordenada completa para devolverla en los filtrados sin normalizar.
            }
    return None


def coordenadas_a_grados(g, m, s, letra):
    if letra:
        grados = g + m / 60 + s / 3600
        if letra == "S" or letra == "W":
            grados *= -1
        return grados
    else:
        return g


def convertir_coordenadas(g):
    grados = int(abs(g))
    grados_a_minutos = (abs(g) - grados) * 60
    minutos = int(grados_a_minutos)
    minutos_a_segundos = (grados_a_minutos - minutos) * 60
    segundos = float(minutos_a_segundos)
    return {
        "grados": grados,
        "minutos": minutos,
        "segundos": segundos
    }


def grados_a_coordenadas(g1, g2):
    latitud_diccionario = convertir_coordenadas(g1)
    longitud_diccionario = convertir_coordenadas(g2)
    letra1 = "S"
    letra2 = "W"
    if g1 >= 0:
        letra1 = "N"
    if g2 >= 0:
        letra2 = "E"

    return {
        "grados1": latitud_diccionario.get("grados"),
        "minutos1": latitud_diccionario.get("minutos"),
        "segundos1": latitud_diccionario.get("segundos"),
        "letra1": letra1,
        "grados2": longitud_diccionario.get("grados"),
        "minutos2": longitud_diccionario.get("minutos"),
        "segundos2": longitud_diccionario.get("segundos"),
        "letra2": letra2
    }


def convertir_24h(hora, letras):
    hora = int(hora)
    if letras.lower() == "am":
        if hora == 12:  # Si es 12 AM, se convierte a 0
            hora = 0
    elif letras.lower() == "pm":
        if hora != 12:  # Si no es 12 PM, le sumo 12 a la hora
            hora += 12
    return hora


def mostrar_telefono(diccionario):
    return diccionario["Telefono"]


def mostrar_nif(diccionario):
    return diccionario["Nif"]


def mostrar_fecha(diccionario, formato_fecha):
    fecha = diccionario["Fecha"]
    if formato_fecha == 1:
        if fecha["letras"]:
            fecha["hora"] = convertir_24h(fecha["hora"], fecha["letras"])
        return ('%02d-%02d-%02d %02d:%02d' % (
        int(fecha["año"]), int(fecha["mes"]), int(fecha["dia"]), int(fecha["hora"]), int(fecha["min"])))
    elif formato_fecha == 2:
        if fecha["letras"]:
            hora = fecha["hora"]
            letra = fecha["letras"]
        else:  # No tiene AM/PM
            if int(fecha["hora"]) % 12 == 0:
                hora = "12"
            else:
                hora = str(int(fecha["hora"]) % 12)
            if 0 <= int(fecha["hora"]) / 12 < 1:
                letra = "AM"
            else:
                letra = "PM"
        return ('%s %d, %d %s:%s %s' % (
        meses[int(fecha["mes"]) - 1], int(fecha["dia"]), int(fecha["año"]), hora, fecha["min"], letra))
    else:
        if fecha["letras"]:
            fecha["hora"] = convertir_24h(fecha["hora"], fecha["letras"])
        return ('%02d:%s:%02s %02d/%02d/%04s' % (
        int(fecha["hora"]), fecha["min"], fecha["seg"], int(fecha["dia"]), int(fecha["mes"]), fecha["año"]))


def mostrar_coord(diccionario, formato_coordenadas):
    coord = diccionario["Coordenadas"]
    if formato_coordenadas == 1:
        grados_latitud = coordenadas_a_grados(float(coord["grados1"]), float(coord["minutos1"]),
                                              float(coord["segundos1"]), coord["letra1"])
        grados_longitud = coordenadas_a_grados(float(coord["grados2"]), float(coord["minutos2"]),
                                               float(coord["segundos2"]), coord["letra2"])
        return '%f, %f' % (grados_latitud, grados_longitud)
    elif formato_coordenadas == 2:
        if not coord["letra1"]:
            coord = grados_a_coordenadas(float(coord["grados1"]), float(coord["grados2"]))
        return '%02dº %d\' %06.4f\" %s, %02dº %d\' %06.4f\" %s' % (
        int(coord["grados1"]), int(coord["minutos1"]), float(coord["segundos1"]), coord["letra1"],
        int(coord["grados2"]), int(coord["minutos2"]), float(coord["segundos2"]), coord["letra2"])
    else:
        if not coord["letra1"]:
            coord = grados_a_coordenadas(float(coord["grados1"]), float(coord["grados2"]))
        return '%03d%02d%07.4f%s%03d%02d%07.4f%s' % (
        int(coord["grados1"]), int(coord["minutos1"]), float(coord["segundos1"]), str(coord["letra1"]),
        int(coord["grados2"]), int(coord["minutos2"]), float(coord["segundos2"]), str(coord["letra2"]))


# Para la función de normalizar
def escribir_diccionarios_normalizar(diccionario, formato_fecha, formato_coordenadas):
    print('%s;%s;%s;%s;%s;%s' % (
    mostrar_telefono(diccionario), mostrar_nif(diccionario), mostrar_fecha(diccionario, formato_fecha),
    mostrar_coord(diccionario, formato_coordenadas), diccionario["Producto"], diccionario["Precio"]))


# Para el resto de funciones sin normalizar
def escribir_diccionarios(diccionario):
    print('%s;%s;%s;%s;%s;%s' % (
    mostrar_telefono(diccionario), mostrar_nif(diccionario), diccionario["Fecha"]["original"],
    diccionario["Coordenadas"]["original"], diccionario["Producto"], diccionario["Precio"]))


def verificar_formato(linea):
    f = p_linea.fullmatch(linea)
    telefono = verificar_telefono(f[1].strip())  # Se deben suprimir los espacios
    nif = verificar_nif(f[2].strip())
    fecha = verificar_fecha(f[3].strip())
    coordenadas = verificar_coord(f[4].strip())
    producto = f[5].strip()
    precio = verificar_precio(f[6].strip())

    if telefono is None or nif is None or fecha is None or coordenadas is None or producto not in productos or precio is None:
        return None
    else:
        return {
            "Telefono": telefono,
            "Nif": nif,
            "Fecha": fecha,
            "Coordenadas": coordenadas,
            "Producto": producto,
            "Precio": precio
        }


def normalizar(fichero):
    try:
        archivo = open(fichero, 'r+', encoding="utf8")  # Para que detecte el símbolo del euro
        for linea in archivo:
            diccionario = verificar_formato(linea.strip())
            if diccionario:
                escribir_diccionarios_normalizar(diccionario, 1, 3)  # Las fechas se normalizan
        archivo.close()
    except FileNotFoundError:
        print("ERROR: El archivo no se ha encontrado")
        exit(1)


def filtrar_telefono(fichero, telefono):
    try:
        archivo = open(fichero, 'r+', encoding="utf8")
        telefono = verificar_telefono(telefono)

        if telefono:
            telefono = telefono.replace(" ", "")
            if len(telefono) == 9:
                telefono = "+34" + telefono
            for linea in archivo:
                diccionario = verificar_formato(linea.strip())
                if diccionario:
                    tlf = diccionario["Telefono"].replace(" ", "")
                    if len(tlf) == 9:
                        tlf = "+34" + tlf
                    if tlf == telefono:
                        escribir_diccionarios(diccionario)
        else:
            print('Uso: Python %s -sphone <telefono> <fichero>' % sys.argv[0], file=sys.stderr)
            exit(2)
        archivo.close()
    except FileNotFoundError:
        print("ERROR: El archivo no se ha encontrado")
        exit(1)


def filtrar_nif(fichero, nif):
    try:
        archivo = open(fichero, 'r+', encoding='utf8')
        nif = verificar_nif(nif)
        if nif:
            for linea in archivo:
                diccionario = verificar_formato(linea.strip())
                if diccionario and diccionario["Nif"] == nif:
                    escribir_diccionarios(diccionario)
        else:
            print('Uso: Python %s -snif <NIF> <fichero>' % sys.argv[0], file=sys.stderr)
            exit(2)
        archivo.close()
    except FileNotFoundError:
        print("ERROR: El archivo no se ha encontrado")
        exit(1)


def filtrar_fechas(fichero, fecha1, fecha2):
    try:
        archivo = open(fichero, 'r+', encoding='utf8')
        inicio = verificar_fecha(fecha1)
        fin = verificar_fecha(fecha2)
        if inicio and fin:
            for linea in archivo:
                diccionario = verificar_formato(linea.strip())
                if diccionario:
                    fecha = diccionario["Fecha"]
                    if comparar_fechas(inicio["año"], inicio["mes"], inicio["dia"], inicio["hora"], inicio["min"],
                                       inicio["seg"], fecha["año"], fecha["mes"], fecha["dia"], fecha["hora"],
                                       fecha["min"],
                                       fecha["seg"]) == -1 and comparar_fechas(fecha["año"], fecha["mes"], fecha["dia"],
                                                                               fecha["hora"], fecha["min"],
                                                                               fecha["seg"], fin["año"], fin["mes"],
                                                                               fin["dia"],
                                                                               fin["hora"], fin["min"],
                                                                               fin["seg"]) == -1:
                        escribir_diccionarios(diccionario)
        else:
            print('Uso: Python %s -stime <desde> <hasta> <fichero>' % sys.argv[0], file=sys.stderr)
            exit(2)
        archivo.close()
    except FileNotFoundError:
        print("ERROR: El archivo no se ha encontrado")
        exit(1)


def semiversin(valor):
    return math.pow(math.sin(valor / 2), 2)


def distancia_coordenadas(coord1, coord2):
    lat1 = math.radians(
        coordenadas_a_grados(float(coord1["grados1"]), float(coord1["minutos1"]), float(coord1["segundos1"]),
                             coord1["letra1"]))
    long1 = math.radians(
        coordenadas_a_grados(float(coord1["grados2"]), float(coord1["minutos2"]), float(coord1["segundos2"]),
                             coord1["letra2"]))
    lat2 = math.radians(
        coordenadas_a_grados(float(coord2["grados1"]), float(coord2["minutos1"]), float(coord2["segundos1"]),
                             coord2["letra1"]))
    long2 = math.radians(
        coordenadas_a_grados(float(coord2["grados2"]), float(coord2["minutos2"]), float(coord2["segundos2"]),
                             coord2["letra2"]))
    r = 6371
    h = semiversin(lat1 - lat2) + math.cos(lat1) * math.cos(lat2) * semiversin(math.fabs(long1 - long2))
    return 2 * r * math.asin(math.sqrt(h))


def filtrar_coordenadas(fichero, coordenada, distancia):
    try:
        archivo = open(fichero, 'r', encoding='utf8')
        coord1 = verificar_coord(coordenada)
        if coord1 and distancia.replace(".", "", 1).isnumeric():
            for linea in archivo:
                diccionario = verificar_formato(linea[:-1])
                if diccionario:
                    coord2 = diccionario["Coordenadas"]
                    if distancia_coordenadas(coord1, coord2) < float(distancia):
                        escribir_diccionarios(diccionario)
        else:
            print('Uso: Python %s -slocation <desde> <hasta> <fichero>' % sys.argv[0], file=sys.stderr)
            exit(2)
        archivo.close()
    except FileNotFoundError:
        print("ERROR: El archivo no se ha encontrado")
        exit(1)


def main():
    if sys.argv[1] == "-n":
        if len(sys.argv) == 3:
            normalizar(sys.argv[2])
        else:
            print('Uso: Python %s -n <fichero>' % sys.argv[0], file=sys.stderr)
            exit(2)
    elif sys.argv[1] == "-sphone":
        if len(sys.argv) == 4:
            filtrar_telefono(sys.argv[3], sys.argv[2])
        else:
            print('Uso: Python %s -sphone <telefono> <fichero>' % sys.argv[0], file=sys.stderr)
            exit(2)
    elif sys.argv[1] == "-snif":
        if len(sys.argv) == 4:
            filtrar_nif(sys.argv[3], sys.argv[2])
        else:
            print('Uso: Python %s -snif <NIF> <fichero>' % sys.argv[0], file=sys.stderr)
            exit(2)
    elif sys.argv[1] == "-stime":
        if len(sys.argv) == 5:
            filtrar_fechas(sys.argv[4], sys.argv[2], sys.argv[3])
        else:
            print('Uso: Python %s -stime <desde> <hasta> <fichero>' % sys.argv[0], file=sys.stderr)
            exit(2)
    elif sys.argv[1] == "-slocation":
        if len(sys.argv) == 5:
            filtrar_coordenadas(sys.argv[4], sys.argv[2], sys.argv[3])
        else:
            print('Uso: Python %s -slocation <desde> <hasta> <fichero>' % sys.argv[0], file=sys.stderr)
            exit(2)
    else:
        print('Uso: Python %s [-n|-sphone|-snif|-stime|-slocation] [argumentos]' % sys.argv[0], file=sys.stderr)
        exit(2)


main()
