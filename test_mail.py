#! /usr/bin/python3
import sys, getopt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

settings={
    'smtp_server':      None,
    'port':             None,
    'protocol':         None,
    'username':         None,
    'password':         None,
    'self_signed_ssl':  None,
    'from':             None,
    'to':               None,
    'subject':          None,
}

def syntax():
    print ("test_mail.py")
    print ("------------")
    print ("Platformy: Linux, Windows")
    print ("Popis:     Posilani emailu")
    print ("")
    print ("Syntax:")
    print ("[   --smtp_server]     - Postovni server")
    print ("[-P|--port]            - Komunikacni port")
    print ("[   --auth typ]        - basic | ssl | starttls")
    print ("[-u|-username user]    - uzivatel")
    print ("[-p|--password pass]   - heslo")
    print ("[   --signed_ssl ]     - SSL certifikat musi byt spravne podpsany")
    print ("[   --selfsigned_ssl ] - SSL certifikat muze byt podepsany self")
    print ("[-f|--from email]      - Od")
    print ("[-t|--to email]        - Adresat (oddeleno , bez mezery)")
    print ("[   --subject subject] - Predmet ")
    print ("[-h|--help]            - Napoveda")
    print ("Obsah zpravy z STDIN")
    sys.exit(0)

def parse_args(argv):
    global settings
    try:
        opts, _ = getopt.getopt(argv, "P:u:f:t:p:h",
        ["smtp_server=", "port=", "auth=", "username=", "password=", "signed_ssl", "selfsigned_ssl",
        "from=", "to=", "subject=", "help"
        ])

    except getopt.GetoptError as e:
        print ('>>>> ERROR: %s' % str(e))
        syntax()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            syntax()
        elif opt in ("-t", "--to"):
            settings['to'] = arg
        elif opt in ("--smtp_server"):
            settings['smtp_server'] = arg
        elif opt in ("--port", "-P"):
            if(arg.isdigit()):
                settings['port'] = int(arg)
            else:
                print(f"Port {arg} neni cislo")
                sys.exit (1)
        elif opt in ("-f", "--from"):
            settings['from'] = arg
        elif opt in ("--username", "-u"):
            settings['username'] = arg
        elif opt in ("--auth"):
            a=arg.upper()
            if(a in ('BASIC', 'SSL', 'STARTTLS')):
                settings['protocol'] = a
            else:
                print(f"Neznamy typ protokolu autentizace")
                sys.exit (1)
        elif opt in ("--password","-p"):
            settings['password'] = arg
        elif opt in ("--signed_ssl"):
            settings['self_signed_ssl'] = False
        elif opt in ("--selfsigned_ssl"):
            settings['self_signed_ssl'] = True
        elif opt in ("--subject"):
            settings['subject'] = arg

def sys_exit(rc, msg):
    print (msg)
    sys.exit(rc)

def check_params():
    global settings
    if (settings['smtp_server']==None): sys_exit(3, "Nezadan smtp_server")
    if (settings['port']==None): sys_exit(3, "Nezadan SMTP port")
    if (settings['protocol']==None): sys_exit(3, "Nezadan auth protocol")
    if (not settings['protocol'] == "BASIC"):
        if (settings['username']==None): sys_exit(3, "Nezadan uzivatel")
        if (settings['password']==None): sys_exit(3, "Nezadano heslo")
    if (settings['from']==None): sys_exit(3, "Nezadan odesilatel")
    if (settings['subject']==None): sys_exit(3, "Nezadan subject")
    if (settings['to']==None): sys_exit(3, "Nezadan adresar")

def process_email(text):
    global settings
    messages=[]
    msg = MIMEMultipart()
    msg['From'] = settings['from']
    msg['To'] = settings['to']
    msg['Subject']=settings['subject']

    message = f"<HTML>\n<HEAD>\n<TITLE>{settings['subject']}</TITLE>"
    message+=f"<META HTTP-EQUIV=\'Content-Type\' CONTENT=\'text/html\'>\n"
    message+="</HEAD>\n<BODY>\n"
    message+=text
    message+="</BODY></HTML>"
    msg.attach(MIMEText(message, 'html'))
    messages.append(msg)

    s=connect_to_smtp()

    for m in (messages):
        try:
            s.sendmail(settings['from'], settings['to'], m.as_string())
        except (smtplib.SMTPDataError, smtplib.SMTPRecipientsRefused) as e:
            print (str(e))
        except:
            print ("Unknown error:", sys.exc_info()[0])

    disconnect_from_stmp(s)

def connect_to_smtp():
    global settings

    if (settings['protocol'].upper() == "BASIC"):
        try:
            s = smtplib.SMTP(settings['smtp_server'] , str(settings['port']))
        except smtplib.SMTPException as e:
            print (e)
            sys.exit(1)
        return s

    elif (settings['protocol'].upper() == "SSL"):
        server=settings['smtp_server'] + ":" + str(settings['port'])
        try:
            s = smtplib.SMTP_SSL(server)
            if (settings['username']  and settings['password'] ):
                s.login(settings['username'], settings['password'])
        except smtplib.SMTPException as e:
            print (e)
            sys.exit(1)

        return s

    elif (settings['protocol'].upper() == "STARTTLS"):
        server=settings['smtp_server'] + ":" + str(settings['port'])
        try:
            s = smtplib.SMTP(settings['smtp_server'] , str(settings['port']))
            s.ehlo() 
            s.starttls()
            s.ehlo()
            if (settings['username']  and settings['password'] ):
                s.login(settings['username'], settings['password'])
        except smtplib.SMTPException as e:
            print (e)
            sys.exit(1)
        return s

def disconnect_from_stmp(connection):
    if connection is not None:
        connection.quit()

def main(script, argv):
    parse_args(argv)
    check_params()

    # precteni emailze stdin
    text=""
    for line in sys.stdin:
        text+=line
    text=text.strip('"')
    process_email(text)

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
