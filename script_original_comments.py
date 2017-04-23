# -*- coding: utf-8 -*-
import argparse
from getpass import getpass
import mechanize
from bs4 import BeautifulSoup
# =============================================================================
# for https
# =============================================================================
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# =============================================================================
# capturar informacion
# =============================================================================
parser = argparse.ArgumentParser(description="Login a Academico.")
parser.add_argument("usuario")
args = parser.parse_args()

args.password = getpass("Ingrese su contraseña: ")
# url = raw_input("Ingrese la URL: ")
# =============================================================================
# script
# =============================================================================
br = mechanize.Browser()
# Browser options
# Ignore robots.txt. Do not do this without thought and consideration.
br.set_handle_robots(False)
# Don't add Referer (sic) header
br.set_handle_referer(False)

# Don't handle Refresh redirections
br.set_handle_refresh(False)
# Setting the user agent as firefox
br.addheaders = [('User-agent', 'Firefox')]

r = br.open("https://webapp.upeu.edu.pe/academico/login.jsp")
print "==============================================================="
# assert br.viewing_html()
# print br.title()
print r.geturl()
print "==============================================================="
# print html
# print r.info()
# resp = mechanize.make_response(html, [("Content-Type", "text/html")],
#                                br.geturl(), 200, "OK")
# br.set_response(resp)
# print "******************"
# for f in br.forms():
#     print f
# print "******************"
br.select_form('datos')
# br.select_form(nr=0) #funciona
# br.select_form(name="datos")
# for c in br.controls:
#     print c.type, c.name, c.value

br.form['f_usuario'] = args.usuario
br.form['f_password'] = args.password
r = br.submit()
print "==============================================================="
print r.geturl()
print "==============================================================="
for link in br.links():
    if link.text and 'Portal del Alumno' == link.text:
        # print link.url
        # print link
        # print link.text
        # req = br.click_link(link)
        r = br.follow_link(link)

print "==============================================================="
print r.geturl()
print "==============================================================="
count = 0
for link in br.links():
    if link.text and 'Temas' == link.text:
        # print link.attrs[1][1]
        count = count + 1
        br.select_form("formulario")
        br.form.find_control('x').readonly = False
        br.form['x'] = link.attrs[1][1][11:43]
        br.form.find_control('y').readonly = False
        br.form['y'] = link.attrs[1][1][46:62]
        br.form.action = 'https://webapp.upeu.edu.pe/academico/portales/alumno/ver_nota.jsp'
        r = br.submit()
        # print r.geturl()
        soup = BeautifulSoup(br.response().read(), "html5lib")
        print soup.find_all('table')[5].find_all('b')[0].get_text()
        temp = soup.find_all('table')[7].find_all('tr')
        for row in temp[1:len(temp) - 1]:
            column = row.find_all('td')
            print column[0].get_text(), column[2].get_text(), column[3].get_text(), column[1].get_text()
        print temp[len(temp) - 1].td.get_text(), temp[len(temp) - 1].th.get_text()
        r = br.back()
    if link.text and 'Asistencia' == link.text:
        # print link
        count = count + 1
        # if count == 3:  # para ingresar en el primero
        r = br.follow_link(link)
        soup = BeautifulSoup(br.response().read(),
                             "html.parser")  # "html5lib"
        # html = str(soup)
        # print soup.find_all('a')
        temp = soup.find_all('table')
        # print len(temp)
        for row in temp[4].find_all(
                'tr', {"style": "background-color:#FFF5E7;"}):
            column = row.find_all('td')
            print column[1].get_text(), column[2].img.get('src')
            if len(column[2]) > 3:
                print column[2].input.get('value')
        r = br.back()
        print "============================================="
    #     # if len(temp) == 8:
        #     print temp[7]
# =============================================================================
# select form by id or action
# def select_form(form):
#   return form.attrs.get('id', None) == 'form1'
# return form.attrs.get('action', None) == '/en/search/'
# =============================================================================
# self.br.form.set_value('CLoad', 'boption')
# br.form['boption'] = 'CLoad'

# ctl =  self.br.form.find_control('hitsPerPage')
# ctl.value = ['50']
# br.form.find_control('control_name').readonly = False
# br.submit(id='searchButton')
# br.submit(name='input')
# =============================================================================
# response3 = br.back()
# response3.get_data()  # like .seek(0) followed by .read()
# response4 = br.reload()  # fetches from server

# for form in br.forms():
# 	print form
# for link in br.links(url_regex="python.org"):
# 	print link
# br.follow_link(link)  # takes EITHER Link instance OR keyword args
# =============================================================================
# # To make sure you're seeing all debug output:
# logger = logging.getLogger("mechanize")
# logger.addHandler(logging.StreamHandler(sys.stdout))
# logger.setLevel(logging.INFO)

# # Sometimes it's useful to process bad headers or bad HTML:
# response = br.response()  # this is a copy of response
# headers = response.info()  # currently, this is a mimetools.Message
# headers["Content-type"] = "text/html; charset=utf-8"
# response.set_data(response.get_data().replace("<!---", "<!--"))
# br.set_response(response)
# =============================================================================

# #Getting the response in beautifulsoup
# soup = BS(br.response().read())

# for product in soup.find_all('h3', class_="newaps"):

#     #printing product name and url
#     print "Product Name : " + product.a.text
#     print "Product Url : " + product.a["href"]
#     print "======================="
