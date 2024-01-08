from PyQt5.Qt import *
from shifr import *

class Ui_signUp(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(570, 375)
        self.label = QLabel(Dialog)
        self.label.setGeometry(QRect(160, 130, 81, 31))
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QLabel(Dialog)
        self.label_2.setGeometry(QRect(160, 230, 81, 31))
        font = QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(Dialog)
        self.label_3.setGeometry(QRect(160, 180, 81, 31))
        font = QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.uname_lineEdit = QLineEdit(Dialog)
        self.uname_lineEdit.setGeometry(QRect(250, 130, 141, 20))
        self.uname_lineEdit.setObjectName("uname_lineEdit")
        self.email_lineEdit = QLineEdit(Dialog)
        self.email_lineEdit.setGeometry(QRect(250, 180, 141, 20))
        self.email_lineEdit.setObjectName("email_lineEdit")
        self.password_lineEdit = QLineEdit(Dialog)
        self.password_lineEdit.setGeometry(QRect(250, 230, 141, 20))
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.signup_btn = QPushButton(Dialog)
        self.signup_btn.setGeometry(QRect(270, 290, 75, 23))
        self.signup_btn.setObjectName("signup_btn")
        self.label_4 = QLabel(Dialog)
        self.label_4.setGeometry(QRect(150, 10, 321, 81))
        font = QFont()
        font.setPointSize(18)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Регистрация"))
        self.label.setText(_translate("Dialog", "Логин"))
        self.label_2.setText(_translate("Dialog", "Пароль"))
        self.label_3.setText(_translate("Dialog", "Email"))
        self.signup_btn.setText(_translate("Dialog", "Войти"))
        self.label_4.setText(_translate("Dialog", "Регистрация"))


class Dialog(QDialog, Ui_signUp):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.signup_btn.clicked.connect(self.insertData)

    @pyqtSlot()
    def insertData(self):
        

        username = trippledesencrypt(self.uname_lineEdit.text())
        email = trippledesencrypt(self.email_lineEdit.text())
        password = trippledesencrypt(self.password_lineEdit.text())

        file = open('login.txt', 'r', encoding='utf-8')
        text = file.readlines()
        file.close()

        if (not username) or (not email) or (not password):
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return

        flag = True
        for i in range(len(text)):
            text[i] = text[i][:-1]
            row = text[i].split(" ")
            if username == row[0]:
                msg = QMessageBox.information(self, 'Внимание!', 'Пользоватеть с таким именем уже зарегистрирован.')
                flag = False
                break
            
        if flag:
            # if log != row[0] and email != row[1]:
            file = open('login.txt', 'a', encoding='utf-8')
            file.write('\n' + username + ' ' + email + ' ' + password)
            file.close()
            self.close()


if __name__ == "__main__":
    import sys
    app    = QApplication(sys.argv)
    w = Dialog()
    w.show()
    sys.exit(app.exec_())
