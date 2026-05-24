import os
from twilio.rest import Client

def send_sms(phone_number, code):
    """
    Envoyer un code par SMS avec Twilio
    """
    try:
        # Récupérer les identifiants Twilio
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_phone = os.environ.get('TWILIO_PHONE_NUMBER')
        
        # Vérifier que Twilio est configuré
        if not all([account_sid, auth_token, twilio_phone]):
            print("⚠️ Twilio non configuré - Mode développement")
            print(f"📱 Code SMS (DEV) : {code}")
            print(f"📞 Pour : {phone_number}")
            return True
        
        # Nettoyer le numéro de téléphone
        # Enlever tous les caractères non numériques
        clean_number = ''.join(filter(str.isdigit, phone_number))
        
        # Ajouter l'indicatif +225 si nécessaire (Côte d'Ivoire)
        if not clean_number.startswith('225') and len(clean_number) == 10:
            clean_number = '225' + clean_number
        
        # Formater pour Twilio
        formatted_number = f"+{clean_number}"
        
        # Initialiser le client Twilio
        client = Client(account_sid, auth_token)
        
        # Envoyer le SMS
        message = client.messages.create(
            body=f"🔐 Votre code de vérification Herbier est : {code}. Valable 10 minutes.",
            from_=twilio_phone,
            to=formatted_number
        )
        
        print(f"✅ SMS envoyé à {formatted_number}")
        print(f"📨 SID: {message.sid}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur envoi SMS: {e}")
        return False

def send_sms_development(phone_number, code):
    """Version de développement : affiche dans la console"""
    print("\n" + "="*50)
    print(f"📱 CODE SMS (DEV) : {code}")
    print(f"📞 Pour : {phone_number}")
    print("="*50 + "\n")
    return True
