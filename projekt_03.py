from pprint import pprint
import os
import csv
import sys

import bs4
import requests
from bs4 import BeautifulSoup



def soup_response(odkaz: str) -> BeautifulSoup:
    response = requests.get(odkaz)
    return BeautifulSoup(response.text, 'html.parser')


def list_of_all_regions() -> list:
    url = sys.argv[1]

    parsed_soup = soup_response(url)
    region_codes = extract_region_codes(parsed_soup)
    region_names = extract_region_names(parsed_soup)
    links_to_regions = extract_region_links(parsed_soup)

    return list(zip(region_codes, region_names, links_to_regions))


def td_tags(soup: bs4.BeautifulSoup, *args) -> list:
    lines = []
    for arg in args:
        lines += soup.select(f'td[headers="{arg}"]')
    return lines


def extract_region_codes(soup: bs4.BeautifulSoup) -> list:
    lines = td_tags(soup, 't1sa1 t1sb1', 't2sa1 t2sb1', 't3sa1 t3sb1')
    return [td.find('a').text for td in lines if td.find('a')]


def extract_region_names(soup: bs4.BeautifulSoup) -> list:
    lines = td_tags(soup, 't1sa1 t1sb2', 't2sa1 t2sb2', 't3sa1 t3sb2')
    return [td.text for td in lines]


def extract_region_links(soup: bs4.BeautifulSoup) -> list:
    lines = td_tags(soup, 't1sa1 t1sb1', 't2sa1 t2sb1', 't3sa1 t3sb1')

    return [td.find('a').get('href') for td in lines if td.find('a')]


def voters_covers(soup) -> list:
    headers = ['sa2', 'sa3', 'sa6']
    vot_cov = []
    for header in headers:
        value = soup.find('td', {'headers': f'{header}'})
        value = value.text.replace('\xa0', '')
        vot_cov.append(int(value))
    return vot_cov


def votes_for_partei(soup) -> list:
    lines = td_tags(soup, 't1sa2 t1sb3', 't2sa2 t2sb3')
    return [(int(td.text.replace('\xa0', ''))) for td in lines if td.text != '-']


def result_connect(soup) -> list:
    return voters_covers(soup) + votes_for_partei(soup)


def extract_partei_names(soup) -> list:
    lines = td_tags(soup, 't1sa1 t1sb2', 't2sa1 t2sb2')
    return [td.text for td in lines if td.text != '-']


def head(soup) -> list:
    head1 = ['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy']
    head2 = extract_partei_names(soup)
    return head1 + head2


def csv_file_creation(codes_names_links) -> csv:
    file_name = sys.argv[2]
    url_odkaz = 'https://www.volby.cz/pls/ps2017nss/' + codes_names_links[0][2]
    link_soup = soup_response(url_odkaz)
    csv_head = head(link_soup)


    with open(f'{file_name}.csv', mode='w', encoding="UTF-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_head)

        for y in codes_names_links:
            url2 = 'https://www.volby.cz/pls/ps2017nss/' + y[2]
            soup = soup_response(url2)
            results = result_connect(soup)
            writer.writerow([y[0], y[1]] + results)
            os.system('cls')
        saved_message(file_name)


def saved_message(file_name):
    print(f'Byly zapsany do souboru {file_name}.csv')
    print('Ukoncuji program...')


def main():
    codes_names_links = list_of_all_regions()
    csv_file_creation(codes_names_links)


if __name__ == '__main__':
    try:
        main()
    except IndexError:
        print('Není zadán vstupní argument')
        quit()
    except requests.exceptions.MissingSchema:
        print('Chyba v zadání URL')
        quit()
    except requests.exceptions.ConnectionError:
        print('Chyba při připojení na server')
        quit()
    except requests.exceptions.InvalidURL:
        print('Neplatná URL adresa')
        quit()
    except requests.exceptions.InvalidSchema:
        print('Neplatná URL adresa')
        quit()
    except requests.exceptions.InvalidHeader:
        print('Neplatná URL adresa')
        quit()
    except requests.exceptions.InvalidSchema:
        print('Neplatná URL adresa')
        quit()
    except FileNotFoundError:
        print('Soubor nebyl nalezen')
        quit()
    except PermissionError:
        print('Nemáte dostatečná práva pro zápis')
        quit()