# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-02-21
        git sha              : :%H$
        copyright            : (C) 2019 by Yesid Polanía (BSF Swissphoto)
        email                : yesidpol.3@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import (QCoreApplication,
                              pyqtSignal)
from qgis.PyQt.QtWidgets import (QWidget,
                                 QLabel,
                                 QGridLayout,
                                 QLineEdit)
from qgis.core import Qgis
from .db_schema_db_panel import DbSchemaDbPanel
from ...lib.db.pg_connector import PGConnector


class PgConfigPanel(QWidget, DbSchemaDbPanel):
    notify_message_requested = pyqtSignal(str, Qgis.MessageLevel)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        DbSchemaDbPanel.__init__(self, PGConnector(''))

        self.mode = "pg"

        lbl_host = QLabel(QCoreApplication.translate("SettingsDialog", "Host"))
        lbl_port = QLabel(QCoreApplication.translate("SettingsDialog", "Port"))
        lbl_user = QLabel(QCoreApplication.translate("SettingsDialog", "User"))
        lbl_password = QLabel(QCoreApplication.translate("SettingsDialog", "Password"))
        lbl_database = QLabel(QCoreApplication.translate("SettingsDialog", "Database"))
        lbl_schema = QLabel(QCoreApplication.translate("SettingsDialog", "Schema"))

        self.txt_host = QLineEdit()
        self.txt_host.setPlaceholderText(QCoreApplication.translate("SettingsDialog", "[Leave empty to use standard host: localhost]"))

        self.txt_port = QLineEdit()
        self.txt_port.setPlaceholderText(
            QCoreApplication.translate("SettingsDialog", "[Leave empty to use standard port: 5432]"))

        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText(QCoreApplication.translate("SettingsDialog", "Database username"))

        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setPlaceholderText(
            QCoreApplication.translate("SettingsDialog", "[Leave empty to use system password]"))

        self.create_db_button.setToolTip(QCoreApplication.translate("SettingsDialog", "Create database"))

        self.create_schema_button.setToolTip(QCoreApplication.translate("SettingsDialog", "Create schema"))

        layout = QGridLayout(self)
        layout.addWidget(lbl_host, 0, 0)
        layout.addWidget(lbl_port, 1, 0)
        layout.addWidget(lbl_user, 2, 0)
        layout.addWidget(lbl_password, 3, 0)
        layout.addWidget(lbl_database, 5, 0)
        layout.addWidget(lbl_schema, 6, 0)

        layout.addWidget(self.txt_host, 0, 1)
        layout.addWidget(self.txt_port, 1, 1)
        layout.addWidget(self.txt_user, 2, 1)
        layout.addWidget(self.txt_password, 3, 1)

        layout.addWidget(self.refresh_db_button, 4, 0, 1, 2)

        layout.addWidget(self.selected_db_combobox, 5, 1)
        layout.addWidget(self.selected_schema_combobox, 6, 1)

        layout.addWidget(self.create_db_button, 5, 2)
        layout.addWidget(self.create_schema_button, 6, 2)

    def showEvent(self, event):
        self._set_controls_enabled(False)

    def read_connection_parameters(self):
        """
        Convenient function to read connection parameters and apply default
        values if needed.
        """
        dict_conn = dict()

        dict_conn['host'] = self.txt_host.text().strip()
        dict_conn['port'] = self.txt_port.text().strip()
        dict_conn['database'] = self.selected_db_combobox.currentText().strip()
        dict_conn['schema'] = self.selected_schema_combobox.currentText().strip()
        dict_conn['username'] = self.txt_user.text().strip()
        dict_conn['password'] = self.txt_password.text().strip()

        return dict_conn

    def get_keys_connection_parameters(self):
        return list(self.read_connection_parameters().keys())

    def write_connection_parameters(self, dict_conn):
        self._disconnect_change_signals()

        self.txt_host.setText(dict_conn['host'])
        self.txt_port.setText(dict_conn['port'])
        self.txt_user.setText(dict_conn['username'])
        self.txt_password.setText(dict_conn['password'])

        if not dict_conn['database']:
            self._connect_change_signals()
            return

        db_name_setting = dict_conn['database']

        self.selected_db_combobox.clear()
        self.selected_schema_combobox.clear()

        if db_name_setting:
            self.selected_db_combobox.addItem(db_name_setting)
        if dict_conn['schema']:
            self.selected_schema_combobox.addItem(dict_conn['schema'])

        self._connect_change_signals()

    def state_changed(self):
        result = True

        if self.state:
            result = (self.state['host'] != self.txt_host.text().strip() or \
                self.state['port'] != self.txt_port.text().strip() or \
                self.state['database'] != self.selected_db_combobox.currentText().strip() or \
                self.state['schema'] != (self.selected_schema_combobox.currentText().strip() or 'public') or \
                self.state['username'] != self.txt_user.text().strip() or \
                self.state['password'] != self.txt_password.text().strip())

        return result
