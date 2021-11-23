#Caricare i valori del file
valori=[]
dati=open("shampoo_sales.csv","r")

def sommashampoo():
    #Separare i valori linea per linea
    for line in dati:
        elements=line.split(",")
        #Ignorare la linea "Date,Sales"
        if elements[0] != "Date":
            #Assegnare valori e convertirli a float
            date=elements[0]
            value=float(elements[1])
            valori.append(float(value))
    somma=sum(valori)
    print(somma)
    #Calcolare Variazione
    variazione=[]
    variazione.append(0.0)
    for item in range(1,len(valori)-1):
        variazione.append(valori[item-1]-valori[item])
    variazionemedia=sum(variazione)/float(len(valori))
    print(variazionemedia)

#Stampare
sommashampoo()


