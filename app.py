from flask import Flask, render_template, request, redirect, url_for, session
import os


app = Flask(__name__)

if __name__ == "__main__":
    app.debug = True;
    app.run()
