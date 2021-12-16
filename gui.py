import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from utils import login, logout, checkauth


class MgallManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.session = None

    def initUI(self):
        layout = QVBoxLayout()

        self.id_text = QLineEdit(self)
        self.id_text.setPlaceholderText("ID")
        self.pw_text = QLineEdit(self)
        self.pw_text.setPlaceholderText("PW")
        self.pw_checkbox = QCheckBox("비밀번호 숨기기", self)
        self.pw_checkbox.stateChanged.connect(self.hidePassword)
        self.pw_checkbox.toggle()
        self.login_button = QPushButton("로그인", self)
        # 로그인 시 로그아웃 버튼으로 활성화
        self.login_button.setMaximumHeight(500)
        self.login_button.clicked.connect(self.trylogin)
        self.login_status_text = QLabel("로그인되지 않음", self)

        self.gall_id_text = QLineEdit(self)
        self.gall_id_text.setPlaceholderText("Gallery ID")
        self.connect_button = QPushButton("접속", self)
        self.connect_button.clicked.connect(self.trycheckauth)
        self.Mgall_rbutton = QRadioButton("마이너 갤러리", self)
        self.mgall_rbutton = QRadioButton("미니 갤러리", self)
        self.manager_status_text = QLabel("", self)

        self.block_vpn_text = QLabel("VPN 차단", self)
        self.block_vpn_box = QComboBox(self)
        self.block_vpn_box.addItem("48시간")
        self.block_vpn_box.addItem("24시간")
        self.block_vpn_box.addItem("차단 해제")
        self.block_mobile_text = QLabel("통신사 IP 차단", self)
        self.block_mobile_box = QComboBox(self)
        self.block_mobile_box.addItem("60분")
        self.block_mobile_box.addItem("30분")
        self.block_mobile_box.addItem("차단 해제")
        self.block_apply = QPushButton("1회 적용", self)
        self.block_auto = QPushButton("자동 차단", self)
        self.block_status_text = QLabel("차단 비활성화됨", self)

        self.delete_text = QLineEdit(self)
        self.delete_text.setPlaceholderText("사용자 ID 리스트 입력")
        self.delete_button = QPushButton("글 삭제", self)
        self.delete_interval_text = QLabel("삭제 주기", self)
        self.delete_box = QComboBox(self)
        self.delete_box.addItem("1분")
        self.delete_box.addItem("3분")
        self.delete_box.addItem("5분")
        self.delete_box.addItem("10분")
        self.delete_auto_button = QPushButton("자동 삭제", self)

        loginbox = QGroupBox()
        loginLayout = QGridLayout()
        loginbox.setLayout(loginLayout)
        loginLayout.addWidget(self.id_text, 1, 2)
        loginLayout.addWidget(self.pw_text, 2, 2)
        loginLayout.addWidget(self.pw_checkbox, 4, 2)
        loginLayout.addWidget(self.login_button, 1, 3, 2, 1)
        loginLayout.addWidget(self.login_status_text, 5, 2)
        layout.addWidget(loginbox)

        managerbox = QGroupBox()
        managerLayout = QGridLayout()
        managerbox.setLayout(managerLayout)
        managerLayout.addWidget(self.gall_id_text, 1, 2, 1, 3)
        managerLayout.addWidget(self.connect_button, 1, 5)
        managerLayout.addWidget(self.Mgall_rbutton, 2, 2)
        managerLayout.addWidget(self.mgall_rbutton, 2, 3)
        managerLayout.addWidget(self.manager_status_text, 3, 2)
        layout.addWidget(managerbox)

        blockerbox = QGroupBox()
        blockerLayout = QGridLayout()
        blockerbox.setLayout(blockerLayout)
        blockerLayout.addWidget(self.block_vpn_text, 2, 2, 1, 2)
        blockerLayout.addWidget(self.block_vpn_box, 2, 4, 1, 1)
        blockerLayout.addWidget(self.block_mobile_text, 3, 2, 1, 2)
        blockerLayout.addWidget(self.block_mobile_box, 3, 4, 1, 1)
        blockerLayout.addWidget(self.block_apply, 2, 5, 1, 1)
        blockerLayout.addWidget(self.block_auto, 3, 5, 1, 1)
        blockerLayout.addWidget(self.block_status_text, 5, 2)
        # HTML 데이터를 확인하여 "VPN : xx:xx 까지, 통신사 IP : xx:xx 까지"
        layout.addWidget(blockerbox)

        deleterbox = QGroupBox()
        deleterLayout = QGridLayout()
        deleterbox.setLayout(deleterLayout)
        deleterLayout.addWidget(self.delete_text, 1, 2, 1, 3)
        deleterLayout.addWidget(self.delete_button, 1, 5)
        deleterLayout.addWidget(self.delete_interval_text, 2, 2, 1, 2)
        deleterLayout.addWidget(self.delete_box, 2, 4, 1, 1)
        deleterLayout.addWidget(self.delete_auto_button, 2, 5)
        layout.addWidget(deleterbox)

        self.setWindowTitle("MgallManager")
        self.setFixedSize(350, 400)
        self.setLayout(layout)
        self.move(300, 300)
        self.show()

    def hidePassword(self):
        if self.pw_checkbox.isChecked():
            self.pw_text.setEchoMode(QLineEdit.Password)

        else:
            self.pw_text.setEchoMode(QLineEdit.Normal)

    def trylogin(self):
        user_id = self.id_text.text()
        user_pw = self.pw_text.text()

        self.session = login(user_id, user_pw)
        if self.session is None:
            self.login_status_text.setText("로그인 실패")

            return

        else:
            self.login_status_text.setText("로그인 완료")
            self.id_text.setEnabled(False)
            self.pw_text.setEnabled(False)
            self.login_button.setEnabled(False)

            return

    def trylogout(self):
        if self.session is not None:
            logout(self.session)
            self.session = None
            """
            버튼 초기화하기.
            """

            return

    def trycheckauth(self):
        gall_id = self.gall_id_text.text()

        if self.session is not None:
            status = checkauth(self.session, gall_id)
            if status:
                self.manager_status_text.setText("관리자 권한 확인됨")
            else:
                self.manager_status_text.setText("관리자 권한 없음")

        else:
            self.manager_status_text.setText("로그인되지 않음")

        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MgallManager()
    sys.exit(app.exec_())
