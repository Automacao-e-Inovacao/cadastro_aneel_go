import psutil


def fechar_tudo(lista_dos_caminhos_dos_processos, lista_dos_nomes_de_processos):
    for proc in psutil.process_iter():
        try:
            for linha in lista_dos_caminhos_dos_processos:
                cmdline = proc.cmdline()
                if linha in cmdline:
                    proc.kill()
                    continue
                else:
                    for linha_2 in cmdline:
                        if 'from multiprocessing' in linha_2:
                            proc.kill()
                            continue
            for linha in lista_dos_nomes_de_processos:
                executavel = proc.exe()
                if linha in executavel:
                    proc.kill()
                    continue
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
