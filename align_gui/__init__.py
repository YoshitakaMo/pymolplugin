'''
PyMOL Alignment GUI Plugin

(c) Schrodinger, Inc.
'''

import os


def dialog(_self=None):
    if _self is None:
        from pymol import cmd as _self

    from pymol.Qt import QtWidgets
    from pymol.Qt.utils import loadUi

    names = _self.get_object_list()

    if len(names) < 2:
        msg = "Need at least 2 molecular objects"
        QtWidgets.QMessageBox.warning(None, "Warning", msg)
        return

    dialog = QtWidgets.QDialog()
    uifile = os.path.join(os.path.dirname(__file__), 'align.ui')
    form = loadUi(uifile, dialog)

    form.input_mobile.addItems(names)
    form.input_target.addItems(names)

    def get_command(*args):
        method = form.input_method.currentText()
        mobile = form.input_mobile.currentText()
        target = form.input_target.currentText()

        if form.check_many.isChecked():
            command = 'extra_fit %s, %s, \\\n    method=%s' % (mobile, target,
                                                               method)
        elif method == 'cealign':
            command = 'cealign %s, %s' % (target, mobile)
        else:
            command = '%s %s, %s' % (method, mobile, target)

        if method != 'cealign':
            if not form.group_outlier.isChecked():
                command += (', \\\n    cycles=0')
            else:
                command += (', \\\n'
                            '    cycles=%d, \\\n'
                            '    cutoff=%.1f' % (
                                form.input_cycles.value(),
                                form.input_cutoff.value(), ))
            if method == 'fit':
                command += ', \\\n    matchmaker=1'

        command += (', \\\n'
                    '    mobile_state=%d, \\\n'
                    '    target_state=%d' % (form.input_mobile_state.value(),
                                             form.input_target_state.value()))

        aln_obj = form.input_object.text()
        if aln_obj:
            command += ', \\\n    object=' + aln_obj

        return command

    def update_output_command(*args):
        form.group_outlier.setEnabled(
            form.input_method.currentText() != 'cealign')
        form.output_command.setText(get_command())

    def update_output_command_many(*args):
        mobile = form.input_mobile.currentText()
        if form.check_many.isChecked():
            if mobile == names[1] and form.input_target.currentText() == names[
                    0]:
                form.input_mobile.setEditText('*')
        elif mobile == '*':
            if form.input_target.currentText() != names[1]:
                form.input_mobile.setEditText(names[1])
            else:
                form.input_mobile.setEditText(names[0])

        form.output_command.setText(get_command())

    def run():
        _self.do(get_command())

    # hook up events
    form.group_outlier.toggled.connect(update_output_command)
    form.check_many.toggled.connect(update_output_command_many)
    form.input_method.currentIndexChanged.connect(update_output_command)
    form.input_mobile.editTextChanged.connect(update_output_command)
    form.input_target.editTextChanged.connect(update_output_command)
    form.input_mobile_state.valueChanged.connect(update_output_command)
    form.input_target_state.valueChanged.connect(update_output_command)
    form.input_cycles.valueChanged.connect(update_output_command)
    form.input_cutoff.valueChanged.connect(update_output_command)
    form.input_object.textChanged.connect(update_output_command)
    form.button_ok.clicked.connect(run)

    update_output_command()
    dialog.show()


def __init_plugin__(app=None):
    from pymol.plugins import addmenuitemqt as addmenuitem
    addmenuitem('Alignment', dialog)
