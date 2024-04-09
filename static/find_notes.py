class FindNotes:

    def __init__(self, session) -> None:
        self.session = session

    def go_to_transation(self, transation_id: str) -> tuple:

        titulo = self.session.findById("wnd[0]").text

        if 'SAP Easy Access' in titulo:
            self.session.findById("wnd[0]/tbar[0]/okcd").text = transation_id
            #   botão enter
            self.session.findById("wnd[0]").sendVKey(0)
            return True, None
        else:
            raise AssertionError(f'Titulo diferente de SAP Easy Access: {titulo}')

    def window_selecao_de_notas(self, tipo_da_nota: str, layout: str, medida: str, somente_em_aberto: bool,
                                sub_codificacao, codificacao) -> None:

        titulo = self.session.findById("wnd[0]").text

        if 'Modificar medidas: seleção de notas' in titulo:
            self.session.findById("wnd[0]/usr/ctxtQMART-LOW").text = tipo_da_nota
            self.session.findById("wnd[0]/usr/ctxtDATUV").text = ""
            self.session.findById("wnd[0]/usr/ctxtDATUB").text = ""
            self.session.findById("wnd[0]/usr/ctxtMNGRP-LOW").text = medida
            self.session.findById("wnd[0]/usr/ctxtVARIANT").text = layout
            self.session.findById("wnd[0]/usr/ctxtQMGRP-LOW").text = codificacao
            self.session.findById("wnd[0]/usr/ctxtQMCOD-LOW").text = sub_codificacao
            el = self.session.findById("wnd[0]/usr/chkDY_QMSM")
            if not el.selected and somente_em_aberto:
                el.selected = True
            self.session.findById("wnd[0]").sendVKey(8)

        else:
            raise AssertionError(f'Titulo diferente de Modificar medidas: seleção de notas: {titulo}')

    def change_type_list(self, modificar: bool) -> None:

        titulo = self.session.findById("wnd[0]").text

        if 'Exibir medidas: lista de notas' in titulo and modificar:
            self.session.findById("wnd[0]/mbar/menu[0]/menu[0]").select()

        elif 'Modificar medidas: lista de notas' in titulo and not modificar:
            self.session.findById("wnd[0]/mbar/menu[0]/menu[0]").select()

    def pops(self) -> None:

        try:
            if 'Os dados serão perdidos'.replace(' ', '') in self.session.findById(
                    "wnd[1]/usr/txtSPOP-TEXTLINE1").text.replace(' ', ''):
                self.session.findById("wnd[1]/usr/btnSPOP-OPTION2").press()
        except:
            pass

        try:
            if 'Cancelar o processamento'.replace(' ', '') in self.session.findById("wnd[1]/titl").text.replace(' ',
                                                                                                                ''):
                self.session.findById("wnd[1]/usr/btnSPOP-OPTION1").press()
        except:
            pass

        try:
            if 'logoff' in self.session.findById("wnd[1]").text:
                self.session.findById("wnd[1]/usr/btnSPOP-OPTION2").press()
        except:
            pass

        try:
            self.session.findById("wnd[1]").close()
        except:
            pass

    def note_exit(self):

        key = 3
        contagem = 0

        titulo = self.session.findById("wnd[0]").text

        while titulo != 'Modificar medidas: lista de notas' and not 'Exibir medidas: lista de notas' in titulo:
            try:
                self.session.findById("wnd[0]").sendVKey(key)
            except:
                self.pops()
            titulo = self.session.findById("wnd[0]").text
            contagem += 1
            if contagem == 10:
                key = 15
            elif contagem > 20:
                raise TimeoutError('loop infinito, não consigo voltar para a tela de menu ou modificar nota')

    def insert_note_in_iw52(self, nota: int) -> tuple:

        self.session.findById("wnd[0]/usr/ctxtRIWO00-QMNUM").text = nota
        self.session.findById("wnd[0]/tbar[1]/btn[5]").press()
        self.pops()

    def obter_numero_da_nota(self, linha) -> int:
        self.session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell").setcurrentcell(linha, "QMNUM")
        nota = self.session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell").getcellvalue(linha, "QMNUM")
        nota = ''.join(filter(str.isdigit, nota))
        return int(nota)
