#!/usr/bin/python3
import smtplib, ssl, re, sqlite3, datetime,subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import CPlib as lib

#import ALLSite as html
Visited_Sites = ""
html = """
<html>
  <head></head>
  <body>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <table style="width: 708px; height: 97px;" border="3">
    <tbody>
        <tr style="height: 36px;">
        <td style="width: 148.95px; height: 36px; text-align: center;"><span style="color: #ff0000;">Moteur de recherche</span></td>
        <td style="width: 172.083px; text-align: center;"><span style="color: #ff0000;">P&eacute;riode de consultation</span></td>
        <td style="width: 170.8px; height: 36px; text-align: center;"><span style="color: #ff0000;">Dur&eacute;e de consultation</span></td>
        <td style="width: 184.167px; height: 36px; text-align: center;"><span style="color: #ff0000;">URL des sites consult&eacute;es</span></td>
        </tr>
"""
# on rentre les renseignements pris sur le site du fournisseur
smtp_address = 'smtp.gmail.com'
smtp_port = 587
# on rentre les informations sur notre adresse e-mail
email_address = 'AzerTuiledelaPsy4A@gmail.com'
email_password = 'teZ49pR8qzamTPJ'
#information sur l'adresse mail qui reçoit
email_receiver = 'adamakkouche42@yahoo.fr'
# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Link"
msg['From'] = email_address
msg['To'] = email_receiver
#Obtention du fichier default
path_to_file = lib.path_firefox_history()
if(path_to_file != 0):#il y'a un moteur de recherche firefox on contruit la base de données, il faut le faire une seul fois
    for path in path_to_file:
        pieces = path.split('/')
        del pieces[len(pieces) - 1]
        path_to_sql_database = "/".join(pieces) + "/History.db" #attention en C à bien mettre r" "
        con = sqlite3.connect(path_to_sql_database)
        c = con.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS visits([visit_date] TEXT,[visit_duration] TEXT,[url] TEXT) ''')#assuming that visit time are save in terms of string
        con.commit()
path_to_file = path_to_file + lib.path_others_history()
#Connection à la base sql et obtention de l'historique
for path in path_to_file:
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    if("firefox" in path):
        rows = cursor.execute("SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch','localtime'), moz_places.url, '00:00:00' FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id AND (SELECT(strftime('%s','now') -(moz_historyvisits.visit_date/1000000)) < 86400)").fetchall()
    else:
        rows = cursor.execute("SELECT datetime(visits.visit_time / 1000000 - 11644473600,'unixepoch','localtime'), urls.url, (visits.visit_duration / 1000000 /3600) || ':' || strftime('%M:%S', visits.visit_duration/1000000/86400.0) FROM urls, visits WHERE urls.id = visits.url AND (SELECT(strftime('%s','now') - (visits.visit_time/1000000 - 11644473600)) < 86400)").fetchall()
    Dic = {}
    for url in rows:
        url_list = url[1].split("/")
        if(url_list[2] not in Dic):
            Dic.update({url_list[2]:[url[0],url[2]]})
        else:
            Dic[url_list[2]][1] = lib.time_addition(Dic[url_list[2]][1],url[2])
    for key in Dic.keys():#vérifier que /home/akkouche/.config/google-chrome/Default/History le nom navigateur est toujours à la troisième position
        html = html + f"""
                <tr style="height: 29px;">
                <td style="width: 148.95px; height: 10px; text-align: center;">{path.split('/')[4]}</td>
                <td style="width: 172.083px; text-align: center;">{Dic[key][0]}</td>
                <td style="width: 170.8px; height: 10px; text-align: center;">{Dic[key][1]}</td>
                <td style="width: 184.167px; height: 10px; text-align: center;">{key}</td>
                </tr>"""
# Create the body of the message (a plain-text and an HTML version).
text = ""
html = html + """
    </tbody>
    </table>
    <p>&nbsp;</p>
</body>
</html>
"""
# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Send the message via local SMTP server.
mail = smtplib.SMTP(smtp_address, smtp_port)
mail.ehlo()

mail.starttls()

mail.login(email_address, email_password)
mail.sendmail(email_address, email_receiver, msg.as_string())
mail.quit()
#Pour chrome contrairement à firefox il semblerait que l'on est un problème lorsque on veux récupérer les élements de la ase sql
