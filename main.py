import random
from datetime import datetime
import sys
from typing import Dict, List, Tuple, Generator
import statistics
import os


class CNPGenerator:
    def __init__(self):
        self.judete = self._init_judete()
        self.populatie_judete = self._init_populatie()
        self.distributie_varsta = self._init_distributie_varsta()

    def _init_judete(self) -> Dict[str, str]:
        return {f"{i:02d}": nume for i, nume in enumerate([
            "Alba", "Arad", "Argeș", "Bacău", "Bihor", "Bistrița-Năsăud",
            "Botoșani", "Brașov", "Brăila", "Buzău", "Caraș-Severin", "Cluj",
            "Constanța", "Covasna", "Dâmbovița", "Dolj", "Galați", "Gorj",
            "Harghita", "Hunedoara", "Ialomița", "Iași", "Ilfov", "Maramureș",
            "Mehedinți", "Mureș", "Neamț", "Olt", "Prahova", "Satu Mare",
            "Sălaj", "Sibiu", "Suceava", "Teleorman", "Timiș", "Tulcea",
            "Vaslui", "Vâlcea", "Vrancea", "București", "București S1",
            "București S2", "București S3", "București S4", "București S5",
            "București S6", "Călărași", "Giurgiu"
        ], 1)}

    def _init_populatie(self) -> Dict[str, int]:
        return {
            "01": 325941, "02": 410143, "03": 569932, "04": 601387,
            "05": 551297, "06": 295988, "07": 392821, "08": 546615,
            "09": 281452, "10": 404979, "11": 246588, "12": 679141,
            "13": 655997, "14": 200042, "15": 479404, "16": 599442,
            "17": 496892, "18": 314684, "19": 291950, "20": 361657,
            "21": 250816, "22": 760774, "23": 542686, "24": 452475,
            "25": 234339, "26": 518193, "27": 454203, "28": 383280,
            "29": 695117, "30": 330668, "31": 212224, "32": 388325,
            "33": 642551, "34": 323544, "35": 650533, "36": 193355,
            "37": 374700, "38": 335312, "39": 341861, "40": 1716961
        }

    def _init_distributie_varsta(self) -> Dict[str, float]:
        return {
            "0-14": 0.15,  # 0-14 ani
            "15-24": 0.12,  # 15-24 ani
            "25-54": 0.46,  # 25-54 ani
            "55-64": 0.13,  # 55-64 ani
            "65+": 0.14  # 65+ ani
        }

    def _get_an_nastere(self, gen: int) -> int:
        current_year = datetime.now().year % 100
        rand = random.random()

        if gen in [5, 6]:  # Pentru persoane născute după 2000
            if rand < self.distributie_varsta["0-14"]:
                return random.randint(current_year - 14, current_year)
            else:
                return random.randint(0, current_year - 15)
        else:  # Pentru persoane născute înainte de 2000
            csum = 0
            for grupa, prob in self.distributie_varsta.items():
                csum += prob
                if rand < csum:
                    if grupa == "65+":
                        return random.randint(30, 54)  # născuți între 1930-1954
                    elif grupa == "55-64":
                        return random.randint(55, 64)  # născuți între 1955-1964
                    elif grupa == "25-54":
                        return random.randint(65, 94)  # născuți între 1965-1994
                    else:
                        return random.randint(95, 99)  # născuți între 1995-1999

    def calculeaza_cifra_control(self, cnp: str) -> int:
        const = "279146358279"
        suma = sum(int(cnp[i]) * int(const[i]) for i in range(12))
        if suma % 11 == 10:
            return 1
        return suma % 11

    def genereaza_cnp(self, judet: str) -> str:
        gen = random.choice([1, 2, 5, 6])
        an = self._get_an_nastere(gen)

        luna = random.randint(1, 12)

        # Verificare an bisect pentru luna februarie
        if luna == 2:
            if (an % 4 == 0 and (an + 2000 if gen in [5, 6] else an + 1900) % 100 != 0) or \
                    ((an + 2000 if gen in [5, 6] else an + 1900) % 400 == 0):
                ziua = random.randint(1, 29)
            else:
                ziua = random.randint(1, 28)
        elif luna in [4, 6, 9, 11]:
            ziua = random.randint(1, 30)
        else:
            ziua = random.randint(1, 31)

        nnn = random.randint(1, 999)
        cnp_partial = f"{gen}{an:02d}{luna:02d}{ziua:02d}{judet}{nnn:03d}"
        cifra_control = self.calculeaza_cifra_control(cnp_partial)
        return cnp_partial + str(cifra_control)


class NumeGenerator:
    def __init__(self):
        self.nume = [
            "Pop", "Popa", "Popescu", "Radu", "Dumitru", "Stan", "Stoica",
            "Gheorghe", "Matei", "Ciobanu", "Ionescu", "Rusu", "Mihai",
            "Constantin", "Marin", "Stefan", "Gheorghiu", "Vasile", "Toma",
            "Florea", "Moldovan", "Ilie", "Ungureanu", "Dinu", "Tudor"
        ]
        self.prenume_feminin = [
            "Maria", "Elena", "Ioana", "Ana", "Alexandra", "Andreea", "Cristina",
            "Mihaela", "Gabriela", "Daniela", "Ionela", "Nicoleta", "Georgiana",
            "Mariana", "Adriana", "Monica", "Alina", "Diana", "Roxana", "Carmen"
        ]
        self.prenume_masculin = [
            "Ioan", "Gheorghe", "Constantin", "Vasile", "Alexandru", "Mihai",
            "Ion", "Andrei", "Stefan", "Cristian", "Daniel", "Nicolae", "Adrian",
            "Gabriel", "George", "Marian", "Florin", "Ionut", "Bogdan", "David"
        ]

    def genereaza_nume(self, cnp: str) -> str:
        gen = int(cnp[0])
        nume = random.choice(self.nume)
        if gen % 2 == 0:
            prenume = random.choice(self.prenume_feminin)
        else:
            prenume = random.choice(self.prenume_masculin)
        return f"{nume} {prenume}"


class HashTable:
    def __init__(self, expected_items: int = 1_000_000):
        # Folosim un număr prim mai mare decât 1.4 * numărul de elemente așteptate
        self.size = 1_500_007  # Număr prim apropiat de 1.5M
        self.table = [[] for _ in range(self.size)]
        self.collisions = 0
        self.items = 0
        self.iterations = []

    def get_load_factor(self) -> float:
        return self.items / self.size

    def hash_function(self, key: str) -> int:
        # Implementare îmbunătățită a funcției de dispersie
        hash_val = 5381  # Număr prim inițial
        for char in key:
            # hash * 33 + c (known as DJB2)
            hash_val = ((hash_val << 5) + hash_val) + ord(char)
        return hash_val % self.size

    def insert(self, cnp: str, nume: str):
        index = self.hash_function(cnp)
        if self.table[index]:
            self.collisions += 1
        self.table[index].append((cnp, nume))
        self.items += 1

        # Afișăm statistici la fiecare 100000 inserări
        if self.items % 100000 == 0:
            print(f"Inserări: {self.items}, Factor încărcare: {self.get_load_factor():.2f}, "
                  f"Coliziuni: {self.collisions}")

    def search(self, cnp: str) -> Tuple[bool, int]:
        index = self.hash_function(cnp)
        iterations = 0
        for entry in self.table[index]:
            iterations += 1
            if entry[0] == cnp:
                self.iterations.append(iterations)
                return True, iterations
        return False, iterations

    def get_bucket_sizes(self) -> List[int]:
        return [len(bucket) for bucket in self.table]


def generate_test_cnps(total_cnps: int, sample_size: int = 1000) -> Generator[str, None, None]:
    """Generator pentru CNP-uri de test pentru a economisi memoria."""
    indices = set(random.sample(range(total_cnps), sample_size))
    current = 0
    for _ in range(total_cnps):
        if current in indices:
            yield str(current)  # Aici ar trebui să fie un CNP valid
        current += 1


def main():
    # Creare director pentru rezultate
    if not os.path.exists("rezultate"):
        os.makedirs("rezultate")

    print("Inițializare generare CNP-uri")

    # Deschidere fișiere pentru salvare date
    with open("rezultate/cnp_uri.txt", "w", encoding='utf-8') as f_cnp, \
            open("rezultate/cnp_nume.txt", "w", encoding='utf-8') as f_cnp_nume, \
            open("rezultate/statistici_hash.txt", "w", encoding='utf-8') as f_stats:

        # Inițializare generatoare
        cnp_gen = CNPGenerator()
        nume_gen = NumeGenerator()
        hash_table = HashTable()

        total_populatie = sum(cnp_gen.populatie_judete.values())
        cnp_generate = 0

        # Generare și salvare CNP-uri și nume
        f_stats.write("Generare CNP-uri și nume\n\n")

        test_cnps = set()  # Folosim set pentru căutare eficientă

        for judet, populatie in cnp_gen.populatie_judete.items():
            nr_cnp = (populatie * 1000000) // total_populatie
            f_stats.write(f"Județul {cnp_gen.judete[judet]}: {nr_cnp} CNP-uri\n")

            for _ in range(nr_cnp):
                cnp = cnp_gen.genereaza_cnp(judet)
                nume = nume_gen.genereaza_nume(cnp)

                # Salvare CNP și nume
                f_cnp.write(f"{cnp}\n")
                f_cnp_nume.write(f"{cnp}: {nume}\n")

                # Inserare în hash table
                hash_table.insert(cnp, nume)

                # Colectăm un eșantion pentru testare
                cnp_generate += 1
                if cnp_generate <= 1000:
                    test_cnps.add(cnp)

        # Testare căutări și salvare rezultate
        print("\nTestare căutări")
        f_stats.write("\nTestare căutări pentru 1000 CNP-uri\n")

        with open("rezultate/cautari.txt", "w", encoding='utf-8') as f_cautari:
            for cnp in test_cnps:
                gasit, iteratii = hash_table.search(cnp)
                f_cautari.write(f"CNP: {cnp}, Găsit: {gasit}, Iterații: {iteratii}\n")

        # Salvare statistici
        print("\nSalvare statistici")
        f_stats.write("\nStatistici Hash Table:\n")
        f_stats.write(f"Număr total CNP-uri: {cnp_generate}\n")
        f_stats.write(f"Dimensiune tabelă hash: {hash_table.size}\n")
        f_stats.write(f"Factor de încărcare: {hash_table.get_load_factor():.2f}\n")
        f_stats.write(f"Număr coliziuni: {hash_table.collisions}\n")

        if hash_table.iterations:
            # Statistici căutare
            f_stats.write("\nStatistici căutare:\n")
            f_stats.write(f"Număr minim iterații: {min(hash_table.iterations)}\n")
            f_stats.write(f"Număr maxim iterații: {max(hash_table.iterations)}\n")
            f_stats.write(f"Medie iterații: {statistics.mean(hash_table.iterations):.2f}\n")
            f_stats.write(f"Mediană iterații: {statistics.median(hash_table.iterations):.2f}\n")

if __name__ == "__main__":
    main()