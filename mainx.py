import hakuMod
import ainesMod
import jaakaappiMod
import reseptiMod
import tkinter

class Ohjelma:
  def __init__( self, tkroot):
    frame = tkinter.Frame( tkroot)
    frame.pack()
    self.button = tkinter.Button( frame, text="QUIT", command=frame.quit)
    self.button.pack(side=tkinter.LEFT)

    #Valikko
    menubar = tkinter.Menu(tkroot)
    #menubar.add_command(label="Tiedosto", command=self.hello)
    menubar.add_command(label="Asetukset", command=tkroot.quit)
    menubar.add_command(label="Lopeta", command=tkroot.quit)
    #Alivalikot
    filemenu = tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=self.hello)
    filemenu.add_command(label="Save", command=self.hello)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=tkroot.quit)
    menubar.add_cascade(label="Tiedosto", menu=filemenu)
    
    tkroot.config(menu=menubar)
  def hello(self):
    print("må")
  def alusta( self):
    # LATAA
    try:
      # Reseptit
      kirja = reseptiMod.ReseptiKirja()
      kirja.lataaKansio("./reseptit/")
      # Jääkaappi
      kaappi = jaakaappiMod.JaaKaappi()
      try:
        # sisältö
        buf = open( "./jaakaappi.txt")
        kaappi.lataaJaakaappi( buf)
        buf.close()
        # allergiatiedot
        buf = open( "./allergiat.txt")
        kaappi.lataaAllergiat( buf)
        buf.close()
      except IOError as e:
          raise
    except FileNotFoundError as e:
      print("Tiedostoa ei löytynyt",str(e)[str(e).index("'"):])


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
