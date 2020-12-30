from . import bp as home
from flask import url_for, render_template, redirect

@home.route('/', methods=['GET'])
def main():
    return render_template('home/main.html')