# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Chooes the fruits you want in your custom smoothie!"
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on Smoothie will be: ", name_on_order)

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingrediants_list = st.multiselect('Choose upto 5 ingrediants:'
                                  , my_dataframe
                                 ,max_selections=5)

if ingrediants_list:
    
    ingrediants_string = ''
    
    for fruit_selected in ingrediants_list:
      
      ingrediants_string += fruit_selected + ' '

      search_on=pd_df. loc[pd_df ['FRUIT_NAME' ] == fruit_selected, 'SEARCH_ON'].iloc[0]
      st.write('The search value for ', fruit_selected,' is ', search_on, '.')

      st.subheader(fruit_selected + ' Nutrition Information')
      
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
      sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        
    #st.text(ingrediants_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingrediants_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:

        #st.write(my_insert_stmt)
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordred!', icon="✅") 



