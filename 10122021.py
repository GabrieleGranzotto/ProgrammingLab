class Model():
    def fit(self, data):
        raise NotImplementedError("Metodo non implementato")
    def predict(self,data):
        raise NotImplementedError("Metodo non implementato")

class IncrementedModel(Model):
    def predict(self,data):
        differenza = []
        for i in range(len(data)-3,len(data)-1):
            differenza.append(data[i]-data[i-1])
        somma = sum(differenza)
        media = somma/3
        prediction = data[len(data)-1] + media
        return prediction

class FitIncrementModel(IncrementedModel):
    def fit(self, data):
        differenza = []
        for  i in range(0,len(data)-4):
            differenza.append(data[i]-data[i-1])
        somma = sum(differenza)
        media = somma/(len(data)-3)
        return media
    
    def predict(self,data):
        return (super().predict(data) + self.fit(data))/2

nuovo_punto = FitIncrementModel
studio_statistico = [8,19,31,41,50,52,60]

punti_predetti = []

for i in range(10):
    punti_predetti.append(nuovo_punto.predict(studio_statistico))

print(punti_predetti)
        