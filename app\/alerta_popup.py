from plyer import notification

def emitir_popup(empresa, noticia, sentimento):
    titulo = f"{empresa} → {sentimento}"
    corpo = f"{noticia}"

    notification.notify(
        title=titulo,
        message=corpo,
        timeout=5  # duração em segundos
    )