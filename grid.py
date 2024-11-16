import queue
import math


class Racs:
    def __init__(self, kezdes, cel, jelenet):
        self._kezdes = kezdes
        self._cel = cel
        self._szelesseg = len(jelenet[0])
        self._magassag = len(jelenet)
        self._jelenet = jelenet

    def megoldas(self):
        front = queue.PriorityQueue()
        front.put((0, self._kezdes))
        honnan_jott = {}
        eddigi_koltseg = {}
        honnan_jott[self._kezdes] = None
        eddigi_koltseg[self._kezdes] = 0

        if not self.nem_akadaly(self._kezdes) or not self.nem_akadaly(self._cel):
            return None

        if not self.teruleten_belul(self._kezdes):
            print("Kezdőpont a határon kívül")
            return None
        if not self.teruleten_belul(self._cel):
            print("Célpont a határon kívül")
            return None

        while not front.empty():
            _, aktualis_pont = front.get()

            if aktualis_pont == self._cel:
                return self.visszakovet(honnan_jott)

            for szomszed in self.szomszedok(aktualis_pont):
                uj_koltseg = eddigi_koltseg[aktualis_pont] + \
                    self.euklideszi_tavolsag(aktualis_pont, szomszed)

                if szomszed not in eddigi_koltseg or uj_koltseg < eddigi_koltseg[szomszed]:
                    eddigi_koltseg[szomszed] = uj_koltseg
                    prioritas = uj_koltseg + \
                        self.euklideszi_tavolsag(self._cel, szomszed)
                    front.put((prioritas, szomszed))
                    honnan_jott[szomszed] = aktualis_pont

        return None

    def szomszedok(self, hely):
        (x, y) = hely
        eredmeny = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]

        eredmeny = filter(self.teruleten_belul, eredmeny)
        eredmeny = filter(self.nem_akadaly, eredmeny)
        return eredmeny


    def teruleten_belul(self, hely):
        (x, y) = hely
        return 0 <= x < self._magassag and 0 <= y < self._szelesseg

    def nem_akadaly(self, hely):
        (x, y) = hely
        return not self._jelenet[x][y]

    def euklideszi_tavolsag(self, hely1, hely2):
        (x1, y1) = hely1
        (x2, y2) = hely2
        return math.sqrt(((x1-x2)**2)+((y1-y2)**2))

    def visszakovet(self, latogatott):
        aktualis = self._cel
        kezdet = self._kezdes
        utvonal = []

        while aktualis != kezdet:
            utvonal.append(aktualis)
            aktualis = latogatott[aktualis]

        utvonal.append(self._kezdes)
        utvonal.reverse()
        return utvonal.copy()


def megtalal_ut(kezdes, cel, jelenet):
    racs = Racs(kezdes, cel, jelenet)
    return racs.megoldas()
