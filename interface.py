import requests
import flet as ft

base_url = 'http://192.168.43.124/'  # endereço IP do ESP8266

class Aplicacao(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.pin_mapping = {"Led": 2}  # pino GPIO do LED no ESP8266
        self.show_password_var = False  # estado da exibição da senha
        self.remember_me_var = False  # estado de lembrar o usuário
        self.username = ""  # armazena o nome do usuário
        self.t01_switch = None
        self.t02_switch = None
        self.t03_switch = None
        self.t04_switch = None
        self.t05_switch = None
        self.t06_switch = None
        self.t07_switch = None
        self.t08_switch = None
        self.t09_switch = None
        self.t10_switch = None

    def build(self):  # constrói a interface do usuário
        self.usuario = ft.TextField(label="Usuário", value=self.username, autofocus=True, bgcolor=ft.colors.BLACK, color=ft.colors.WHITE)
        self.senha = ft.TextField(label="Senha", password=True, bgcolor=ft.colors.BLACK, color=ft.colors.WHITE)
        self.show_password_checkbox = ft.Checkbox(label="Mostrar Senha", value=self.show_password_var, on_change=self.toggle_password_visibility)
        self.remember_me_checkbox = ft.Checkbox(label="Lembrar de mim", value=self.remember_me_var, on_change=self.toggle_remember_me)
        self.login_button = ft.ElevatedButton(text="Login", on_click=self.clique, bgcolor=ft.colors.DEEP_PURPLE, color=ft.colors.WHITE)
        
        return ft.Column(
            [
                ft.Text("Bem-vindo, Faça Login!", color=ft.colors.WHITE),
                self.usuario,
                self.senha,
                self.show_password_checkbox,
                self.remember_me_checkbox,
                self.login_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def toggle_password_visibility(self, e):  # função para alternar a visibilidade da senha
        self.senha.password = not e.control.value
        self.senha.update()

    def toggle_remember_me(self, e):  # função para alternar o estado de lembrar o usuário
        self.remember_me_var = e.control.value

    def clique(self, e):  # verificações de entrada do usuário
        usuario_input = self.usuario.value
        senha_input = self.senha.value

        if usuario_input == "admin" and senha_input == "admin":
            if self.remember_me_var:
                self.username = usuario_input  # Armazena o nome do usuário se 'Lembrar de mim' estiver marcado
            else:
                self.username = ""  # Limpa o nome do usuário se 'Lembrar de mim' não estiver marcado

            self.page.clean()
            self.page.add(self.build_tela_controle())
        else:
            self.page.clean()
            self.page.add(self.build())
            self.page.add(ft.Text("Senha incorreta", color=ft.colors.RED))

    def build_tela_controle(self):  # constrói a tela de controle
        self.t01_switch = ft.Switch(label="T01", on_change=lambda e: self.toggle_saida(e, "Led"))
        self.t02_switch = ft.Switch(label="T02", on_change=lambda e: self.toggle_saida(e, "Led"))
        self.t03_switch = ft.Switch(label="T03", on_change=lambda e: self.toggle_saida(e, "Led"))
        self.t04_switch = ft.Switch(label="T04", on_change=lambda e: self.toggle_saida(e, "Led"))
        self.t05_switch = ft.Switch(label="T05", on_change=lambda e: self.toggle_saida(e, "Led"))
        self.t06_switch = ft.Switch(label="T06", on_change=lambda e: self.toggle_saida(e, "Led"))
        self.t07_switch = ft.Switch(label="T07", on_change=lambda e: self.toggle_saida(e, "Led"))
        self.t08_switch = ft.Switch(label="T08", on_change=lambda e: self.toggle_saida(e, "Led"))
        self.t09_switch = ft.Switch(label="T09", on_change=lambda e: self.toggle_saida(e, "Led"))
        self.t10_switch = ft.Switch(label="T10", on_change=lambda e: self.toggle_saida(e, "Led"))
        toggle_all_switch = ft.Switch(label="Alternar Todos", on_change=self.toggle_todas_saidas)
        logout_button = ft.ElevatedButton(text="Logout", on_click=self.logout, bgcolor=ft.colors.DEEP_PURPLE, color=ft.colors.WHITE)
        
        return ft.Column(
            [
                ft.Text("Painel de Controle do Torno", color=ft.colors.WHITE),
                ft.Row(
                    [self.t01_switch, 
                     self.t02_switch, 
                     self.t03_switch, 
                     self.t04_switch, 
                     self.t05_switch, 
                     self.t06_switch, 
                     self.t07_switch, 
                     self.t08_switch, 
                     self.t09_switch, 
                     self.t10_switch], alignment=ft.MainAxisAlignment.CENTER),
                toggle_all_switch,
                logout_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def toggle_todas_saidas(self, e):
        valor = e.control.value
        self.t01_switch.value = valor
        self.t02_switch.value = valor
        self.t03_switch.value = valor
        self.t04_switch.value = valor
        self.t05_switch.value = valor
        self.t06_switch.value = valor
        self.t07_switch.value = valor
        self.t08_switch.value = valor
        self.t09_switch.value = valor
        self.t10_switch.value = valor
        self.t01_switch.update()
        self.t02_switch.update()
        self.t03_switch.update()
        self.t04_switch.update()
        self.t05_switch.update()
        self.t06_switch.update()
        self.t07_switch.update()
        self.t08_switch.update()
        self.t09_switch.update()
        self.t10_switch.update()
        if valor:
            self.ligar_saida("Led")
        else:
            self.ligar_saida("Led")

    def toggle_saida(self, e, key):
        if e.control.value:
            self.ligar_saida(key)
        else:
            self.desligar_saida(key)

    def ligar_saida(self, key):
        url = base_url + f'toggle_{key}_rele'
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Pedido para ligar o {key} enviado com sucesso")
        else:
            print(f"Falha ao ligar o {key}. Código de status: {response.status_code}")

    def desligar_saida(self, key):
        url = base_url + f'toggle_{key}_rele'
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Pedido para desligar o {key} enviado com sucesso")
        else:
            print(f"Falha ao desligar o {key}. Código de status: {response.status_code}")

    def logout(self, e):
        self.page.clean()
        self.page.add(self.build())

def main(page: ft.Page):
    page.title = "Suporte de Controle"
    page.theme_mode = ft.ThemeMode.DARK  # Configura o tema para escuro
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.BLACK  # Define o fundo da página como preto

    app = Aplicacao()
    page.add(app)

ft.app(target=main)
