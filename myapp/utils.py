from django.core.mail import send_mail

def send_code_email(Username, Code, From_email, To_email):
    send_mail(
        "Código de verificação",
        f"Olá, {Username}! Seu código de verificação é: {Code}",
        From_email,
        [To_email],
    )