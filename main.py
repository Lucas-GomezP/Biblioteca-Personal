
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="La Anti AntiBiblioteca de Lucas",
    page_icon="📖",
    layout="wide",
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

def split_artists(value):
    if not value:
        return []

    return [
        artist.strip()
        for artist in value.split(",")
        if artist.strip()
    ]

# ---------- ENCABEZADO ----------

st.image(
    "assets/header.jpg",
    width='stretch'
)
st.markdown("## Mi Anti AntiBiblioteca")
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

if selected_isbn is not None:
    selected = books[books["ISBN"] == selected_isbn]

    if selected.empty:
        st.session_state.selected_isbn = None
        st.rerun()

    book = selected.iloc[0]

    if st.button("← Volver al catálogo"):
        st.session_state.selected_isbn = None
        st.rerun()

    st.write("")
    st.caption("FICHA BIBLIOGRÁFICA")
    st.title(book["Titulo"])

    if book["Artistas"]:
        artist_names = split_artists(book["Artistas"])

        artist_cols = st.columns(len(artist_names))

        for col, artist_name in zip(artist_cols, artist_names):
            with col:
                if st.button(
                    artist_name,
                    key=f"detail_artist_{book['ISBN']}_{artist_name}",
                    width='stretch',
                ):
                    st.session_state.selected_artist = artist_name
                    st.session_state.selected_isbn = None
                    st.session_state.selected_saga = None
                    st.session_state.selected_editorial = None
                    st.rerun()
    else:
        st.caption("Autoría no especificada")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Información")
        st.write("**ISBN:**", book["ISBN"] or "—")
        if book["Editorial"]:
            if st.button(
                book["Editorial"],
                key=f"detail_editorial_{book['ISBN']}",
            ):
                st.session_state.selected_editorial = book["Editorial"]
                st.session_state.selected_isbn = None
                st.session_state.selected_artist = None
                st.session_state.selected_saga = None
                st.rerun()
        else:
            st.write("**Editorial:** —")
        st.write("**Año de publicación:**", book["Año de publicación"] or "—")
        estado = book["Estado"] or "Sin estado"
        color = STATUS_COLORS.get(estado, "#666666")

        st.markdown(
            f"""
            <div style="
                display:inline-block;
                background:{color};
                color:#111;
                padding:5px 12px;
                border-radius:4px;
                font-size:0.9rem;
                font-weight:600;
                margin-top:5px;
            ">
                {estado}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("#### Colección")
        if book["Saga"]:
            if st.button(
                book["Saga"],
                key=f"detail_saga_{book['ISBN']}",
                width='stretch'
            ):
                st.session_state.selected_saga = book["Saga"]
                st.session_state.selected_isbn = None
                st.session_state.selected_artist = None
                st.session_state.selected_editorial = None
                st.rerun()
        else:
            st.write("**Saga:** —")
        st.write("**Libros relacionados:**", book["Libros relacionados"] or "—")

    # Acceso directo a libros relacionados
    related = [
        title.strip()
        for title in book["Libros relacionados"].split(",")
        if title.strip()
    ]

    if related:
        st.divider()
        st.markdown("#### Explorar libros relacionados")

        for title in related:
            matches = books[
                books["Titulo"].str.casefold() == title.casefold()
            ]

            if not matches.empty:
                related_book = matches.iloc[0]

                if st.button(
                    f"↗ {related_book['Titulo']}",
                    key=f"related_{related_book['ISBN']}",
                ):
                    st.session_state.selected_isbn = related_book["ISBN"]
                    st.rerun()
            else:
                st.caption(f"Libro no encontrado en el catálogo: {title}")

    st.stop()

# ---------- SAGA ----------

if st.session_state.selected_saga is not None:

    saga_name = st.session_state.selected_saga

    if st.button("← Volver al catálogo"):
        st.session_state.selected_saga = None
        st.rerun()

    st.caption("SAGA")
    st.title(saga_name)

    saga_books = books[books["Saga"] == saga_name]

    st.caption(f"{len(saga_books)} libros")

    for _, book in saga_books.iterrows():

        col_info, col_button = st.columns([5, 1])

        with col_info:
            st.markdown(f"**{book['Titulo']}**")
            if book["Artistas"]:
                artist_names = split_artists(book["Artistas"])

                artist_cols = st.columns(len(artist_names))

                for col, artist_name in zip(artist_cols, artist_names):
                    with col:
                        if st.button(
                            artist_name,
                            key=f"detail_artist_{book['ISBN']}_{artist_name}",
                            width='stretch',
                        ):
                            st.session_state.selected_artist = artist_name
                            st.session_state.selected_isbn = None
                            st.session_state.selected_saga = None
                            st.rerun()
            else:
                st.caption("Autoría desconocida")

            estado = book["Estado"] or "Sin estado"
            color = STATUS_COLORS.get(estado, "#666666")

            st.markdown(
                f"""
                <span style="
                    background:{color};
                    color:#111;
                    padding:3px 8px;
                    border-radius:3px;
                    font-size:0.75rem;
                    font-weight:600;
                ">
                    {estado}
                </span>
                """,
                unsafe_allow_html=True,
            )

        with col_button:
            if st.button(
                "Ver ficha →",
                key=f"saga_book_{book['ISBN']}",
                width='stretch',
            ):
                st.session_state.selected_saga = None
                st.session_state.selected_isbn = book["ISBN"]
                st.rerun()

        st.divider()

    st.stop()





# ---------- ARTISTA ----------

if st.session_state.selected_artist is not None:

    artist_name = st.session_state.selected_artist

    if st.button("← Volver al catálogo"):
        st.session_state.selected_artist = None
        st.rerun()

    st.caption("ARTISTA")
    st.title(artist_name)

    artist_books = books[
        books["Artistas"].apply(
            lambda value: artist_name in split_artists(value)
        )
    ]

    st.caption(f"{len(artist_books)} obras en el catálogo")

    for _, book in artist_books.iterrows():

        col_info, col_button = st.columns([5, 1])

        with col_info:
            st.markdown(f"**{book['Titulo']}**")

            if book["Saga"]:
                if st.button(
                    book["Saga"],
                    key=f"detail_saga_{book['ISBN']}",
                    width='stretch'
                ):
                    st.session_state.selected_saga = book["Saga"]
                    st.session_state.selected_artist = None
                    st.session_state.selected_isbn = None
                    st.rerun()

            estado = book["Estado"] or "Sin estado"
            color = STATUS_COLORS.get(estado, "#666666")

            st.markdown(
                f"""
                <span style="
                    background:{color};
                    color:#111;
                    padding:3px 8px;
                    border-radius:3px;
                    font-size:0.75rem;
                    font-weight:600;
                ">
                    {estado}
                </span>
                """,
                unsafe_allow_html=True,
            )

        with col_button:
            if st.button(
                "Ver ficha →",
                key=f"artist_book_{book['ISBN']}",
                width='stretch',
            ):
                st.session_state.selected_artist = None
                st.session_state.selected_isbn = book["ISBN"]
                st.rerun()

        st.divider()

    st.stop()

# ---------- CATÁLOGO Y FILTROS ----------

st.title("Biblioteca")

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


# ---------- LISTA DE LIBROS DE LA EDITORIAL ----------

if selected_editorial is not None:
    editorial_books = books[
        books["Editorial"].str.casefold() == selected_editorial.casefold()
    ]

    if st.button("← Volver al catálogo"):
        st.session_state.selected_editorial = None
        st.rerun()

    st.write("")
    st.caption("EDITORIAL")
    st.title(selected_editorial)

    st.divider()

    if editorial_books.empty:
        st.info("No se encontraron libros de esta editorial.")
    else:
        for _, book in editorial_books.iterrows():
            col_info, col_button = st.columns([5, 1])

            with col_info:
                st.markdown(f"**{book['Titulo']}**")

                if book["Artistas"]:
                    artist_names = split_artists(book["Artistas"])

                    artist_cols = st.columns(len(artist_names))

                    for col, artist_name in zip(artist_cols, artist_names):
                        with col:
                            if st.button(
                                artist_name,
                                key=f"editorial_artist_{book['ISBN']}_{artist_name}",
                                width='stretch',
                            ):
                                st.session_state.selected_artist = artist_name
                                st.session_state.selected_editorial = None
                                st.session_state.selected_isbn = None
                                st.session_state.selected_saga = None
                                st.rerun()

                if book["Saga"]:
                    if st.button(
                        book["Saga"],
                        key=f"editorial_saga_{book['ISBN']}",
                        width='stretch'
                    ):
                        st.session_state.selected_saga = book["Saga"]
                        st.session_state.selected_editorial = None
                        st.session_state.selected_artist = None
                        st.session_state.selected_isbn = None
                        st.rerun()

                estado = book["Estado"] or "Sin estado"
                color = STATUS_COLORS.get(estado, "#666666")

                st.markdown(
                    f"""
                    <div style="
                        display:inline-block;
                        background:{color};
                        color:#111;
                        padding:5px 12px;
                        border-radius:4px;
                        font-size:0.9rem;
                        font-weight:600;
                        margin-top:5px;
                    ">
                        {estado}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_button:
                if st.button(
                    "Ver ficha →",
                    key=f"editorial_book_{book['ISBN']}",
                    width='stretch',
                ):
                    st.session_state.selected_isbn = book["ISBN"]
                    st.session_state.selected_editorial = None
                    st.rerun()

            st.divider()

    st.stop()
# ---------- LISTA CLICKEABLE ----------

if filtered.empty:
    st.info("No se encontraron libros con esos criterios.")
else:
    for _, book in filtered.iterrows():
        col_info, col_button = st.columns([5, 1])

        with col_info:
            st.markdown(f"**{book['Titulo']}**")
            if book["Artistas"]:
                artist_names = split_artists(book["Artistas"])

                artist_cols = st.columns(len(artist_names))

                for col, artist_name in zip(artist_cols, artist_names):
                    with col:
                        if st.button(
                            artist_name,
                            key=f"artist_{book['ISBN']}_{artist_name}",
                            width='stretch',
                        ):
                            st.session_state.selected_artist = artist_name
                            st.session_state.selected_isbn = None
                            st.session_state.selected_saga = None
                            st.rerun()
            else:
                st.caption("Autoría desconocida")

            if book["Saga"]:
                if st.button(
                    f"Saga: {book['Saga']}",
                    key=f"saga_{book['ISBN']}",
                    width='stretch'
                ):
                    st.session_state.selected_saga = book["Saga"]
                    st.session_state.selected_isbn = None
                    st.rerun()

        estado = book["Estado"] or "Sin estado"
        color = STATUS_COLORS.get(estado, "#666666")
        
        if book["Editorial"]:
            if st.button(
                book["Editorial"],
                key=f"editorial_{book['ISBN']}",
                width='stretch',
            ):
                st.session_state.selected_editorial = book["Editorial"]
                st.session_state.selected_isbn = None
                st.session_state.selected_artist = None
                st.session_state.selected_saga = None
                st.rerun()

        st.markdown(
            f"""
            <span style="
                background:{color};
                color:#111;
                padding:3px 8px;
                border-radius:3px;
                font-size:0.75rem;
                font-weight:600;
            ">
                {estado}
            </span>
            """,
            unsafe_allow_html=True,
        )

        with col_button:
            if st.button(
                "Ver ficha →",
                key=f"book_{book['ISBN']}",
                width='stretch',
            ):
                st.session_state.selected_isbn = book["ISBN"]
                st.rerun()

        st.divider()