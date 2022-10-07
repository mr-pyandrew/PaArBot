import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from django.core.management import BaseCommand

from ...models import Bearing, Leaf, Tree

URL = 'https://podshypnik.info'

book_titles = [
               '/index.php?zid=reference_book&typ=3189_t6',
               '/index.php?zid=reference_book&typ=3189_t8',
               '/index.php?zid=reference_book&typ=3635'
               ]

book_names = [
    '/index.php?zid=basic_sizes&typ=3189_t6&sketch=sk44',
    '/index.php?zid=basic_sizes&typ=3189_t6&sketch=sk43k',
    '/index.php?zid=basic_sizes&typ=3189_t8&sketch=sk00',
    '/index.php?zid=basic_sizes&typ=3189_t8&sketch=sk02',
    '/index.php?zid=basic_sizes&typ=3189_t8&sketch=sk07',
    '/index.php?zid=basic_sizes&typ=3635&sketch=sk1',
    '/index.php?zid=basic_sizes&typ=3635&sketch=sk3',
    '/index.php?zid=basic_sizes&typ=3635&sketch=sk5',
    '/index.php?zid=basic_sizes&typ=3635&sketch=sk7',
    '/index.php?zid=basic_sizes&typ=3635&sketch=sk9',
    '/index.php?zid=basic_sizes&typ=3635&sketch=sk11'
]


class Command(BaseCommand):
    help = 'Help'

    def handle(self, *args, **options):
        flag = False
        for name in book_titles:
            r = requests.get(URL + name)
            r.encoding = 'cp1251'
            soup = bs(r.text, "html.parser")
            title = soup.find('div', class_="page_content").h4.text
            print('-------------------------------------')
            print('Корень: ' + title)
            if flag:
                main_leaf = Leaf.objects.create(main_menu=True, leaf=title)
            table1 = soup.find('div', class_="page_content")
            for j in table1.find_all('tr')[1:]:
                row_data = j.find_all('td')
                for i in row_data:
                    try:
                        print('Категория ' + i.text.replace('\n', ''))
                        if 'Подшипники шариковые радиально-упорные сдвоенные, наружные кольца обращены друг к другу разноименными торцами, угол контакта α=26º' == i.text.replace('\n', ''):
                            flag = True
                        if flag:
                            print('Категория ' + i.text.replace('\n', ''))

                            low_leaf = Leaf.objects.create(main_menu=False, leaf=i.text.replace('\n', ''))
                            tree = Tree.objects.create(branch=main_leaf, leaf=low_leaf)
                            r0 = requests.get(URL + i.a['href'])
                            r0.encoding = 'cp1251'
                            soup0 = bs(r0.text, "html.parser")
                            table10 = soup0.find('table', class_='parameters')
                            for j0 in table10.find_all('tr')[1:]:
                                for i0 in j0.find_all('td'):
                                    if i0.a:
                                        # i0.a['href']
                                        r1 = requests.get(URL + i0.a['href'])
                                        r1.encoding = 'cp1251'
                                        soup1 = bs(r1.text, "html.parser")
                                        table2 = soup1.find_all('table', class_='parameters')
                                        description = ''
                                        try:
                                            description += soup1.find('div', class_="page_content").h2.text + '\n'
                                        except:
                                            pass
                                        try:
                                            description += soup1.find('div', class_="page_content").p.text + '\n'
                                        except:
                                            pass

                                        for k in range(len(table2)):
                                            if k == 0:
                                                description += 'Характеристики подшипника\n'
                                            elif k == 1:
                                                description += 'Тело качения\n'
                                            for j1 in table2[k].find_all('tr')[k:]:
                                                row_data1 = j1.find_all('td')
                                                for i1 in row_data1:
                                                    description += i1.text + ' '
                                                description += '\n'
                                        Bearing.objects.create(title=i0.a.text, description=description, tree=tree)
                                        print(i0.a.text)
                    except:
                        pass
                print('-------------------------------------\n\n')
