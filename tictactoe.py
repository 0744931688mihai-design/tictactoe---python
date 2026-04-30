import tkinter as tk
import joc

mod_ales = None

def alege_mod(mod):
    global mod_ales
    mod_ales = mod
    
    # 1. Ascundem meniul cu modurile de joc
    frame_mod.pack_forget() 
    
    # 2. Adaptăm textul butoanelor în funcție de ce am ales
    if mod == "Multiplayer":
        btn_incepe_x.config(text="Jucătorul 1 (X) începe",font=('Arial', 25))
        btn_incepe_o.config(text="Jucătorul 2 (O) începe",font=('Arial', 25))
    else:
        btn_incepe_x.config(text="Eu (X) încep",font=('Arial', 25))
        btn_incepe_o.config(text="Botul (O) începe",font=('Arial', 25))
        
    # 3. Afișăm meniul în care alegem cine mută primul
    frame_inceput.pack(pady=20)

def porneste_joc(cine_incepe):
    meniu.destroy() # Închidem meniul
    joc.start_joc(mod_ales, cine_incepe) # Pornim jocul cu cele 2 setări

# --- CREAREA FERESTREI ---
meniu = tk.Tk()
meniu.title("Setări Joc")
from tkinter import messagebox
import random

# Variabile globale
tabla = []
butoane = []
jucator_curent = ""
mod_curent = ""
fereastra_joc = None

def verifica_victorie(simbol):
    for i in range(3):
        if tabla[i][0] == tabla[i][1] == tabla[i][2] == simbol: return True
    for j in range(3):
        if tabla[0][j] == tabla[1][j] == tabla[2][j] == simbol: return True
    if tabla[0][0] == tabla[1][1] == tabla[2][2] == simbol: return True
    if tabla[0][2] == tabla[1][1] == tabla[2][0] == simbol: return True
    return False

def verifica_remiza():
    for i in range(3):
        for j in range(3):
            if tabla[i][j] == " ": return False
    return True

def dezactiveaza_butoane():
    for i in range(3):
        for j in range(3):
            butoane[i][j].config(state=tk.DISABLED)
def gaseste_mutare_critica(simbol):
    for i in range(3):
        rand=[tabla[i][0], tabla[i][1],tabla[i][2]]
        if rand.count(simbol)== 2 and rand.count(" ")==1:
            spatiu_gol=rand.index(" ")
            return (i, spatiu_gol)
    for i in range(3):
        col=[tabla[0][i], tabla [1][i], tabla[2][i]]
        if col.count(simbol)==2 and col.count(" ")==1:
            spatiu_gol_col=col.index(" ")
            return(spatiu_gol_col, i)
    diag1=[tabla[0][0], tabla[1][1], tabla[2][2]]
    if diag1.count(simbol)==2 and diag1.count(" ")==1:
        spatiu_diag1=diag1.index(" ")
        return( spatiu_diag1, spatiu_diag1)
    diag2=[tabla[0][2], tabla[1][1], tabla[2][0]]
    if diag2.count(simbol)==2 and diag2.count(" ")==1:
        spatiu_diag2=diag2.index(" ")
        return (spatiu_diag2, 2-spatiu_diag2)
    return None
def mutare_bot():
    global jucator_curent
    
    pozitii_libere = [(i, j) for i in range(3) for j in range(3) if tabla[i][j] == " "]
    if not pozitii_libere: return

    # Aici botul decide cum joacă în funcție de dificultate
    if mod_curent == "Usor":
        rand, coloana = random.choice(pozitii_libere)
    elif mod_curent == "Mediu":
        rand, coloana = random.choice(pozitii_libere) # O să îl faci tu mai târziu
    elif mod_curent == "Greu":
        aux=gaseste_mutare_critica('0')
        if aux:
            rand, coloana=aux
        elif    gaseste_mutare_critica('X'):
                    rand,coloana=gaseste_mutare_critica('X')

        elif tabla[1][1]==" ":
            rand,coloana=1,1
        else:
            marg=[(1,0),(0,1),(1,2),(2,1)]
            marg_liber=[c for c in marg if tabla[c[0]][c[1]]==" "]
            
            if marg_liber:
                rand,coloana=random.choice(marg_liber)
            else:    
                colt=[(0,0), (2,2), (0,2), (2,0)]
                colt_liber=[c for c in colt if tabla[c[0]][c[1]]==" "]
                if colt_liber:
                    rand,coloana=random.choice(colt_liber)
                else:
                    rand,coloana=random.choice(pozitii_libere)
    else:
        rand, coloana = random.choice(pozitii_libere)
        
    # Executăm mutarea
    tabla[rand][coloana] = "O"
    butoane[rand][coloana].config(text="O", disabledforeground="black")
    
    if verifica_victorie("O"):
        dezactiveaza_butoane()
        messagebox.showinfo("Final", "Ai pierdut! Unlucky")
    elif verifica_remiza():
        messagebox.showinfo("Final", "Remiză!")
    else:
        jucator_curent = "X" # Rândul se întoarce la X

def click_buton(rand, coloana):
    global jucator_curent
    
    # Permitem click-ul doar dacă spațiul e liber
    if tabla[rand][coloana] == " ":
        
        # Dacă jucăm cu botul și NU e rândul lui X, ignorăm click-ul omului
        if mod_curent != "Multiplayer" and jucator_curent != "X":
            return
            
        # Efectuăm mutarea curentă (indiferent dacă e X sau O în multiplayer)
        tabla[rand][coloana] = jucator_curent
        butoane[rand][coloana].config(text=jucator_curent)
        
        # Verificăm dacă cel care a dat click a câștigat
        if verifica_victorie(jucator_curent):
            dezactiveaza_butoane()
            messagebox.showinfo("Final", "Ai câștigat!")
            return
        elif verifica_remiza():
            messagebox.showinfo("Final", "Remiză!")
            return
            
        # Schimbăm jucătorul
        if jucator_curent == "X":
            jucator_curent = "O"
        else:
            jucator_curent = "X"
            
        # Dacă NU e multiplayer și acum e rândul lui O, chemăm botul
        if mod_curent != "Multiplayer" and jucator_curent == "O":
            fereastra_joc.after(500, mutare_bot)

# ==========================================
# FUNCȚIA APELATĂ DIN MAIN.PY
# ==========================================
def start_joc(mod_ales, cine_incepe):
    global tabla, butoane, jucator_curent, mod_curent, fereastra_joc
    
    mod_curent = mod_ales
    jucator_curent = cine_incepe # "X" sau "O"
    tabla = [[" " for _ in range(3)] for _ in range(3)]
    
    fereastra_joc = tk.Tk()
    fereastra_joc.title(f"Joc X și 0 - Mod: {mod_curent}")
    
    # Creăm butoanele
    butoane = [[None for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buton = tk.Button(
                fereastra_joc, text=" ", font=('Arial', 40, 'bold'), width=8, height=3,
                command=lambda r=i, c=j: click_buton(r, c)
            )
            buton.grid(row=i, column=j)
            butoane[i][j] = buton

    # Dacă jucăm cu Botul și ai ales ca el să înceapă, îl punem să mute
    if mod_curent != "Multiplayer" and jucator_curent == "O":
        fereastra_joc.after(500, mutare_bot)

    fereastra_joc.mainloop()
meniu.geometry("806x650")

# --- PASUL 1: Cadrul pentru Modul de Joc ---
frame_mod = tk.Frame(meniu)
tk.Label(frame_mod, text="1. Alege Modul de Joc", font=('Arial', 40, 'bold')).pack(pady=10)

tk.Button(frame_mod, text="Multiplayer (2 Jucători)", width=30, font=('Arial', 25),command=lambda: alege_mod("Multiplayer")).pack(pady=5)
tk.Button(frame_mod, text="Singleplayer - Ușor", width=30, font=('Arial', 25),command=lambda: alege_mod("Usor")).pack(pady=5)
tk.Button(frame_mod, text="Singleplayer - Greu", width=30, font=('Arial', 25),command=lambda: alege_mod("Greu")).pack(pady=5)

frame_mod.pack(pady=20) # Îl afișăm primul pe ecran

# --- PASUL 2: Cadrul pentru Cine Începe ---
# Acest cadru este creat, dar NU îi dăm .pack() încă. Rămâne ascuns.
frame_inceput = tk.Frame(meniu)
tk.Label(frame_inceput, text="2. Cine mută primul?", font=('Arial', 30, 'bold')).pack(pady=10)

btn_incepe_x = tk.Button(frame_inceput, text="", width=25, command=lambda: porneste_joc("X"))
btn_incepe_x.pack(pady=10)

btn_incepe_o = tk.Button(frame_inceput, text="", width=25, command=lambda: porneste_joc("O"))
btn_incepe_o.pack(pady=10)

meniu.mainloop()