import matplotlib.pyplot as plt
import numpy as np
import math
import random

def funkcja(x):
    return -0.1*x**2+4*x+7

xmin = -1
xmax = 41
wielkosc_populacji = 11
liczba_generacji = 30
szansa_krzyzowania = 0.95
szansa_mutowania = 0.001

roznica = abs(xmin) if xmin<0 else 0
dlugosc_binarna = 0
populacja=[]
nowa_populacja=[]
przystosowanie_min=[]
przystosowanie_max=[]
przystosowanie_avg=[]

def policz_dlugosc_binarana(xmax, roznica):
    binarna = bin(xmax+roznica).replace("0b", "")
    global dlugosc_binarna
    dlugosc_binarna = len(binarna)
    
def skaluj_zakres(liczba, min_wejsciowy, max_wejsciowy, min_wyjsciowy, max_wyjsciowy):
    wspolczynnik = (max_wyjsciowy - min_wyjsciowy) / (max_wejsciowy - min_wejsciowy)
    liczba_wyjsciowa = min_wyjsciowy + (liczba - min_wejsciowy) * wspolczynnik
    return liczba_wyjsciowa

def skaluj_populacje(min_wejsciowy, max_wejsciowy, min_wyjsciowy, max_wyjsciowy):
    global populacja
    wspolczynnik = (max_wyjsciowy - min_wyjsciowy) / (max_wejsciowy - min_wejsciowy)
    for i in range(wielkosc_populacji):  
        populacja[i] = round(min_wyjsciowy + (populacja[i] - min_wejsciowy) * wspolczynnik)

def decimal_binary(n):
    new_n = bin(n).replace("0b", "")
    ile = dlugosc_binarna - len(new_n)
    new_n = ("0"*ile)+new_n
    new_n = list(new_n)
    return new_n

def generuj_populacje():
    global populacja
    for i in range (wielkosc_populacji):
        populacja.append(random.randint(xmin, xmax))

def suma_przystosowan(populacja):
    global minimum
    minimum = 0
    for osobnik in populacja:
        if funkcja(osobnik) < minimum:
            minimum = funkcja(osobnik)
    suma = 0
    for osobnik in populacja:
        suma+=funkcja(osobnik)-minimum
    return suma

def reprodukuj_populacje():
    global populacja
    suma = suma_przystosowan(populacja)
    for i in range (len(populacja)):
        akumulator = 0
        losowa_wartosc = random.uniform(0, suma)
        for index, wartosc in enumerate(populacja):
            akumulator += funkcja(populacja[index])-minimum
            if akumulator > losowa_wartosc:
                nowa_populacja.append(populacja[index])
                break
    podmien_populacje()

def krzyzuj_populacje():
    global populacja
    global nowa_populacja
    if (wielkosc_populacji%2==1):
        nowa_populacja.append(decimal_binary(populacja[-1]))
    for i in range(math.floor(len(populacja)/2)):
        indexa = random.randrange(len(populacja))
        a = populacja[indexa]
        del populacja[indexa]
        indexb = random.randrange(len(populacja))
        b = populacja[indexb]
        del populacja[indexb]
        krzyzuj(a, b)   
    podmien_populacje()
    
def krzyzuj(a, b):
    global nowa_populacja
    a = decimal_binary(a)
    b = decimal_binary(b)
    losowa_wartosc = random.uniform(0, 1)
    if losowa_wartosc<szansa_krzyzowania:
        punkt_krzyzowania = random.randrange(1, dlugosc_binarna)
        new_a = a[:punkt_krzyzowania]+b[punkt_krzyzowania:]
        new_b = b[:punkt_krzyzowania]+a[punkt_krzyzowania:]
        nowa_populacja.append(new_a)
        nowa_populacja.append(new_b)
    else:
        nowa_populacja.append(a)
        nowa_populacja.append(b)
            
def mutuj_populacje():
    global populacja
    for osobnik in populacja:
        for i in range (dlugosc_binarna):
            losowa_wartosc = random.uniform(0, 1)
            if losowa_wartosc<szansa_mutowania:
                if osobnik[i] == '0':
                    osobnik[i] = '1'
                else:
                    osobnik[i] = '0'
            
def podmien_populacje():
    global populacja
    global nowa_populacja
    populacja = nowa_populacja.copy()
    nowa_populacja = []
    
def binary_decimal():
    global nowa_populacja
    for liczba_binarna in populacja:
        liczba_dziesietna = 0
        potega = 0
        for cyfra in reversed(liczba_binarna):
            if cyfra == '1':
                liczba_dziesietna += 2 ** potega
            potega += 1
        nowa_populacja.append(liczba_dziesietna)
    podmien_populacje()
    
def statystyki():
    global przystosowanie_avg
    global przystosowanie_min
    global przystosowanie_max
    suma = 0
    aktualne_min = funkcja(populacja[0])
    aktualne_max = funkcja(populacja[0])
    for osobnik in populacja:
        przystosowanie = funkcja(osobnik)
        suma+=przystosowanie
        if (aktualne_max<przystosowanie):
            aktualne_max=przystosowanie
        if (aktualne_min>przystosowanie):
            aktualne_min=przystosowanie
        
    przystosowanie_avg.append(suma/wielkosc_populacji)
    przystosowanie_max.append(aktualne_max)
    przystosowanie_min.append(aktualne_min)
    
def cykl():
    reprodukuj_populacje()
    skaluj_populacje(xmin, xmax, 0, 2**dlugosc_binarna-1)
    krzyzuj_populacje()
    mutuj_populacje()
    binary_decimal()
    skaluj_populacje(0, 2**dlugosc_binarna-1, xmin, xmax)
    statystyki()
    
def wykresy():
    plt.figure(num="Przystosowania")
    ypoints = np.array(przystosowanie_min)
    plt.plot(ypoints, label="Przystosowanie min", color="blue")
    ypoints = np.array(przystosowanie_max)
    plt.plot(ypoints, label="Przystosowanie max", color="red")
    ypoints = np.array(przystosowanie_avg)
    plt.plot(ypoints, label="Przystosowanie avg", color="green")
    plt.legend()
    plt.show()
    
    plt.figure(num="Wykres zadanej funkcji")
    x = np.linspace(-1, 41, 100)
    y = -0.1*x**2+4*x+7
    plt.plot(x, y, label="y = -0.1x^2 + 4x + 7", color="blue")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Wykres funkcji y = -0.1x^2 + 4x + 7")
    plt.grid(True)
    plt.legend()
    plt.show()


policz_dlugosc_binarana(xmax, roznica)
generuj_populacje()
statystyki()
# populacja = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8]
# print("Wygenerowana populacja:   ", populacja)

# reprodukuj_populacje()
# print("Populacja po reprodukcji: ", populacja)

# skaluj_populacje(xmin, xmax, 0, 2**dlugosc_binarna)
# print("Przeskslowana populacja:  ", populacja)

# krzyzuj_populacje()
# print("Populacja po krzyzowaniu  ", populacja)

# mutuj_populacje()
# print("Populacja po mutowaniu:   ", populacja)

# binary_decimal()
# print("Populacja w dziesietnym:  ", populacja)

# skaluj_populacje(0, 2**dlugosc_binarna, xmin, xmax)
# print("Przeskalowana populacja:  ", populacja)
# statystyki()

for i in range (liczba_generacji):
    cykl()

wykresy()