#!/usr/bin/env python3

import argparse
import os
import sys
import requests
from urllib.parse import quote

LINK="https://en.wikipedia.org/api/rest_v1/"
PDF_EP="page/pdf/"
SUMMARY_EP="page/summary/"
RANDOM_EP="page/random/summary/"

PDF_SAVE_PATH=os.path.join(os.path.expanduser("~"), "WIKIPEDIA_PDFS")



parser = argparse.ArgumentParser(
    prog="wiki.py",
    description="search wikipedia right from your terminal!\nAuthor: Suyash Nepal\nCreated on: Aug 2024",
    epilog="Contact me: suy.nepal@gmail.com",
    formatter_class=argparse.RawTextHelpFormatter
)

# add arguments to the parser

parser.add_argument("-s", "--search", help="search for a query and get a pdf back\nSTORAGE_DIRECTORY: $HOME/WIKIPEDIA_PDFS/", metavar="QUERY", type=str)
parser.add_argument("-i", "--info", help="get summary of the query", metavar="QUERY", type=str)
parser.add_argument("-r", "--random", help="get summary of a random article", action="store_true")

args = parser.parse_args()

if args.search != None:
    search_query = quote(args.search)
    req_url = LINK + PDF_EP + search_query
    response = requests.get(req_url)
    if not response.ok:
        print("failed to fetch the required pdf")
        sys.exit(1)
    b = response.content
    if not os.path.isdir(PDF_SAVE_PATH):
        os.mkdir(PDF_SAVE_PATH)
    PDF_FILE_PATH = os.path.join(PDF_SAVE_PATH, args.search.strip() + ".pdf")
    if not os.path.isfile(PDF_FILE_PATH):
        with open(PDF_FILE_PATH, "wb") as f:
            f.write(b)
    else:
        print("File already exists!")
        sys.exit(1)

if args.info != None:
    search_query = quote(args.info)
    req_url = LINK + SUMMARY_EP + search_query
    response = requests.get(req_url)
    if not response.ok:
        print("failed to retrieve the required info")
        sys.exit(1)
    print("Title: ", response.json()['title'])
    print(response.json()["extract"])

if args.random:
    req_url = LINK + RANDOM_EP
    response = requests.get(req_url)
    if not response.ok:
        print("failed to retrieve the required info")
        sys.exit(1)

    print("Title: ", response.json()['title'])
    print("Summary: ", response.json()['extract'])
