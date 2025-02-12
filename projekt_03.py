'Marek Sojka'
'mara1x@email.cz'
'Marek98'


import os
import csv
import sys
import logging
import requests
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO)

def soup_response(odkaz: str) -> BeautifulSoup:
    """
    Fetches the URL and returns a BeautifulSoup object of the page content.

    Parameters:
    odkaz (str): The URL to fetch.

    Returns:
    BeautifulSoup: Parsed HTML content of the page.
    """
    try:
        response = requests.get(odkaz)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        logging.error("An error occurred while fetching the URL: %s", e)
        sys.exit(1)

def list_of_all_regions() -> list:
    """
    Parses the main URL and extracts region codes, names, and links.

    Returns:
    list: A list of tuples containing region codes, names, and links.
    """
    try:
        url = sys.argv[1]
        parsed_soup = soup_response(url)
        region_codes = extract_region_codes(parsed_soup)
        region_names = extract_region_names(parsed_soup)
        links_to_regions = extract_region_links(parsed_soup)
        return list(zip(region_codes, region_names, links_to_regions))
    except IndexError:
        logging.error("URL argument is missing.")
        sys.exit(1)
    except Exception as e:
        logging.error("An error occurred while listing all regions: %s", e)
        sys.exit(1)

def td_tags(soup: BeautifulSoup, *args) -> list:
    """
    Extracts <td> tags with specific headers from the soup object.

    Parameters:
    soup (BeautifulSoup): The parsed HTML content.
    args: The headers to search for.

    Returns:
    list: A list of <td> tags.
    """
    lines = []
    for arg in args:
        lines += soup.select(f'td[headers="{arg}"]')
    return lines

def extract_region_codes(soup: BeautifulSoup) -> list:
    """
    Extracts region codes from the soup object.

    Parameters:
    soup (BeautifulSoup): The parsed HTML content.

    Returns:
    list: A list of region codes.
    """
    lines = td_tags(soup, 't1sa1 t1sb1', 't2sa1 t2sb1', 't3sa1 t3sb1')
    return [td.find('a').text for td in lines if td.find('a')]

def extract_region_names(soup: BeautifulSoup) -> list:
    """
    Extracts region names from the soup object.

    Parameters:
    soup (BeautifulSoup): The parsed HTML content.

    Returns:
    list: A list of region names.
    """
    lines = td_tags(soup, 't1sa1 t1sb2', 't2sa1 t2sb2', 't3sa1 t3sb2')
    return [td.text for td in lines]

def extract_region_links(soup: BeautifulSoup) -> list:
    """
    Extracts region links from the soup object.

    Parameters:
    soup (BeautifulSoup): The parsed HTML content.

    Returns:
    list: A list of region links.
    """
    lines = td_tags(soup, 't1sa1 t1sb1', 't2sa1 t2sb1', 't3sa1 t3sb1')
    return [td.find('a').get('href') for td in lines if td.find('a')]

def voters_covers(soup) -> list:
    """
    Extracts voter coverage details from the soup object.

    Parameters:
    soup (BeautifulSoup): The parsed HTML content.

    Returns:
    list: A list of voter coverage details.
    """
    headers = ['sa2', 'sa3', 'sa6']
    vot_cov = []
    for header in headers:
        value = soup.find('td', {'headers': f'{header}'})
        value = value.text.replace('\xa0', '')
        vot_cov.append(int(value))
    return vot_cov

def votes_for_partei(soup) -> list:
    """
    Extracts votes for each party from the soup object.

    Parameters:
    soup (BeautifulSoup): The parsed HTML content.

    Returns:
    list: A list of votes for each party.
    """
    lines = td_tags(soup, 't1sa2 t1sb3', 't2sa2 t2sb3')
    return [(int(td.text.replace('\xa0', ''))) for td in lines if td.text != '-']

def result_connect(soup) -> list:
    """
    Combines voter coverage details and votes for parties into a single list.

    Parameters:
    soup (BeautifulSoup): The parsed HTML content.

    Returns:
    list: A combined list of voter coverage details and votes for parties.
    """
    return voters_covers(soup) + votes_for_partei(soup)

def extract_partei_names(soup) -> list:
    """
    Extracts party names from the soup object.

    Parameters:
    soup (BeautifulSoup): The parsed HTML content.

    Returns:
    list: A list of party names.
    """
    lines = td_tags(soup, 't1sa1 t1sb2', 't2sa1 t2sb2')
    return [td.text for td in lines if td.text != '-']

def head(soup) -> list:
    """
    Constructs the header for the CSV file.

    Parameters:
    soup (BeautifulSoup): The parsed HTML content.

    Returns:
    list: A list of header names for the CSV file.
    """
    head1 = ['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy']
    head2 = extract_partei_names(soup)
    return head1 + head2

def csv_file_creation(codes_names_links) -> None:
    """
    Creates a CSV file with the extracted data.

    Parameters:
    codes_names_links (list): A list of tuples containing region codes, names, and links.
    """
    try:
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
    except IndexError:
        logging.error("File name argument is missing.")
        sys.exit(1)
    except Exception as e:
        logging.error("An error occurred while creating the CSV file: %s", e)
        sys.exit(1)

def saved_message(file_name):
    """
    Prints a message indicating that the data has been saved to a file.

    Parameters:
    file_name (str): The name of the file where data is saved.
    """
    print(f'Byly zapsany do souboru {file_name}.csv')
    print('Ukoncuji program...')

def main():
    """
    Main function to execute the entire script.
    """
    try:
        codes_names_links = list_of_all_regions()
        csv_file_creation(codes_names_links)
    except Exception as e:
        logging.error("An error occurred in the main function: %s", e)
        sys.exit(1)

if __name__ == '__main__':
    main()
