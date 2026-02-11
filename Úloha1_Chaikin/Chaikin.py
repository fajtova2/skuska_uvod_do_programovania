#Aproximácia krivky metódou Chaikin
#Anna Fajtová, 2. ročník, B-SGG
#Zimný semester 2025/2026
#Úvod do programovania MZ370P19

class Point: #bod v 2D
    def __init__(self, x, y): #konštruktor
        self.x = float(x)
        self.y = float(y)
    def __eq__(self, other): #porovnávanie či sa dva body rovnajú
        if not isinstance(other, Point):
            return False
        return (self.x, self.y) == (other.x, other.y)

class Polyline: #trieda pre polyliniu
    def __init__(self, points):
        self.points = points
    def closed(self): #rozlíšenie v uzavrenosti medzi polylíniou a polygónom
        if len(self.points) >= 2 and self.points[0] == self.points[-1]:
            return True
        return False

class Polygon(Polyline): #treida pre polygón, dedí od polylínie
    def closed(self): #polygón je vždy uzavretý
        return True

class Chaikin: #trieda pre vypočty
    def __init__(self, geometry): 
        self.geometry = geometry
    def corner_cutting(self): #jedna iterácia vyhladenia krivky
        p = self.geometry.points 
        new = [] #zoznam pre novovzniknuté body
        for i in range(len(p) - 1):
            p0, p1 = p[i], p[i+1] #začiatok a koniec úsečky
            
            q_x = 0.75 * p0.x + 0.25 * p1.x  #vzorce podľa chaikina
            q_y = 0.75 * p0.y + 0.25 * p1.y
            new.append(Point(q_x, q_y))
            r_x = 0.25 * p0.x + 0.75 * p1.x
            r_y = 0.25 * p0.y + 0.75 * p1.y
            new.append(Point(r_x, r_y))

        if self.geometry.closed(): #ak je to polygón, musia sa prepojiť nové body
            first = new[0]
            new.append(Point(first.x, first.y))
            
        self.geometry.points = new

    def run(self, n): #vyhladenie pre zadané n iterácií
        if 0 <= n <= 15:
            for _ in range(n):
                self.corner_cutting()
            return True
        print("Chyba - rozsah iterácií musí byť 0 až 15 :(")
        return False

points = []
try:
    with open("points.txt", "r") as f:
        for line in f:
            if not line.strip(): #preskočenie prázdnych riadkov
                continue
            u = line.replace("[", "").replace("]", "").replace(",", " ").split()
            if len(u) != 2: #ošetrenie aby c riadku boli iba dve suradnice
                print("ajaj, neplatný  formát dát, skús to znova")
                points = [] 
                break
            try:
                points.append(Point(u[0], u[1]))
            except ValueError: #ošetrenie neplatného formátu dát
                print("ajaj, neplatný  formát dát, skús to znova") 
                points = []
                break
except FileNotFoundError: #ošetrenie neexistencie súboru
    print("Neexistujúca krivka v neexistujúcom súbore sa ešte bohužiaľ vyhladť nedá :(")

if len(points) >= 2: 
    try:
        n = int(input("Počet iterácií: "))
        geometry = Polyline(points) #inštancia polyline
        i = Chaikin(geometry)  #inicialitácia      
        if i.run(n):
            with open("chaikin.txt", "w") as f:
                for p in geometry.points: #zápis bodov v rovnakom tvare ako vstup
                    f.write(f"[{p.x},{p.y}]\n")
            print("Podarilo sa!!! Výsledok je v súbore chaikin.txt")    
    except ValueError: #ušetrenie zlého zadania počtu iterácií
        print("Chyba - iterácia musí byť celé číslo")
elif len(points) == 1:  #ak je menej než 2 body
    print("Nedostatok bodov na spracovanie :(")

    