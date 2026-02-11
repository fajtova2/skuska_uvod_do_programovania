#RLE kompresia
#Anna Fajtová, 2. ročník, B-SGG
#Zimný semester 2025/2026
#Úvod do programovania MZ370P19

class RLE: 
    def __init__(self): #konštruktor
        self.__escape = 255 #zapúzdrenie

    def compress(self, data): #metóda s logikou RLE
        res = [] #prázdny zoznam pre vysledky metódy
        i = 0 #index pre začiatok
        while i < len(data): 
            count = 1
            while i + 1 < len(data) and data[i] == data[i+1]: #cyklus hľadá rovnaké po sebe idúce čísla
                count += 1
                i += 1
            res.extend([self.__escape + count, data[i]]) #do výsledku sa pridá dvojica escape+počet a hodnota
            i += 1
        return res

    def decompress(self, data): #dekompresia kompresie
        res = []
        for i in range(0, len(data), 2): #prechádza cez zoznam v pároch
            count = data[i] - self.__escape #vypočet pôvodného počtu opakovaní
            res.extend([data[i+1]] * count)
        return res

input_file = "input.txt" #vstupné dáta
output_file = "output.txt" #výstupné dáta

try:
    with open(input_file, "r") as f:
        a = [int(x) for x in f.read().split()] #text načíta, rozdelí podľa medzier a prevedie na celé čísla

    if not a: #ošetrenie ak je vstup prázdny
        print("V súbore nie sú žiadne dáta :(")
    else:
        rle = RLE() 
        comp = rle.compress(a) #spustenie RLE kompresie
        decomp = rle.decompress(comp) #spustenie dekompresie

        with open(output_file, "w") as f: #vytvorenie výstupného súboru a zápis výsledkov
            f.write("RLE kompresia s escape znakom 255:\n")
            f.write(" ".join(map(str, comp)) + "\n") 
            f.write("Dekompresia kompresie:\n")
            f.write(" ".join(map(str, decomp)) + "\n")

        print(f"Wohooo, podarilo sa! Výsledok je uložený v súbore '{output_file}'.")
        
except FileNotFoundError: #ošetrenie neexistencie súboru
    print(f"Chyba - súbor {input_file} neexistuje :(")
except ValueError: #ošetrenie situácie keď má súbor chybné znaky
    print("Chyba - vstup obsahuje nesprávny formát dát (desatinné čísla alebo text) :(")