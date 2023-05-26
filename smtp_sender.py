import numpy as np
import smtplib # library for smtp protocol
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Funcion para leer los contactos de un archivo, con el formato 'nombre mail@dominio'
def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

# Funcion para 
def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

# Definimos el mail y pedimos al usuario el ingreso de la contraseña
MY_ADDRESS = 'franco.riba@mi.unc.edu.ar'
PASSWORD = input("My password: ")

names, emails = get_contacts('contacts.txt')
message_template = read_template('message.txt')

# Configuramos los parametros para el SMTP-Server
s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(MY_ADDRESS, PASSWORD)

# Enviamos el mail a cada contacto
for name, email in zip(names, emails):
    msg = MIMEMultipart()       # Crea el mensaje

    # add in the actual person name to the message template
    message = message_template.substitute(PERSON_NAME=name.title())

    # Configuramos los parametros del mail
    msg['From']=MY_ADDRESS
    msg['To']=email
    msg['Subject']="SMTP"

    # Agregamos el cuerpo del mensaje
    msg.attach(MIMEText(message, 'plain'))

    # Enviamos el mensaje
    s.send_message(msg)
    
    del msg