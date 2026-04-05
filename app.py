import streamlit as st
import random
from PIL import Image
from lists import locais_dragoes, detalhes_dragoes, detalhes_personagens

# Configuração da Página
st.set_page_config(page_title="Ingeborger RPG", layout="wide")

# Sidebar para Navegação
st.sidebar.title("Menu de Navegação")
pagina = st.sidebar.radio("Ir para:", ["Teste de Habilidade", "Gerador de Encontros", "Dragonário", "Fichas"])

# --- PÁGINA: TESTE DE HABILIDADE ---
if pagina == "Teste de Habilidade":
    st.header("🎲 Teste de Habilidade")
    
    col1, col2 = st.columns(2)
    with col1:
        forca = st.number_input("Força", value=0)
        resistencia = st.number_input("Resistência", value=0)
        destreza = st.number_input("Destreza", value=0)
    with col2:
        intel = st.number_input("Inteligência", value=0)
        percepcao = st.number_input("Percepção", value=0)
        comando = st.number_input("Comando", value=0)

    st.divider()
    
    atr_map = {"Força": forca, "Resistência": resistencia, "Destreza": destreza, 
               "Inteligência": intel, "Percepção": percepcao, "Comando": comando}
    
    sel_atr = st.selectbox("Atributo do Teste", list(atr_map.keys()))
    dificuldade = st.number_input("Dificuldade (DC)", value=10)

    if st.button("Rolar Dados"):
        rolagem = random.randint(1, 20)
        total = rolagem + atr_map[sel_atr]
        
        if total >= dificuldade:
            st.success(f"Sucesso! Rolagem: {rolagem} (+{atr_map[sel_atr]}) = {total} vs DC {dificuldade}")
        else:
            st.error(f"Falha! Rolagem: {rolagem} (+{atr_map[sel_atr]}) = {total} vs DC {dificuldade}")

# --- PÁGINA: GERADOR DE ENCONTROS ---
elif pagina == "Gerador de Encontros":
    st.header("🐉 Gerador de Encontros")
    local = st.selectbox("Selecione o Local", list(locais_dragoes.keys()))
    
    if st.button("Gerar Dragão"):
        dragao = random.choice(locais_dragoes[local])
        st.subheader(f"Um {dragao} apareceu!")
        try:
            img = Image.open(f"img/{dragao}.png")
            st.image(img, width=400)
        except:
            st.warning("Imagem não encontrada na pasta /img")

# --- PÁGINA: DRAGONÁRIO ---
elif pagina == "Dragonário":
    st.header("📖 Dragonário")
    drag_sel = st.selectbox("Consultar Dragão", list(detalhes_dragoes.keys()))
    
    d = detalhes_dragoes[drag_sel]
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(f"img/{drag_sel}.png")
        except:
            st.info("Sem imagem")
            
    with col2:
        st.subheader(drag_sel)
        st.write(f"**Classificação:** {d['Classificação']}")
        st.write(f"**Habitat:** {d['Habitat']}")
        st.write(f"**Poder:** {d['Poder']}")
        st.write(f"**Alimentação:** {d['Alimentação']}")

# --- PÁGINA: FICHAS ---
elif pagina == "Fichas":
    st.header("🛡️ Fichas de Personagens")
    char_sel = st.selectbox("Selecione o Personagem", list(detalhes_personagens.keys()))
    
    c = detalhes_personagens[char_sel]
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(c["Foto"], use_container_width=True)
        except:
            st.error("Foto não encontrada")
            
    with col2:
        st.subheader(char_sel)
        st.write(f"**Esquadrão:** {c['Esquadrão']}")
        st.write(f"**Patente:** {c['Patente']}")
        
    st.markdown("### 📊 Atributos Base")
        
    # Usando .get() para evitar erros e debugando as chaves
    attrs = c.get("Atributos")
    
    if attrs:
        m1, m2, m3 = st.columns(3)
        m4, m5, m6 = st.columns(3)
        
        # Garantindo que as chaves existam dentro de 'Atributos'
        m1.metric("FOR", attrs.get("FOR", 0))
        m2.metric("RES", attrs.get("RES", 0))
        m3.metric("INT", attrs.get("INT", 0))
        m4.metric("DES", attrs.get("DES", 0))
        m5.metric("PER", attrs.get("PER", 0))
        m6.metric("COM", attrs.get("COM", 0))
    else:
        # Debug: Isso vai mostrar o que o Python REALMENTE está vendo dentro do dicionário
        st.error(f"Erro: Chave 'Atributos' não encontrada para {char_sel}.")
        st.write("Chaves disponíveis neste personagem:", list(c.keys()))

    st.divider()
    st.subheader("Dragões do Personagem")
    d_cols = st.columns(3)
    for i, d in enumerate(c["Dragões"]):
        with d_cols[i]:
            try:
                st.image(d["Imagem"], caption=d["Nome"], width=150)
            except:
                st.write(f"{d['Nome']}")