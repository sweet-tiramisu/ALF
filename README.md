import sys
import random
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
    else:                               # Meses con 31 días
        return 0 < dia <= 31

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

    if prefijo == 'X':
        numero_final = int("0" + str(numero))
    elif prefijo[0] == 'Y':
        numero_final = int("1" + str(numero))
    elif prefijo[0] == 'Z':
        numero_final = int("2" + str(numero))

    letra = letras[numero_final % 23]
    return "%s%07d%s" % (prefijo, numero_final, letra)

def bisiesto(anyo):
    return anyo % 4 == 0 and (anyo % 400 == 0 or anyo % 100 != 0)

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

def generar_Formato():
    lista = []
    contador = 0
    while contador < 3:
        tlf = str(generaTelefonos())
        nif = str(random.choice([generar_nif(), generar_nie()]))
        fecha = str(generar_fechas())
        coordenadas = str(generar_coordenadas())
        producto = str(generar_producto())
        precio = str(generar_precio())

        linea = "%s ; %s ; %s ; %s ; %s ; %s" % (tlf,nif,fecha,coordenadas,producto,precio)
        lista.append(linea)
        contador = contador + 1

    return lista

# EJERCICIO 5 :
def main():
    #  EJERCICIO SESION 1 :
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
    lista = generar_Formato()

    for i in lista:
        print(i, end = "\n")


main()



