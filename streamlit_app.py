import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

fruit_selection = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_display = my_fruit_list.loc[fruit_selection]

if fruits_to_display.size > 0:
  streamlit.dataframe(fruits_to_display)
 
def get_fruityvice_data(fruit):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


def get_fruit_load_list(my_cnx):
  with my_cnx.cursor() as cur:
    cur.execute("SELECT * from fruit_load_list")
    return cur.fetchall()
  
def add_fruit_to_load_list(my_cnx, fruit_to_add):
  with my_cnx.cursor() as cur:
    cur.execute(f"INSERT INTO fruit_load_list values('{fruit_to_add}')")
    return True
  

streamlit.header('Fruityvice Food Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like info about?')
  if not fruit_choice:
    streamlit.error("Please specify a fruit to get informatino about it")
  else:
    streamlit.write('The user entered: ' + fruit_choice)
    fruityvice_data = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_data)
except URLError as e:
  streamlit.error()
  
    
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list(my_cnx)
  streamlit.dataframe(my_data_rows)

fruit_to_add = streamlit.text_input('What fruit would you like into add to Load table?')
 
if streamlit.button('Add Fruit to Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list(my_cnx, fruit_to_add)
  streamlit.text("Thanks for adding: " + fruit_to_add)


