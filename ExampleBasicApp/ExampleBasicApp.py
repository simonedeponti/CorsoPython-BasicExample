import clr
clr.AddReference("System")
clr.AddReference("System.Data")
clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")
import System
import os.path
import traceback
from xml.etree import ElementTree
from System.Data import DataTable
from System.Drawing import Point, Size
from System.Windows.Forms import (
    DockStyle, Application, Form, Panel,
    Label, TextBox, Button, DataGridView,
    DataGridViewColumnHeadersHeightSizeMode
)


def parseXML(xml_file):
    # Does not work with
    # tree = ElementTree.parse(xml_file)
    with open(xml_file, 'r') as xml_stream:
        tree = ElementTree.parse(xml_stream)
    root = tree.getroot()
    assert root.tag == 'contacts'
    contacts = []
    for contact_node in root.iter('contact'):
        contact = {
            'id': contact_node.attrib['id']
        }
        for property_node in contact_node.iter():
            if property_node.tag == 'company':
                contact['company'] = {
                    'name': property_node.get('name'),
                    'roles': []
                }
                for role_node in property_node.iter('role'):
                    contact['company']['roles'].append(role_node.text)
            else:
                contact[property_node.tag] = property_node.text
        contacts.append(contact)
    meta = {}
    meta_node = root.find('./meta')
    if meta_node is not None:
        for property_node in meta_node.iter():
            meta[property_node.tag] = (
                int(property_node.text.strip(), 10)
                if property_node.tag == 'txn'
                else property_node.text
            )
    return (contacts, meta)


class ExampleAppForm(Form):

    _COLUMNS = [
        ("Name", System.String, "name"),
        ("Surname", System.String, "surname"),
        ("Company", System.String, lambda x: x["company"]["name"])
    ]

    def __init__(self):
        self.Text = "Example App"
        self.Name = "ExampleApp"
        self.ClientSize = Size(370, 400)
        self.MinimumSize = Size(370, 300)
        self._table = DataTable()
        self._columns = {
            d[0]: self._table.Columns.Add(d[0], d[1])
            for d in self._COLUMNS
        }
        self._loadPanel = Panel()
        self._loadPanel.Location = Point(0, 0)
        self._loadPanel.Size = Size(215, 30)
        self._loadPanel.Dock = DockStyle.Top

        self._fileTextBoxLabel = Label()
        self._fileTextBoxLabel.Text = "Load file"
        self._fileTextBoxLabel.Size = Size(100, 16)
        self._fileTextBoxLabel.Location = Point(5, 7)
        self._loadPanel.Controls.Add(self._fileTextBoxLabel)

        self._fileTextBox = TextBox()
        self._fileTextBox.Size = Size(200, 20)
        self._fileTextBox.Location = Point(110, 5)
        self._loadPanel.Controls.Add(self._fileTextBox)

        self._loadButton = Button()
        self._loadButton.Size = Size(50, 20)
        self._loadButton.Location = Point(315, 5)
        self._loadButton.Text = "Load"
        self._loadPanel.Controls.Add(self._loadButton)

        self._dataPanel = Panel()
        self._dataPanel.Location = Point(0, 35)
        self._dataPanel.Size = Size(370, 185)

        self._dataGrid = DataGridView()
        self._dataGrid.AllowUserToOrderColumns = True
        self._dataGrid.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize
        self._dataGrid.Location = Point(0, 0)
        self._dataGrid.Size = Size(360, 180)
        self._dataGrid.DataSource = self._table
        self._dataPanel.Controls.Add(self._dataGrid)

        self.Controls.Add(self._loadPanel)
        self.Controls.Add(self._dataPanel)

        self._loadButton.Click += self.loadData

    def loadData(self, sender, event):
        filepath = self._fileTextBox.Text
        if not filepath or not os.path.exists(filepath):
            return
        try:
            contacts, meta = parseXML(filepath)
        except:
            traceback.print_exc()
            return
        for contact in contacts:
            row = self._table.NewRow()
            for col_name, __, key in self._COLUMNS:
                if callable(key):
                    row[col_name] = key(contact)
                else:
                    row[col_name] = contact[key]
            self._table.Rows.Add(row)

Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)


form = ExampleAppForm()
Application.Run(form)