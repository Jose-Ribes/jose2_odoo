def calcular_consumo_vuelo(peso_total, es_vip=False):
    """
    Calcula el porcentaje de batería que consumirá el vuelo.
    Lógica:
    - Coste fijo de despegue/aterrizaje: 5%
    - Coste por peso: 1.2% por cada kilo.
    - Descuento VIP: Si el cliente es VIP, el dron va en 'modo ahorro' (10% menos de consumo).
    """
    
    # Consumo base
    consumo = 5.0 + (peso_total * 1.2)
    
    # Aplicar reducción si es VIP (opcional para el ejercicio)
    if es_vip:
        consumo = consumo * 0.9
        
    return round(consumo, 2)

def validar_estado_bateria(bateria_actual, consumo_estimado):
    """
    Verifica si el dron tiene energía suficiente.
    Retorna True si es apto, False si no.
    """
    return bateria_actual >= consumo_estimado