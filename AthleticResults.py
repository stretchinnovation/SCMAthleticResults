import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

import glob
files = glob.glob("PICKUP/ResultsData.csv")
#uploaded_file = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

if files:
    # Read raw lines from the first file
    with open(files[0], "rb") as f:
        lines = [line.decode("utf-8").strip().split(",") for line in f.readlines()]

    # Extract headers
    header1 = lines[0]   # row 1
    header2 = lines[2]   # row 3

    # Extract data
    data1 = [lines[1]]   # row 2 belongs to header1
    data2 = lines[3:6]    # rows after row 3 belong to header2

    # Build DataFrames
    df1 = pd.DataFrame(data1, columns=header1)
    df2 = pd.DataFrame(data2, columns=header2)

    # --- Build single string from df1 ---
    # Specify the order of fields you want
    df1.columns = df1.columns.str.strip()

    # Allocate each field into its own string variable
    round = str(df1.iloc[0]["Round"])
    heat = str(df1.iloc[0]["Heat"])
    gender = str(df1.iloc[0]["Gender"])
    age = int(df1.iloc[0]["Age"])
    item = str(df1.iloc[0]["Item"])
else:
    st.error("No CSV files found in PICKUP/")
    
if round == "F":
    round = "FINAL"
else: 
    round = "HEAT "+heat

if age < 20:
    age = "U19"
elif age in range (20,30):
    age = "SENIOR"
else: 
    age = "MASTERS" #+str(age)

# Now you can build your head string in any order you like
head = f"{round} {age} {gender} {item}"

# Display the string instead of the DataFrame
#st.subheader("Header Row 1 Data")
#st.write(head)

# Specify which columns you want to show
columns_to_show = ["Place", "Surname", "Firstname", "Number", "Team", "Performance"]
#st.dataframe(df2[columns_to_show])

# Load Poppins font globally
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
    <style>
    .custom-subheader {
        font-family: 'Poppins', sans-serif;
        font-size: 1.5em;
        font-weight: 600;
        text-transform: uppercase;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    </style>
    """,
    unsafe_allow_html=True
) 
st.markdown(
    """
    <style>
    .stApp {
        background-color: #00000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create a Styler with transparent backgrounds
styled = (
    df2[columns_to_show]
    .style
    .hide(axis="index")
    .set_table_styles(
        [
            # Table dimensions
            {"selector": "table", "props": [
                ("width", "100vw"),
                ("max-height", "240px"),
                ("margin", "0 auto"),
                ("padding", "0px 0px"),
                ("border-collapse", "collapse")  # ensure borders collapse
            ]},
            # Header styling (no borders)
            {"selector": "th", "props": [
                ("font-family", "Poppins"),
                ("font-weight", "bold"),
                ("background-color", "#00000000"),
                ("text-transform", "uppercase"),
                ("margin", "0 auto"),
                ("padding", "0px 30px"),
                ("border", "none"),
                ("font-size", "18px"),
                ("white-space", "nowrap")  # prevent wrapping in headers
            ]},
            # Cell styling (no borders)
            {"selector": "td", "props": [
                ("font-family", "Poppins"),
                ("text-transform", "uppercase"),
                ("background-color", "#00000000"),
                ("margin", "0 auto"),
                ("padding", "6px 30px"),
                ("border", "none"),
                ("font-size", "18px"),
                ("white-space", "nowrap")  # prevent wrapping in headers
            ]},
            # Force fixed widths with !important
            {"selector": "td.col0, th.col0", "props": [
                ("text-align", "center"),
                ("width", "60px !important"),
                ("padding", "0px 30px"),
            ]},
            {"selector": "td.col1, th.col1", "props": [
                ("text-align", "left"),
                ("width", "auto"),
                ("padding", "0px 30px"),
            ]},
            {"selector": "td.col2, th.col2", "props": [
                ("text-align", "left"),
                ("width", "auto"),
                ("padding", "0px 30px"),
            ]},
            {"selector": "td.col3, th.col3", "props": [
                ("text-align", "center"),
                ("text-align", "center"),
                ("width", "100px !important"),
                ("padding", "0px 30px"),
            ]},
            {"selector": "td.col4, th.col4", "props": [
                ("text-align", "center"),
                ("text-align", "center"),
                ("width", "100px !important"),
                ("padding", "0px 30px"),
            ]},
            {"selector": "td.col5, th.col5", "props": [
                ("text-align", "center"),
                ("text-align", "center"),
                ("width", "100px !important"),
                ("padding", "0px 30px"),
            ]},
            # Alignment overrides
            {"selector": "td.col0", "props": [("text-align", "center")]}, # Place
            {"selector": "td.col3", "props": [("text-align", "center")]}, # Number
            {"selector": "td.col4", "props": [("text-align", "center")]}, # Team
            {"selector": "td.col5", "props": [("text-align", "center")]}, # Performance
        ]
    )
)
# Inject CSS for centering
st.markdown(
    """
    <style>
    /* Center the RESULTS div in the page */
    #RESULTS {
        display: flex;
        justify-content: left;   /* horizontal center */
        align-items: top;       /* vertical center */
        flex-direction: column;    /* stack header + table */
        min-height: 100vh;         /* take full viewport height */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Render header
st.markdown(
    f"""
    <div id="RESULTS">
        <div class="custom-subheader">{head}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Render the styled table
html_table = styled.to_html()
components.html(html_table, height=800, scrolling=True)

