import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from PIL import Image
from wordcloud import WordCloud

def count_keywords() -> str:
    if "keywords" in st.session_state:
        keywords = st.session_state.keywords
        keywords.iloc[-50:].plot.barh(figsize=(8, 12), title=f'ICLR {st.session_state.year} Submission Top 50 Keywords')
        img_path = f"data/{st.session_state.year}-top50_keywords.png"
        plt.savefig(img_path, bbox_inches='tight', dpi=300)
        return img_path
    
    df = st.session_state.notes
    df['keywords'] = df['keywords'].apply(eval)

    data = df['keywords']
    keywords = {}
    for kw in data:
        kw = [_k.lower().strip() for _k in kw]
        for x in kw:
            # p = _k.split(";")
            # for x in p:
                if x in keywords.keys():
                    keywords[x] += 1
                else:
                    keywords[x] = 1
    
    # sort values
    keywords = {k: v for k, v in sorted(keywords.items(), key=lambda item: item[1])[::-1]}
    keywords = pd.Series(keywords).sort_values(ascending=True)
    keywords.iloc[-50:].plot.barh(figsize=(8, 12), title=f'ICLR {st.session_state.year} Submission Top 50 Keywords')
    st.session_state.keywords = keywords
    img_path = f"data/{st.session_state.year}-top50_keywords.png"
    plt.savefig(img_path, bbox_inches='tight', dpi=300)
    return img_path

def create_wordcloud() -> str:
    wc = WordCloud(background_color="black", max_words=300, max_font_size=64, width=1280, height=640, random_state=0)
    if "keywords" not in st.session_state:
        count_keywords()
    
    wc.generate_from_frequencies(st.session_state.keywords.to_dict())
    img_path = f"data/{st.session_state.year}-wordcloud.png"
    fig = plt.figure(figsize=(16, 8))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(img_path, bbox_inches='tight', dpi=200)

    return img_path


def extract_keywords(df: pd.DataFrame) -> set:
    data = df['keywords'].apply(eval)
    s = set()
    
    for kw in data:
        kw = [_k.lower().strip() for _k in kw]
        for _k in kw:
            p = _k.split(";")
            for x in p:
                if len(x) == 0:
                    continue
                if x[0] == " ":
                    x = x[1:]
                if x[-1] == ".":
                    x = x[:-1]
                s.add(x)
    
    return s

def button_clicked():
    csv_path = f"data/ICLR{option[4:]}.csv"
    
    notes = pd.read_csv(csv_path)
    notes.drop(columns=["id"], inplace=True)
    key_words = extract_keywords(notes)
    st.session_state.notes = notes
    st.session_state.filtered_notes = notes
    st.session_state.key_words = key_words
    st.session_state.columns = []

def multi_filtering():
    selected_columns = set(st.session_state.columns)
    df:pd.DataFrame = st.session_state.notes.copy()
    data = df['keywords'].apply(eval)
    new_data = pd.DataFrame()
    for i, kw in enumerate(data):
        kw = [_k.lower().strip() for _k in kw]
        
        if selected_columns.issubset(set(kw)):
            rec = df.iloc[i].T
            new_data = pd.concat([new_data, rec], axis=1)
        
    st.session_state.filtered_notes = new_data.transpose()
    st.session_state.is_pushed_reset = False

st.set_page_config(layout='wide')
st.title("Analysis of ICLR")

paper_tab, stat_tab = st.tabs(["papers", "statistics"])

with paper_tab:
    options = [f"ICLR{x}" for x in range(2024, 2020, -1)]
    option = st.selectbox(label='select the year', options=options)

    st.button('display the table', on_click=button_clicked)
    st.session_state.year = option[4:]

    st.session_state.is_pushed_reset = False

    if 'filtered_notes' in st.session_state:
        col1, col2 = st.columns((3, 1))
        with col1:
            selcted_columns = st.multiselect('choose the keyword', options=st.session_state.key_words, default=[], key="multiselect")
    
            if (not st.session_state.is_pushed_reset) and selcted_columns != st.session_state.columns:
                st.session_state.columns = selcted_columns
            
        with col2:
            st.button('filtering', on_click=multi_filtering)
        
        if st.button("reset"):
            button_clicked()
            st.session_state.is_pushed_reset = True

        if st.session_state.filtered_notes.shape[0] != 0:
            st.dataframe(st.session_state.filtered_notes)
            st.write(st.session_state.columns)
            st.write(st.session_state)
        else:
            st.write("<center> No hit </center>", unsafe_allow_html=True)
    

with stat_tab:
    try:
        st.dataframe(st.session_state.notes)
        container = st.container()
        col_keywords, col_wordcloud = st.columns((1, 1))
        with col_keywords:
            display_button = st.button("Display Top 50 Keywords")
        with col_wordcloud:
            wordcloud_button = st.button("Display Word Cloud")
        
        if display_button:
            st.session_state.img_path = count_keywords()
            img_path = st.session_state.img_path
            im = Image.open(img_path)
            container.image(im)
        
        elif wordcloud_button:
            st.session_state.img_path = create_wordcloud()
            img_path = st.session_state.img_path
            im = Image.open(img_path)
            container.image(im)
        
    except:
        st.write("No Data")