import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

VENDAS_ARQUIVO = "vendas.json"


def abrir_relatorio_mensal():

    janela = tk.Toplevel()
    janela.title("Relatório Mensal")
    janela.geometry("900x650")

    frame_lista = tk.Frame(janela)
    frame_lista.pack(fill="both", expand=True, padx=20, pady=10)

    scrollbar = tk.Scrollbar(frame_lista)
    scrollbar.pack(side="right", fill="y")

    lista = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, width=120)
    lista.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=lista.yview)

    detalhes = tk.Text(janela, height=14)
    detalhes.pack(fill="x", padx=20, pady=10)

    frame_topo = tk.Frame(janela)
    frame_topo.pack(pady=10)

    tk.Label(frame_topo, text="Mês:").grid(row=0, column=0)
    entry_mes = tk.Entry(frame_topo, width=5)
    entry_mes.grid(row=0, column=1)

    tk.Label(frame_topo, text="Ano:").grid(row=0, column=2)
    entry_ano = tk.Entry(frame_topo, width=8)
    entry_ano.grid(row=0, column=3)

    label_total = tk.Label(janela, text="Total do mês: R$ 0,00")
    label_total.pack()

    label_qtd = tk.Label(janela, text="Quantidade de vendas: 0")
    label_qtd.pack()

    vendas = []
    vendas_mostradas = []

    # ===== CARREGAR =====
    def carregar_relatorio():

        nonlocal vendas

        lista.delete(0, tk.END)
        detalhes.delete("1.0", tk.END)
        vendas_mostradas.clear()

        mes = entry_mes.get().strip()
        ano = entry_ano.get().strip()

        if not mes or not ano:
            return

        mes = mes.zfill(2)
        filtro = f"{mes}/{ano}"

        total_mes = 0
        qtd_vendas = 0

        if os.path.exists(VENDAS_ARQUIVO):
            try:
                with open(VENDAS_ARQUIVO, "r", encoding="utf-8") as f:
                    vendas = json.load(f)
            except json.JSONDecodeError:
                vendas = []
        else:
            vendas = []

        for venda in vendas:

            if filtro in venda.get("data", ""):

                vendas_mostradas.append(venda)
                qtd_vendas += 1

                status = venda.get("status", "ATIVA")

                if status != "CANCELADA":
                    total_mes += venda.get("total", 0)

                lista.insert(
                    tk.END,
                    f"{venda.get('data')} - R${venda.get('total', 0):.2f} - {status}"
                )

        label_total.config(
            text=f"Total do mês: R$ {total_mes:.2f}".replace(".", ",")
        )
        label_qtd.config(
            text=f"Quantidade de vendas: {qtd_vendas}"
        )

    # ===== DETALHES =====
    def mostrar_detalhes(event):

        selecionado = lista.curselection()

        if not selecionado:
            return

        index = selecionado[0]

        if index >= len(vendas_mostradas):
            return

        venda = vendas_mostradas[index]

        detalhes.delete("1.0", tk.END)

        status = venda.get("status", "ATIVA")

        detalhes.insert(tk.END, f"DATA: {venda.get('data')}\n")
        detalhes.insert(tk.END, f"STATUS: {status}\n")
        detalhes.insert(tk.END, "-" * 40 + "\n\n")

        itens = venda.get("itens", {})

        if isinstance(itens, dict):
            for _, item in itens.items():
                nome = item.get("nome", "Sem nome")
                qtd = item.get("qtd", 0)
                preco = item.get("preco", 0)

                detalhes.insert(
                    tk.END,
                    f"{nome} | Qtd: {qtd} | R$ {preco * qtd:.2f}\n"
                )

        detalhes.insert(tk.END, f"\nTOTAL: R$ {venda.get('total', 0):.2f}")

        detalhes.update_idletasks()

    # ===== CANCELAR =====
    def cancelar():

        selecionado = lista.curselection()

        if not selecionado:
            messagebox.showerror("Erro", "Selecione uma venda!")
            return

        index = selecionado[0]

        if index >= len(vendas_mostradas):
            messagebox.showerror("Erro", "Seleção inválida!")
            return

        venda = vendas_mostradas[index]

        if venda.get("status") == "CANCELADA":
            messagebox.showwarning("Aviso", "Já cancelada!")
            return

        if not messagebox.askyesno("Confirmar", "Cancelar venda?"):
            return

        # atualiza na lista original
        for v in vendas:
            if v == venda:
                v["status"] = "CANCELADA"
                v["motivo_cancelamento"] = "Cancelada pelo usuário"
                break

        with open(VENDAS_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(vendas, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Sucesso", "Venda cancelada!")

        carregar_relatorio()

    # ===== EVENTOS =====
    lista.bind("<<ListboxSelect>>", mostrar_detalhes)

    # ===== BOTÕES =====
    tk.Button(frame_topo, text="Buscar", command=carregar_relatorio).grid(row=0, column=4)
    tk.Button(frame_topo, text="Cancelar Venda", command=cancelar).grid(row=0, column=5)

    # ===== INICIAL =====
    hoje = datetime.now()
    entry_mes.insert(0, hoje.strftime("%m"))
    entry_ano.insert(0, hoje.strftime("%Y"))

    carregar_relatorio()