import tkinter as tk
from tkinter import ttk

class DraggableTreeview(ttk.Treeview):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_drop)
        self.drag_data = {"item": None, "index": None}

    def on_click(self, event):
        # Obter o item clicado
        self.drag_data["item"] = self.identify_row(event.y)
        self.drag_data["index"] = self.index(self.drag_data["item"])

    def on_drag(self, event):
        # Mover o item enquanto arrasta
        item = self.drag_data["item"]
        if item:
            self.move(item, '', self.index(self.identify_row(event.y)))

    def on_drop(self, event):
        # Soltar o item no novo local
        item = self.drag_data["item"]
        if item:
            self.drag_data["item"] = None
            self.drag_data["index"] = None

# Função para inserir dados na árvore com cores alternadas
def insert_data(tree):
    data = [
        ('1', 'John Doe', '28'),
        ('2', 'Jane Smith', '34'),
        ('3', 'Mike Johnson', '45'),
        ('4', 'Anna Brown', '23'),
        ('5', 'Sam White', '37')
    ]

    for index, row in enumerate(data):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        tree.insert('', 'end', values=row, tags=(tag,))

# Criar a janela principal
root = tk.Tk()
root.title("Árvore de Tabela com Tkinter")

# Criar a árvore de tabela
tree = DraggableTreeview(root, columns=('ID', 'Nome', 'Idade'), show='headings')

# Definir os cabeçalhos das colunas
tree.heading('ID', text='ID')
tree.heading('Nome', text='Nome')
tree.heading('Idade', text='Idade')

# Definir o tamanho das colunas
tree.column('ID', width=50)
tree.column('Nome', width=150)
tree.column('Idade', width=50)

# Definir as cores alternadas
tree.tag_configure('evenrow', background='lightgrey')
tree.tag_configure('oddrow', background='white')

# Empacotar a árvore na janela
tree.pack(fill='both', expand=True)

# Inserir dados na árvore com cores alternadas
insert_data(tree)

# Executar a aplicação
root.mainloop()
