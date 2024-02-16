from imports import *

#OPTIMIZER
def Round(num):
    if num != None and num != '':
        return round(num, 4)
    return num





def feed_fomulate(nutrient_requirements, ingredients_x):
    total_nutrient = {}
    not_satisfied = {}
    selected_ingridients={}


    # Convert data into NumPy arrays
    costs = np.array([ingredients_x[ingredient]['cost'] for ingredient in ingredients_x])


    nutrient_content = np.array([[ingredients_x[ingredient].get(nutrient, 0) for nutrient in nutrient_requirements] for ingredient in ingredients_x])

    # Define the problem
    prob = LpProblem("Least_Cost_Feed_Formulation", LpMinimize)


    # Define the decision variables (amount of each ingredient)
    amounts = LpVariable.dicts("Amount", ingredients_x, lowBound=0, cat='Continuous')


    # Define the objective function (cost minimization)
    prob += lpSum(costs * [amounts[i] for i in ingredients_x]), "Total_Cost"

    def check(num):
        if num==None:
            return 0
        else:
            return num
    # Add minimum and maximum requirements for each ingredient
    for ingredient in ingredients_x:
        min_amount = check(ingredients_x[ingredient]['min'])
        max_amount = ingredients_x[ingredient]['max']


        # Min constraint
        if min_amount is not None:
            prob += amounts[ingredient] >= (min_amount)/100, f"{ingredient}_min"

        # Max constraint (if not None)
        if max_amount is not None:
            prob += amounts[ingredient] <= (max_amount)/100, f"{ingredient}_max"


    # Add nutrient constraints
    for idx, nutrient in enumerate(nutrient_requirements):
        min_value = check(nutrient_requirements[nutrient]['min'])
        max_value = nutrient_requirements[nutrient]['max']

        # Min constraint
        if min_value is not None:
            prob += lpSum(nutrient_content[:, idx] * [amounts[i] for i in ingredients_x]) >= (min_value), f"{nutrient}_min"

        # Max constraint (if not None)
        if max_value is not None:
            prob += lpSum(nutrient_content[:, idx] * [amounts[i] for i in ingredients_x]) <= (max_value), f"{nutrient}_max"


    prob += lpSum(amounts[i] for i in ingredients_x) == 1, "Total_Quantity_Constraint"

    # path=r"C:\Users\Felix Mokaya\Downloads\Cbc-2.10-win64-msvc15-mdd\bin\cbc.exe"
    path='/usr/bin/cbc'
    
    # Solve the problem
    status = prob.solve(COIN_CMD(msg=False, path=path))



    # Print the optimal amounts of each ingredient for feasible solutions
    for ingredient in ingredients_x:
        if amounts[ingredient].varValue !=0:
            ingredient_value=ingredients_x[ingredient]
            ingredient_value['ammount']=Round((amounts[ingredient].varValue)*100)
            selected_ingridients[ingredient]=ingredient_value

        


    total_dict = Counter()
    for key, ratio_value in selected_ingridients.items():
        ratio_value=ratio_value['ammount']
        inner_dict = ingredients_x.get(key, {})  # Get the inner dictionary based on the key, or use an empty dictionary if not found
        multiplied_dict = {k: v * ratio_value/100 if v is not None else 0 for k, v in inner_dict.items()}
        total_dict += Counter(multiplied_dict)

    total_dict = Counter({k: round(v, 4) for k, v in total_dict.items()})
    
    # Calculate total nutrient values and check if they meet requirements
    for nutrient in nutrient_requirements:
        nutrient_values = np.array([ingredients_x[i].get(nutrient, 0) * amounts[i].varValue if amounts[i].varValue is not None else 0 for i in ingredients_x])
        total_value = np.sum(nutrient_values)
        # Check if the nutrient values satisfy the requirements
        min_value = nutrient_requirements[nutrient]['min']
        max_value = nutrient_requirements[nutrient]['max']


        if min_value is not None and max_value is not None:
            if min_value <= total_value <= max_value:
                total_nutrient[nutrient] = Round(total_value)
            else:
                not_satisfied[nutrient] = Round(total_value)
        elif min_value is not None:
            if min_value <= total_value:
                total_nutrient[nutrient] = Round(total_value)
            else:
                not_satisfied[nutrient] = Round(total_value)
        elif max_value is not None:
            if total_value <= max_value:
                total_nutrient[nutrient] = Round(total_value)
            else:
                not_satisfied[nutrient] = Round(total_value)
        



    # return the context with total nutrient values
    
    context = {
        'final_data':dict(total_dict),
        'total_nutrient': total_nutrient,
        'not_satisfied': not_satisfied,
        'status': status,
        'nutrient_requirements':nutrient_requirements,
        'selected_ingridients':selected_ingridients,
        'cost':Round(value(prob.objective))
    }
    return context
