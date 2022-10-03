from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QMainWindow
from PyQt5 import QtWidgets, QtCore
import mysql.connector
from cadastro import Ui_Dialog as ui_cad
from login import Ui_Dialog as ui_log

class Banco():
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='',
            database=''
        )

        self.cursor = self.conexao.cursor()

    def inserir(self, nome, senha, email, special=0):
        try:
            sql = f"insert into users(nome, senha, email, special) values ('{nome}', '{senha}', '{email}', {special})"
            self.cursor.execute(sql)
            self.conexao.commit()


        except Exception as e:
            print('An exception has occured:', e)
    
    def login(self, nome, senha):
        try:
            sql = f'select senha from users where nome = "{nome}"'
            self.cursor.execute(sql)
            resultado = self.cursor.fetchall()
            print(resultado, 'abc')
            if len(resultado) == 0:
                resultado = 'notfound'
                return resultado
            elif resultado[0][0] == senha:
                resultado = 'sim'
                return resultado
            else:
                resultado = 'nao'
                return resultado
        except Exception as e:
            print(' an error has occured:', e)

class Login(QMainWindow, ui_log):
    def __init__(self):
        super().__init__()

        self.db = Banco()
        self.db.conexao.reset_session()
        self.setupUi(self)

        self.btn_signup.clicked.connect(self.cadastro)
        self.btn_login.clicked.connect(self.login)
        self.txt_senha.textChanged.connect(self.mudar)

    def mudar(self):
        self.label_error.setText('')
    def login(self):
        nome = self.txt_login.text()
        senha = self.txt_senha.text()
        print(nome, senha)
        lo =  self.db.login(nome, senha)
        print(lo)
        if lo == 'sim':
            print('wi')
        elif lo == 'notfound':
            QMessageBox.information(self, 'Error', 'Usuário nao encontrado!')
        else:
            self.label_error.setText('Senha inválida!')
            self.txt_senha.setText('')




    def cadastro(self):
        if login.isEnabled():
            login.close()
        cad.show()

class Cadastro(QMainWindow, ui_cad):
    def __init__(self):
        super().__init__()

        self.db = Banco()
        self.setupUi(self)

        self.btn_back.clicked.connect(self.back)
        self.btn_submit.clicked.connect(self.submit)
        self.c_showpass.stateChanged.connect(self.clickBox)
       

    def clickBox(self, state):

        if state == QtCore.Qt.Checked:
            self.txt_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.txt_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            
    def submit(self):
        email = self.txt_email.text()
        nome = self.txt_user.text()
        senha = self.txt_password.text()

        if email == '' or nome == '' or senha == '':
            self.label_error.setText('Por favor, preencha todos os campos!')
        else:

            resultado = QMessageBox.question(self, 'Certeza?', 'Voce deseja continuar ?', QMessageBox.Yes | QMessageBox.No)
            
            if resultado == QMessageBox.Yes:
                if nome == 'Nicory':
                    self.db.inserir(nome, senha, email, 1)
                else:
                    self.db.inserir(nome, senha, email)
                QMessageBox.information(self, 'Confirmado', 'Cadastro concluído com sucesso!')

                self.txt_email.setText('')
                self.txt_user.setText('')
                self.txt_password.setText('')

                self.back()

            else:
                pass
        
                

    def back(self):
        if cad.isEnabled():
            cad.close()
        login.show()





if __name__ == '__main__':
    app=QApplication([])
    login = Login()
    cad = Cadastro()
    login.show()
    app.exec()