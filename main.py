import sys
import regex as re
import math

# Expresiones regulares
p_tlf = re.compile( r"^((\d{3}) (\d{3}) (\d{3}))|(\+(\d ?){10,15})$")
p_nif = re.compile(r"^([XYZ\d])(\d{7})((?![ÑIOU])[A-Z])$")
p_fecha = re.compile(r"^((?P<anyo>\d{4})-(?P<mes>\d{2})-(?P<dia>\d{2}) +(?P<hora>\d{2}):(?P<min>\d{2}))|"
                     r"((?i)(?P<mes>(j(anuary|une|uly)|february|m(arch|ay)|a(pril|ugust)|september|october|november|december)) +(?P<dia>\d{1,2}), +(?P<anyo>\d{1,4}) +(?P<hora>\d{1,2}):(?P<min>\d{2}) +(?P<letras>AM|PM))|"
                     r"((?P<hora>\d{2}):(?P<min>\d{2}):(?P<seg>\d{2}) +(?P<dia>\d{2})/(?P<mes>\d{2})/(?P<anyo>\d{4}))$")
p_coord = re.compile(
    r"^((?P<grados1>(\+?|-)\d{1,2}\.\d+) *, *(?P<grados2>(\+{0,1}|-)\d{1,3}\.\d+))|"
    r"((?P<grados1>\d{1,2})° *(?P<minutos1>\d{1,2})' *(?P<segundos1>\d{1,2}\.\d{4})\" *(?P<letra1>[NS]) *, *(?P<grados2>\d{1,3})° *(?P<minutos2>\d{1,2})' *(?P<segundos2>\d{1,2}\.\d{4})\" *(?P<letra2>[EW]))|"
    r"((?P<grados1>(\d{3}))(?P<minutos1>\d{2})(?P<segundos1>\d{2}.\d{4})(?P<letra1>[NS])(?P<grados2>\d{3})(?P<minutos2>\d{2})(?P<segundos2>\d{2}.\d{4})(?P<letra2>[EW]))$")
p_precio = re.compile(r"^\d+(\.\d+)?€$")
p_productos = re.compile(r"^[^;]+$")
p_linea = re.compile(r"^(([^;]+);){5}([^;]+)$")

# Lista de meses, una para lograr la conversión 'january' -> '1' y la otra para convertir '3' -> 'March'
meses_minuscula = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
                    "november", "december"]
meses = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December"]


# Comprueba si un año es bisiesto o no
def bisiesto(anyo):
    return anyo % 4 == 0 and (anyo % 400 == 0 or anyo % 100 != 0)

# Comprueba si una fecha es correcta o no, teniendo en cuenta si pertenece a un mes de 31, 30, 29 o 28 días
def fecha_correcta(anyo, mes, dia):
    if mes == 2:
        if bisiesto(anyo):
            return 0 < dia <= 29  # Comparaciones concadenadas. Pág : 21
        return 0 < dia <= 28
    elif mes in [4, 6, 9, 11]:  # Meses con 30 días
        return 0 < dia <= 30
    elif mes in [1, 3, 5, 7, 8, 10, 12]:  # Meses con 31 días
        return 0 < dia <= 31
    return 0

# Comprueba si la hora es correcta, es decir, si las horas, los minutos y los segundos se encuentran en los rangos establecidos
def verificar_hora(horas, minutos, segundos):
    return 0 <= horas <= 23 and 0 <= minutos <= 59 and 0 <= segundos <= 59

# Compara dos fechas, devuelve -1 si la primera es la más antigua, 1 si lo es la segunda y 0 si son iguales
def comparar_fechas(fecha1, fecha2):
    for elemento in ["año", "mes", "dia", "hora", "min", "seg"]:
        if fecha1[elemento] < fecha2[elemento]:
            return -1
        if fecha1[elemento] > fecha2[elemento]:
            return 1
    return 0

# Dado el número de un DNI, calcula la letra que le corresponde
def letra_dni(dni):
    lista = 'TRWAGMYFPDXBNJZSQVHLCKE'
    numero = dni % 23
    return "%s" % lista[numero]

# Comprueba si un NIF es válido o no, es decir, si su letra es la que le corresponde
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

# Verifica el formato de un teléfono y lo devuelve en forma de cadena (None si es inválido)
def verificar_telefono(tlf):
    m = p_tlf.fullmatch(tlf)
    if m:
        return m[0]
    return None

# Verifica el formato de un NIF, comprueba si es correcto y lo devuelve en forma de cadena (None si es inválido o incorrecto)
def verificar_nif(nif):
    d = p_nif.fullmatch(nif)
    if d and nif_valido(nif):
        return d[0]
    return None

# Verifica el formato de una fecha, comprueba si es correcta, realiza las conversiones que sean necesarias ('August' -> 8)
# y la devuelve en forma de diccionario formado por diferentes campos (None si es inválida o incorrecta)
def verificar_fecha(fecha):
    f = p_fecha.fullmatch(fecha)
    if f:
        mes = f["mes"]
        if not f["mes"].isnumeric():                    # Si se trata del segundo formato -> 'May'
            m = f["mes"].lower()                        # 'May' o 'MAy' o 'MAY' -> 'may'
            mes = meses_minuscula.index(m) + 1          # 'may' -> 5     'meses_minuscula' es una lista declarada arriba

        seg = int(f["seg"] or 0)                        # Si no tiene segundos (Primer formato) se establecen a 0.

        if verificar_hora(int(f["hora"]), int(f["min"]), int(seg)) and fecha_correcta(int(f["anyo"]), int(mes),
                                                                                      int(f["dia"])):
            return {
                "dia": int(f["dia"]),
                "mes": int(mes),
                "año": int(f["anyo"]),
                "hora": int(f["hora"]),
                "min": int(f["min"]),
                "seg": int(seg),
                "letras": f["letras"],
                "original": f[0]     # Guardamos la fecha completa para devolverla en los filtrados.
            }
    return None

# Comprueba si una coordenada es válida o no, de la misma manera que se hace con las horas
def coordenada_valida(grados1, minutos1, segundos1, grados2, minutos2, segundos2):
    return 0 <= abs(grados1) < 90 and 0 <= minutos1 < 60 and 0 <= segundos1 < 60 and 0 <= abs(
        grados2) < 180 and 0 <= minutos2 < 60 and 0 <= segundos2 < 60

# Verifica el formato de una coordenada, comprueba si es correcta, inicializa los campos a 0 si no existen y la devuelve
# en forma de diccionario formado por diferentes campos (None si es inválida o incorrecta)
def verificar_coord(coordenadas):
    c = p_coord.fullmatch(coordenadas)
    if c:
        # En el caso de que el campo de minutos o segundos no exista, se asignará un 0.
        minutos1 = (c["minutos1"] or "0")
        minutos2 = (c["minutos2"] or "0")
        segundos1 = (c["segundos1"] or "0")
        segundos2 = (c["segundos2"] or "0")

        if coordenada_valida(float(c["grados1"]), float(minutos1), float(segundos1),
                             float(c["grados2"]), float(minutos2), float(segundos2)):
            return {
                "grados1": c["grados1"],
                "minutos1": minutos1,
                "segundos1": segundos1,
                "letra1": c["letra1"],
                "grados2": c["grados2"],
                "minutos2": minutos2,
                "segundos2": segundos2,
                "letra2": c["letra2"],
                "original": c[0]  # Guardamos la coordenada completa para devolverla en los filtrados sin normalizar.
            }
    return None

# Verifica el formato de un producto y lo devuelve en forma de cadena (None si es inválido)
def verificar_producto(producto):
    prod = p_productos.fullmatch(producto)
    if prod:
        return prod[0]
    return None

# Verifica el formato de un precio y lo devuelve en forma de cadena (None si es inválido)
def verificar_precio(precio):
    p = p_precio.fullmatch(precio)
    if p:
        return p[0]
    return None

# Convierte grados, minutos y segundos a grados
def coordenadas_a_grados(g, m, s, letra):
    if letra:
        grados = g + m / 60 + s / 3600
        if letra == "S" or letra == "W":
            grados *= -1
        return grados
    return g

# Convierte unos grados dados a grados, minutos y segundos, y los devuelve en forma de diccionario
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

# Convierte una coordenada en formato decimal a grados, minutos y segundos, y la devuelve en forma de diccionario
def grados_a_coordenadas(g1, g2):
    latitud_diccionario = convertir_coordenadas(g1)
    longitud_diccionario = convertir_coordenadas(g2)
    letra1 = "N"
    letra2 = "E"
    if g1 < 0:
        letra1 = "S"
    if g2 < 0:
        letra2 = "W"

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

# Convierte una hora dada en el sistema horario de 12 horas a su equivalente en el sistema horario de 24 horas
def convertir_24h(hora, letras):
    hora = int(hora)
    if letras.lower() == "am":
        if hora == 12:  # Si es 12 AM, se convierte a 0
            hora = 0
    elif letras.lower() == "pm":
        if hora != 12:  # Si no es 12 PM, le sumo 12 a la hora
            hora += 12
    return hora

# Muestra por consola el campo de la fecha de un diccionario dado en el formato que le especifiquemos
# (1 = YYYY-MM-DD HH:MM ; 2 = Month D, Y HH:MM AM/PM ; 3 = HH:MM:SS DD/MM/YYYY)
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

# Muestra por consola el campo de las coordenadas de un diccionario dado en el formato que le especifiquemos
# (1 = Decimal ; 2 = Sexagesimal ; 3 = GPS)
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
        return '%02d° %d\' %06.4f\" %s, %02d° %d\' %06.4f\" %s' % (
        int(coord["grados1"]), int(coord["minutos1"]), float(coord["segundos1"]), coord["letra1"],
        int(coord["grados2"]), int(coord["minutos2"]), float(coord["segundos2"]), coord["letra2"])
    else:
        if not coord["letra1"]:
            coord = grados_a_coordenadas(float(coord["grados1"]), float(coord["grados2"]))
        return '%03d%02d%07.4f%s%03d%02d%07.4f%s' % (
        int(coord["grados1"]), int(coord["minutos1"]), float(coord["segundos1"]), str(coord["letra1"]),
        int(coord["grados2"]), int(coord["minutos2"]), float(coord["segundos2"]), str(coord["letra2"]))

# Muestra por la consola los campos de un diccionario normalizados y separados por punto y coma
def escribir_diccionarios_normalizar(diccionario, formato_fecha, formato_coordenadas):
    print('%s;%s;%s;%s;%s;%s' % (
    diccionario["Telefono"], diccionario["Nif"], mostrar_fecha(diccionario, formato_fecha),
    mostrar_coord(diccionario, formato_coordenadas), diccionario["Producto"], diccionario["Precio"]))

# Muestra por la consola los campos de un diccionario (manteniendo el formato) y separados por punto y coma
def escribir_diccionarios(diccionario):
    print('%s;%s;%s;%s;%s;%s' % (
    diccionario["Telefono"], diccionario["Nif"], diccionario["Fecha"]["original"],
    diccionario["Coordenadas"]["original"], diccionario["Producto"], diccionario["Precio"]))

# Verifica el formato de una línea de una lista de compras y la devuelve en forma de diccionario con los diferentes
# campos que la forman (None si es inválida)
def verificar_formato(linea):
    f = p_linea.fullmatch(linea)
    if f:
        # Se deben comprobar los formatos y suprimir los espacios que pudieran existir entre la cadena y el separador de campo
        telefono = verificar_telefono(f[1].strip())
        nif = verificar_nif(f[2].strip())
        fecha = verificar_fecha(f[3].strip())
        coordenadas = verificar_coord(f[4].strip())
        producto = verificar_producto(f[5].strip())
        precio = verificar_precio(f[6].strip())

        if telefono and nif and fecha and coordenadas and producto and precio :
            return {
                "Telefono": telefono,
                "Nif": nif,
                "Fecha": fecha,
                "Coordenadas": coordenadas,
                "Producto": producto,
                "Precio": precio
            }
    return None

# Invocada con la opción '-n', normaliza un registro de compras (fechas en el segundo formato y las coordenadas en el tercero)
# Muestra un mensaje de error si no se puede abrir el fichero
def normalizar(fichero):
    try:
        archivo = open(fichero, 'r+', encoding="utf8")  # Para que detecte el símbolo del euro
        for linea in archivo:
            diccionario = verificar_formato(linea.strip())
            if diccionario:
                escribir_diccionarios_normalizar(diccionario, 2, 3)  # Las fechas y coordenadas se normalizan
        archivo.close()
    except FileNotFoundError:
        print("ERROR: El archivo no se ha encontrado")
        exit(1)

# Invocada con la opción '-sphone', filtra un registro de compras y muestra solo aquellas cuyo número de teléfono
# coincida con el especificado. Muestra un mensaje de error si no se puede abrir el fichero o si el formato del
# teléfono es incorrecto
def filtrar_telefono(fichero, telefono):
    try:
        archivo = open(fichero, 'r+', encoding="utf8")
        telefono = verificar_telefono(telefono)
        if telefono:
            telefono = telefono.replace(" ", "")
            if len(telefono) == 9:
                telefono = "+34" + str(telefono)  # Si es un número español se añade el prefijo '+34'
            for linea in archivo:
                diccionario = verificar_formato(linea.strip())
                if diccionario:
                    tlf = diccionario["Telefono"].replace(" ", "")
                    if len(tlf) == 9:
                        tlf = "+34" + str(tlf)
                    if tlf == telefono:
                        escribir_diccionarios(diccionario)
        else:
            print('Uso: Python %s -sphone <telefono> <fichero>' % sys.argv[0], file=sys.stderr)
            exit(2)
        archivo.close()
    except FileNotFoundError:
        print("ERROR: El archivo no se ha encontrado")
        exit(1)

# Invocada con la opción '-snif', filtra un registro de compras y muestra solo aquellas cuyo NIF coincida con el
# especificado. Muestra un mensaje de error si no se puede abrir el fichero o si el formato del NIF es incorrecto
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

# Invocada con la opción '-stime', filtra un registro de compras y muestra solo aquellas cuya fecha se entra las dos
# especificadas en la entrada. Muestra un mensaje de error si no se puede abrir el fichero o si el formato de las
# fechas es incorrecto
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
                    if comparar_fechas(inicio, fecha) < 1 and comparar_fechas(fecha, fin) < 1:
                        escribir_diccionarios(diccionario)
        else:
            print('Uso: Python %s -stime <desde> <hasta> <fichero>' % sys.argv[0], file=sys.stderr)
            exit(2)
        archivo.close()
    except FileNotFoundError:
        print("ERROR: El archivo no se ha encontrado")
        exit(1)

# Define la función del semiverseno para calcular la distancia entre dos coordenadas
def semiversin(valor):
    return math.pow(math.sin(valor / 2), 2)

# Calcula la distancia entre dos coordenadas y devuelve un real que representa los kilómetros que hay entre ellas
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

# Invocada con la opción '-slocation', filtra un registro de compras y muestra solo aquellas cuya coordenada se encuentre
# a una distancia igual o menor a la dada de una coordenada determinada. Muestra un mensaje de error si no se puede abrir
# el fichero o si el formato del NIF es incorrecto
def filtrar_coordenadas(fichero, coordenada, distancia):
    try:
        archivo = open(fichero, 'r', encoding='utf8')
        coord1 = verificar_coord(coordenada)
        if coord1 and distancia.replace(".", "", 1).isnumeric():
            for linea in archivo:
                diccionario = verificar_formato(linea[:-1])
                if diccionario:
                    coord2 = diccionario["Coordenadas"]
                    if distancia_coordenadas(coord1, coord2) <= float(distancia):
                        escribir_diccionarios(diccionario)
        else:
            print('Uso: Python %s -slocation <desde> <hasta> <fichero>' % sys.argv[0], file=sys.stderr)
            exit(2)
        archivo.close()
    except FileNotFoundError:
        print("ERROR: El archivo no se ha encontrado")
        exit(1)

# Define el comportamiento del programa principal (interpretar las órdenes que el usuario le introduzca) y muestra
# mensajes de error si el formado de la órden introducida es incorrecto
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

# Ejecuta el programa principal
main()
