import numpy as np
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.auth

# Función para leer los contactos de un archivo, con el formato 'nombre mail@dominio'
def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

# Función para leer el template del mensaje
def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

# Obtén las credenciales OAuth 2.0
credentials, project_id = google.auth.default()

# Define la dirección de correo y solicita la contraseña al usuario
MY_ADDRESS = credentials.email
PASSWORD = input("Password: ")

# Obtiene los nombres y correos electrónicos de los contactos
names, emails = get_contacts('contacts.txt')

# Lee el template del mensaje
message_template = read_template('message.txt')

# Configura el servidor SMTP
smtp_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
smtp_server.starttls()

# Inicia sesión en el servidor SMTP
smtp_server.login(MY_ADDRESS, PASSWORD)

# Envía el correo a cada contacto
for name, email in zip(names, emails):
    msg = MIMEMultipart()

    # Personaliza el mensaje con el nombre del contacto
    message = message_template.substitute(PERSON_NAME=name.title())

    # Configura los parámetros del correo
    msg['From'] = MY_ADDRESS
    msg['To'] = email
    msg['Subject'] = "SMTP"

    # Agrega el cuerpo del mensaje
    msg.attach(MIMEText(message, 'plain'))

    # Envía el mensaje
    smtp_server.send_message(msg)

    del msg

# Cierra la conexión con el servidor SMTP
smtp_server.quit()
