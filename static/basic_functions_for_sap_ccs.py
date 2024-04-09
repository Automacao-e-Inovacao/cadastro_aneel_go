import time
import os
import win32com.client


class BasicFunctionsForSapCcs:
    usuario_rede = os.getlogin()

    def __init__(self, empresa: str, abrir_processo_sap: bool) -> None:

        if abrir_processo_sap:
            os.popen(r'"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe"')

        while True:
            time.sleep(3)
            try:
                SapGuiAuto = win32com.client.GetObject("SAPGUI")
                break
            except:
                pass

        application = SapGuiAuto.GetScriptingEngine
        if empresa == '':
            connection = application.Children(0)
        else:
            connection = application.OpenConnection(empresa, True)

        while True:
            time.sleep(3)
            try:
                self.session = connection.Children(0)
                break
            except:
                pass

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

    def login_sap_ccs(self, senha: str) -> tuple:
        self.session.findById("wnd[0]/usr/txtRSYST-BNAME").text = self.__class__.usuario_rede
        self.session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = senha
        self.session.findById("wnd[0]").sendVKey(0)
        time.sleep(2)

        if self.session.findById("wnd[1]", False):
            self.session.findById("wnd[1]/usr/radMULTI_LOGON_OPT2").select()
            self.session.findById("wnd[1]/usr/radMULTI_LOGON_OPT2").setFocus()
            self.session.findById("wnd[1]/tbar[0]/btn[0]").press()
        time.sleep(2)

        booleano = False
        for index in range(10):
            try:
                self.voltar_ate('SAP Easy Access', 3)
                booleano = True
                break
            except:
                pass

        if not booleano:
            for index in range(10):
                try:
                    self.voltar_ate('SAP Easy Access', 15)
                    booleano = True
                    break
                except:
                    pass

        if not booleano:
            return False, f'Erro ao tentar ir para a tela inicial, msg: {self.session.findById("wnd[0]").text}'

    def voltar_ate(self, titulo: str, key: int) -> None:
        if titulo in self.session.findById("wnd[0]").text:
            return

        try:
            self.session.findById("wnd[0]").sendVKey(key)
        except:
            pass

        if self.session.findById("wnd[1]", False):
            self.pops()

        if titulo in self.session.findById("wnd[0]").text:
            return
        else:
            raise AssertionError('Título ainda não é o desejado')
