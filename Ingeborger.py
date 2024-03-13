import tkinter as tk
from tkinter import ttk
import random
import time
from PIL import Image, ImageTk
from lists import *

def on_selecionar_personagem(*args):
    personagem_selecionado = fichas_combobox.get()

    if personagem_selecionado in detalhes_personagens:
        detalhes = detalhes_personagens[personagem_selecionado]

        # Exibir foto do personagem
        foto_path = detalhes["Foto"]
        foto = Image.open(foto_path)
        foto = foto.resize((200, 200))
        foto = ImageTk.PhotoImage(foto)
        foto_label.config(image=foto)
        foto_label.image = foto

        # Exibir informações detalhadas
        nome_label.config(text=personagem_selecionado, font=('Arial', 16, 'bold'))
        esquadrao_label.config(text=f"Esquadrão: {detalhes['Esquadrão']}")
        patente_label.config(text=f"Patente: {detalhes['Patente']}")

        # Exibir dragões
        for i, dragao_info in enumerate(detalhes["Dragões"]):
            dragao_imagem_path = dragao_info["Imagem"]
            dragao_imagem = Image.open(dragao_imagem_path)
            dragao_imagem = dragao_imagem.resize((100, 100))
            dragao_imagem = ImageTk.PhotoImage(dragao_imagem)
            dragao_labels[i].config(image=dragao_imagem, text=dragao_info["Nome"])
            dragao_labels[i].image = dragao_imagem
    else:
        nome_label.config(text="Personagem não encontrado")
        esquadrao_label.config(text="")
        patente_label.config(text="")
        foto_label.config(image="")
        for i in range(3):
            dragao_labels[i].config(image="", text="")

def on_consulta_dragao():
    dragao_selecionado = dragao_combobox.get()
    if dragao_selecionado in detalhes_dragoes:
        detalhes = detalhes_dragoes[dragao_selecionado]
        
        # Exibir imagem
        image_path = f"./img/{dragao_selecionado}.png"
        image = Image.open(image_path)
        image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(image)
        detalhes_image_label.config(image=photo)
        detalhes_image_label.image = photo

        # Exibir informações detalhadas
        detalhes_nome_label.config(text=dragao_selecionado, font=('Arial', 16, 'bold'))
        detalhes_info_label.config(text=f"Classificação: {detalhes['Classificação']}\n"
                                       f"Habitat: {detalhes['Habitat']}\n"
                                       f"Poder: {detalhes['Poder']}\n"
                                       f"Alimentação: {detalhes['Alimentação']}\n"
                                       f"Localização: {detalhes['Localização']}")
    else:
        detalhes_nome_label.config(text="Dragão não encontrado")
        detalhes_info_label.config(text="")


def fazer_teste():
    progresso["value"] = 10
    janela.update_idletasks()
    time.sleep(1)
    progresso["value"] = 100
    
    atributo = atributos[atributo_combobox.get()]
    resultado_rolagem = random.randint(1, 20) + int(atributo.get())
    dificuldade = int(dificuldade_entry.get())
    resultado_final = resultado_rolagem - dificuldade
    
    if resultado_final >= 0:
        resultado_label["text"] = f"Sucesso! Rolagem: {resultado_rolagem} (+{atributo.get()}) >= {dificuldade_entry.get()}"
        if (dificuldade - int(atributo.get()) >= 15):
            resultado_label["text"] += f"\n{atributo_nome} aumentou em 1!"
    else:
        resultado_label["text"] = f"Falha! Rolagem: {resultado_rolagem} (+{atributo.get()}) < {dificuldade_entry.get()}"

def on_button_click():
    local_selecionado = local_combobox.get()
    
    if local_selecionado in locais_dragoes:
        dragao_selecionado = random.choice(locais_dragoes[local_selecionado])

        result_label.config(text=f"Nome: {dragao_selecionado}")
        image_path = f"./img/{dragao_selecionado}.png"
        image = Image.open(image_path)
        image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo
    else:
        result_label.config(text="Local não reconhecido")

def mostrar_pagina(pagina):
    if pagina == 0:
        notebook.select(0)
    elif pagina == 1:
        notebook.select(1)

# Configuração da interface
janela = tk.Tk()
janela.title("Navegação entre Páginas")

# Configurar tamanho da janela
window_width = 800
window_height = 600
screen_width = janela.winfo_screenwidth()
screen_height = janela.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
janela.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Configurar fonte
font_style = ttk.Style()
font_style.configure('TLabel', font=('Arial', 12))
font_style.configure('TButton', font=('Arial', 12))

# Criar um Notebook (guia) para a navegação entre páginas
notebook = ttk.Notebook(janela)

# Página 1 - Teste de Habilidade
pagina_teste = ttk.Frame(notebook)
notebook.add(pagina_teste, text="Teste de Habilidade")

atributos = {
    "Força": tk.StringVar(),
    "Resistência": tk.StringVar(),
    "Destreza": tk.StringVar(),
    "Inteligência": tk.StringVar(),
    "Percepção": tk.StringVar(),
    "Comando": tk.StringVar()
}

for i, atributo_nome in enumerate(atributos.keys()):
    ttk.Label(pagina_teste, text=atributo_nome).grid(row=i, column=0, padx=5, pady=5)
    ttk.Entry(pagina_teste, textvariable=atributos[atributo_nome]).grid(row=i, column=1, padx=5, pady=5)

atributo_combobox = ttk.Combobox(pagina_teste, values=list(atributos.keys()))
atributo_combobox.grid(row=0, column=3, padx=5, pady=5)
atributo_combobox.set("Força")

ttk.Label(pagina_teste, text="Dificuldade:").grid(row=1, column=3, padx=5, pady=5)
dificuldade_entry = ttk.Entry(pagina_teste)
dificuldade_entry.grid(row=1, column=4, padx=5, pady=5)

teste_button = ttk.Button(pagina_teste, text="Teste", command=fazer_teste)
teste_button.grid(row=2, column=3, columnspan=2, padx=5, pady=5)

progresso = ttk.Progressbar(pagina_teste, orient="horizontal", length=100, mode="determinate")
progresso.grid(row=3, column=3, columnspan=2, padx=5, pady=5)

resultado_label = ttk.Label(pagina_teste, text="")
resultado_label.grid(row=4, column=3, columnspan=2, padx=5, pady=5)

# Página 2 - Gerador de Encontros
pagina_encontros = ttk.Frame(notebook)
notebook.add(pagina_encontros, text="Gerador de Encontros")

locais = list(locais_dragoes.keys())
local_combobox = ttk.Combobox(pagina_encontros, values=locais)
local_combobox.set("Selecione o Local")
local_combobox.pack(pady=10)

button = ttk.Button(pagina_encontros, text="Gerar encontro", command=on_button_click)
button.pack(pady=10)

result_label = ttk.Label(pagina_encontros, text="", font=('Arial', 12))
result_label.pack(pady=10)

image_label = ttk.Label(pagina_encontros)
image_label.pack(pady=10)

# Adicione o Notebook à janela principal
notebook.pack(padx=10, pady=10)

# Página 3 - Dragonário
pagina_dragonario = ttk.Frame(notebook)
notebook.add(pagina_dragonario, text="Dragonário")

# Layout da página do Dragonário
detalhes_image_label = ttk.Label(pagina_dragonario)
detalhes_image_label.grid(row=1, column=0, rowspan=4, padx=10, pady=10)

detalhes_nome_label = ttk.Label(pagina_dragonario, text="", font=('Arial', 16, 'bold'))
detalhes_nome_label.grid(row=1, column=1, pady=10, sticky="w")

detalhes_info_label = ttk.Label(pagina_dragonario, text="")
detalhes_info_label.grid(row=2 , column=1, pady=10, sticky="w")

dragao_combobox = ttk.Combobox(pagina_dragonario, values=list(detalhes_dragoes.keys()))
dragao_combobox.set("Selecione o Dragão")
dragao_combobox.grid(row=0, column=0, padx=10, pady=10)

consulta_button = ttk.Button(pagina_dragonario, text="Consultar Dragão", command=on_consulta_dragao)
consulta_button.grid(row=0, column=1, padx=10, pady=10)

# Página 4 - Fichas
pagina_fichas = ttk.Frame(notebook)
notebook.add(pagina_fichas, text="Fichas")

# Barra de seleção
fichas_combobox = ttk.Combobox(pagina_fichas, values=list(detalhes_personagens.keys()))
fichas_combobox.set("Selecione o Personagem")
fichas_combobox.grid(row=0, column=0, padx=10, pady=10)

confirmar_button = ttk.Button(pagina_fichas, text="Confirmar", command=on_selecionar_personagem)
confirmar_button.grid(row=0, column=2, padx=10, pady=10)

# Foto e informações
foto_label = ttk.Label(pagina_fichas)
foto_label.grid(row=1, column=1, rowspan=3, padx=10, pady=10)

nome_label = ttk.Label(pagina_fichas, text="", font=('Arial', 16, 'bold'))
nome_label.grid(row=1, column=0, pady=10, sticky="w")

esquadrao_label = ttk.Label(pagina_fichas, text="")
esquadrao_label.grid(row=2, column=0, pady=10, sticky="w")

patente_label = ttk.Label(pagina_fichas, text="")
patente_label.grid(row=3, column=0, pady=10, sticky="w")

# Dragões
dragao_labels = []
for i in range(3):
    dragao_label = ttk.Label(pagina_fichas, text="")
    dragao_label.grid(row=4, column=i, pady=10, padx=10, sticky="w")
    dragao_labels.append(dragao_label)

# Iniciar a interface
janela.mainloop()
