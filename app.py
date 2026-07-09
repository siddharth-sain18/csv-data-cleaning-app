import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI/ML PROJECT-1", page_icon="📊", layout="wide")

st.markdown("""
<style>
            
.stApp{
    background-color: var(--background-color);
    color: var(--text-color);
}
            
div[data-testid="stVerticalBlock"] > div:has(div.stDataFrame){
    background-color: var(--secondary-background-color);
    color: var(--text-color);
    padding:20px;
    border-radius:12px;
    box-shadow:0 4px 10px rgba(0,0,0,0.15);
    margin-bottom:20px;
}

h1{
    color: var(--text-color);
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-weight:700;
}

h2,h3,h4,h5,h6{
    color: var(--text-color);
}

section[data-testid="stSidebar"]{
    background-color:#0f172a !important;
}

section[data-testid="stSidebar"] *{
    color:#f8fafc !important;
}

.stMarkdown,
.stText,
.stDataFrame,
.stTable,
label,
p,
span,
div{
    color: inherit !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"]{
    color: inherit !important;
}

.stSelectbox label{
    color: inherit !important;
}

[data-testid="stFileUploader"] label{
    color: inherit !important;
}

[data-testid="stDataFrame"]{
    color: inherit !important;
}

button[data-baseweb="tab"]{
    color: inherit !important;
    font-weight:600;
}

.stButton>button,
.stDownloadButton>button{
    border-radius:8px;
    width:100%;
}

[data-testid="stAlert"]{
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)
numeric_col = []

def scatter(df):
    xaxis=st.sidebar.selectbox("SELECT X-AXIS:",numeric_col)
    yaxis=st.sidebar.selectbox("SELECT Y-AXIS:",numeric_col)
    fig, ax = plt.subplots()
    ax.scatter(df[xaxis], df[yaxis], color='#1e3a8a', alpha=0.7, edgecolors='w')
    ax.set_xlabel(xaxis)
    ax.set_ylabel(yaxis)
    ax.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig)
    plt.close(fig)

def barplot(df):
    xaxis=st.sidebar.selectbox("SELECT X-AXIS:",numeric_col)
    yaxis=st.sidebar.selectbox("SELECT Y-AXIS:",numeric_col)
    fig, ax = plt.subplots()
    ax.bar(df[xaxis], df[yaxis], color='#3b82f6', edgecolor='none')
    ax.set_xlabel(xaxis)
    ax.set_ylabel(yaxis)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    st.pyplot(fig)
    plt.close(fig)

def lineplot(df):
    xaxis=st.sidebar.selectbox("SELECT X-AXIS:",numeric_col)
    yaxis=st.sidebar.selectbox("SELECT Y-AXIS:",numeric_col)
    fig, ax = plt.subplots()
    ax.plot(df[xaxis], df[yaxis], color='#10b981', linewidth=2, marker='o')
    ax.set_xlabel(xaxis)
    ax.set_ylabel(yaxis)
    ax.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig)
    plt.close(fig)

def histogram(df):
    xaxis=st.sidebar.selectbox("SELECT X-AXIS:",numeric_col)
    fig, ax = plt.subplots()
    ax.hist(df[xaxis], bins=20, color='#6366f1', edgecolor='white')
    ax.set_xlabel(xaxis)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    st.pyplot(fig)
    plt.close(fig)

def showdata(df):
    st.dataframe(df, use_container_width=True)

def dropnull(df):
    df=df.dropna()
    return df

def afternull(df):
    st.markdown("---")
    st.subheader("✨ DATA AFTER CLEANING")
    st.dataframe(df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Dimensions (Rows × Columns)", value=f"{df.shape[0]} × {df.shape[1]}")
    
    nullCount=df.isnull().sum().sum()
    if nullCount<1:
        with col2:
            st.success("NO NULL VALUES FOUND")

def dropdupl(df):
    st.sidebar.markdown("### 🔀 Duplicate Settings")
    dropCol=st.sidebar.multiselect("CHOOSE COLUMNS FOR DUPLICATE VALUES GROUP ANALYSIS: ",df.columns)
    if len(dropCol)>0:
        beforedrop=df.shape[0]
        df = df.drop_duplicates(subset=dropCol)
        afterdrop=df.shape[0]
        if afterdrop==beforedrop:
            st.sidebar.info("NO DUPLICATES FOUND")
        else:
            st.sidebar.success("Logical duplicates removed based on selected columns")
            if st.button("CLICK HERE TO SHOW DATASET AFTER DROP DUPLICATES...."):
                showdata(df)
    else:
        st.sidebar.warning("Select at least one column")
    return df

def showdupl(df):
    st.markdown("---")
    showCol=st.multiselect("CHOOSE COLUMNS FOR DUPLICATE VALUES GROUP ANALYSIS: ",df.columns)
    if len(showCol)>0:
        dupdata= df[df.duplicated(subset=showCol,keep=False)]
        if len(dupdata)>0:
            st.subheader("🔍 DUPLICATED ROWS ARE: ")
            st.dataframe(dupdata, use_container_width=True)
        else:
            st.info("NO duplicates FOUND based on selected columns")
    else:
        st.warning("Select at least one column")

st.title("📊 CSV DATA CLEANING APPLICATION")
st.markdown("Upload your datasets, clean missing entries, eliminate duplicates, and visualize instantly.")

uploadedFile=st.file_uploader("UPLOAD YOUR CSV FILE", type=["csv"])

if uploadedFile is not None:
    try:
        df=pd.read_csv(uploadedFile,encoding='utf-8')
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        st.stop()
    numeric_col=df.select_dtypes(include=np.number).columns
    
    tab1, tab2 = st.tabs(["📋 Dataset Overview", "📈 Data Visualization"])
    
    with tab1:
        st.header("Current Dataset Status")
        st.dataframe(df, use_container_width=True)
        
        m1, m2 = st.columns(2)
        with m1:
            st.metric(label="Original Dimensions (Rows × Columns)", value=f"{df.shape[0]} × {df.shape[1]}")
        
        nullCount=df.isnull().sum().sum()
        if nullCount<1:
            with m2:
                st.success("NO NULL VALUES FOUND")
        else:
            with m2:
                st.warning(f"⚠️ Total Missing Values: {nullCount}")
            
            st.sidebar.markdown("### 🛠️ Null Value Handling")
            nullvalue=st.sidebar.selectbox("WHAT TO DO FOR NULL VALUES: ",["-- Select an option --","DROP THE ROWS","FILL WITH MEAN","FILL WITH MEDIAN","FILL WITH MODE"],index=0)
            
            match nullvalue:
                case "DROP THE ROWS":
                    df=dropnull(df)
                case "FILL WITH MEAN":
                    df=df.fillna(df.mean(numeric_only=True))
                case "FILL WITH MEDIAN":
                    df=df.fillna(df.median(numeric_only=True))
                case "FILL WITH MODE":
                    df=df.fillna(df.mode().iloc[0])
            
            if nullvalue!="-- Select an option --":
                afternull(df)
        
        st.sidebar.markdown("### 👥 Duplicate Value Handling")
        duplvalue=st.sidebar.selectbox("WHAT TO DO FOR DUPLICATE VALUES: ",["-- Select an option --","DROP THE DUPLICATE ROWS","SHOW THE DUPLICATE ROWS"],index=0)
        match duplvalue:
            case "DROP THE DUPLICATE ROWS":
               df=dropdupl(df)
            case "SHOW THE DUPLICATE ROWS":
                showdupl(df)

        st.markdown("---")
        st.subheader("📥 Export Cleaned Dataset")
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="🚀 Download Cleaned CSV",
            data=csv_data,
            file_name="cleaned_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    with tab2:
        if duplvalue=="DROP THE DUPLICATE ROWS":
            st.header("Visual Analytics Engine")
            st.sidebar.markdown("### 📊 Presentation Settings")
            plotselection=st.sidebar.selectbox("SELECT TYPE OF PLOT: ",["-- Select an option --","SCATTER PLOT","BAR PLOT","LINE PLOT","HISTOGRAM"],index=0)
            
            if plotselection != "-- Select an option --":
               
                with st.container():
                    st.markdown(f"### Visualizing: {plotselection}")
                    match plotselection:
                        case "SCATTER PLOT":
                            scatter(df)
                        case "BAR PLOT":
                            barplot(df)
                        case "LINE PLOT":
                            lineplot(df)
                        case "HISTOGRAM":
                            histogram(df)
            else:
                st.info("Select a plot option from the sidebar configuration panel to view visualizations.")
        else:
            st.info("Please select 'DROP THE DUPLICATE ROWS' processing step to activate the Visualizations suite.")
