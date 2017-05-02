# -*- coding: utf-8 -*-
import argparse
from getpass import getpass
import mechanize
from bs4 import BeautifulSoup
import ssl
import openpyxl
import sys
import re
import time
from urllib2 import HTTPError
import os


def get_notas(browser):
    text = ""
    browser.open(
        "https://webapp.upeu.edu.pe/academico/datos_alumno/cursos/cursos.jsp")
    for link in browser.links():
        # por cursos
        if re.match("Nota:", link.text):
            browser.follow_link(link)
            soup = BeautifulSoup(browser.response().read(), "html.parser")
            get_course = soup.find_all('table')[5].find_all('b')[
                0].get_text().split("\n")
            text = text + "############################################################\n" +\
                "Curso: " + \
                get_course[0] + \
                get_course[1].lstrip() + "\n" + \
                "==========\nNOTAS:\n==========\n"
            notas_table = soup.find_all('table')[7].find_all('tr')
            for row in notas_table[1:len(notas_table) - 1]:
                column = row.find_all('td')
                text = text + \
                    column[0].get_text() + \
                    column[2].get_text() + \
                    column[3].get_text() + "\t" + \
                    column[1].a.get_text() + "\n"

            text = text + \
                notas_table[len(notas_table) - 1].td.get_text() + \
                notas_table[len(notas_table) - 1].th.get_text() + "\n"
            browser.back()
    return text


def get_asistencia(browser):
    browser.open(
        "https://webapp.upeu.edu.pe/academico/datos_alumno/alum_cursos/cursos.jsp")
    text = ""
    for link in browser.links():
        if "Asistencia" == link.text:
            text = text + "==========\nASISTENCIA:\n==========\n"
            browser.follow_link(link)
            soup = BeautifulSoup(browser.response().read(), "html.parser")
            for row in soup.find_all('table')[4].find_all(
                'tr',
                {"style": "background-color:#FFF5E7;"}
            ):
                column = row.find_all('td')
                if column[2].img.get('src') == 'img/P.gif':
                    pass
                elif column[2].img.get('src') == 'img/F.gif':
                    text = text + column[1].get_text() + "\tFalta\t"
                    if len(column[2]) > 3:
                        text = text + column[2].input.get('value')
                    text = text + "\n"
                elif column[2].img.get('src') == 'img/T.gif':
                    text = text + column[1].get_text() + "\tTarde\t"
                    if len(column[2]) > 3:
                        text = text + column[2].input.get('value')
                    text = text + "\n"
                else:
                    print column[1].get_text(), column[2].img.get('src')
            browser.back()
    return text


def buscar(browser, cod):
    browser.open(
        "https://webapp.upeu.edu.pe/academico/datos_alumno/buscar/buscar.jsp")
    soup = BeautifulSoup(browser.response().read(), "html.parser")
    f = soup.find("form", {"name": "datos2"})
    # archivo
    new = BeautifulSoup(
        "<input type='text' name='f_buscar_1' value='%s'/>" % cod).find("input")
    f.insert(0, new)
    html = str(f)
    resp = mechanize.make_response(html, [("Content-Type", "text/html")],
                                   browser.geturl(), 200, "OK")
    browser.set_response(resp)
    browser.select_form("datos2")
    browser.submit()
    browser.select_form("datos1")
    browser.submit()


def login(browser):
    parser = argparse.ArgumentParser(description="Login a Academico.")
    parser.add_argument("usuario")
    args = parser.parse_args()
    args.password = getpass("Ingrese su contraseña: ")
    browser.set_handle_robots(False)
    browser.set_handle_referer(False)
    browser.set_handle_refresh(False)
    browser.addheaders = [('User-agent', 'Firefox')]
    browser.open("https://webapp.upeu.edu.pe/academico/login.jsp")
    print "==============================================================="
    print browser.geturl()
    print "==============================================================="
    # formulario login
    browser.select_form('datos')
    browser.form['f_usuario'] = args.usuario
    browser.form['f_password'] = args.password
    browser.submit()


def main(excel_name):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    browser = mechanize.Browser()
    login(browser)
    book = openpyxl.load_workbook(excel_name)
    sheet = book.active
    cells = sheet['A1': 'B4']
    start_time = time.time()
    new_path = os.getcwd() + "/alumnos"
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    os.chdir(new_path)
    for codigo, nombre in cells:
        print codigo.value, nombre.value
        if len(str(codigo.value)) == 9:
            buscar(browser, codigo.value)
            file = open(nombre.value + ".txt", 'w')
            file.write(get_notas(browser))
            # file.write(get_asistencia(browser))
            file.close()
    print time.time() - start_time


if __name__ == '__main__':
    try:
        main("items.xlsx",)
    except HTTPError, e:
        print e.code, e.reason
