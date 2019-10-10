'''
Excel Exporter PyMOL Plugin

Requires Qt PyMOL and xlwings

(c) Schrodinger, Inc.
'''

import os
import sys
import pymol
from pymol.Qt import QtWidgets, utils as pymolqtutils

# magic number for iterate vs. iterate_state
STATELESS = -999


def dumpexcel(selection='all',
              props='chain segi resi resn name b q',
              state=STATELESS):
    '''
DESCRIPTION

    Open a new Excel spreadsheet with atom property data from the given
    selection.
    '''
    try:
        import xlwings
    except ImportError:
        raise pymol.CmdException('Requires xlwings (conda install xlwings)')

    try:
        sheet = xlwings.Book().sheets[0]
    except IndexError:
        sheet = None

    if not isinstance(props, (list, tuple)):
        props = props.split()

    table = [props]

    kwargs = {
        'expression': '_append((' + ','.join(props) + '))',
        'space': {
            '_append': table.append
        },
    }

    if state == STATELESS:
        pymol.cmd.iterate(selection, **kwargs)
    else:
        pymol.cmd.iterate_state(state, selection, **kwargs)

    xlwings.view(table, sheet)


def _check_xlwings():
    try:
        import xlwings
        return True
    except ImportError:
        pass

    if not pymolqtutils.conda_ask_install('xlwings', None,
            'Python package "xlwings" required.',
            url='https://github.com/ZoomerAnalytics/xlwings/blob/master/LICENSE.txt'):
        return False

    # can't import freshly installed xlwings without this
    import site
    site.addsitepackages(set(sys.path))

    return True


def qtdialog():
    dialog = QtWidgets.QDialog()
    uifile = os.path.join(os.path.dirname(__file__), 'excelexporter.ui')
    form = pymolqtutils.loadUi(uifile, dialog)
    form._dialog = dialog

    # pre-fill form with likely data
    names = pymol.cmd.get_object_list()
    names += ['(' + n + ')' for n in pymol.cmd.get_names('public_selections')]
    form.input_sele.addItems(names)

    checkboxes = {
        'x': form.check_x,
        'y': form.check_y,
        'z': form.check_z,
    }

    prop_names = [
        'model', 'segi', 'chain', 'resi', 'resv', 'resn', 'name', 'alt', 'b',
        'q', 'elem', 'type', 'formal_charge', 'partial_charge', 'numeric_type',
        'text_type', 'stereo', 'ID', 'rank', 'index', 'vdw', 'ss', 'color',
        'reps', 'protons', 'state'
    ]

    # user properties
    p_set = set()
    pymol.cmd.iterate('all', 'p_set_update(p)',
            space={'p_set_update': p_set.update})
    prop_names.extend('p.' + prop for prop in sorted(p_set))

    ncols = 3

    for i, prop in enumerate(prop_names):
        check = QtWidgets.QCheckBox(prop, form.groupBox)
        form.gridLayout.addWidget(check, i // ncols, i % ncols, 1, 1)
        checkboxes[prop] = check

    # add state properties to list
    prop_names.extend('xyz')

    for prop in ['chain', 'resi', 'resn', 'name']:
        checkboxes[prop].setChecked(True)

    @form.button_ok.clicked.connect
    def _(*args):
        props = [p for p in prop_names if checkboxes[p].isChecked()]
        sele = form.input_sele.currentText()
        statetext = form.input_state.checkedButton().text()

        if statetext.startswith('current'):
            state = -1
        elif statetext.startswith('all'):
            state = 0
        else:
            state = STATELESS
            props = [p for p in props if p not in ['x', 'y', 'z']]

        if not _check_xlwings():
            return

        with pymolqtutils.PopupOnException():
            dumpexcel(sele, props, state)

    form._dialog.show()


def __init_plugin__(app=None):
    if sys.platform not in ('darwin', 'win32'):
        return

    from pymol.plugins import addmenuitemqt
    addmenuitemqt('Excel Exporter', qtdialog)
