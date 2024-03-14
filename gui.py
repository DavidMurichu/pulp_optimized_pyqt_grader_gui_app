from imports import *
from setup import show_dialog
try: 
    #GUI PYQT
    class DoubleSpinBoxDelegate(QItemDelegate):
        def createEditor(self, parent, option, index):
            editor = QDoubleSpinBox(parent)
            editor.setFrame(False)
            editor.setRange(0, 10000)  # Set the range as needed
            return editor

    class MyButton(QPushButton):
        def __init__(self, button_id, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.button_id = button_id

    class CentralController(QWidget):
        data_updated = pyqtSignal()
        fomulation_updated = pyqtSignal()

    class MainWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.move(100, 50)
            self.show()
            screen= QGuiApplication.primaryScreen()
            primary_screen = QGuiApplication.primaryScreen()
            screen_geometry = primary_screen.geometry()
            
            # Use screen geometry to determine base width and height
            base_width = screen_geometry.width()
            base_height = screen_geometry.height()

            self.scaled_width = int(base_width * scale_factor)
            self.scaled_height = int(base_height * scale_factor)
            
            self.setWindowTitle('Micron Feeder')
            self.setStyleSheet("background-color: #6C22A6; color:black;  font-size: 17px;")
            self.resize(self.scaled_width, self.scaled_height)
            self.central_controller = CentralController()

            # ingredient table
            ingredient_table = self.create_table(column_count=4, 
                                                row_count=0, 
                                                header=['Stock', 'Ingredient', 'Delete', 'Edit'])
            # nutrient_table
            nutrient_table = self.create_table(column_count=2, 
                                            row_count=0, 
                                            header=['Nutrient', 'Value'])

            self.feed_store_ingredient_table=ingredient_table
            self.feed_store_nutrient_table=nutrient_table



            # Add tabs
            self.initUI()

        def initUI(self):

            tab_widget = QTabWidget(self)
            self.tab_widget=tab_widget
            formulation_tab = QWidget()
            saved_fomulation_tab = QWidget()
            feed_store_tab = QWidget()
            add_ingredient_tab = QWidget()
            analysis_tab = QWidget()
            

            tab_widget.setStyleSheet("background-color: #E7E0DE; ")

            tab_widget.addTab(add_ingredient_tab, "Add Ingredient")
            tab_widget.addTab(saved_fomulation_tab, "Saved Formulations")
            tab_widget.addTab(feed_store_tab, "Feed Store")
            tab_widget.addTab(formulation_tab, "Formulation")
        
            tab_widget.addTab(analysis_tab, "Analysis")
            tab_widget.setTabEnabled(4, False)
            tab_widget.setTabEnabled(3, False)
            font = QFont()
            font.setPointSize(16)  # Set font size
            self.tab_widget.setFont(font)


            self.formulation_tab_widgets(formulation_tab)
            self.feed_store_tab_widgets(feed_store_tab)
            self.add_ingredient_tab_widgets(add_ingredient_tab)
            self.analysis_tab_widgets(analysis_tab)
            self.fomulation_tab_widgets(saved_fomulation_tab)


            # Set vertical layout
            layout = QVBoxLayout(self)
            layout.addWidget(tab_widget)
            self.setLayout(layout)

        # Tab_WIDGETS

    # Add ingredient widgets
        def add_ingredient_tab_widgets(self, add_ingredient_tab):
            # ingridient_header=["Ingridient","Cost Per Unit", "Value"]
            nutrient_header=["Nutrient", "Value"]
            layout = QVBoxLayout(add_ingredient_tab)

            # Add_ingridient buttons
            button= self.container(w=200, h=100, color='rgb(192, 192, 190)')
            button_layout=QVBoxLayout(button)

            # Submit button
            submit_button = QPushButton("Save")
            submit_button.clicked.connect(lambda: self.save_data(nutrient_table=nutrient_table, cost=cost, ingredient=ingredient))
            button_layout.addWidget(submit_button)

            # Connect the save signal to the central controller
            submit_button.clicked.connect(self.central_controller.data_updated.emit)


            # forms
            card= self.container(w=400, h=100, color='rgb(192, 192, 192)')
            card_layout=QVBoxLayout(card)

            form= QFormLayout()

            validator = QDoubleValidator()
            validator.setBottom(0)

            ingredient=self.add_ingredient_ingredient=QLineEdit()
            cost=self.add_ingredient_cost=QLineEdit()
            
            cost.setValidator(validator)
            ingredient.setStyleSheet("background-color: rgb(192, 192, 192);")
            cost.setStyleSheet("background-color: rgb(192, 192, 192);")

            form.addRow("Ingredient", ingredient)
            form.addRow("Cost", cost)

            card_layout.addLayout(form)
            nutrient_table=self.add_ingredient_nutrient_table= self.create_table(column_count=2, row_count=len(self.nutrient_get()), header=nutrient_header)
            self.populate_nutrient(table=nutrient_table)
            # Set the delegate for the second column
            delegate = DoubleSpinBoxDelegate()
            nutrient_table.setItemDelegateForColumn(1, delegate)

            # header layoput 
            header_items=QWidget()
            header_layout=QHBoxLayout(header_items)
            header_layout.addWidget(card)
            header_layout.addWidget(button)

            layout.addWidget(header_items)

            layout.addWidget(nutrient_table)
            add_button_holder=self.container(w=80,h=50, color='green')
            add_button_holder_lay=QHBoxLayout(add_button_holder)
        # Add a button to trigger the row addition
            add_row_button = QPushButton("Add Row")
            add_row_button.setStyleSheet(
                "QPushButton {"
                "   border: none;"  # Remove border
                "   background-color: green;"  # Match container's background color
                "   color: black;"
                "   font-size: 16px;"  # Increase font size
                "}"
                "QPushButton:hover {"
                "   background-color: #5cb85c;}"  # Change background color on hover
            )
            add_row_button.clicked.connect(lambda: self.add_row_to_table(nutrient_table))
            add_button_holder_lay.addWidget(add_row_button)
            add_button_holder_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Connect to the nutrient table
            layout.addWidget(add_button_holder)
        def populate_nutrient(self, table):
            row_data=self.nutrient_get()
            for row, data in enumerate(row_data):
                item=QTableWidgetItem(data)
                table.setItem(row, 0, item)

        def add_row_to_table(self, nutrient_table):
            # Check if all rows are occupied
            for row in range(nutrient_table.rowCount()):
                item = nutrient_table.item(row, 0)
                if item is None or item.text() == "":
                    # There is at least one row not occupied, no need to add a new row
                    return

            # If all rows are occupied, add a new row
            current_row_count = nutrient_table.rowCount()
            nutrient_table.setRowCount(current_row_count + 1)

        def save_data(self, nutrient_table, cost, ingredient):
            # This is a placeholder method. Replace it with your actual save logic.
            save_ingredient_data(self, nutrient_table=nutrient_table, cost=cost, ingredient=ingredient)
            self.populate_nutrient(table=nutrient_table)


    # Feed store tab widgets
        def feed_store_tab_widgets(self, feed_store_tab):
                layout = QVBoxLayout(feed_store_tab)
                grid_layout = QGridLayout()


                ingredient_table= self.feed_store_ingredient_table
                ingredient_table.setMaximumHeight(math.floor(self.scaled_height*0.8))
                ingredient_table.setStyleSheet("background-color: #83C0C1;")
                self.populate_table(ingredient_table=ingredient_table)
                grid_layout.addWidget(ingredient_table, 0,0)


                self.central_controller.data_updated.connect(lambda: self.update_table(ingredient_table=self.feed_store_ingredient_table))
                n_container=self.container(w=500, h=math.floor(self.scaled_height*0.8), color='#83C0C1')
                n_layout= QVBoxLayout(n_container)

                nutrient_table=self.feed_store_nutrient_table
                nutrient_table.setMaximumHeight(300)
                n_layout.addWidget(nutrient_table)
                grid_layout.addWidget(n_container, 0, 1)



                button_container=self.container(w=100, h=100, color='rgb(192, 192, 192)')
                button_container_layout= QHBoxLayout(button_container)

                    # Add a Submit button to handle checked checkboxes
                submit_button = QPushButton("Submit")
                submit_button.clicked.connect(lambda: self.handle_checked_boxes(ingredient_table))
                button_container_layout.addWidget(submit_button)
                grid_layout.addWidget(button_container, 1,0)
                grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            
            

                layout.addLayout(grid_layout)
                layout.setAlignment(Qt.AlignmentFlag.AlignTop)



        def populate_table(self, ingredient_table):
            ingredients_data, _=get_data()
            ingredient_table.setRowCount(len(ingredients_data))
            for row, ingredients in enumerate(ingredients_data):
                # Container for the checkbox
                checkbox_container = QWidget()
                checkbox_container_layout = QHBoxLayout(checkbox_container)
                checkbox_container_layout.setContentsMargins(10, 0, 10, 0)  # Adjust the margins as needed

                # Checkbox
                checkbox_item = QCheckBox()
                checkbox_item.setChecked(False)  # Unchecked by default
                checkbox_container_layout.addWidget(checkbox_item)
                ingredient_table.setCellWidget(row, 0, checkbox_container)

                checkbox_item.setProperty('id', ingredients['id']) 

                # Ingredient name
                ingredient_name_item = QTableWidgetItem(ingredients["ingredient"])
                ingredient_name_item.setFlags(ingredient_name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                ingredient_table.setItem(row, 1, ingredient_name_item)

                # Delete button
                delete_button = MyButton(ingredients['id'], 'Delete', self)
                delete_button.clicked.connect(lambda _, row=row: self.delete_row(table= ingredient_table,model='Feed', row=row))
                ingredient_table.setCellWidget(row, 2, delete_button)

                # Edit button
                edit_button = MyButton(ingredients['id'],'Edit', self)
                edit_button.clicked.connect(lambda _, row=row: self.edit_row(row, ingredient_table=ingredient_table, nutrient_table=self.feed_store_nutrient_table))
                ingredient_table.setCellWidget(row, 3, edit_button)
                # Connect signals with a lambda function to include 'id'
            self.ingredient_table_cell_clicked(row=0, col=1)
            ingredient_table.cellClicked.connect(self.ingredient_table_cell_clicked)

            
        def delete_row(self, table, row, model, id=None):
            if id == None:
                sender = self.sender()
                id = sender.button_id
            model=globals()[model]
            object = get_object_or_404(model, id=id)
            object.delete()
            table.removeRow(row)

            self.central_controller.data_updated.emit()
        
            self.populate_analysis(tables=self.fomular_tables, result={})
            QMessageBox.warning( self, "deleted", "deleted")

        def edit_row(self, row, ingredient_table, nutrient_table):
            self.ingredient_table_cell_clicked(row=row, col=1)
            sender = self.sender()
            id = sender.button_id
            self.add_ingredient_ingredient.setText(ingredient_table.item(row, 1).text())

            for row in range(nutrient_table.rowCount()):
                nutrient=nutrient_table.item(row, 0).text()
                value=nutrient_table.item(row, 1).text()
                if nutrient != 'cost':
                    self.add_ingredient_nutrient_table.setItem(row, 0, QTableWidgetItem(nutrient))
                    self.add_ingredient_nutrient_table.setItem(row, 1, QTableWidgetItem(value))
                    
                else:
                    self.add_ingredient_cost.setText(value)
                    
            self.delete_row(ingredient_table,model='Feed', row=row, id=id)
            self.tab_widget.setCurrentIndex(0)  

        # signal handler
        def update_table(self, ingredient_table):
            # This method is called when the data_updated signal is emitted
            # Update the ingredient_table in the "Feed Store" tab here
            self.populate_table(ingredient_table=self.feed_store_ingredient_table)

        # signal handler

        def update_fomular(self):
            # When the signal is emitted, update the table with new data
            fomular_names, _ = get_fomulars()

            # Clear the existing table
            self.Fomular_table.setRowCount(len(fomular_names))

            # Populate the table with new data
            for row, (name, id) in enumerate(fomular_names.items()):
                item = QTableWidgetItem(name)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.Fomular_table.setItem(row, 0, item)
                # Delete button
                delete_button = MyButton(id, 'Delete', self)
                delete_button.clicked.connect(lambda _, row=row: self.delete_row(table= self.Fomular_table,model='Fomular', row=row))
                self.Fomular_table.setCellWidget(row, 1, delete_button)


        def ingredient_table_cell_clicked(self, row, col):
            # Retrieve the id of the clicked cell
            item = self.feed_store_ingredient_table.item(row, 1)
            # Assuming the id is stored in column 1
            if item:
                item=item.text()
                self.populate_nutrient_table(ingredient_name=item)



        def populate_nutrient_table(self, ingredient_name):
            _, nutrients_data = get_data()
            table = self.feed_store_nutrient_table
            for data in nutrients_data:
                if data['ingredient'] == ingredient_name:
                    table.setRowCount(len(data['nutrient']))
                    for row, (key, value) in enumerate(data['nutrient'].items()):
                        nutrient_item = QTableWidgetItem(key)
                        nutrient_item.setFlags(nutrient_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                        table.setItem(row, 0, nutrient_item)
                        nutrient_value = QTableWidgetItem(str(value))
                        nutrient_value.setFlags(nutrient_value.flags() & ~Qt.ItemFlag.ItemIsEditable)
                        
                        table.setItem(row, 1, nutrient_value)

            
        def handle_checked_boxes(self, ingredient_table):
            checked_ids_ingredient = self.collect_checked_ids(ingredient_table)
            # checked_ids_nutrient = self.collect_checked_ids(nutrient_table)

            nutrients, ingridients=fomulation_data(checked_ids_ingredient)
            self.populate_fomulation_tab(nutrients=nutrients, ingridients=ingridients)
            self.tab_widget.setTabEnabled(3, True)
            # print("Checked IDs (Nutrient):", checked_ids_nutrient)

        def collect_checked_ids(self, table):
            checked_ids = []
            for row in range(table.rowCount()):
                checkbox_container = table.cellWidget(row, 0)
                checkbox_item = checkbox_container.layout().itemAt(0).widget()
                if checkbox_item.isChecked():
                    checked_ids.append(checkbox_item.property('id'))
            return checked_ids    

    # Formulation tab widgets
        def formulation_tab_widgets(self, formulation_tab):
            layout = QVBoxLayout(formulation_tab)
            
            container=self.container(w=1000, h=500, color='#83C0C1')
            self.c_layout=QGridLayout(container)

            self.fomulation_ingredient_table=self.create_table(column_count=3, row_count=0, header=['Ingredient', 'Min%', 'Max%'])
            ingredient_table_layout=QVBoxLayout(self.fomulation_ingredient_table)

            self.fomulation_nutrient_table=self.create_table(column_count=3, row_count=0, header=['Nutrient', 'Min%', 'Max%'])
            nutrient_table_layout=QVBoxLayout(self.fomulation_nutrient_table)
            

        
            box=self.container(w=100, h=100, color='rgb(192, 192, 192)')
            box_lay= QVBoxLayout(box)
            fomulate_button = QPushButton("Fomulate")
            fomulate_button.clicked.connect(lambda: self.collect_fomulation_data())
            fomulate_button.setStyleSheet(
                "QPushButton {"
        
                
            
                "   color: black;"
                "   font-size: 14px;"  # Increase font size
                "}"
                )
            
            clear_button=QPushButton('Clear')
            clear_button.clicked.connect(lambda: self.clear_table( table_widget=self.fomulation_ingredient_table))
            clear_button.clicked.connect(lambda: self.clear_table( table_widget=self.fomulation_nutrient_table))

            box_lay.addWidget(fomulate_button)
            box_lay.addWidget(clear_button)
            self.c_layout.addWidget(self.fomulation_ingredient_table, 0,0)
            self.c_layout.addWidget(self.fomulation_nutrient_table, 0,1)
    
        

            layout.addWidget(container)
            layout.addWidget(box)
            layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    
        def populate_fomulation_tab(self, nutrients, ingridients):
            # Set the delegate for the second column
            delegate = DoubleSpinBoxDelegate()
            ingredient_table=self.fomulation_ingredient_table
            ingredient_table.setRowCount(len(ingridients))
            for row, ingredient in enumerate(ingridients):
                inredient_item=QTableWidgetItem(ingredient)
                inredient_item.setFlags(inredient_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                ingredient_table.setItem(row, 0, inredient_item)
                ingredient_table.setItemDelegateForColumn(1, delegate)
                ingredient_table.setItemDelegateForColumn(2, delegate)



            nutrient_table=self.fomulation_nutrient_table
            nutrient_table.setRowCount(len(nutrients))
            for row, nutrient in enumerate(nutrients):
                nutrient_item=QTableWidgetItem(nutrient)
                nutrient_item.setFlags(nutrient_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                nutrient_table.setItem(row, 0, nutrient_item)
                nutrient_table.setItemDelegateForColumn(1, delegate)
                nutrient_table.setItemDelegateForColumn(2, delegate)
            
        
            self.tab_widget.setCurrentIndex(3)

        def collect_fomulation_data(self):
            self.tab_widget.setTabEnabled(4, True)

            # Collect data from the ingredient table
            ingredient_data = []
            for row in range(self.fomulation_ingredient_table.rowCount()):
                ingredient_item = self.fomulation_ingredient_table.item(row, 0)
                max_percentage_item = self.fomulation_ingredient_table.item(row, 2)
                min_percentage_item = self.fomulation_ingredient_table.item(row, 1)

                ingredient = ingredient_item.text() if ingredient_item else ''
                max_percentage = float(max_percentage_item.text()) if max_percentage_item and max_percentage_item.text() else None
                min_percentage = float(min_percentage_item.text()) if min_percentage_item and min_percentage_item.text() else 0

                ingredient_data.append({'ingredient': ingredient, 'max': max_percentage, 'min': min_percentage})
            # Collect data from the nutrient table
            nutrient_data = {}
            for row in range(self.fomulation_nutrient_table.rowCount()):
                nutrient_item = self.fomulation_nutrient_table.item(row, 0)
                max_percentage_item = self.fomulation_nutrient_table.item(row, 2)
                min_percentage_item = self.fomulation_nutrient_table.item(row, 1)

                nutrient = nutrient_item.text() if nutrient_item else ''
                max_percentage = float(max_percentage_item.text()) if max_percentage_item and max_percentage_item.text() else None
                min_percentage = float(min_percentage_item.text()) if min_percentage_item and min_percentage_item.text() else 0

                nutrient_data[nutrient]={'max': max_percentage, 'min': min_percentage}


            result=prepare_fomulation_data(ingredient_data=ingredient_data, nutrient_data=nutrient_data)

            self.populate_analysis(result, self.analysis_tables, op=1)


        # Analysis widgets
        def analysis_tab_widgets(self, analysis_tab):
            layout = QVBoxLayout(analysis_tab)
            self.analysis_tables, scroll_area=self.shared_analysis()

            # self.populate_analysis()
            layout.addWidget(scroll_area)


        # Common Functions
        def container(self, w, color, h=None):
            widget= QWidget()
            if h: widget.setFixedSize(w, h)
            elif w: widget.setFixedWidth(w)
            widget.setStyleSheet(f"background-color:{color};")
            return widget
        
        def create_table(self, column_count, row_count, header):
            table = QTableWidget()
            table.setColumnCount(column_count)
            table.setRowCount(row_count)
            table.setHorizontalHeaderLabels(header)
            table.horizontalHeader().setStretchLastSection(True)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            table.setStyleSheet( """QTableWidget {
            border: 1px solid black;
            }
            QTableWidget::item {
            background-color: transparent; /* Set background color to transparent */
            border: 1px solid black;
            
            }
            QHeaderView::section {
            background-color: #83C0C1; /* Set background color of header row */
            }
            """)
            table.verticalHeader().setVisible(False)
            return table

    

        def populate_analysis(self, result, tables, op=0):

            if result:
                status=result['status']
                cost=result['cost']
                total_nutrient=result['total_nutrient']
                nutrient_requirements=result['nutrient_requirements']
                not_satisfied=result['not_satisfied']
                selected_ingredients=result['selected_ingridients']
            else:
                status=None
                cost=None
                total_nutrient={}
                nutrient_requirements={}
                not_satisfied={}
                selected_ingredients={}

            # Populate status_table
            self.populate_table_analysis(tables['status_table'], [('Optimal' if status == 1 else 'Infeasible', cost)
                                                    ])
        
    
        

            # Create data for the populate_table_analysis function
            data = []  # Header row

            for ingredient, values in selected_ingredients.items():
                row_data = [ingredient, values.get('ammount', ''), values.get('min', ''), values.get('max', '')]
                data.append(row_data)

            # Now, call the populate_table_analysis function
            self.populate_table_analysis(tables['ingredient_table'], data)

            # Populate nutrient_table
            nutrient_data = []
            for nutrient, value in total_nutrient.items():
                for n, v in nutrient_requirements.items():
                    if n == nutrient:
                        nutrient_data.append((nutrient, '', value, v['min'], v['max']))
            for nutrient, value in not_satisfied.items():
                for n, v in nutrient_requirements.items():
                    if n == nutrient:
                        nutrient_data.append(('', nutrient, value, v['min'], v['max']))
            self.populate_table_analysis(tables['nutrient_table'], nutrient_data)

            # Populate Total_nutrient_table
            total_nutrient_data = []
            for nutrient, value in total_nutrient.items():
                if nutrient not in ['min', 'max']:
                    for n, v in nutrient_requirements.items():
                        if n == nutrient:
                            total_nutrient_data.append((nutrient, value, v['min'], v['max']))
            self.populate_table_analysis(tables['Total_nutrient_table'], total_nutrient_data)

            # Populate recommedation_table
            recommendation_data = []
            if not_satisfied:
                for nutrient in not_satisfied.keys():
                    recommendation_data.append((f' {nutrient} ',))
            else:
                recommendation_data.append(('No Recommedation', 'Optimal' if status == 1 else 'Infeasible'))
            self.populate_table_analysis(tables['recommedation_table'], recommendation_data)
            if op==1:
                submit_container= self.container(w=200, h=100, color='rgb(192, 192, 190)')
                submit_container_layout=QVBoxLayout(submit_container)
                form=QFormLayout()

                name_holder=QLineEdit()
                form.addRow('Fomular Name', name_holder)
                save_button=QPushButton('Save Fomular')
                save_button.clicked.connect(lambda:self.save_fomular_result( result=result, name=name_holder.text()))

                submit_container_layout.addWidget(save_button)
                submit_container_layout.addLayout(form)

                tables['grid_layout'].addWidget(submit_container, 0,1)
                self.tab_widget.setCurrentIndex(4)


        def populate_table_analysis(self, table, data):
            table.setRowCount(len(data))
            for i, row_data in enumerate(data):
                for j, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    table.setItem(i, j, item)
        def save_fomular_result(self,name, result):
            status=save_fomular(self, name=name, result=result)  
            if status==1:
                self.central_controller.fomulation_updated.emit()
                QMessageBox.information(self, "Fomular Saved", "Fomular saved successfully!")

                

        def fomulation_tab_widgets(self, fomulation_tab):
            layout = QVBoxLayout(fomulation_tab)
            self.central_controller.fomulation_updated.connect( self.update_fomular)
            fomular_names,_=get_fomulars()
            self.Fomular_table=Fomular_table=self.create_table(column_count=2, row_count=len(fomular_names), header=[ 'Fomulars', 'delete'])
            Fomular_table.setMaximumHeight(200)
            Fomular_table.setMaximumWidth(400)
            Fomular_table.verticalHeader().setVisible(True)
        

            for row, (name, id) in enumerate(fomular_names.items()):
                item = QTableWidgetItem(name)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.Fomular_table.setItem(row, 0, item)
                # Delete button
                delete_button = MyButton(id, 'Delete', self)
                delete_button.clicked.connect(lambda _, row=row: self.delete_row(table= self.Fomular_table,model='Fomular', row=row))
                self.Fomular_table.setCellWidget(row, 1, delete_button)


            layout.addWidget(Fomular_table)
            self.fomular_tables, scroll_area=self.shared_analysis()
            # self.populate_analysis()
            Fomular_table.cellClicked.connect(self.get_fomular_data)
        


            # self.populate_analysis()
            layout.addWidget(scroll_area)
            
        def get_fomular_data(self, row, col):
            fomular=self.Fomular_table.item(row, 0).text()
            _, result=get_fomulars()
            result=result[fomular]
            self.populate_analysis(result=result, tables=self.fomular_tables)
            


        def group_box(self, title, table, height, width):
            group_box = QGroupBox(f'{title}', self)
            group_box.setMaximumHeight(height+200)
            group_box.setMaximumWidth(width)
            # Create a QVBoxLayout for the group box
            group_box_layout = QVBoxLayout(group_box)
            group_box_layout.addWidget(table)
            return group_box
        def shared_analysis(self):
            shared_widgets={}
            container=self.container(w=math.floor(self.scaled_width), h=900, color='#83C0C1')
            grid_layout=shared_widgets['grid_layout']=QGridLayout(container)

            status_table=self.create_table(column_count=2, row_count=0, header=[ 'Status', 'Cost'])
            status_table.setMaximumHeight(60)
            status_table.setMaximumWidth(300)
            shared_widgets['status_table']=status_table
            grid_layout.addWidget(status_table, 0,0)

            shared_widgets['ingredient_table']=ingredient_table=self.create_table(column_count=4, row_count=0, header=['Ingredient', 'Ammount', 'Min%', 'Max%' ])

            # Create a QGroupBox with a title
            ingredient_table_group_box=self.group_box(title='Ingredients', table=ingredient_table, height=200, width=440)
            grid_layout.addWidget(ingredient_table_group_box, 1,0)

            shared_widgets['nutrient_table']=nutrient_table=self.create_table(column_count=5, row_count=0, header=['Satisfied', 'Unsatisfied', 'Value', 'Min%', 'Max%' ])
        
            nutrient_table_group_box=self.group_box(title='Nutrients Achieved', table=nutrient_table, height=200, width=700)
            grid_layout.addWidget(nutrient_table_group_box, 1,1)
            
            shared_widgets['Total_nutrient_table']=Total_nutrient_table=self.create_table(column_count=4, row_count=0, header=['Nutrient', 'Ammount', 'Min%', 'Max%' ])
            Total_nutrient_table_group_box=self.group_box(title='Total Nutrients', table=Total_nutrient_table, height=200, width=450)
            grid_layout.addWidget(Total_nutrient_table_group_box, 2,0)
            
            recommedation_table=self.create_table(column_count=1, row_count=0, header=['Recommedation' ])
            recommedation_table.setMaximumHeight(200)
            recommedation_table.setMaximumWidth(600)
            recommedation_table_group_box=self.group_box(title='Recommedation', table=recommedation_table, height=200, width=600)
            grid_layout.addWidget(recommedation_table_group_box, 2,1)
            grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            shared_widgets['recommedation_table']=recommedation_table
            scroll_area = QScrollArea(self)
            scroll_area.setWidget(container)
            return shared_widgets, scroll_area
        def nutrient_get(self):
            nutrients_required=set()
            obj = Feed.objects.all()
            for feed_instance in obj:
                for ingridient, nutrients in feed_instance.ingridient_batch.items():
                    for nutrient, value in nutrients.items():
                        if nutrient != 'cost':
                            if is_unique(nutrient, nutrients_required):
                                nutrients_required.add(nutrient)
            if nutrients_required:
                return list(nutrients_required)
            else:
                return 10
        
        def clear_table(self, table_widget):
            # Clear editable cells 
            for row in range(table_widget.rowCount()):
                max_item = table_widget.item(row, 2)
                min_item = table_widget.item(row, 1)
                if max_item is not None:
                    max_item.setText("")

                if min_item is not None:
                    min_item.setText("")

    if __name__ == '__main__':
        app = QApplication([])
        scale_factor=0.8
        window = MainWindow()
        app.exec()
except Exception as e:
    show_dialog(f"{e}")







