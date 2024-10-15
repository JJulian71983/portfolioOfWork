import streamlit as st
import json

# Page Configurations, Titles, Headings
st.set_page_config(page_title="Econ Games", layout="wide", initial_sidebar_state="auto")

if not st.session_state["auth_passed"]:
    st.switch_page("pages/1_Login.py")
else:
    st.title(body=r"$\text{\Large Tobacco\ Market\ of\ 1690}$")
if "quantity" not in st.session_state:
    st.session_state["quantity"] = 0
if "counter" not in st.session_state:
    st.session_state["counter"] = 0
st.session_state["counter"] += 1

with st.sidebar:
    st.page_link(page="home.py", label="Home", use_container_width=False)
    st.page_link(page="pages/3_Prisoners_Dilemma.py", label="Prisoner\'s Dilemma", use_container_width=False)
    if st.button(label="Logout", key="logout", on_click=None, use_container_width=False):
        st.session_state["disconnect"] = True
        st.switch_page("home.py")
with st.popover(label="Rules"):
    st.write("1) Each team will select a quantity amount between 0 and 100 units.")
team, messages = st.columns(spec=[0.08, 0.92])
with team:
    if st.session_state["teamName"] == "team1":
        quantity1_input = st.number_input(label="Team 1 Quantity", min_value=0, max_value=100, value="min", step=1, format="%i")
        game_inputs = {
            "team": 1,
            "inputs": {
                "round": st.session_state["counter"],
                "quantity": quantity1_input
            }
        }
        f = open("C:\\Anaconda\\Projects\\tobaccoMarket\\game_inputs.json", "a")
        f.write(json.dumps(obj=game_inputs))
        f.close()
    if st.session_state["teamName"] == "team2":
        quantity2_input = st.number_input(label="Team 2 Quantity", min_value=0, max_value=100, value="min", step=1, format="%i")
        game_inputs = {
            "team": 2,
            "inputs": {
                "round": st.session_state["counter"],
                "quantity": quantity2_input
            }
        }
        f = open("C:\\Anaconda\\Projects\\tobaccoMarket\\game_inputs.json", "a")
        f.write(json.dumps(obj=game_inputs))
        print(f)
        f.close()
    if st.session_state["teamName"] == "jjulian71983":
        admin1_input = st.number_input(label="Team 1 Quantity", min_value=0, max_value=100, value="min", step=1, format="%i")
        admin2_input = st.number_input(label="Team 2 Quantity", min_value=0, max_value=100, value="min", step=1, format="%i")
submit_button = st.button(label="Submit")

# User inputs
team1_quantity = admin1_input
team2_quantity = admin2_input
equilibrium_quantity = 135
equilibrium_price = 0.48

# Random economic shocks
drought = False
disease = False
war = False
increase_preference = False
political_favor = False
negative_cost_shocks = [drought, disease, war]
positive_price_shocks = [increase_preference, political_favor]

# Price and quantity variables
quantity_supplied = team1_quantity + team2_quantity
print("Quantity supplied: " + str(quantity_supplied))
if quantity_supplied == 0:
    team1_weight = 0
    team2_weight = 0
else:
    team1_weight = team1_quantity / quantity_supplied
    team2_weight = team2_quantity / quantity_supplied
if quantity_supplied < equilibrium_quantity:
    team1_sold_quantity = team1_quantity
    team2_sold_quantity = team2_quantity
else:
    team1_sold_quantity = round(equilibrium_quantity * team1_weight, 0)
    print("Team 1 sold quantity: " + str(team1_sold_quantity))
    team2_sold_quantity = round(equilibrium_quantity * team2_weight, 0)
    print("Team 2 sold quantity: " + str(team2_sold_quantity))

# Revenue variables
if True in positive_price_shocks:
    equilibrium_price = equilibrium_price + 0.2
else:
    pass
team1_revenue = round(equilibrium_price * team1_sold_quantity, 2)
print("Team 1 revenue: " + str(team1_revenue))
team2_revenue = round(equilibrium_price * team2_sold_quantity, 2)
print("Team 2 revenue: " + str(team2_revenue))

# Cost variables
fixed_costs = 1
if True in negative_cost_shocks:
    fixed_costs = fixed_costs + 8
else:
    pass
variable_costs = 0.0044
team1_cost = round(fixed_costs + (variable_costs * (team1_quantity * team1_quantity)), 2)
print("Team 1 cost: " + str(team1_cost))
team2_cost = round(fixed_costs + (variable_costs * (team2_quantity * team2_quantity)), 2)
print("Team 2 cost: " + str(team2_cost))

# Profit variables
team1_profit = round(team1_revenue - team1_cost, 2)
print("Team 1 profit: " + str(team1_profit))
team2_profit = round(team2_revenue - team2_cost, 2)
print("Team 2 profit: " + str(team2_profit))
if submit_button:
    st.write("Team 1 profit: " + str(team1_profit))
    st.write("Team 1 revenue: " + str(team1_revenue))
    st.write("Team 1 cost: " + str(team1_cost))
    st.write("Team 1 sold quantity: " + str(team1_sold_quantity))
    st.write("Team 2 profit: " + str(team2_profit))
    st.write("Team 2 revenue: " + str(team2_revenue))
    st.write("Team 2 cost: " + str(team2_cost))
    st.write("Team 2 sold quantity: " + str(team2_sold_quantity))
