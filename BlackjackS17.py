"""
Módulo de Blackjack
Contiene todas las funciones necesarias para jugar blackjack con conteo de cartas Hi-Lo
"""

# BlackjackS17.py
import random
from collections import Counter

def make_shoe(num_mazos=1):
    """Crea y baraja un zapato con mazos de cartas"""

    # Configuración del juego
    numeracion = ["A"] + [str(i) for i in range(2, 11)] + ["J", "Q", "K"]
    suits = [chr(i) for i in range(9828, 9832)]

    # Valores de las cartas
    valores = {"A": 1, "J": 10, "Q": 10, "K": 10}
    for i in range(2, 11):
        valores[str(i)] = i

    # Crear el mazo usando dictionary comprehension
    mazo_valores = {f"{n} {s}": valores[n] for n in numeracion for s in suits}
    mazo_base = list(mazo_valores.keys())

    mazo = mazo_base.copy() * num_mazos
    random.shuffle(mazo)
    return mazo, mazo_valores


def hit(mazo, lista):
    """Toma una carta del mazo y la agrega a la lista"""
    if mazo:
        carta = mazo.pop()
        lista.append(carta)
    return carta


def is_pair(carta1, carta2):
    """Verificar si dos cartas tienen el mismo valor"""
    valor1 = 1 if carta1.split()[0] == "A" else carta1.split()[0]
    valor2 = 1 if carta2.split()[0] == "A" else carta2.split()[0]
    return valor1 == valor2 or (valor1 in ["J", "Q", "K", "10"] and valor2 in ["J", "Q", "K", "10"])


def contar_mano(mano, mazo_valores):
    """Cuenta el valor de una mano y retorna el total y número de ases"""
    total = 0
    num_ases = 0

    for carta in mano:
        valor_carta = carta.split()[0]
        if valor_carta == "A":
            num_ases += 1
        else:
            total += mazo_valores[carta]

    # Sumar los ases de manera óptima
    for _ in range(num_ases):
        if total + 11 <= 21:
            total += 11
        else:
            total += 1

    return total, num_ases


def contar_cartas(mano):
    """Sistema de conteo Hi-Lo"""
    lo_hi = {"A": -1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1,
             "7": 0, "8": 0, "9": 0, "10": -1, "J": -1, "Q": -1, "K": -1}

    total = 0
    for carta in mano:
        valor_carta = carta.split()[0]
        total += lo_hi[valor_carta]

    return total


def estrategia_basica(true_count, cartas_p, carta_visible, mazo_valores, puede_split=False):
    """Estrategia básica de blackjack con ajustes Hi-Lo"""
    # Hard totals (sin as usable)
    ESTRATEGIA_BASICA_HARD = {
        8: {c: "hit" for c in range(2, 12)},
        9: {c: "hit" for c in range(2, 12) if c not in [5, 6]},
        10: {c: "double" for c in range(2, 10)},
        11: {c: "double" for c in range(2, 11)},
        12: {c: "hit" for c in range(2, 12) if c not in [4, 5, 6]},
        13: {c: "stand" for c in range(2, 7)},
        14: {c: "stand" for c in range(2, 7)},
        15: {c: "stand" for c in range(2, 7)},
        16: {c: "stand" for c in range(2, 7)},
        17: {c: "stand" for c in range(2, 12)}
    }

    # Ajustes basados en true count
    ESTRATEGIA_BASICA_HARD[8].update(
        {6: "double" if true_count >= 2 else "hit"})
    ESTRATEGIA_BASICA_HARD[9].update(
        {5: "double", 6: "double", 2: "double" if true_count >= 1 else "hit", 7: "double" if true_count >= 3 else "hit"})
    ESTRATEGIA_BASICA_HARD[10].update(
        {10: "hit", 11: "double" if true_count >= 4 else "hit"})
    ESTRATEGIA_BASICA_HARD[11].update(
        {11: "double" if true_count >= 1 else "hit"})
    ESTRATEGIA_BASICA_HARD[12].update({c: "stand" for c in range(4, 7)})
    ESTRATEGIA_BASICA_HARD[13].update({d: "hit" for d in range(7, 12)})
    ESTRATEGIA_BASICA_HARD[14].update({d: "hit" for d in range(7, 12)})
    ESTRATEGIA_BASICA_HARD[15].update({d: "hit" for d in range(7, 12)})
    ESTRATEGIA_BASICA_HARD[16].update({d: "hit" for d in range(7, 12)})

    ESTRATEGIA_BASICA_HARD[12].update({2: "stand" if true_count >= 3 else "hit", 3: "stand" if true_count >= 2 else "hit",
                                      4: "stand" if true_count >= -1 else "hit", 5: "stand" if true_count >= -2 else "hit", 6: "stand" if true_count >= -1 else "hit"})
    ESTRATEGIA_BASICA_HARD[13].update(
        {2: "stand" if true_count >= -1 else "hit", 3: "stand" if true_count >= -2 else "hit"})
    ESTRATEGIA_BASICA_HARD[15].update(
        {10: "hit" if true_count >= 4 else "stand"})
    ESTRATEGIA_BASICA_HARD[16].update({9: "hit" if true_count >= 5 else "stand",
                                      10: "hit" if true_count >= 0 else "stand", 11: "hit" if true_count >= 3 else "stand"})

    # Soft totals (con as usable)
    ESTRATEGIA_BASICA_SOFT = {
        13: {c: "hit" for c in range(2, 12) if c not in [5, 6]},
        14: {c: "hit" for c in range(2, 12) if c not in [5, 6]},
        15: {c: "hit" for c in range(2, 12) if c not in [4, 5, 6]},
        16: {c: "hit" for c in range(2, 12) if c not in [4, 5, 6]},
        17: {c: "hit" for c in range(2, 12) if c not in [3, 4, 5, 6]},
        18: {2: "stand", 3: "double", 4: "double", 5: "double", 6: "double", 7: "stand", 8: "stand", 9: "hit", 10: "hit", 11: "hit"},
        19: {c: "stand" for c in range(2, 12) if c not in [6]},
        20: {c: "stand" for c in range(2, 12)},
        21: {c: "stand" for c in range(2, 12)}
    }

    # Completar estrategias soft
    ESTRATEGIA_BASICA_SOFT[13].update({5: "double", 6: "double"})
    ESTRATEGIA_BASICA_SOFT[14].update({5: "double", 6: "double"})
    ESTRATEGIA_BASICA_SOFT[15].update({c: "double" for c in range(4, 7)})
    ESTRATEGIA_BASICA_SOFT[16].update({c: "double" for c in range(4, 7)})
    ESTRATEGIA_BASICA_SOFT[17].update({c: "double" for c in range(3, 7)})
    ESTRATEGIA_BASICA_SOFT[19].update({6: "double"})

    # Pares para split
    ESTRATEGIA_BASICA_PARES = {
        (2, 2): {c: "split" for c in range(2, 8)},
        (3, 3): {c: "split" for c in range(2, 8)},
        (4, 4): {c: "hit" for c in range(2, 12) if c not in [5, 6, 7]},
        (5, 5): {c: "double" for c in range(2, 10)},
        (6, 6): {c: "split" for c in range(2, 8)},
        (7, 7): {c: "split" for c in range(2, 8)},
        (8, 8): {c: "split" for c in range(2, 12)},
        (9, 9): {c: "hit" for c in range(2, 12) if c not in [7, 10, 11]},
        (10, 10): {c: "stand" for c in range(2, 12)},
        (1, 1): {c: "split" for c in range(2, 12)}
    }

    # Completar estrategias de pares
    ESTRATEGIA_BASICA_PARES[(2, 2)].update({c: "hit" for c in range(8, 12)})
    ESTRATEGIA_BASICA_PARES[(3, 3)].update({c: "hit" for c in range(8, 12)})
    ESTRATEGIA_BASICA_PARES[(4, 4)].update({c: "split" for c in range(5, 8)})
    ESTRATEGIA_BASICA_PARES[(5, 5)].update({10: "hit", 11: "hit"})
    ESTRATEGIA_BASICA_PARES[(6, 6)].update({c: "hit" for c in range(8, 12)})
    ESTRATEGIA_BASICA_PARES[(7, 7)].update({c: "hit" for c in range(8, 12)})
    ESTRATEGIA_BASICA_PARES[(9, 9)].update({c: "stand" for c in [7, 10, 11]})

    carta_dealer = 11 if mazo_valores[carta_visible] == 1 else mazo_valores[carta_visible]
    total, ases = contar_mano(cartas_p)

    if is_pair(cartas_p[0], cartas_p[1]) and puede_split:
        par = (mazo_valores[cartas_p[0]], mazo_valores[cartas_p[0]])
        recomendacion = ESTRATEGIA_BASICA_PARES[par][carta_dealer]
    elif ases == 1 and len(cartas_p) == 2:
        recomendacion = ESTRATEGIA_BASICA_SOFT[total][carta_dealer]
    elif 8 <= total <= 17:
        recomendacion = ESTRATEGIA_BASICA_HARD[total][carta_dealer]
    elif total > 17:
        recomendacion = "stand"
    elif total < 8:
        recomendacion = "hit"

    return recomendacion


# ---- Helpers estadísticos y simulación ----
def _valor(carta: str) -> str:
    return carta.split()[0]

def conteo_por_valor(mazo_restante):
    vals = [_valor(c) for c in mazo_restante]
    return Counter(vals)

def prob_10_val(mazo_restante):
    n = len(mazo_restante)
    if n == 0: return 0.0
    cnt = conteo_por_valor(mazo_restante)
    return (cnt.get('10',0) + cnt.get('J',0) + cnt.get('Q',0) + cnt.get('K',0)) / n

def probs_por_valor(mazo_restante):
    n = len(mazo_restante)
    orden = ['A'] + [str(i) for i in range(2,11)] + ['J','Q','K']
    if n == 0:
        return {v:0.0 for v in orden}
    cnt = conteo_por_valor(mazo_restante)
    return {v: cnt.get(v,0)/n for v in orden}

def contar_mano_detallado(mano, mazo_valores):
    # Total con As como 1 (duro); marca si puede ser soft (+10)
    total_sin_ases = sum(mazo_valores[c] for c in mano if _valor(c) != "A")
    ases = sum(1 for c in mano if _valor(c) == "A")
    total_duro = total_sin_ases + ases
    is_soft = ases > 0 and (total_duro + 10) <= 21
    total = total_duro + 10 if is_soft else total_duro
    return total, ases, is_soft

def dealer_play_sim(mazo_local, mano_dealer, mazo_valores, hit_soft_17=False):
    # Simula el turno del dealer (H17 opcional)
    while True:
        total, ases, is_soft = contar_mano_detallado(mano_dealer, mazo_valores)
        if total < 17 or (hit_soft_17 and total == 17 and is_soft):
            hit(mazo_local, mano_dealer)
        else:
            break
    return mano_dealer

def resolver(ph, dh, mazo_valores):
    vp, _ = contar_mano(ph, mazo_valores)
    vd, _ = contar_mano(dh, mazo_valores)
    if vp > 21: return -1  # pierde
    if vd > 21: return  1  # gana
    if vp > vd:  return  1
    if vp < vd:  return -1
    return 0  # push

def sim_action(current_deck, player_hand, dealer_hand, mazo_valores,
               action="stand", hit_soft_17=False, n=5000):
    wins = losses = pushes = 0
    for _ in range(n):
        mazo_local = current_deck.copy()
        random.shuffle(mazo_local)

        ph = player_hand.copy()
        dh = dealer_hand.copy()

        if action == "hit1":
            hit(mazo_local, ph)
        elif action == "double":
            if len(ph) == 2:
                hit(mazo_local, ph)

        dealer_play_sim(mazo_local, dh, mazo_valores, hit_soft_17)
        r = resolver(ph, dh, mazo_valores)
        if r == 1: wins += 1
        elif r == -1: losses += 1
        else: pushes += 1

    total = max(1, wins+losses+pushes)
    return {
        "win%": 100*wins/total,
        "push%": 100*pushes/total,
        "lose%": 100*losses/total
    }

# (Opcional) Exportar explícitamente la API pública
__all__ = [
    # existentes:
    "make_shoe", "hit", "contar_mano", "contar_cartas", "estrategia_basica", "is_pair",
    # nuevos:
    "conteo_por_valor", "prob_10_val", "probs_por_valor",
    "contar_mano_detallado", "dealer_play_sim", "resolver", "sim_action"
]