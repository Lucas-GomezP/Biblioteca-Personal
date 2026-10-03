import streamlit as st
from utils import split_artists

def comp_editorial(book):
    if book["Editorial"]:
        st.markdown("**Editorial:**")
        if st.button(
            f"🏛️ {book['Editorial']}",
            key=f"editorial_{book['ISBN']}",
            width='stretch',
        ):
            st.session_state.selected_editorial = book["Editorial"]
            st.session_state.selected_isbn = None
            st.session_state.selected_artist = None
            st.session_state.selected_saga = None
            st.rerun()
    else:
        st.markdown("**Editorial:**")
        st.caption("Editorial desconocida")

def comp_artistas(book):
    if book["Artistas"]:
        st.markdown("**Artistas involucrados:**")
        artist_names = split_artists(book["Artistas"])

        artist_cols = st.columns(len(artist_names))

        for col, artist_name in zip(artist_cols, artist_names):
            with col:
                if st.button(
                    f"🎨 {artist_name}",
                    key=f"artist_{book['ISBN']}_{artist_name}",
                    width='stretch',
                ):
                    st.session_state.selected_artist = artist_name
                    st.session_state.selected_isbn = None
                    st.session_state.selected_saga = None
                    st.rerun()
    else:
        st.markdown("**Artistas involucrados:**")
        st.caption("Autoría desconocida")

def comp_saga(book):
    if book["Saga"]:
        st.markdown("**Saga:**")
        if st.button(
            f"📚 {book['Saga']}",
            key=f"saga_{book['ISBN']}",
            width='stretch'
        ):
            st.session_state.selected_saga = book["Saga"]
            st.session_state.selected_isbn = None
            st.rerun()
    else:
        st.markdown("**Saga:**")
        st.caption("No pertenece a ninguna saga")

def comp_layout_botones(book):
    col_artistas, col_editorial, col_saga = st.columns([1, 1, 1])
    with col_artistas:
        comp_artistas(book)
    with col_editorial:
        comp_editorial(book)
    with col_saga:
        comp_saga(book)


def comp_estado(book):
    STATUS_COLORS = {
        "Leido": "green",              # verde
        "Leyendo": "blue",             # azul
        "No leido": "red",            # rojo
        "Pensando si obtener": "gray", # gris
        "Deseado": "yellow",             # amarillo
    }
    estado = book["Estado"] or "Sin estado"
    st.badge(estado, color=STATUS_COLORS.get(estado, "#666666"), width='stretch')

def comp_titulo(book):
    st.markdown(f"### **{book['Titulo']}**")
    comp_estado(book)

def comp_ver_ficha(book):
    st.divider()
    if st.button(
        "📋 Ver ficha →",
        key=f"book_{book['ISBN']}",
        width='stretch',
    ):
        st.session_state.selected_isbn = book["ISBN"]
        st.rerun()

def comp_volver_catalogo():
    if st.button("← Volver al catálogo"):
        st.session_state.selected_saga = None
        st.session_state.selected_isbn = None
        st.session_state.selected_artist = None
        st.session_state.selected_editorial = None
        st.rerun()