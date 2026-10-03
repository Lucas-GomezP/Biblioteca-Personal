import streamlit as st
from componentes import comp_volver_catalogo, comp_titulo, comp_layout_botones, comp_ver_ficha, comp_artistas, comp_editorial, comp_saga, comp_estado
from utils import split_artists

def seccion_artistas(books):
    if st.session_state.selected_artist is not None:
        artist_name = st.session_state.selected_artist
        comp_volver_catalogo()
        st.title(artist_name)
        artist_books = books[
            books["Artistas"].apply(
                lambda value: artist_name in split_artists(value)
            )
        ]
        col_cat, col_info = st.columns([1, 2])
        with col_cat:
            st.caption("ARTISTA")
        with col_info:
            st.caption(f"{len(artist_books)} obras en el catálogo")

        st.divider()
        
        for _, book in artist_books.iterrows():
            comp_titulo(book)
            comp_layout_botones(book)
            comp_ver_ficha(book)
            st.divider()
        st.stop()

def seccion_saga(books):
    if st.session_state.selected_saga is not None:
        saga_name = st.session_state.selected_saga
        comp_volver_catalogo()
        st.title(saga_name)
        saga_books = books[books["Saga"] == saga_name]

        col_cat, col_info = st.columns([1, 2])
        with col_cat:
            st.caption("SAGA")
        with col_info:
            st.caption(f"{len(saga_books)} libros en el catálogo")

        st.divider()

        for _, book in saga_books.iterrows():
            comp_titulo(book)
            comp_layout_botones(book)
            comp_ver_ficha(book)
            st.divider()

        st.stop()

def seccion_editorial(books):
    if st.session_state.selected_editorial is not None:
        editorial_name = st.session_state.selected_editorial
        comp_volver_catalogo()
        st.title(editorial_name)
        editorial_books = books[
            books["Editorial"].str.casefold() == st.session_state.selected_editorial.casefold()
        ]

        col_cat, col_info = st.columns([1, 2])
        with col_cat:
            st.caption("EDITORIAL")
        with col_info:
            st.caption(f"{len(editorial_books)} libros en el catálogo")

        st.divider()

        for _, book in editorial_books.iterrows():
            comp_titulo(book)
            comp_layout_botones(book)
            comp_ver_ficha(book)
            st.divider()
        st.stop()

def seccion_ficha_libro(books):
    if st.session_state.selected_isbn is not None:
        selected = books[books["ISBN"] == st.session_state.selected_isbn]

        if selected.empty:
            st.session_state.selected_isbn = None
            st.rerun()

        book = selected.iloc[0]

        comp_volver_catalogo()

        st.title(book["Titulo"])
        st.caption("FICHA BIBLIOGRÁFICA")


        st.divider()

        st.markdown("### Información")
        st.caption(f"**ISBN:** {book['ISBN'] or '—'}")

        col_anio, col_estado = st.columns([1, 1])
        with col_anio:
            st.write("**Año de publicación:**", book["Año de publicación"] or "—")
        with col_estado:
            comp_estado(book)

        comp_artistas(book)
        comp_editorial(book)
        comp_saga(book)

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
                        width='stretch'
                    ):
                        st.session_state.selected_isbn = related_book["ISBN"]
                        st.rerun()
                else:
                    st.caption(f"Libro no encontrado en el catálogo: {title}")

        st.stop()