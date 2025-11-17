"""
Detector de Hype
Aplicativo Streamlit para analisar o "hype" de um termo de pesquisa usando
dados do TikTok.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import utils 

TEMA_COR = "#E02E30"

st.set_page_config(
    page_title="Detector de Hype", 
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ESTILOS CSS 
try: 
    img_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" 
    try:
        with open("capa.png", "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        pass 
except Exception as e:
    st.error(f"Erro ao carregar a imagem de capa: {e}")
    img_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

css_styles = utils.load_css_styles(img_base64, TEMA_COR)
st.markdown(css_styles, unsafe_allow_html=True)


st.markdown("""
<style>
    /* Ajusta a margem da lista */
    [data-baseweb="tab-list"] { 
        margin-bottom: 20px !important; 
    }
    
    /* Estilos para a lista de links */
    .link-list { 
        list-style-type: none; 
        padding-left: 0; 
    }
    .link-list li { 
        background-color: #ffffff; 
        border: 1px solid #e0e0e0; 
        border-radius: 10px; 
        padding: 16px 20px; 
        margin-bottom: 12px; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .link-list li:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.07);
    }
    .link-list li a { 
        font-size: 1.1rem; 
        font-weight: 600; 
        color: #E02E30; /* TEMA_COR */
        text-decoration: none;
        display: block; 
    }
    .link-list li a:hover { 
        text-decoration: underline; 
    }
    .link-list li p { 
        margin-top: 5px; 
        margin-bottom: 0; 
        color: #333; 
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Função principal que renderiza a interface do Streamlit."""
    
    # CAPA
    st.markdown("""
    <div class="hype-cover">
        <h1>Detector de Hype</h1>
    </div>
    """, unsafe_allow_html=True)


    # --- ABAS ---
    tab_inicial, tab_analise = st.tabs(["Tendências", "Explorar"])

    # --- ABA INICIAL---
    with tab_inicial:
        st.markdown("""
            <p style="font-size: 1.1rem;">Acesse as tendências oficiais do TikTok e Google trends para descobrir o que está em alta no Brasil:</p>
            
            <ul class="link-list">
                <li>
                    <a href="https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/pt" target="_blank">
                        <strong>TikTok Trends</strong>
                    </a>
                    <p>Veja as hashtags e vídeos mais populares no momento.</p>
                </li>
                <li>
                    <a href="https://trends.google.com.br/trending?geo=BR" target="_blank">
                        <strong>Google Trends</strong>
                    </a>
                    <p>Veja o que está bombando no Google Trends.</p>
                </li>
            </ul>
            <p></p>      
            <p style="font-size: 1.1rem;">Tendências do TikTok Brasil aplicadas ao varejo farma (Insights via IA):</p>                
        """, unsafe_allow_html=True)
        model = utils.get_gemini_model()
        prompt = ("""Quero que você atue como um analista de tendências especializado em comportamento do consumidor e buscas virais no TikTok Brasil.
            Sua tarefa é gerar um RANKING DIÁRIO de termos, produtos e temas que ESTÃO OU PODEM ESTAR HIPADOS no TikTok BRASIL hoje, com base em padrões comportamentais, ciclos de consumo, sazonalidade e tendências emergentes. 

            IMPORTANTE:
            - NÃO invente dados específicos do TikTok, apenas gere tendências plausíveis e coerentes.
            - Traga apenas termos/expressões que façam sentido atualmente.
            - Seja direto e organizado.
            - Liste apenas os termos, sem textos longos.

            ### ENTREGUE O RESULTADO NO FORMATO A SEGUIR:

            ## 🧪 Medicamentos 
            1. termo — descrição curta
            2. ...
            (10 itens)

            ## ✨ Dermocosméticos 
            (subcategorias como: anticaspa, antiqueda, bronzeador, anti-estrias, anti-idade corporal, anti-manchas, anticelulite, capilar antioliosidade, capitar recuperação, capilar sensibilidade, cuidados genicologicos, desodorante, mãos e pés, pós banho, dermo solar facial, hidratação corporal, limpeza corporal, limpeza facial etc)
            1. termo — descrição curta
            2. ...
            (10 itens)

            ## 💄 Beleza e Cuidados
            (subcategorias como: acessorio cabelo, acessorio maquiagem, acessorio coloração, acessorio manicure, colonias, perfume, condicionar, shampoo, tonalizante, finalizadores etc)
            1. termo — descrição curta
            2. ...
            (10 itens)

            ## 👶 Mundo Infantil
            (subcategorias como: acessorio alimentação infantil, acessorio mamadeiras, acessorio chupetas, acessorio higiene infantil, banho infantil, bico mamadeira, fralda infantil, toalha umidecida infantil, nutrição kids etc)
            1. termo — descrição curta
            2. ...
            (10 itens)

            ## 🏋️ Fitness 
            (subcategorias: emagrecedores, barras de proteína, ganho de massa, suplementos, pré-treino etc)
            1. termo — descrição curta
            2. ...
            (10 itens)

            ### REGRAS DE FORMATAÇÃO:
            - Sempre entregar exatamente 10 termos por categoria.
            - Cada termo deve ter 1 linha apenas, com uma descrição muito breve.
            - Mantenha o estilo claro e objetivo.
            - Evite repetir termos entre categorias.

            Agora gere o ranking atualizado de hoje.""")
        response = model.generate_content(prompt)
        text = response.text
        # Encontra o início da seção "Medicamentos"
        start = text.find("## 🧪 Medicamentos")

        # Corta o texto a partir da seção
        if start != -1:
            text = text[start:]

        st.write(text)

    # --- ABA DE ANÁLISE  ---
    with tab_analise:
        # ENTRADA DE PESQUISA
        search_term = st.text_input("Digite o termo a ser analisado", key="search_term")
        if not search_term:
            st.info("Por favor, digite um termo na barra de pesquisa acima para carregar a análise do TikTok.")
        else:
            search_term = search_term.strip()

            # COLETA E PROCESSAMENTO DE DADOS 
            videos = None
            df = pd.DataFrame()
            growth_data = None
            ihp_metrics = {} # Inicializa como dict vazio

            with st.spinner(f"Coletando e analisando dados para '{search_term}'..."):
                
                # TIKTOK
                videos = utils.fetch_tiktok_data(search_term)
                
                if videos:
                    df = pd.DataFrame(videos)
                    
                    # Lógica para extrair o ID do autor do campo aninhado 'author'
                    if 'author' in df.columns:
                        # Cria a coluna 'author_user_id' extraindo o 'id' do dict 'author'
                        # Usa .get('id') para evitar erros se 'id' não existir
                        # Verifica se 'x' é um dict para evitar erros em dados nulos (NaN)
                        df['author_user_id'] = df['author'].apply(
                            lambda x: x.get('id') if isinstance(x, dict) else pd.NA
                        )
                    else:
                        # Se a coluna 'author' não existir, cria 'author_user_id' com Nulos
                        df['author_user_id'] = pd.NA
                    
                    # Garante que as colunas necessárias existam
                    required_cols = ['create_time', 'play_count', 'digg_count', 'comment_count', 'share_count', 'desc', 'cover', 'id', 'play']
                    for col in required_cols:
                        if col not in df.columns:
                            if col == 'create_time': df[col] = pd.NA
                            elif col in ['play_count', 'digg_count', 'comment_count', 'share_count']: df[col] = 0
                            else: df[col] = ""
                    
                    # Conversão de tipos e tratamento de nulos
                    df['create_time'] = pd.to_datetime(df['create_time'], unit='s', errors='coerce')
                    for col in ['play_count', 'digg_count', 'comment_count', 'share_count']:
                        df[col] = df[col].fillna(0).astype(int)
                        
                    growth_data = utils.calculate_growth_metrics(df)

                # CÁLCULO FINAL DO IHP
                ihp_metrics = utils.calculate_ihp(growth_data)
                ihp_total_score = ihp_metrics['ihp_total_score']
                recommendation = utils.get_ihp_recommendation(ihp_total_score)



            # EXIBIÇÃO DO IHP E RECOMENDAÇÃO 
            st.markdown("<h3>Índice de Hype do TikTok (IHT)</h3>", unsafe_allow_html=True)
            
            # Cards do IHP (com .get() para segurança caso ihp_metrics esteja vazio)
            delta_text = (
                f"Views: {ihp_metrics.get('views_momentum', 0):.0f} | "
                f"Likes: {ihp_metrics.get('likes_momentum', 0):.0f} | "
                f"Coments: {ihp_metrics.get('comments_momentum', 0):.0f} | "
                f"Shares: {ihp_metrics.get('shares_momentum', 0):.0f} | "
                f"Criadores: {ihp_metrics.get('ucm_momentum', 0):.0f}"
            )
            
            # Inclui o Fator de Distribuição na exibição principal
            fd_score = ihp_metrics.get('fd_score', 0)
            fd_text = f"Distribuição (FD): {fd_score:.0f}/100"

            col_main, col_tooltip = st.columns([4.2, 0.5])

            with col_main:
                left_col, right_col = st.columns([3, 2])

                with left_col:
                    st.markdown(
                        f"<div style='font-size:2.4rem; font-weight:800; color:{TEMA_COR}; margin-bottom:6px;'>"
                        f"{ihp_total_score:.0f}/200</div>",
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"<div style='color:#666; font-size:0.95rem;' title='{delta_text}'>"
                        f"<strong>Momentum:</strong> {ihp_metrics.get('ihp_total_score', 0):.0f}% | "
                        f"<strong>{fd_text}</strong></div>",
                        unsafe_allow_html=True
                    )
                    
                    # Tooltip detalhado para o Momentum
                    st.markdown(
                        f"<div style='color:#666; font-size:0.8rem; margin-top: 5px;'>"
                        f"Detalhe do Momentum (14d vs 60d): {delta_text}</div>",
                        unsafe_allow_html=True
                    )


                    if not growth_data:
                        st.markdown(
                            "<div class='warning-card'>A pontuação do TikTok é 0 (API falhou ou não retornou dados).</div>",
                            unsafe_allow_html=True
                        )
                    
                with right_col:
                    st.markdown("<div class='recommendation-title'>Interpretação</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='recommendation-text'>{recommendation}</div>", unsafe_allow_html=True)


            # Popover de Ajuda 
            with col_tooltip:
                st.popover("❓").markdown("""
                    ##### O que é o IHT?
                    O IHT (0-200) mede o **momentum e a organicidade** de um produto no TikTok. Ele é composto por duas partes:
                    
                    1.  **Momentum (70%):** Compara a média de engajamento (14d vs 60d).
                    2.  **Fator de Distribuição (FD) (30%):** Mede a proporção de **Criadores Únicos** dentro da amostra total vídeos. Um FD de 100 indica que todos os vídeos da amostra foram postados por criadores diferentes (alta organicidade).
                    
                    ---
                    **Interpretação do Score:**
                    * **Pontuação 200:** Hype explosivo, amplamente distribuído.
                    * **Pontuação 100:** Interesse estável/crescente, com engajamento e distribuição saudáveis.
                    * **Pontuação < 100:** Interesse em queda ou alta concentração (poucos criadores postando muito), o que pode indicar campanha paga.
                    
                    ---
                    **Peso das Métricas (Foco Orgânico):**
                    * Comentários e Shares (60%)
                    * Criadores Únicos e Likes (30%)
                    * Views (10%)
                    """)

            st.markdown("<br>", unsafe_allow_html=True)

            if videos is None:
                st.warning("Não foi possível conectar à API do TikTok ou obter dados.")
            elif not videos:
                st.warning(f"Nenhum vídeo encontrado para '{search_term}' no TikTok.")
            else:
                # Métricas
                tiktok_views = df['play_count'].sum()
                tiktok_likes = df['digg_count'].sum()
                tiktok_comments = df['comment_count'].sum()
                tiktok_shares = df['share_count'].sum()

                st.subheader(f"Engajamento Total")
                c1, c2, c3, c4 = st.columns(4)
                
                c1.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Views</div>
                    <div class="metric-value-white">{utils.format_number(tiktok_views)}</div>
                </div>""", unsafe_allow_html=True)
                c2.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Likes</div>
                    <div class="metric-value-white">{utils.format_number(tiktok_likes)}</div>
                </div>""", unsafe_allow_html=True)
                c3.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Comentários</div>
                    <div class="metric-value-white">{utils.format_number(tiktok_comments)}</div>
                </div>""", unsafe_allow_html=True)
                c4.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Compartilhamentos</div>
                    <div class="metric-value-white">{utils.format_number(tiktok_shares)}</div>
                </div>""", unsafe_allow_html=True)

                # Gráfico
                df['date'] = df['create_time'].dt.to_period('D').dt.to_timestamp()
                df_time = (df.groupby('date', as_index=False)['play_count'].sum().sort_values('date'))

                if not df_time.empty:
                    fig = px.line(df_time, x='date', y='play_count', markers=True, 
                                    title="", 
                                    labels={'date': 'Data', 'play_count': 'Visualizações'}, 
                                    color_discrete_sequence=[TEMA_COR])
                    st.plotly_chart(fig, use_container_width=True)

                # Tabela de Médias 
                if growth_data and (growth_data.get('views_14d_avg', 0) > 0 or growth_data.get('views_60d_avg', 0) > 0):
                    st.subheader("Análise de Momentum")
                    
                    st.markdown(f"""
                        <table class="thirtyd-table">
                            <thead>
                                <tr>
                                    <th> </th>
                                    <th>Views</th>
                                    <th>Likes</th>
                                    <th>Comentários</th>
                                    <th>Compartilhamentos</th>
                                    <th>Criadores\Dia</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Últimos 14 dias</td>
                                    <td>{utils.format_number(growth_data.get('views_14d_avg', 0))}</td>
                                    <td>{utils.format_number(growth_data.get('likes_14d_avg', 0))}</td>
                                    <td>{utils.format_number(growth_data.get('comments_14d_avg', 0))}</td>
                                    <td>{utils.format_number(growth_data.get('shares_14d_avg', 0))}</td>
                                    <td>{growth_data.get('creators_14d_avg', 0):.1f}</td>
                                </tr>
                                <tr>
                                    <td>Últimos 60 dias</td>
                                    <td>{utils.format_number(growth_data.get('views_60d_avg', 0))}</td>
                                    <td>{utils.format_number(growth_data.get('likes_60d_avg', 0))}</td>
                                    <td>{utils.format_number(growth_data.get('comments_60d_avg', 0))}</td>
                                    <td>{utils.format_number(growth_data.get('shares_60d_avg', 0))}</td>
                                    <td>{growth_data.get('creators_60d_avg', 0):.1f}</td>
                                </tr>
                            </tbody>
                        </table>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Não há dados de engajamento recentes (últimos 60 dias) na amostra de vídeos para calcular as médias.")

                st.divider()
                
                # Vídeos Mais Populares
                st.subheader("Vídeos Mais Populares")
                df['link'] = df.apply(lambda row: row.get('play', '') or f"https://www.tiktok.com/video/{row.get('id', '')}", axis=1)
                top_videos = df.sort_values('play_count', ascending=False).head(12)
                num_cols = 4

                for i in range(0, len(top_videos), num_cols):
                    cols = st.columns(num_cols)
                    subset = top_videos.iloc[i:i + num_cols]
                    for col, (_, row) in zip(cols, subset.iterrows()):
                        link = row['link']
                        cover_url = row['cover'] or 'https://via.placeholder.com/250x250?text=Capa+Indisponível'
                        
                        views = utils.format_number(row['play_count'])
                        likes = utils.format_number(row['digg_count'])
                        
                        with col:
                            st.markdown(f"""
                            <div style="text-align:center; margin-bottom: 15px;">
                                <a href="{link}" target="_blank">
                                    <img src="{cover_url}" 
                                        style="width:100%; height: 250px; object-fit: cover; border-radius:10px;" alt="Capa do Vídeo"/>
                                </a>
                                <div style="margin-top:5px; font-size:0.9rem;">
                                    👀 {views} &nbsp;|&nbsp; ❤️ {likes}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)


# --- PONTO DE ENTRADA  ---
if __name__ == "__main__":
    main()