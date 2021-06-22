def importar_CSV(self):
    importar = dlg.askopenfile(title='Selecione Arquivo CSV', mode='r', filetypes=(('CSV files', '.csv'),))
    try:
        importar = importar.readline()
        for i in importar[3:].strip().split(';'):
            if i not in self.lista_numeros:
                self.lista_numeros.append(i)
    except Exception as erro:
        print('Erro: ', erro)
        pass
    for num, item in enumerate(self.lista_numeros):
        self.Treeview_status.yview_moveto(1)

        # if num >= self.controle:

        self.Treeview_status.yview_moveto(1)
        self.Treeview_status.insert('', 'end', values=[self.controle, item, self.msg_texto, self.anexo_name])
        self.Treeview_status.yview_moveto(1)
        self.controle = self.controle + 1
    self.Treeview_status.yview_moveto(1)
    return self.controle, self.lista_numeros