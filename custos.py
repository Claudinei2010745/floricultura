import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

CUSTOS_ARQUIVO = "dados/custos.json"


def abrir_tela_custos():

    janela = tk.Toplevel()
    janela.title("Controle de Custos Mensal")
    janela.geometry("500x500")

    frame = tk.Frame(janela)
    frame.pack(pady=10)

    # ===== CAMPOS =====
    campos = {}

    itens = [
        "Aluguel",
        "Água",
        "Luz",
        "Funcionários",
        "Gasolina",
        "Internet",
        "Plantas"
    ]

    for i, item in enumerate(itens):
        tk.Label(frame, text=item).grid(row=i, column=0, sticky="w", pady=5)

        entry = tk.Entry(frame)
        entry.grid(row=i, column=1)

        campos[item.lower()] = entry

    # ===== LABEL TOTAL =====
    label_total = tk.Label(janela, text="Total: R$ 0,00", font=("Arial", 12, "bold"))
    label_total.pack(pady=10)

    # ===== SALVAR =====
    def salvar():

        hoje = datetime.now()
        chave = hoje.strftime("%m/%Y")

        dados = {}

        total = 0

        for key, entry in campos.items():

            try:
                valor = float(entry.get().replace(",", "."))
            except:
                valor = 0

            dados[key] = valor
            total += valor

        if os.path.exists(CUSTOS_ARQUIVO):
            with open(CUSTOS_ARQUIVO, "r", encoding="utf-8") as f:
                try:
                    arquivo = json.load(f)
                except:
                    arquivo = {}
        else:
            arquivo = {}

        arquivo[chave] = dados

        with open(CUSTOS_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(arquivo, f, indent=4, ensure_ascii=False)

        label_total.config(text=f"Total: R$ {total:.2f}".replace(".", ","))

        messagebox.showinfo("Sucesso", "Custos salvos com sucesso!")

    # ===== CARREGAR =====
    def carregar():

        hoje = datetime.now()
        chave = hoje.strftime("%m/%Y")

        if not os.path.exists(CUSTOS_ARQUIVO):
            return

        with open(CUSTOS_ARQUIVO, "r", encoding="utf-8") as f:
            try:
                arquivo = json.load(f)
            except:
                return

        if chave not in arquivo:
            return

        dados = arquivo[chave]

        total = 0

        for key, entry in campos.items():

            valor = dados.get(key, 0)
            entry.delete(0, tk.END)
            entry.insert(0, str(valor))

            total += valor

        label_total.config(text=f"Total: R$ {total:.2f}".replace(".", ","))

    # ===== BOTÕES =====
    tk.Button(janela, text="Salvar Custos", command=salvar).pack(pady=5)
    tk.Button(janela, text="Carregar Mês Atual", command=carregar).pack(pady=5)

    carregar()