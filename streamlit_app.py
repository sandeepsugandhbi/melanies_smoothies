# Import python packages
import streamlit as st
import os

from snowflake.snowpark.functions import col

name_on_order = st.text_input('Name on Smoothie: ')
if name_on_order:
    st.write('The name on your Smoothie will be ', name_on_order)

    
# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!! :cup_with_straw: {st.__version__}")
st.write(
  """**Choose the fruits you want in your custom smoothie** """
)

#option = st.selectbox(
 #   "What is your favorite fruit?",
  #  ("Banana", "Strawberries", "Peaches")

#)


#st.write("You favorite fruit:", option)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select('FRUIT_NAME')
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
'Choose upto 5 ingredients: ', my_dataframe, max_selections=5
)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    #The += operator means "add this to what is already in the variable"
    #We never defined a variable named fruit_chosen, but Python understands that whatever 
    #is placed in that position is a counter for items in the list.
    #First version
    #for fruit_chosen in ingredients_list:
        #ingredients_string += fruit_chosen
        #st.write(ingredients_string)
    #st.write(ingredients_string)

    #Improved version
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        #st.write(ingredients_string)
        
    st.write(ingredients_string)

    #Insert  into table
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order )
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)
    time_to_instert = st.button('Submit Order')
    if time_to_instert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+ name_on_order +'!', icon="✅")

import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)


