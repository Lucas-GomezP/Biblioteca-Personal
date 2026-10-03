
import pandas as pd
import streamlit as st
from componentes import comp_editorial, comp_artistas, comp_saga, comp_layout_botones, comp_estado, comp_titulo, comp_ver_ficha, comp_volver_catalogo
from secciones import seccion_artistas, seccion_editorial, seccion_saga, seccion_ficha_libro
from utils import split_artists

st.set_page_config(
    page_title="La Anti AntiBiblioteca de Lucas",
    page_icon="📖",
    layout="centered",
)

# ---------- ESTILO ----------

st.markdown("""
<style>
    .stApp {
        background-color: #171715;
    }
    h1, h2, h3 {
        font-family: Georgia, serif;
    }
    div[data-testid="stButton"] button {
        border-radius: 3px;
        text-align: left;
    }
    .book-title {
        font-family: Georgia, serif;
        font-size: 1.2rem;
        font-weight: 600;
    }
    .muted {
        color: #aaa79d;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

STATUS_COLORS = {
    "Leido": "#4CAF50",              # verde
    "Leyendo": "#2196F3",             # azul
    "No leido": "#E53935",            # rojo
    "Pensando si obtener": "#808080", # gris
    "Deseado": "#F2C94C",             # amarillo
}

# ---------- DATOS ----------

@st.cache_data
def load_books():
    df = pd.read_csv(
        "libros.tsv",
        sep="\t",
        dtype=str,
        keep_default_na=False,
        encoding="utf-8-sig",
    )

    df.columns = df.columns.str.strip()

    required = [
        "ISBN", "Titulo", "Artistas", "Editorial",
        "Año de publicación", "Estado", "Saga",
        "Libros relacionados",
    ]

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(
            "Faltan columnas en libros.tsv: " + ", ".join(missing)
        )

    return df


try:
    books = load_books()
except Exception as e:
    st.error(f"No se pudo cargar el catálogo: {e}")
    st.stop()



# ---------- ENCABEZADO ----------

st.image(
    "assets/header.jpeg",
    width='stretch'
)
st.markdown("# Mi Anti AntiBiblioteca")
st.caption("BIBLIOTECA PERSONAL DE MI SER · CATÁLOGO DE LECTURAS")
st.divider()


# ---------- NAVEGACIÓN ----------

if "selected_isbn" not in st.session_state:
    st.session_state.selected_isbn = None
if "selected_saga" not in st.session_state:
    st.session_state.selected_saga = None
if "selected_artist" not in st.session_state:
    st.session_state.selected_artist = None
if "selected_editorial" not in st.session_state:
    st.session_state.selected_editorial = None
selected_isbn = st.session_state.selected_isbn
selected_editorial = st.session_state.selected_editorial

# ---------- FICHA DEL LIBRO ----------
seccion_ficha_libro(books)

# ---------- SAGA ----------
seccion_saga(books)

# ---------- ARTISTA ----------
seccion_artistas(books)

# ---------- EDITORIAL ----------
seccion_editorial(books)

# ---------- CATÁLOGO Y FILTROS ----------
with st.sidebar:
    st.header("Filtros")

    query = st.text_input(
        "Buscar",
        placeholder="Título, artista, ISBN...",
    ).casefold().strip()

    statuses = sorted(books["Estado"].loc[
        books["Estado"] != ""
    ].unique().tolist())

    editorials = sorted(books["Editorial"].loc[
        books["Editorial"] != ""
    ].unique().tolist())

    artists = sorted(
        {
            artist
            for value in books["Artistas"]
            for artist in split_artists(value)
        }
    )

    sagas = sorted(books["Saga"].loc[
        books["Saga"] != ""
    ].unique().tolist())

    status = st.selectbox("Estado", ["Todos"] + statuses)
    editorial = st.selectbox("Editorial", ["Todas"] + editorials)
    artist = st.selectbox("Artista", ["Todos"] + artists)
    saga = st.selectbox("Saga", ["Todas"] + sagas)

    order = st.selectbox(
        "Ordenar por",
        ["Título A-Z", "Título Z-A", "Año más reciente", "Año más antiguo"],
    )

filtered = books.copy()

if query:
    searchable = filtered[
        ["ISBN", "Titulo", "Artistas", "Editorial", "Saga"]
    ].agg(" ".join, axis=1).str.casefold()

    filtered = filtered[searchable.str.contains(query, regex=False)]

if status != "Todos":
    filtered = filtered[filtered["Estado"] == status]

if editorial != "Todas":
    filtered = filtered[filtered["Editorial"] == editorial]

if artist != "Todos":
    filtered = filtered[
        filtered["Artistas"].apply(
            lambda value: artist in split_artists(value)
        )
    ]

if saga != "Todas":
    filtered = filtered[filtered["Saga"] == saga]

if order == "Título A-Z":
    filtered = filtered.sort_values("Titulo", key=lambda s: s.str.casefold())
elif order == "Título Z-A":
    filtered = filtered.sort_values(
        "Titulo", key=lambda s: s.str.casefold(), ascending=False
    )
elif order == "Año más reciente":
    filtered = filtered.sort_values(
        "Año de publicación", ascending=False
    )
else:
    filtered = filtered.sort_values(
        "Año de publicación", ascending=True
    )

st.caption(f"{len(filtered)} libros encontrados")


# ---------- LISTA CLICKEABLE ----------

if filtered.empty:
    st.info("No se encontraron libros con esos criterios.")
else:
    for _, book in filtered.iterrows():
        comp_titulo(book)
        comp_layout_botones(book)
        comp_ver_ficha(book)

        st.divider()