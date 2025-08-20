import streamlit as st
from BlackjackS17 import (
    make_shoe, hit, contar_mano, contar_cartas, estrategia_basica, is_pair,
    prob_10_val, probs_por_valor, conteo_por_valor,
    contar_mano_detallado, dealer_play_sim, resolver, sim_action
)
import base64, os
import pandas as pd

st.set_page_config(
    page_title="Blackjack Trainer",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personalizado para el tema de casino
st.markdown("""
<style>
            
        /* Fondo para TODA la app */
        .stApp, [data-testid="stAppViewContainer"]{
        background: linear-gradient(135deg, #0f4c3a 0%, #2d5a3d 50%, #0f4c3a 100%);
        min-height: 100vh;
        }

        /* Quita fondos blancos por encima del fondo */
        main .block-container{
        background: transparent;
        padding: 20px 20px 100px; /* como tenías */
        }

        /* Header transparente para que no tape el fondo */
        [data-testid="stHeader"]{
        background: transparent;
        }

        .game-controls button[kind="secondary"]{
            transition: transform .06s ease, box-shadow .12s ease;
        }
        .game-controls button:hover{
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(0,0,0,.25);
        }
        .game-table {
            background: radial-gradient(ellipse at center, #0d7377 0%, #14a085 50%, #0d7377 100%);
            border: 8px solid #8B4513;
            border-radius: 200px;
            margin: 20px auto;
            padding: 40px;
            box-shadow: 
                inset 0 0 50px rgba(0,0,0,0.3),
                0 10px 30px rgba(0,0,0,0.5);
            position: relative;
            max-width: 1200px;
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;            /* si no caben, se apilan sin estorbar */
            justify-content: center;    /* centra columnas */
            align-items: flex-start;
            gap: 10px; 
        }

        .dealer-area, .player-area{
            flex: 1 1 400px;   /* grow, shrink, basis ≈ columna responsiva */
            min-width: 320px;  /* evita compresión excesiva */
            max-width: 560px;  /* tope para que no se desborde */
            margin: 0;         /* el gap de .game-table ya da el espacio */
            text-align: center;
        }
                
        .dealer-label, .player-label {
            color: #FFD700;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            margin-bottom: 20px;
            text-align: center;
        }
                
        .speech-bubble {
            background: #ffeb3b;
            padding: 8px 16px;
            border-radius: 1rem;
            box-shadow: 2px 2px 4px #0004;
            font-weight: bold;
            color: black;
            display: inline-block;
            position: relative;
            margin-top: 0.5rem;
        }

        .speech-bubble::after {
            content: "";
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            border-width: 0 10px 10px;
            border-style: solid;
            border-color: transparent transparent #ffeb3b transparent;
        }

        .speech-bubble.small {
            font-size: 0.9rem;
            padding: 4px 10px;
            border-radius: 0.8rem;
        }
        
        .game-controls {
            text-align: center;
            margin: 30px 0;
        }
        
        .status-message {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #FFD700;
            margin: 20px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        }
        
        .card-fallback {
            background: white;
            color: black;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 12px;
            text-align: center;
            flex-direction: column;
        }
            
        .card {
            width: 80px;
            height: 110px;
            border-radius: 10px;
            box-shadow: 3px 3px 10px rgba(0,0,0,0.4);
            position: relative;
            border: 2px solid #333;
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
            flex-shrink: 0;
            transition: transform 0.6s;
            transform-style: preserve-3d;
        }

        .card-back {
            background: #000080;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 24px;
            position: absolute;
            backface-visibility: hidden;
        }

        .card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 8px;
            display: block;
            backface-visibility: hidden;
        }

        .card.flip {
            transform: rotateY(180deg);
        }

        /* Las cartas ya usan wrap, pero reforzamos que no se amontonen */
        .cards-container{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;   /* al pedir más cartas, se acomodan en la línea siguiente */
        width: 100%;
        }

        @keyframes deal {
            0% { transform: scale(0); }
            100% { transform: scale(1); }
        }

        .card.deal {
            animation: deal 1s forwards;
        }

        .split-hands {
            display: flex;
            flex-direction: column;
            gap: 20px;
            align-items: center;
        }

        .hand-container {
            border: 2px solid #FFD700;
            border-radius: 15px;
            padding: 10px;
            margin: 10px 0;
            background: rgba(255, 215, 0, 0.1);
        }

        .active-hand {
            border-color: #FF4500;
            background: rgba(255, 69, 0, 0.2);
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);
        }

        .hand-label {
            color: #FFD700;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
            
        /* Opcional: en pantallas muy chicas, fuerza columna única */
        @media (max-width: 900px){
        .dealer-area, .player-area{
            flex: 1 1 100%;
            max-width: 800px;
        }
        }
    </style>
""", unsafe_allow_html=True)

# Inicialización del estado
# Ruta de imágenes: ahora configurable y guardada en session_state
if 'ruta_imgs' not in st.session_state:
    st.session_state.ruta_imgs = r"C:\Users\ultra\OneDrive\Escritorio\USEFUL_SCRIPTS\BLACKJACK_APP\imgs_cartas"

# Contadores de sesión y flags
for key, val in {
    "wins": 0, "losses": 0, "pushes": 0,
    "stats_recorded": False,     # para no duplicar el conteo al hacer rerun
    "dealer_hits_soft_17": False # H17 toggle
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.mazo, st.session_state.mazo_valores = make_shoe(6)
    st.session_state.cartas_player = []
    st.session_state.manos_player = []  # Lista de manos divididas
    st.session_state.cartas_croupier = []
    st.session_state.game_over = False
    st.session_state.message = "¡Presiona 'Nueva Mano' para empezar!"
    st.session_state.victory = False
    st.session_state.double = False
    st.session_state.split = False
    st.session_state.cards_dealt = 0
    st.session_state.mano_activa = 0  # Índice de la mano activa al dividir
    st.session_state.splits_count = 0  # Contador de divisiones
    st.session_state.manos_completadas = []  # Estado de cada mano dividida

def convertir_nombre_carta(carta):
    """Convierte el nombre de la carta al formato del archivo de imagen"""
    try:
        partes = carta.split(' ')
        if len(partes) != 2:
            return None
        
        valor, palo = partes
        
        palo_map = {
            '♠': 'spades',
            '♥': 'hearts', 
            '♦': 'diamonds',
            '♣': 'clubs',
            '♤': 'spades',
            '♧': 'clubs'
        }
        
        palo_eng = palo_map.get(palo, palo)
        nombre_archivo = f"{valor}_{palo_eng}"
        
        return nombre_archivo
        
    except Exception as e:
        return None

def cargar_imagen_base64(ruta_completa):
    """Carga una imagen y la convierte a base64 con manejo de errores"""
    try:
        if not os.path.exists(ruta_completa):
            return None
            
        with open(ruta_completa, "rb") as img_file:
            img_data = img_file.read()
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            return img_base64
            
    except Exception as e:
        return None

def mostrar_carta(carta, hidden=False):
    """Renderiza una carta con estilo de casino usando las imágenes reales"""
    
    if hidden:
        # Carta oculta - mostrar reverso
        ruta_carta = os.path.join(st.session_state.ruta_imgs, "card_back.png")

        img_base64 = cargar_imagen_base64(ruta_carta)
        
        if img_base64:
            return f"""<div class="card deal"><img src="data:image/png;base64,{img_base64}" alt="Carta oculta"></div>"""
        else:
            return f"""<div class="card card-back">?</div>"""
    else:
        # Carta visible
        nombre_archivo = convertir_nombre_carta(carta)
        
        if nombre_archivo:
            extensiones = ['.png', '.jpg', '.jpeg']
            img_base64 = None
            
            for ext in extensiones:
                ruta_carta = os.path.join(st.session_state.ruta_imgs, f"{nombre_archivo}{ext}")
                img_base64 = cargar_imagen_base64(ruta_carta)
                if img_base64:
                    break
            
            if img_base64:
                return f"""<div class="card deal"><img src="data:image/png;base64,{img_base64}" alt="{carta}"></div>"""
        
        # Fallback si no encuentra la imagen
        valor = carta.split(' ')[0] if ' ' in carta else carta[:1]
        palo = carta.split(' ')[1] if ' ' in carta else carta[1:]
        
        return f"""
        <div class="card card-fallback">
            <div style="font-size: 16px;">{valor}</div>
            <div style="font-size: 24px; margin-top: 5px;">{palo}</div>
        </div>
        """

def mostrar_cartas_dealer():
    """Muestra todas las cartas del dealer con la lógica correcta"""
    if not st.session_state.cartas_croupier:
        return ""
    
    cards_html = ""
    
    for i, carta in enumerate(st.session_state.cartas_croupier):
        if i == 1 and not st.session_state.game_over:
            # Segunda carta oculta durante el juego
            cards_html += mostrar_carta(carta, hidden=True)
        else:
            # Todas las demás cartas visibles
            cards_html += mostrar_carta(carta, hidden=False)
    
    return cards_html

def mostrar_cartas_player():
    """Muestra todas las cartas del jugador con soporte para manos divididas"""
    if st.session_state.split and st.session_state.manos_player:
        # Mostrar manos divididas
        html_content = '<div class="split-hands">'
        
        # Mano original
        if st.session_state.cartas_player:
            active_class = "active-hand" if st.session_state.mano_activa == 0 else ""
            html_content += f'<div class="hand-container {active_class}">'
            html_content += '<div class="hand-label">Mano 1</div>'
            html_content += '<div class="cards-container">'
            for carta in st.session_state.cartas_player:
                html_content += mostrar_carta(carta, hidden=False)
            html_content += '</div>'
            
            # Mostrar valor de la mano
            valor_mano, _ = contar_mano(st.session_state.cartas_player, st.session_state.mazo_valores)
            html_content += f'<div style="text-align: center; margin-top: 0.5rem;"><div class="speech-bubble small">{valor_mano}</div></div>'
            html_content += '</div>'
        
        # Manos adicionales
        for i, mano in enumerate(st.session_state.manos_player):
            active_class = "active-hand" if st.session_state.mano_activa == i + 1 else ""
            html_content += f'<div class="hand-container {active_class}">'
            html_content += f'<div class="hand-label">Mano {i + 2}</div>'
            html_content += '<div class="cards-container">'
            for carta in mano:
                html_content += mostrar_carta(carta, hidden=False)
            html_content += '</div>'
            
            # Mostrar valor de la mano
            if len(mano) > 0:
                valor_mano, _ = contar_mano(mano, st.session_state.mazo_valores)
                html_content += f'<div style="text-align: center; margin-top: 0.5rem;"><div class="speech-bubble small">{valor_mano}</div></div>'
            html_content += '</div>'
        
        html_content += '</div>'
        return html_content
    else:
        # Mano normal (no dividida)
        if not st.session_state.cartas_player:
            return ""
        
        cards_html = ""
        for carta in st.session_state.cartas_player:
            cards_html += mostrar_carta(carta, hidden=False)
        
        return cards_html

def nueva_mano():
    """Inicia una nueva mano"""
    st.session_state.cartas_player = []
    st.session_state.manos_player = []
    st.session_state.cartas_croupier = []
    st.session_state.game_over = False
    st.session_state.cards_dealt = 0
    st.session_state.double = False
    st.session_state.split = False
    st.session_state.mano_activa = 0
    st.session_state.splits_count = 0
    st.session_state.manos_completadas = []
    st.session_state.stats_recorded = False


    # Repartir cartas iniciales
    hit(st.session_state.mazo, st.session_state.cartas_player)
    hit(st.session_state.mazo, st.session_state.cartas_croupier)
    hit(st.session_state.mazo, st.session_state.cartas_player)
    hit(st.session_state.mazo, st.session_state.cartas_croupier)
    
    st.session_state.game_started = True
    valor_player, _ = contar_mano(st.session_state.cartas_player, st.session_state.mazo_valores)

    if valor_player == 21:
        st.session_state.message = "¡21! Excelente mano."
        player_stand()
    else:
        st.session_state.message = "Tu turno - ¿Qué quieres hacer?"

def obtener_mano_activa():
    """Obtiene la mano activa actual"""
    if st.session_state.mano_activa == 0:
        return st.session_state.cartas_player
    else:
        return st.session_state.manos_player[st.session_state.mano_activa - 1]

def player_hit():
    """Jugador pide carta"""
    if not st.session_state.game_over:
        mano_activa = obtener_mano_activa()
        hit(st.session_state.mazo, mano_activa)
        valor_mano, _ = contar_mano(mano_activa, st.session_state.mazo_valores)
        
        if valor_mano > 21:
            # Marcar mano actual como completada
            st.session_state.manos_completadas.append(st.session_state.mano_activa)
            
            if st.session_state.split:
                # Si hay más manos por jugar
                if st.session_state.mano_activa < len(st.session_state.manos_player):
                    st.session_state.mano_activa += 1
                    st.session_state.message = f"Mano {st.session_state.mano_activa} se pasó. Jugando mano {st.session_state.mano_activa + 1}"
                else:
                    # Todas las manos completadas
                    verificar_resultado_final()
            else:
                st.session_state.game_over = True
                st.session_state.message = "¡Te pasaste! Perdiste."
                st.session_state.victory = False
        elif valor_mano == 21:
            st.session_state.message = "¡21! Excelente mano."
            if st.session_state.split:
                avanzar_siguiente_mano()

def player_double():
    """Jugador pide doblar y carta"""
    mano_activa = obtener_mano_activa()
    if not st.session_state.game_over and len(mano_activa) == 2:
        hit(st.session_state.mazo, mano_activa)
        valor_mano, _ = contar_mano(mano_activa, st.session_state.mazo_valores)
        st.session_state.double = True

        if valor_mano > 21:
            st.session_state.manos_completadas.append(st.session_state.mano_activa)
            if st.session_state.split:
                if st.session_state.mano_activa < len(st.session_state.manos_player):
                    st.session_state.mano_activa += 1
                    st.session_state.message = f"Mano {st.session_state.mano_activa} se pasó. Jugando mano {st.session_state.mano_activa + 1}"
                else:
                    verificar_resultado_final()
            else:
                st.session_state.game_over = True
                st.session_state.victory = False
                st.session_state.message = "¡Te pasaste! Perdiste."
        else:
            if st.session_state.split:
                avanzar_siguiente_mano()
            else:
                player_stand()

def avanzar_siguiente_mano():
    """Avanza a la siguiente mano en caso de split"""
    st.session_state.manos_completadas.append(st.session_state.mano_activa)
    
    if st.session_state.mano_activa < len(st.session_state.manos_player):
        st.session_state.mano_activa += 1
        st.session_state.message = f"Jugando mano {st.session_state.mano_activa + 1}"
    else:
        # Todas las manos completadas, jugar dealer
        player_stand()

def verificar_resultado_final():
    """Verifica el resultado final cuando hay manos divididas"""
    # Jugar turno del dealer
    dealer_play_sim(st.session_state.mazo, st.session_state.cartas_croupier,
                st.session_state.mazo_valores,
                hit_soft_17=st.session_state.dealer_hits_soft_17)
    
    valor_dealer, _ = contar_mano(st.session_state.cartas_croupier, st.session_state.mazo_valores)
    
    # Evaluar cada mano
    resultados = []
    
    # Mano principal
    valor_mano, _ = contar_mano(st.session_state.cartas_player, st.session_state.mazo_valores)
    resultado = evaluar_mano_vs_dealer(valor_mano, valor_dealer)
    resultados.append(f"Mano 1: {resultado}")
    
    # Manos divididas
    for i, mano in enumerate(st.session_state.manos_player):
        valor_mano, _ = contar_mano(mano, st.session_state.mazo_valores)
        resultado = evaluar_mano_vs_dealer(valor_mano, valor_dealer)
        resultados.append(f"Mano {i+2}: {resultado}")
    
    st.session_state.message = " | ".join(resultados)
    st.session_state.game_over = True

    if not st.session_state.stats_recorded:
        # cuenta por mano
        for res in resultados:
            if "Ganaste" in res: st.session_state.wins += 1
            elif "Perdiste" in res: st.session_state.losses += 1
            else: st.session_state.pushes += 1
        st.session_state.stats_recorded = True

def evaluar_mano_vs_dealer(valor_mano, valor_dealer):
    """Evalúa una mano individual contra el dealer"""
    if valor_mano > 21:
        return "Perdiste"
    elif valor_dealer > 21:
        return "Ganaste"
    elif valor_dealer > valor_mano:
        return "Perdiste"
    elif valor_mano > valor_dealer:
        return "Ganaste"
    else:
        return "Empate"

def player_split():
    """Jugador divide cartas"""
    es_par = is_pair(st.session_state.cartas_player[0], st.session_state.cartas_player[1])
    
    if (not st.session_state.game_over and 
        len(st.session_state.cartas_player) == 2 and 
        es_par and 
        st.session_state.splits_count < 3):  # Máximo 3 splits (4 manos total)
        
        # Crear nueva mano con la segunda carta
        segunda_carta = st.session_state.cartas_player.pop()
        nueva_mano = [segunda_carta]
        
        # Dar carta a ambas manos
        hit(st.session_state.mazo, st.session_state.cartas_player)  # Mano original
        hit(st.session_state.mazo, nueva_mano)  # Nueva mano
        
        # Agregar la nueva mano a la lista
        st.session_state.manos_player.append(nueva_mano)
        
        st.session_state.split = True
        st.session_state.splits_count += 1
        st.session_state.mano_activa = 0
        st.session_state.message = "Cartas divididas. Jugando mano 1"

def player_stand():
    """Jugador se planta"""
    if not st.session_state.game_over:
        if st.session_state.split:
            # Marcar mano actual como completada
            st.session_state.manos_completadas.append(st.session_state.mano_activa)
            
            # Si hay más manos por jugar
            if st.session_state.mano_activa < len(st.session_state.manos_player):
                st.session_state.mano_activa += 1
                st.session_state.message = f"Jugando mano {st.session_state.mano_activa + 1}"
                return
        
        # Turno del dealer
        dealer_play_sim(st.session_state.mazo, st.session_state.cartas_croupier,
                st.session_state.mazo_valores,
                hit_soft_17=st.session_state.dealer_hits_soft_17)
        
        if st.session_state.split:
            verificar_resultado_final()
        else:
            # Lógica normal para mano única
            valor_player, _ = contar_mano(st.session_state.cartas_player, st.session_state.mazo_valores)
            valor_dealer, _ = contar_mano(st.session_state.cartas_croupier, st.session_state.mazo_valores)
            
            if valor_dealer > 21:
                st.session_state.message = "¡El dealer se pasó! ¡Ganaste!"
                st.session_state.victory = True
            elif valor_dealer > valor_player:
                st.session_state.message = "El dealer gana."
                st.session_state.victory = False
            elif valor_player > valor_dealer:
                st.session_state.message = "¡Ganaste!"
                st.session_state.victory = True
            else:
                st.session_state.message = "¡Empate!"
                st.session_state.victory = None

            if not st.session_state.stats_recorded:
                if st.session_state.victory is True:
                    st.session_state.wins += 1
                elif st.session_state.victory is False:
                    st.session_state.losses += 1
                else:
                    st.session_state.pushes += 1
                st.session_state.stats_recorded = True
                
            st.session_state.game_over = True

# Layout principal
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Título
st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <h1 style="color: #FFD700; font-size: 48px; text-shadow: 3px 3px 6px rgba(0,0,0,0.8); margin: 0;">
        🃏 BLACKJACK TRAINER 🃏
    </h1>
    <p style="color: #FFD700; font-size: 18px; margin-top: 10px;">Practica tu estrategia básica</p>
</div>
""", unsafe_allow_html=True)

# ===== MESA DE JUEGO (una sola llamada) =====
game_started = st.session_state.get("game_started", False)
game_over    = st.session_state.get("game_over", False)
split_mode   = st.session_state.get("split", False)

# ---- Dealer ----
dealer_cards_html = ""
dealer_bubble = ""

if game_started:
    dealer_cards_html = f'<div class="cards-container">{mostrar_cartas_dealer()}</div>'
    if game_over:
        valor_dealer, _ = contar_mano(st.session_state.cartas_croupier,
                                      st.session_state.mazo_valores)
        dealer_bubble = f'<div class="speech-bubble small">{valor_dealer}</div>'
    elif st.session_state.cartas_croupier:
        visible = st.session_state.mazo_valores.get(st.session_state.cartas_croupier[0], 0)
        dealer_bubble = f'<div class="speech-bubble small">{visible}</div>'

dealer_section = f"""
<div class="dealer-area">
  <div class="dealer-label">🎯 DEALER</div>
  {dealer_cards_html}
  <div style="text-align:center; margin-top:.5rem;">{dealer_bubble}</div>
</div>
"""

# ---- Player ----
player_cards_block = ""
player_bubble = ""

if game_started:
    if split_mode:
        # Tu función ya devuelve el bloque HTML con manos divididas
        player_cards_block = mostrar_cartas_player()
        player_bubble = ""   # cada mano puede mostrar su propio valor
    else:
        player_cards_block = f'<div class="cards-container">{mostrar_cartas_player()}</div>'
        valor_player, _ = contar_mano(st.session_state.cartas_player,
                                      st.session_state.mazo_valores)
        player_bubble = f'<div class="speech-bubble small">{valor_player}</div>'

player_section = f"""
<div class="player-area">
  <div class="player-label">👤 JUGADOR</div>
  {player_cards_block}
  <div style="text-align:center; margin-top:.5rem;">{player_bubble}</div>
</div>
"""

# ---- Mesa completa ----
html_mesa = f"""
<div class="game-table">
  {dealer_section}
  {player_section}
</div>
"""

st.markdown(html_mesa, unsafe_allow_html=True)


# Mensaje de estado
st.markdown(f'<div class="status-message">{st.session_state.message}</div>', unsafe_allow_html=True)

# Controles del juego
st.markdown('<div class="game-controls">', unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("🎴 Nueva Mano", use_container_width=True):
        nueva_mano()
        st.rerun()

with col2:
    if st.button("👆 Pedir", use_container_width=True, disabled=st.session_state.game_over or not st.session_state.game_started):
        player_hit()
        st.rerun()

with col3:
    if st.button("✋ Plantarse", use_container_width=True, disabled=st.session_state.game_over or not st.session_state.game_started):
        player_stand()
        st.rerun()

with col4:
    mano_activa = obtener_mano_activa() if st.session_state.game_started else []
    can_double = (st.session_state.game_started and 
                  not st.session_state.game_over and 
                  len(mano_activa) == 2)
    if st.button("🤲 Doblar", use_container_width=True, disabled=not can_double):
        player_double()
        st.rerun()

with col5:
    mano_activa = obtener_mano_activa() if st.session_state.game_started else []
    can_split = (st.session_state.game_started and 
                 not st.session_state.game_over and 
                 len(mano_activa) == 2 and
                 st.session_state.splits_count < 3 and
                 is_pair(mano_activa[0], mano_activa[1]))
    if st.button("✂ Dividir", use_container_width=True, disabled=not can_split):
        player_split()
        st.rerun()

with col6:
    if st.button("🔄 Reiniciar", use_container_width=True):
        st.session_state.game_started = False
        st.session_state.mazo, st.session_state.mazo_valores = make_shoe(6)
        st.session_state.cartas_player = []
        st.session_state.cartas_croupier = []
        st.session_state.game_over = False
        st.session_state.message = "¡Presiona 'Nueva Mano' para empezar!"
        st.session_state.victory = False
        st.session_state.double = False
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar con estadísticas
with st.sidebar:
    #st.header("⚙️ Configuración")
    #st.session_state.ruta_imgs = st.text_input("Carpeta de imágenes", st.session_state.ruta_imgs)
    #st.session_state.dealer_hits_soft_17 = st.toggle("Dealer pega en 17 suave (H17)", value=st.session_state.dealer_hits_soft_17)

    st.header("📈 Estadísticas en vivo")

    # Métricas base
    if st.session_state.game_started:

        # --- Probabilidad de 10/J/Q/K
        p10 = prob_10_val(st.session_state.mazo)
        st.subheader("🎯 Próxima carta")
        st.metric("Prob. de 10/J/Q/K", f"{100*p10:.1f}%")
        st.progress(min(100, int(100*p10)))

        # Parte conteo cartas y sugerencias
        cartas_restantes = len([c for c in st.session_state.mazo if c])
        cartas_jugadas = []
        if st.session_state.cartas_player:
            cartas_jugadas.extend(st.session_state.cartas_player)
        if st.session_state.cartas_croupier and st.session_state.game_over:
            cartas_jugadas.extend(st.session_state.cartas_croupier)
        elif st.session_state.cartas_croupier:
            cartas_jugadas.append(st.session_state.cartas_croupier[0])

        conteo_running = contar_cartas(cartas_jugadas) if cartas_jugadas else 0
        mazos_restantes = cartas_restantes/52 if cartas_restantes>0 else 0
        true_count = (conteo_running/mazos_restantes) if mazos_restantes>0 else 0

        # --- Recomendación en vivo
        if st.session_state.cartas_player and st.session_state.cartas_croupier:
            carta_visible = st.session_state.cartas_croupier[0]
            mano_activa = (st.session_state.cartas_player
                           if st.session_state.mano_activa==0
                           else st.session_state.manos_player[st.session_state.mano_activa-1])
            try:
                sugerencia = estrategia_basica(true_count, mano_activa, carta_visible,
                                               st.session_state.mazo_valores,
                                               puede_split=(len(mano_activa)==2))
                st.info(f"🧠 Sugerencia (TC={true_count:.1f}): **{sugerencia.upper()}**")
            except Exception:
                pass

        # --- Simulación rápida del estado actual
        st.subheader("🧪 Simulación rápida")
        n_sims = st.slider("Simulaciones", 1000, 20000, 5000, 1000)
        accion = st.radio("Acción evaluada", ["Plantarse ahora", "Pedir 1 carta", "Doblar (1 carta)"], horizontal=False)

        if st.session_state.cartas_player and st.session_state.cartas_croupier:
            ph = (st.session_state.cartas_player
                  if st.session_state.mano_activa==0
                  else st.session_state.manos_player[st.session_state.mano_activa-1])
            dh = st.session_state.cartas_croupier.copy()
            deck = st.session_state.mazo

            akey = "stand" if accion=="Plantarse ahora" else ("hit1" if accion=="Pedir 1 carta" else "double")
            res = sim_action(deck, ph, dh, st.session_state.mazo_valores,
                             action=akey,
                             hit_soft_17=st.session_state.dealer_hits_soft_17,
                             n=n_sims)
            c1, c2, c3 = st.columns(3)
            c1.metric("Win %", f"{res['win%']:.1f}%")
            c2.metric("Push %", f"{res['push%']:.1f}%")
            c3.metric("Lose %", f"{res['lose%']:.1f}%")

        st.subheader("➕ Conteo Cartas")

        colA, colB, colC = st.columns(3)
        colA.metric("Running", conteo_running)
        colC.metric("True", f"{true_count:.1f}")

        # Distribución por valor
        st.subheader("📊 Distribución Cartas Restantes")

        dist = probs_por_valor(st.session_state.mazo)
        df = pd.DataFrame({"valor": list(dist.keys()), "probabilidad": [100*v for v in dist.values()]})
        st.bar_chart(df.set_index("valor"))

    else:
        st.info("Inicia una mano para ver estadísticas.")

    st.header("📉 Historial de sesión")
    jugadas = st.session_state.wins + st.session_state.losses + st.session_state.pushes
    wr = (100*st.session_state.wins/jugadas) if jugadas>0 else 0
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Jugadas", jugadas)
    c2.metric("Wins", st.session_state.wins)
    c3.metric("Pushes", st.session_state.pushes)
    c4.metric("Losses", st.session_state.losses)
    st.caption(f"Winrate sesión: **{wr:.1f}%**")
