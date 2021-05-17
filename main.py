from utils import *
import guiview
import Gen
import tkinter as tk
import tkinter.ttk as ttk
import param


font = param.FONT


def main():
    def start():

        print(param.items)
        history = tools.History()

        toolbox = setupToolbox(base.Toolbox())

        toolbox.decorate("mate", history.decorator)
        toolbox.decorate("mutate", history.decorator)

        population = toolbox.population(n=param.MU)
        history.update(population)

        algorithms.eaMuPlusLambda(population, toolbox, param.MU, param.LAMBDA, param.CXPB, param.MUTPB, param.NGEN,
                                  verbose=False)

        fits = [ind.fitness.values[1] for ind in population]

        individual = getBestIndividual(fits, population)

        input_bin = Gen.Gen(toolbox, individual, history)

        final_knapsack = mapGenToKnapsack(individual)

        print(individual)

        print(final_knapsack.items)

        print("History")
        print(history.getGenealogy(individual))

        guiview.showGui(param.items,final_knapsack.items,input_bin)

    def ustawienia(b):
        def zapisz(okno):
            param.NGEN = int(generacja.get())
            param.MU = int(rozmiarPopulacji.get())
            param.MAX_WEIGHT = int(waga.get())
            okno.destroy()
            b.config(command=lambda: ustawienia(b))

        b.config(command="None")

        styl = {"font": ("Arial", "15"), "background": "#555", "fg": "white"}
        okno = tk.Tk()
        okno.overrideredirect(True)  # aplikacja bezramkowa
        okno.geometry("300x250+{}+{}".format(window.winfo_x()+8,window.winfo_y()+31))
        okno.title("Algorytm Genetyczny - Ustawienia")
        okno.configure(background='#555')
        oknoUstawienia = tk.LabelFrame(okno,styl,text="Ustawienia",fg="lightblue")

        tk.Label(oknoUstawienia, styl, text="Waga plecaka").grid(row=0,column=0)
        waga = tk.Entry(oknoUstawienia, styl, justify="center", width="10")
        waga.insert(0,param.MAX_WEIGHT)
        waga.grid(row=0,column=1,pady=10)

        tk.Label(oknoUstawienia,styl, text="Liczba generacji").grid(row=1,column=0)
        generacja = tk.Entry(oknoUstawienia, styl, justify="center", width="10")
        generacja.insert(0,param.NGEN)
        generacja.grid(row=1,column=1,pady=10)

        tk.Label(oknoUstawienia, styl, text="Rozmiar populacji").grid(row=2, column=0)
        rozmiarPopulacji = tk.Entry(oknoUstawienia, styl, justify="center", width="10")
        rozmiarPopulacji.insert(0,param.MU)
        rozmiarPopulacji.grid(row=2,column=1,pady=10)

        oknoUstawienia.pack(pady=15)

        tk.Button(okno, text="Zapisz", command=lambda: zapisz(okno), bg="darkgreen", fg="#eee", activebackground="#666",width=15).pack(pady=10)

        okno.mainloop()



    def drawTable():
        global licznik, rzad
        licznik = 0
        for item in param.items:
            if licznik % 2 == 0:
                rzad = ('evenrow')
            else:
                rzad = ('oddrow')

            tabela.insert(parent='', index='end', iid=licznik, text=licznik + 1, values=(
                licznik, param.items[item][0], param.items[item][1]

            ), tags=rzad)
            licznik += 1

    def aktualizujMape():
        licznik = 0
        nowaMapa = {}
        for x in tabela.get_children():
            wiersz = tabela.item(x, 'values')

            nowaMapa[licznik] = (int(wiersz[1]), int(wiersz[2]))
            licznik += 1

        param.items = nowaMapa
        param.NBR_ITEMS = len(tabela.get_children())

    def wybierz(event):
        region = tabela.identify("region", event.x, event.y)
        if region == "cell":
            wybrany = tabela.focus()
            wartosci = tabela.item(wybrany, 'values')

            id.config(state='normal')
            id.delete(0, tk.END)
            id.insert(0, wartosci[0])
            id.config(state='disabled')

            waga.delete(0, tk.END)
            waga.insert(0, wartosci[1])
            wartosc.delete(0, tk.END)
            wartosc.insert(0, wartosci[2])

    def edytuj():
        wybrany = tabela.focus()
        tabela.item(wybrany, values=(id.get(), waga.get(), wartosc.get()))
        id.config(state='normal')
        id.delete(0, tk.END)
        id.config(state='disabled')
        waga.delete(0, tk.END)
        wartosc.delete(0, tk.END)

        tabela.selection_remove(wybrany)

        aktualizujMape()

    def dodaj():
        global licznik
        if licznik % 2 == 0:
            rzad = ('evenrow')
        else:
            rzad = ('oddrow')
        tabela.insert(parent='', index='end', iid=licznik, values=(
            licznik, waga.get(), wartosc.get()
        ), tags=rzad)
        id.config(state='normal')
        id.delete(0, tk.END)
        id.config(state='disabled')
        waga.delete(0, tk.END)
        wartosc.delete(0, tk.END)
        licznik += 1

        if tabela.selection():
            tabela.selection_remove(tabela.focus())

        aktualizujMape()

    def usun():
        if not tabela.selection():
            return
        wybrany = tabela.focus()
        tabela.delete(wybrany)
        aktualizujMape()

        tabela.delete(*tabela.get_children())
        if tabela.selection():
            tabela.selection_remove(tabela.focus())
        id.config(state='normal')
        id.delete(0, tk.END)
        id.config(state='disabled')
        waga.delete(0, tk.END)
        wartosc.delete(0, tk.END)
        drawTable()


    # readValues()

    window = tk.Tk()
    window.geometry("500x550")
    window.configure(background='#555')
    window.title("Algorytm Genetyczny - Problem Plecakowy")

    ustawieniaButton = tk.Button(window,font=("Arial",15),text="⛭",command=lambda: ustawienia(ustawieniaButton),background="#555",fg="white")
    ustawieniaButton.pack(anchor="nw")


    tabelaRamka = tk.Frame(window)
    tabelaRamka.pack(pady=15)



    tabela = ttk.Treeview(tabelaRamka, selectmode="browse")

    styl = ttk.Style()
    styl.theme_use('clam')
    styl.configure('Treeview',
                   background="gray50",
                   foreground="black",
                   fieldbackground="gray50",
                   bd=0)
    styl.map('Treeview', background=[("selected", "#0492c2")])

    tabela['columns'] = ("id", "waga", "wartosc")
    tabela.column("id", width=50)
    tabela.column("waga", width=150)
    tabela.column("wartosc", width=150)
    tabela.heading("id", text="ID")
    tabela.heading("waga", text="Waga")
    tabela.heading("wartosc", text="Wartosc")

    tabela['show'] = 'headings'

    tabela.tag_configure('oddrow', background="skyblue")
    tabela.tag_configure('evenrow', background="lightblue")

    drawTable()

    scroll = ttk.Scrollbar(tabelaRamka, orient='vertical', command=tabela.yview)
    scroll.pack(side='right', fill='y')

    tabela.configure(yscrollcommand=scroll.set)

    tabela.pack()

    tabela.bind("<ButtonRelease-1>", lambda event: wybierz(event))

    edycja = tk.Frame(window, bg="#555")

    editFont = (font, 15)

    tk.Label(edycja, text="ID", bg="#555", fg="lightblue", font=editFont).grid(row=0, column=0)
    tk.Label(edycja, text="Waga", bg="#555", fg="lightblue", font=editFont).grid(row=0, column=1)
    tk.Label(edycja, text="Wartosc", bg="#555", fg="lightblue", font=editFont).grid(row=0, column=2)

    id = tk.Entry(edycja, state="disabled", justify="center", font=editFont, width=10,
                  disabledforeground="gray55", disabledbackground="#555")
    id.grid(row=1, column=0)
    waga = tk.Entry(edycja, justify="center", font=editFont, width=10, bg="#555", fg="white", insertbackground='white')
    waga.grid(row=1, column=1)
    wartosc = tk.Entry(edycja, justify="center", font=editFont, width=10, bg="#555", fg="white", insertbackground='white')
    wartosc.grid(row=1, column=2)

    edycja.pack()

    przyciski = tk.LabelFrame(window, text="Polecenia zmiany listy", font=(font, 12), bg="#555", fg="lightblue")

    edytuj = tk.Button(przyciski, text='Zapisz Zmiany', command=edytuj, bg="#888", fg="#eee", activebackground="#666")
    edytuj.grid(row=0, column=0, padx=15, pady=15)
    usun = tk.Button(przyciski, text="Usun Wybrany", command=usun, bg="#888", fg="#eee", activebackground="#666")
    usun.grid(row=0, column=1, padx=15, pady=15)
    dodaj = tk.Button(przyciski, text='Dodaj Nowy', command=dodaj, bg="#888", fg="#eee", activebackground="#666")
    dodaj.grid(row=0, column=2, padx=15, pady=15)

    przyciski.pack(pady=15)

    start = tk.Button(window, text="Uruchom generacje osobnikow", command=start, width=35, font=editFont, bg="#377758", fg="orange", activebackground="green", activeforeground="yellow")
    start.pack(padx=15, pady=5)

    window.mainloop()


if __name__ == "__main__":
    main()