import hakuMod
import ainesMod
import jaakaappiMod
import reseptiMod
import tkinter

class Ohjelma:
  def __init__( self, tkroot):
    tkroot.title("Reseptikokki")
    #tkroot.columnconfigure(0, weight=1)
    #tkroot.rowconfigure(1, weight=1)

    tkroot.rowconfigure(0, weight=1)
    tkroot.rowconfigure(1, weight=1)
    tkroot.rowconfigure(2, weight=8)
    tkroot.columnconfigure(0, weight=1)
    tkroot.columnconfigure(1, weight=1)
    tkroot.columnconfigure(2, weight=1)
    self.frame = tkinter.Frame( tkroot)#,width=tkinter.FALSE)
    self.frame.grid(row=0,column=0)
    #frame.pack()
    #tkroot.pack(fill=tkinter.BOTH, expand=1)

    #Valikko
    self.menubar = tkinter.Menu(tkroot)
    #menubar.add_command(label="Tiedosto", command=self.hello)
    self.menubar.add_command(label="Asetukset", command=tkroot.quit)
    self.menubar.add_command(label="Lopeta", command=tkroot.quit)
    #Alivalikot
    self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
    self.filemenu.add_command(label="Open", command=self.hello)
    self.filemenu.add_command(label="Save", command=self.hello)
    self.filemenu.add_separator()
    self.filemenu.add_command(label="Exit", command=tkroot.quit)
    self.menubar.add_cascade(label="Tiedosto", menu=self.filemenu)
    tkroot.config(menu=self.menubar)

    #Ylaosan nappiframe
    self.topspace = tkinter.Frame( self.frame)
    self.topspace.grid(row=0, column=0, sticky=tkinter.W)
    #Ylaosan nappiframe2
    self.bottomspace = tkinter.Frame( self.frame)
    self.bottomspace.grid(row=1, column=0, sticky=tkinter.W)
    #infobox
    self.info = tkinter.Label( tkroot, text="Jääkaappi")
    self.info.grid(row=0, column=1)
    #hakunappi
    self.button = tkinter.Button( self.topspace, text="HAE", command=tkroot.quit)
    self.button.pack(side=tkinter.LEFT, expand=True, anchor=tkinter.W)
    #haku
    self.searchField = tkinter.Entry( self.topspace)
    self.searchField.pack(side=tkinter.LEFT)
    #hakunappi
    self.button = tkinter.Button( self.topspace, text="HAE jääkaapin sisällöllä", command=tkroot.quit)
    self.button.pack(side=tkinter.LEFT)
    #jaakaappinappi
    self.button = tkinter.Button( self.topspace, text="NÄYTÄ jääkaappi", command=tkroot.quit)
    self.button.pack(side=tkinter.LEFT)
    #allergiat
    tkinter.Label( self.bottomspace, text="Allergiat").pack(side=tkinter.LEFT)
    self.allergyField = tkinter.Entry( self.bottomspace)
    self.allergyField.pack(side=tkinter.LEFT)
    #puuttuvamaara
    tkinter.Label( self.bottomspace, text="Puuttuvia aineksia <=").pack(side=tkinter.LEFT )
    self.puutelist = tkinter.IntVar( tkroot)
    self.puutelist = tkinter.OptionMenu( self.bottomspace, self.puutelist, 0, 1,2)
    self.puutelist.pack(side=tkinter.LEFT)

    #Resepti ikkuna / Jaakaappi
    self.infolista = tkinter.Listbox(tkroot)
    self.infolista.grid(row=2, column=1, sticky='NSEW')
    self.infolista.bind('<<ListboxSelect>>', self.selectRecipe)
    #TODO bind wörrkiin
    #Resepti lista
    self.reseptilista = tkinter.Listbox(tkroot)
    self.reseptilista.grid(row=2, column=0, sticky='NSEW')
    #self.reseptilista.insert(tkinter.END, "a list entry")

    #for item in ["one", "two", "three", "four"]:
        #reseptilista.insert(tkinter.END, item)
    
  def hello(self):
    print("må")

  def selectRecipe(self, event):
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print("select",index,value)
  def alusta( self):
    # LATAA
    try:
      # Reseptit
      self.kirja = reseptiMod.ReseptiKirja()
      self.kirja.lataaKansio("./reseptit/")
      # Jääkaappi
      self.kaappi = jaakaappiMod.JaaKaappi()
      try:
        # sisältö
        buf = open( "./jaakaappi.txt")
        self.kaappi.lataaJaakaappi( buf)
        buf.close()
        # allergiatiedot
        buf = open( "./allergiat.txt")
        self.kaappi.lataaAllergiat( buf)
        buf.close()
      except IOError as e:
          raise
    except FileNotFoundError as e:
      print("Tiedostoa ei löytynyt",str(e)[str(e).index("'"):])
    #LAITA UI:n reseptit
    for resepti in self.kirja.reseptit: 
      self.reseptilista.insert(tkinter.END, resepti.nimi)
    


    # TKINTER
    #w = tkinter.Label(tkroot, text="HellO")
    #w.pack()

def main():
  # TULOSTA
  try:
    root = tkinter.Tk()
    ohjelma = Ohjelma( root)
    ohjelma.alusta()
    root.mainloop()
  except KeyboardInterrupt:
    print("\nHyvästi!")
  except EOFError:
    print("\nHyvästi!")
  except:
    raise


if __name__ == '__main__':
  main()
