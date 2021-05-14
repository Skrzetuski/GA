from utils import *
import guiview
import Gen
import tkinter as tk
import tkinter.ttk as ttk
import param


def main():
    def test():
        random.seed(64)
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
            # aktualizujMape()

    def edytuj():
        wybrany = tabela.focus()
        tabela.item(wybrany, values=(id.get(), waga.get(), wartosc.get()))
        aktualizujMape()

    def dodaj():
        global licznik
        # nth = tabela.size()
        if licznik % 2 == 0:
            rzad = ('evenrow')
        else:
            rzad = ('oddrow')
        tabela.insert(parent='', index='end', iid=licznik, values=(
            licznik, waga.get(), wartosc.get()
        ), tags=rzad)
        waga.delete(0, tk.END)
        wartosc.delete(0, tk.END)
        licznik += 1
        aktualizujMape()

    def usun():
        wybrany = tabela.focus()
        tabela.delete(wybrany)
        aktualizujMape()
        # loguj()
        tabela.delete(*tabela.get_children())
        drawTable()

    window = tk.Tk()
    window.geometry("500x500")
    window.configure(background='#555')

    tabelaRamka = tk.Frame(window)
    tabelaRamka.pack()

    tabela = ttk.Treeview(tabelaRamka, selectmode="browse")

    styl = ttk.Style()
    styl.theme_use('clam')
    styl.configure('Treeview',
                   background="gray50",
                   foreground="yellow",
                   fieldbackground="orange",
                   bd=0)
    styl.map('Treeview', background=[("selected", "lightgreen")])

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

    edycja = tk.Frame(window)
    edycja.pack()

    id = tk.Entry(edycja)
    id.config(state="disabled")
    id.pack()
    waga = tk.Entry(edycja)
    waga.pack()
    wartosc = tk.Entry(edycja)
    wartosc.pack()
    edytuj = tk.Button(edycja, text='Edytuj', command=edytuj)
    edytuj.pack()
    dodaj = tk.Button(edycja, text='Dodaj', command=dodaj)
    dodaj.pack()
    usun = tk.Button(edycja, text="Usun", command=usun)
    usun.pack()

    test = tk.Button(window, text="Test", command=test)
    test.pack()

    edycja.pack()

    window.mainloop()





















if __name__ == "__main__":
    main()
