import streamlit as st
import streamlit.components.v1 as components

# Style: CSS para esconder o menu hamburger (☰) e o footer
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    


def render_sobre():
    st.markdown("<h2 style='text-align: center; color: white;'>📞 Contatos</h2>", unsafe_allow_html=True)
    st.markdown("")

    
    st.divider()
    st.markdown("")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image("icons/whatsapp.png", caption="28 99918-3961", width=90)

    with col2:
        st.image("icons/gmail.png", caption="viniciusmeireles@gmail.com", width=100)

    with col3:
        st.image("icons/location.png", caption="Vitória/ES", width=90)    

    with col4:
        st.image("icons/linkedin.png",caption= "/pviniciusmeireles", width=90)
    with col5:    
        st.image("Img/logo.png", caption="Desenvolvedor", width=230)
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    
    
