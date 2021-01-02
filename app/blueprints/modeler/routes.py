from . import bp as modeler
from flask import url_for, render_template, redirect

@modeler.route('/', methods=['GET'])
def main():
    return render_template('modeler/main.html')