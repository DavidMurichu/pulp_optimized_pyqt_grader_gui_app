from imports import *

from optimizer import feed_fomulate

# BackEnds


def check(num):
    if num == '' or num== None:
        return 0
    return float(num)

def data_check(str):
    try:
        if str.text() == '' or str.text() == None:
            return None
        return str
    except:
        return None

def save_ingredient_data(self, nutrient_table, ingredient, cost):
    data = {}
    nutrient_data={}
    nutrients_=set()

    # Get data from the form
    ingredient_value = ingredient.text().strip().lower()
    cost_value = cost.text()
    if ingridient_exist(ingredient_value):
        QMessageBox.warning(self, "Ingridient Exists", "Duplicate")
    else:
        # Iterate through rows of nutrient_table
        for row in range(nutrient_table.rowCount()):
            nutrient_item = data_check(nutrient_table.item(row, 0))
            value_item = data_check(nutrient_table.item(row, 1))

            if nutrient_item and value_item and is_unique(nutrient_item.text().strip().lower(), nutrients_):
                nutrient_name = nutrient_item.text().strip().lower()
                nutrients_.add(nutrient_name)
                if ingredient_value == nutrient_name:
                    nutrient_name=f'{nutrient_name}_n'
                value = value_item.text()
                nutrient_data[nutrient_name] = check(value)


        # Check if any data is missing
        if not nutrient_data or not ingredient_value or not cost_value:
            QMessageBox.warning(self, "Incomplete Data", "Please fill in all the data.")
            return

        # Store data in dictionaries
        try:
            nutrient_data["cost"] = float(cost_value)
        except:
            QMessageBox.warning(self, "Invalid Cost", "Please fill Correct data.")
            return 
        data[ingredient_value]=nutrient_data


        #Create a Feed instance and save it to the database
        feed_instance = Feed(ingridient_batch=data)
        feed_instance.save()
        # Clear the form fields and the table
        ingredient.clear()
        cost.clear()
        # Add 10 empty rows to the table
        nutrient_table.setRowCount(14)
        for row in range(nutrient_table.rowCount()):
            # Clear the first column (string input)
            nutrient_table.setItem(row, 0, QTableWidgetItem(""))

            # Clear the second column (numeric input)
            numeric_item = QTableWidgetItem("")
            numeric_item.setData(Qt.ItemDataRole.EditRole, None)  # Clear the numeric input
            nutrient_table.setItem(row, 1, numeric_item)
        # Show a success message
        QMessageBox.information(self, "Data Saved", "Data saved successfully!")
        

def get_data():
    feed_instances = Feed.objects.all()
    ingredients_data = []
    nutrients_data = []
    for feed_instance in feed_instances:
        for ingredient, nutrients in feed_instance.ingridient_batch.items():
            ingredients_data.append({
                'id': feed_instance.id,  # Add 'id' key here
                'ingredient': ingredient,
            })
        nutrients_data.append({
            'ingredient': ingredient,
            'nutrient': nutrients,
        })

    return ingredients_data, nutrients_data

 
nutrients_required=set()

def is_unique(value, my_set):
        return value.strip().lower() not in my_set 
def fomulation_data(selected_id):
    global obj
    nutrients_required=set()
    ingridients = []
    for id in selected_id:
        obj = get_object_or_404(Feed, id=int(id))
        for ingridient, nutrients in obj.ingridient_batch.items():
            ingridients.append(ingridient)
            # fomulate_data[ingridient]=nutrients
            for nutrient, value in nutrients.items():
                if nutrient != 'cost':
                    if is_unique(nutrient, nutrients_required):
                        nutrients_required.add(nutrient)
    return list(nutrients_required), ingridients


# ingredient exist checker 
        
def ingridient_exist(check_ingridient):
    feed_instances = Feed.objects.all()
    for feed_instance in feed_instances:
        for ingredient, nutrients in feed_instance.ingridient_batch.items():
        
            if ingredient == check_ingridient:
                return True          
    return False

def prepare_fomulation_data(ingredient_data, nutrient_data, id_name):
    fomulate_data={}
    nutrients_required=set()
    ingridients = []
    for id in id_name:
        obj = get_object_or_404(Feed, id=int(id))
        for ingridient, nutrients in obj.ingridient_batch.items():
            ingridients.append(ingridient)
            fomulate_data[ingridient]=nutrients
            for nutrient, value in nutrients.items():
                if nutrient != 'cost':
                    if is_unique(nutrient, nutrients_required):
                        nutrients_required.add(nutrient)
    for data in ingredient_data:
        for ingredient ,nutrients in fomulate_data.items():
            if data['ingredient']==ingredient:
                nutrients['max']=data['max']
                nutrients['min']=data['min']


    return feed_fomulate(nutrient_requirements=nutrient_data, ingredients_x=fomulate_data)



def save_fomular(self, name, result):
    if name!='' and result['final_data']:
        if result['status']== -1:
            return QMessageBox.information(self, "Infeasible", "Can not save infeasible fomulars")
        fomular={name:result}
        fomular_instance=Fomular(result=fomular)
        fomular_instance.save() 
        return 1


    return QMessageBox.information(self, "Empty Name", "Please recheck if Name is Set")

def get_fomulars():
    fomular_names={}
    fomulars={}
    queryset=Fomular.objects.all()
    for fomular_instance in queryset:

        result_data = fomular_instance.result
        id=fomular_instance.id
        for name, _ in result_data.items():
            fomular_names.update({name:id})      
        fomulars.update(result_data)
    return fomular_names, fomulars
