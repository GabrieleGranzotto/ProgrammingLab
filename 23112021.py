class CSVFile():
    
    def __init__(self, name):
        self.name = name
    def get_data(self):
        dati=open(self.name,'r')    
        elenco=[]
        for line in dati:
            element = line.split(',')
            if (element[0]!='Date'):
                elenco.append([element[0],element[1]])
        return elenco


testo = CSVFile('shampoo_sales.csv')
print(testo.get_data())
                