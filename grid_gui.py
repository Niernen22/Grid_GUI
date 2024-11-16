import sys
import tkinter
import grid


class Racs(tkinter.Canvas):
    def __init__(self, master, jelenet, kezdes_es_cel):
        self.sorok, self.oszlopok = len(jelenet), len(jelenet[0])
        self.negyzet_meret = min(40, 500 / self.sorok, 500 / self.oszlopok)
        tkinter.Canvas.__init__(self, master,
                                height=self.negyzet_meret * self.sorok + 1,
                                width=self.negyzet_meret * self.oszlopok + 1, background="white")
        self.jelenet = jelenet
        self.kezdes_es_cel = kezdes_es_cel
        self.jelenet_rajzolasa(jelenet)
        self.bind("<Button-1>", self.bal_klikk)
        self.bind("<Button-2>", self.jobb_klikk)
        self.bind("<Button-3>", self.jobb_klikk)
        self.focus_set()
        self.configure(highlightthickness=0)

    def jelenet_rajzolasa(self, jelenet):
        for sor in range(len(jelenet)):
            for oszlop in range(len(jelenet[0])):
                x0, y0 = oszlop * self.negyzet_meret, sor * self.negyzet_meret
                x1, y1 = x0 + self.negyzet_meret, y0 + self.negyzet_meret
                szin = "black" if jelenet[sor][oszlop] else "white"
                self.create_rectangle(x0, y0, x1, y1, width=1, outline="black", fill=szin)

    def bal_klikk(self, event):
        sor, oszlop = pont = self.forditott_atalakitas(event)
        if 0 <= sor < self.sorok and 0 <= oszlop < self.oszlopok:
            if not self.jelenet[sor][oszlop]:
                self.delete("kezdes")
                self.pont_rajzolasa(pont, szin="red", cimkek="kezdes")
                self.kezdes_es_cel[0] = pont

    def jobb_klikk(self, event):
        sor, oszlop = pont = self.forditott_atalakitas(event)
        if 0 <= sor < self.sorok and 0 <= oszlop < self.oszlopok:
            if not self.jelenet[sor][oszlop]:
                self.delete("cel")
                self.pont_rajzolasa(pont, szin="green", cimkek="cel")
                self.kezdes_es_cel[1] = pont

    def pont_rajzolasa(self, pont, szin="black", cimkek=""):
        x, y = self.atalakitas(pont[0], pont[1])
        sugar = self.negyzet_meret / 4.0
        self.create_oval(x - sugar, y - sugar, x + sugar, y + sugar, fill=szin, tags=cimkek)

    def atalakitas(self, sor, oszlop):
        x = self.negyzet_meret * (oszlop + 0.5)
        y = self.negyzet_meret * (sor + 0.5)
        return (x, y)

    def forditott_atalakitas(self, event):
        sor = int(event.y / self.negyzet_meret)
        oszlop = int(event.x / self.negyzet_meret)
        return (sor, oszlop)

    def rajzol_utvonal(self, utvonal):
        self.delete("utvonal")

        for i in range(1, len(utvonal)):
            sor1, oszlop1 = utvonal[i - 1]
            sor2, oszlop2 = utvonal[i]
            x1, y1 = self.atalakitas(sor1, oszlop1)
            x2, y2 = self.atalakitas(sor2, oszlop2)
            self.create_line(x1, y1, x2, y2, fill="green", width=5, tags="utvonal")

    def torol_utvonal(self):
        self.delete("utvonal")



class RacsNavigacioGUI(tkinter.Frame):
    def __init__(self, master, jelenet):
        tkinter.Frame.__init__(self, master)
        self.jelenet = jelenet
        self.kezdes_es_cel = [None, None]
        
        self.title_label = tkinter.Label(self, text="Rács Navigáció", font=("Roboto", 16, "bold"))
        self.title_label.pack(pady=10)

        self.racs = Racs(self, jelenet, self.kezdes_es_cel)
        self.racs.pack(side=tkinter.LEFT, padx=10, pady=10)

        menu = tkinter.Frame(self, padx=20, pady=10)
        
        tkinter.Label(menu, text="Bal kattintás: kezdőpont kijelölése.", font=("Roboto", 10)).grid(row=0, column=0, sticky=tkinter.W, pady=5)
        tkinter.Label(menu, text="Jobb kattintás: célpont kijelölése.", font=("Roboto", 10)).grid(row=1, column=0, sticky=tkinter.W, pady=5)
        
        tkinter.Button(menu, text="Útvonal keresése", command=self.utvonal_kereses, width=20, height=2, bg="green", font=("Roboto", 12)).grid(row=2, column=0, pady=10)
        tkinter.Button(menu, text="Útvonal törlése", command=self.utvonal_torlese, width=20, height=2, bg="red", font=("Roboto", 12)).grid(row=3, column=0, pady=10)
        
        separator = tkinter.Frame(self, height=2, bd=1, relief="sunken")
        separator.pack(fill=tkinter.X, padx=5, pady=5)
        
        menu.pack(side=tkinter.RIGHT, fill=tkinter.Y, padx=10, pady=10)

        self.pack_propagate(False)
        self.configure(width=800, height=600)



    def utvonal_kereses(self):
        kezdes, cel = self.kezdes_es_cel
        if kezdes is not None and cel is not None:
            utvonal = grid.megtalal_ut(kezdes, cel, self.jelenet)
            if utvonal:
                self.racs.rajzol_utvonal(utvonal)

    def utvonal_torlese(self):
        self.racs.torol_utvonal()


def jelenet_betoltese(jelenet_fajl):
    jelenet = []
    with open(jelenet_fajl) as infile:
        for sor, sor_adatai in enumerate(infile, start=1):
            jelenet.append([])
            for oszlop, karakter in enumerate(sor_adatai.strip(), start=1):
                if karakter == ".":
                    jelenet[-1].append(False)
                elif karakter == "X":
                    jelenet[-1].append(True)
                else:
                    print(f"Nem ismert karakter '{karakter}' a {sor}. sor {oszlop}. oszlopában.")
                    return None
    if len(jelenet) < 1:
        print("A jelenetnek legalább egy sorral kell rendelkeznie.")
        return None
    if len(jelenet[0]) < 1:
        print("A jelenetnek legalább egy oszloppal kell rendelkeznie.")
        return None
    if not all(len(sor) == len(jelenet[0]) for sor in jelenet):
        print("Nem minden sor egyforma hosszú.")
        return None
    return jelenet


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Rács Navigáció")
    jelenet = jelenet_betoltese(sys.argv[1])
    if jelenet is not None:
        RacsNavigacioGUI(root, jelenet).pack()
        root.resizable(height=False, width=False)
        root.mainloop()

