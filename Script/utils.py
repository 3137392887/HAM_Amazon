def convertir_usd_a_cop(precio_usd, tasa_cambio=4000):
    """
    Convierte un precio en USD a COP usando una tasa fija o dinámica.
    """
    try:
        return round(float(precio_usd) * tasa_cambio, 2)
    except (TypeError, ValueError):
        return None
