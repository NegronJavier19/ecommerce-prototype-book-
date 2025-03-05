import json
import os
from flask import Flask, render_template, request

from frontend_model.shopModel import *

def getProducts():
    products = getProductsModel()
    return products

def getBrands():
    return getBrandsModel()

def getColors():
    return getColorsModel()

def getVideoRes():
    return getVideoResModel()

def getWifi():
    return getWifiModel()

# Function to load books from JSON
def load_books():
    json_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'products.json')
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Route to load a specific book page dynamically
def book_page(book_name):
    books = load_books()
    
    # Find the book matching the requested name
    book = next((b for b in books if b['name'].lower().replace(" ", "-") == book_name.lower()), None)

    if book:
        return render_template(f"{book_name}.html", book=book)
    else:
        return "Book not found", 404

