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