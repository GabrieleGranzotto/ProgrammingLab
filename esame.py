#Esame di Laboratorio di Programmazione 10/02/2022
#Artificial Intelligence and Data Analytics, Università degli Studi di Trieste
#a.a. 2021-2022, studente: Gabriele Granzotto

#Questo programma calcola prende dei dati da un file in estensione CSV formattato come:
#date, passengers
#yyyy-mm,value
#...
#e ne calcola la differenza media tra i vari mesi negli anni

#classe per le eccezioni
class ExamException(Exception):
    pass

#classe che serve per chiamare il file, formattarlo e renderlo disponibile all'utilizzo
class CSVTimeSeriesFile():
    
    #metodo __init__
    def __init__(self, name):

        self.name = name
        self.can_read = True

    #metodo che prende i dati e gli lavora per renderli utilizzabili
    def get_data(self):

        #prova ad aprire il file e se non riesce alza una eccezione, modifica la variabile booleana can_read in False
        #e stampa che un errore di apertura
        try:
            my_file=open(self.name, 'r')
        except: 
            self.can_read = False
            raise ExamException('Errore in apertura del file')

        #se non è leggibile stampa a schermo che non è leggibile e torna "None", "niente"
        if not self.can_read:
            raise ExamException("Errore, file non aperto o illeggibile")
        #se è leggibile apre il file
        else:
            dati=open(self.name,'r')     
            elenco=[]
            #scorre il file fino alla fine e divide in due colonne, dove la virgola è il divisorio
            for line in dati:
                try:
                    element = line.split(',')
                    element[-1]=element[-1].strip()
                    #se il primo elemento della riga del file non è "Date" o "date" allora 
                    #prova ad aggiungere in fondo alla lista il primo elemento (la data) e il secondo (il valore)
                    if '-' in element[0][4]:
                        if '.' not in element[1] and '-' not in element[1]:
                            try:
                                temp = element[0].split('-')
                                temp_year_int = int(temp[0])
                                temp_month_int = int(temp[1])
                                if temp_month_int <= 12 and temp_month_int > 0:
                                    try:
                                        elenco.append([element[0],int(element[1])])
                                    except:
                                        pass
                            except:
                                pass
                except:
                    pass
            #controllo che la lista sia fatta in modo strettamente crescente
            lista_temp = []
            for line in elenco:
                temp = line[0].split('-')
                lista_temp.append([int(temp[0]),int(temp[1])])
            for i in range(1,len(lista_temp)):
                if lista_temp[i][0]<lista_temp[i-1][0] or (lista_temp[i][0]==lista_temp[i-1][0] and lista_temp[i][1]<=lista_temp[i-1][1]):
                    raise ExamException("Lista non ordinata in modo crescente per data")
                    
            return elenco #ritorna la lista dei dati
  


#metodo che prende i valori del file, l'anno da cui iniziare ad analizzare e l'anno finale e calcola la differenza media mensile
def compute_avg_monthly_difference(elenco, first_year, last_year):

    #Divide la data in Anno e Mese separati e converte il Mese in numerico, infine assegna ad una nuova lista
    lista = []
    for line in elenco:
        element = line[0].split('-')
        lista.append([element[0],int(element[1]),line[1]])
    
    #controlla se il gli anni inseriti in Input siano corretti (non devono per forza essere in ordine crescente ma almeno esserci entrambi
    flag_last_year = False #usate due variabili di controllo
    flag_first_year = False
    for line in lista:
        if line[0] == last_year:
            flag_last_year = True
        if line[0] == first_year:
            flag_first_year = True
    if (not flag_first_year) or (not flag_last_year):
        raise ExamException('Gli anni inseriti in Input non sono presenti nel file')         
    
    #Crea una lista con gli anni nella lista presi in considerazione solo una volta
    elenco_anni = []
    for item in lista:
        if item[0] not in elenco_anni:
            elenco_anni.append(item[0])
    
    #blocco che serve per creare una lista con da un lato l'anno (in stringa) e dall'altro una lista di 12 valori corrispondenti ai valori dei mesi
    lista_definitiva = []
    for item in elenco_anni:
        #crea una lista di liste per ogni anno formata da [mese(int),passeggeri(int)]
        lista_anno = []
        for line in lista:
            if line[0] == item: 
                lista_anno.append([line[1],line[2]])
        #riordina la lista controllando con la variabile booleana "flag" se manca un mese, in tal caso inserire il valore "None"
        #il riordino non sarebbe stato obbligatorio perché già controllato prima che le date fossero crescenti
        #ma era il metodo più comodo a me per procedere
        lista_ordinata = []
        for i in range(1,13):
            flag=True
            for value in lista_anno:
                if value[0] == i:
                    lista_ordinata.append(value[1])
                    flag=False
                if not flag:
                    break
            if flag:
                lista_ordinata.append(None)
        #crea una lista definitiva che è formata da [anno(str),[valori per mese(int)]]
        lista_definitiva.append([item, lista_ordinata])

    #viene creata una nuova lista che al suo interno abbia solo i 12 valori interessati solo per gli anni interessati (che sono stati omessi)
    lista_utile = []
    for year in range(int(first_year),int(last_year)+1):
        for line in lista_definitiva:
            if line[0] == str(year):
                    lista_utile.append(line[1])

    #blocco che serve a calcolare la "data average difference" e salvarla nella lista "risultato"
    risultato = []
    #ciclo con "j" che sta per i mesi
    for j in range(12):
        differenze = [] 
        #questo serve per vedere quanti anni non hanno un valore valido per il mese preso in esame
        counter = 0
        for item in lista_utile:
            if item[j] != None:
                counter = counter+1
        #se il mese ha più di 2 valori validi si procede
        if counter >= 2:
            for i in range(len(lista_utile)-1):
                #se uno dei due è uguale a None allora imposta automaticamente a 0 il valore
                if lista_utile[i+1][j] == None or lista_utile[i][j] == None:
                    differenze.append(0)
                #in caso contrario calcola la differenza
                else:
                    differenze.append(lista_utile[i+1][j] - lista_utile[i][j])
            #il risultato viene calcolato con la sommatoria delle differenze fratto tutti gli anni buoni 
            risultato.append(sum(differenze)/(counter-1))
        #sennò si imposta in automatico a 0 il valore per quel mese
        else:
            risultato.append(0)

    return risultato

##########################################################################################
#Inizio del Main
##########################################################################################

#introduzione per l'utente
print("Questo e' un programma che serve a calcolare la differenza media dei passeggeri nei voli con i dati presi da un file CSV\n\n")
#assegnazione della variabile alla classe
try:
    time_series_file = CSVTimeSeriesFile(name='data.csv')
except:
    pass
#richiamo del metodo get_data()
time_series = time_series_file.get_data()

#inserimento via terminale dei due anni, se non sono un numero dichiara errore
print("Inserire il primo anno da prendere in considerazione: ")
first_year = str(input())
try: 
    int(first_year)
except:
    raise ExamException("L'input non e' un numero")
print("Inserire l'ultimo anno: ")
last_year = str(input())
try: 
    int(last_year)
except:
    raise ExamException("L'input non e' un numero")
#inversione degli anni per metterli in ordine crescente
if int(first_year)>int(last_year):
    swap = last_year
    last_year = first_year
    first_year = swap
#richiamo del metodo per creare la lista e stampa del risultato arrotondato a 2 decimali dopo la virgola
list_data_avg_difference = compute_avg_monthly_difference(time_series, first_year, last_year)
print("\n\nla lista della differenza dei passeggeri medi e': ")
for line in list_data_avg_difference:
    print("%.2f" % round(line, 2))