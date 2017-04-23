# -*- coding: utf-8 -*-
import argparse
from getpass import getpass
import mechanize
from bs4 import BeautifulSoup
import ssl
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
parser = argparse.ArgumentParser(description="Login a Academico.")
parser.add_argument("usuario")
args = parser.parse_args()
args.password = getpass("Ingrese su contraseña: ")
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_referer(False)
br.set_handle_refresh(False)
br.addheaders = [('User-agent', 'Firefox')]
r = br.open("https://webapp.upeu.edu.pe/academico/login.jsp")
print "==============================================================="
print r.geturl()
print "==============================================================="
br.select_form('datos')
br.form['f_usuario'] = args.usuario
br.form['f_password'] = args.password
br.submit()
r = br.open("https://webapp.upeu.edu.pe/academico/portales/alumno/cursos.jsp")
print "==============================================================="
print r.geturl()
print "==============================================================="
f = open(raw_input("Ingrese el nombre del archivo .txt "), 'w')
for link in br.links():
    if link.text and 'Temas' == link.text:
        br.select_form("formulario")
        br.form.find_control('x').readonly = False
        br.form['x'] = link.attrs[1][1][11:43]
        br.form.find_control('y').readonly = False
        br.form['y'] = link.attrs[1][1][46:62]
        br.form.action = 'https://webapp.upeu.edu.pe/academico/portales/alumno/ver_nota.jsp'
        r = br.submit()
        soup = BeautifulSoup(br.response().read(), "html.parser")
        title = soup.find_all('table')[5].find_all('b')[
            0].get_text().split("\n")
        f.write("############################################################\n")
        f.write("Curso: " + title[0])
        f.write(title[1].lstrip())
        f.write("\n")
        f.write("==========\nNOTAS:\n==========\n")
        print title[0]
        temp = soup.find_all('table')[7].find_all('tr')
        for row in temp[1:len(temp) - 1]:
            column = row.find_all('td')
            f.write(column[0].get_text())
            f.write(column[2].get_text())
            f.write(column[3].get_text())
            f.write("\t")
            f.write(column[1].b.get_text())
            f.write("\n")
        f.write(temp[len(temp) - 1].td.get_text())
        f.write(temp[len(temp) - 1].th.get_text())
        f.write("\n")
        r = br.back()
    if link.text and 'Asistencia' == link.text:
        f.write("==========\nASISTENCIA:\n==========\n")
        r = br.follow_link(link)
        soup = BeautifulSoup(br.response().read(), "html.parser")
        temp = soup.find_all('table')
        for row in temp[4].find_all(
            'tr',
            {"style": "background-color:#FFF5E7;"}
        ):
            column = row.find_all('td')
            if column[2].img.get('src') == 'img/P.gif':
                pass
            elif column[2].img.get('src') == 'img/F.gif':
                f.write(column[1].get_text())
                f.write("\tFalta\t")
                if len(column[2]) > 3:
                    f.write(column[2].input.get('value'))
                f.write("\n")
            elif column[2].img.get('src') == 'img/T.gif':
                f.write(column[1].get_text())
                f.write("\tTarde\t")
                if len(column[2]) > 3:
                    f.write(column[2].input.get('value'))
                f.write("\n")
            else:
                print column[1].get_text(), column[2].img.get('src')
        r = br.back()
f.close()
