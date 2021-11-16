print("Dammi il numero di valori da inserire: ")
n=int(input())
my_list = list()
print("\nDammi una serie di {} valori: ".format(n))
for i in range(n):
    my_list.append(int(input()))
print("\n")
print("Il valore della somma e' {}!".format(sum(my_list)))
print("\n\n")
