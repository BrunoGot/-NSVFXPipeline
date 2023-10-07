import os
import sys

from PySide2.QtWidgets import QWidget, QApplication, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QTextEdit, \
    QPushButton, QTreeView, QLayout
from PySide2.QtGui import QStandardItem, QStandardItemModel

from pipeline import fileSystem as fs


class BlenderSaveUI(QWidget):
    def __init__(self, engine):
        super(BlenderSaveUI, self).__init__()
        self.engine = engine
        self.project_structure = {}
        self.datas = {}
        self.base_path = r'D:/Prod/03_WORK_PIPE/01_ASSET_3D'
        self.current_selected_path = self.base_path


        # GUI panel
        main_layout = QVBoxLayout()
        info_panel = QHBoxLayout()
        left_panel = QVBoxLayout()
        left_panel.addLayout(self.add_pipeline_folder("AssetType"))
        left_panel.addLayout(self.add_pipeline_folder("AssetName"))
        left_panel.addLayout(self.add_pipeline_folder("Task"))
        left_panel.addLayout(self.add_pipeline_folder("Subtask"))
        left_panel.addLayout(self.add_pipeline_folder("Version"))
        info_panel.addLayout(left_panel)

        # treeview
        self.tree_view = QTreeView()
        self.tree_model = QStandardItemModel()
        self.tree_model = self.fill_tree_view(self.tree_model)
        self.tree_view.setModel(self.tree_model)
        self.tree_view.clicked.connect(lambda index: self.tree_node_clicked(self.tree_model.itemFromIndex(index)))
        self.tree_view.setMinimumSize(100, 300)
        info_panel.addWidget(self.tree_view)
        main_layout.addLayout(info_panel)
        # comments
        main_layout.addWidget(QLabel("comment"))
        comment_box = QTextEdit()
        comment_box.setMaximumHeight(75)
        main_layout.addWidget(comment_box)
        # btn layouts
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.on_save)
        button_layout.addWidget(save_btn)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.on_close)
        button_layout.addWidget(cancel_btn)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        #self.show()

    def tree_node_clicked(self, item):
        print(f"QStandardItem = {item.parent()}")
        # current_depth = self.get_depth_node(item)
        parent_list = [item.text()]
        parent_list += self.get_parent_list(item)
        path = os.path.join(*reversed(parent_list))
        print(f"path = {path}")
        self.current_selected_path = os.path.join(self.base_path, path)
        print(f"new_node_path = {self.current_selected_path}")
        if os.path.isdir(self.current_selected_path):
            # self.current_selected_path = new_node_path
            nodes = self.add_node(self.current_selected_path, os.listdir(self.current_selected_path))
            item.appendRows(nodes)
        self.tree_view.viewport().update()
        self.tree_view.setExpanded(self.tree_model.indexFromItem(item), True)

        self.fill_asset_form(parent_list)

    def fill_asset_form(self, parent_list):
        i = 1
        for line_edit in self.project_structure.values():
            if len(parent_list) >= i:
                line_edit.setText(parent_list[-i])
                i += 1
            else:
                break

    def get_parent_list(self, node):
        """
        recursive function to get the list of parents of the node item
        :param QStandardItem node:
        :return str[]: list of node in parents
        """
        parents = []
        parent = node.parent()
        if parent is not None:
            parents.append(parent.text())
            parents.extend(self.get_parent_list(parent))
        return parents

    def add_node(self, parent_path, list_elem):
        nodes = []
        for e in list_elem:
            node = QStandardItem()
            node.setText(e)
            path = os.path.join(parent_path, e)
            if os.path.isdir(path):
                pass
                # childrens = os.listdir(path)
                # node.appendRows(self.add_node(path, childrens))
            nodes.append(node)
        return nodes

    def fill_tree_view(self, tree_model):
        types_folder = os.listdir(self.current_selected_path)  # fs.asset_base_path)
        root_node = tree_model.invisibleRootItem()
        root_node.appendRows(
            self.add_node(self.current_selected_path, types_folder))  # fs.asset_base_path, types_folder))
        return tree_model

    def add_pipeline_folder(self, label_name):
        layout = QHBoxLayout()
        project_label = QLabel(label_name)
        layout.addWidget(project_label)
        project_line_edit = QLineEdit()
        layout.addWidget(project_line_edit)
        self.project_structure[label_name] = project_line_edit
        return layout

    def on_save(self):
        for i, j in self.project_structure.items():
            self.datas[i] = j.text()
        self.engine.save(self.datas)
        self.close()

    def on_close(self):
        self.close()


def show_ui(engine):
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    w = BlenderSaveUI(engine)
    w.show()
    app.exec_()
    print(f"datas = {w.datas}")
    return w.datas


if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    w = BlenderSaveUI()
    sys.exit(app.exec_())