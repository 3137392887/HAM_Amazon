import smtplib
import logging
import os
from email.message import EmailMessage
from config import GMAIL_USUARIO, GMAIL_CLAVE


def enviar_resumen_por_correo(destinatario, ruta_archivo):
    remitente = GMAIL_USUARIO
    clave_app = GMAIL_CLAVE  
    

    asunto = "Resumen de productos más baratos en Amazon"
    cuerpo = "Adjunto encontrarás el resumen con los productos más económicos encontrados por el robot."

    # Crear mensaje
    mensaje = EmailMessage()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.set_content(cuerpo)

    # Adjuntar archivo
    with open(ruta_archivo, "rb") as f:
        contenido = f.read()
        nombre_archivo = os.path.basename(ruta_archivo)
        mensaje.add_attachment(contenido, maintype="application", subtype="octet-stream", filename=nombre_archivo)

    # Enviar correo
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remitente, clave_app)
            smtp.send_message(mensaje)
        print("Correo enviado exitosamente.")
        logging.info("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        logging.info(f"Error al enviar el correo: {e}")