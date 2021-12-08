class Model():
    def fit(self, data):
        raise NotImplementedError("Metodo non implementato")
    def predict(self,data):
        raise NotImplementedError("Metodo non implementato")

class Incremented(Model):
    def predict(self,data):
        differenza = []
        for i in range(0,len(data)-2):
            differenza.append(data[i+1]-data[i])
        somma = sum(differenza)
        media = somma/len(data)
        prediction = data[len(data)-1] + media
        return prediction


dati = open('shampoo_sales.csv', 'r')
valori=[] 

def puliziadati():
    lista_dati = []
    #Separare i valori linea per linea
    for line in dati:
        elements=line.split(",")
        #Ignorare la linea "Date,Sales"
        if elements[0] != "Date":
            #Assegnare valori e convertirli a float
            date=elements[0]
            value=float(elements[1])
            lista_dati.append(float(value))
    return lista_dati

valori = puliziadati()
risultati = Incremented
print(risultati.predict(valori))

