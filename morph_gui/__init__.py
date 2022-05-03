'''
PyMOL Morphing GUI Plugin

(c) Schrodinger, Inc.
'''

import os


def dialog(_self=None):
    if _self is None:
        from pymol import cmd as _self

    from pymol.Qt import QtWidgets
    from pymol.Qt.utils import loadUi

    names = _self.get_object_list('enabled')

    if len(names) < 2 and _self.count_states('enabled') < 2:
        msg = "Need 2 molecular objects or one multistate object"
        QtWidgets.QMessageBox.warning(None, "Warning", msg)
        return

    dialog = QtWidgets.QDialog()
    uifile = os.path.join(os.path.dirname(__file__), 'morph.ui')
    form = loadUi(uifile, dialog)

    # pre-fill form with likely data
    form.input_sele1.addItems(names)
    form.input_sele2.addItems(names)
    if len(names) > 1:
        form.input_sele2.setEditText(names[1])
    else:
        form.input_state1.setValue(0)
    form.input_name.setText(_self.get_unused_name("morph"))

    def get_command(*args):
        morph = "linear"
        if form.input_method_rigimol.isChecked():
            morph = 'rigimol'

        sele1 = form.input_sele1.currentText()
        sele2 = form.input_sele2.currentText()

        try:
            nstates1 = _self.count_states(sele1)
            nstates2 = _self.count_states(sele2)

            form.input_state1.setMaximum(nstates1)
            form.input_state2.setMaximum(nstates2)
        except Exception as e:
            nstates1 = 1
            print(e)

        state1 = form.input_state1.value()
        state2 = form.input_state2.value()

        allstates = (state1 == 0 and nstates1 > 1)
        if allstates:
            sele2 = sele1
            state2 = 0

        form.input_sele2.setDisabled(allstates)
        form.input_state2.setDisabled(allstates)
        form.superpose.setDisabled(allstates)

        command = ('morph %s, %s, %s, %d, %d, %d, %d, %s' % (
            form.input_name.text(), sele1, sele2, state1, state2,
            form.input_refinement.value(), form.input_steps.value(), morph))

        if not allstates and form.superpose.isChecked():
            command = (
                ('align %s, %s, '
                 'mobile_state=%d, target_state=%d\n' %
                 (form.input_sele1.currentText(),
                  form.input_sele2.currentText(), state1, state2)) + command)

        return command

    def update_output_command(*args):
        form.output_command.setText(get_command())

    def run():
        _self.do(get_command())

    # hook up events
    form.input_sele1.editTextChanged.connect(update_output_command)
    form.input_sele2.editTextChanged.connect(update_output_command)
    form.input_state1.valueChanged.connect(update_output_command)
    form.input_state2.valueChanged.connect(update_output_command)
    form.superpose.stateChanged.connect(update_output_command)
    form.input_refinement.valueChanged.connect(update_output_command)
    form.input_steps.valueChanged.connect(update_output_command)
    form.input_method_rigimol.toggled.connect(update_output_command)
    form.input_method_linear.toggled.connect(update_output_command)
    form.input_name.textChanged.connect(update_output_command)
    form.button_ok.clicked.connect(run)

    update_output_command()
    dialog.show()


def __init_plugin__(app=None):
    from pymol.plugins import addmenuitemqt as addmenuitem
    addmenuitem('Morphing', dialog)
