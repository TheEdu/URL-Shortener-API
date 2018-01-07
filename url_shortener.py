# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 00:23:48 2018

@author: edu
"""

import sqlite3
from flask import Flask, request, redirect, jsonify
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
app.config.update(
    DATABASE=r'C:\sqlite\databases\urlShortenerDB.db'
)

def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.isolation_level = None #Auto commit ON
    con.row_factory = sqlite3.Row #Allows the rows to be treated as if they were dictionaries instead of tuples.
    return con

def full_url(url):
    import re
    p = re.compile('^(http://|https://)')
    if p.search(url) == None:
        url = "https://"+url
    return url
    

@app.route("/")
def save_link():
    url = request.args.get('url','')
    short_link = request.args.get('short-link','')
    
    if url != '' and short_link != '':
        #Get Today date in seconds from 1970
        dt = datetime.today()
        today = dt.timestamp()
        
        #Connecting to the DB
        con = connect_db()
        cur = con.cursor()
        
        cur.execute("SELECT * FROM url_link_map where link=? and expiration_date>=?",(short_link,today,))
        row = cur.fetchone()

        if row:
          message = "Short-Link already in use, please try a different one"
          return_url = "http://localhost:3001/?url="+url+"&short-link=****"
        else:
          url = full_url(url)
          expiration_date = (dt + relativedelta(months=+6)).timestamp()
          cur.execute("INSERT INTO url_link_map(url,link,expiration_date) values(?,?,?)",(url,short_link,expiration_date,))
          message = "Short-Link Successfully Created."
          return_url = "http://localhost:3001/" + short_link
    
        #Closing connection
        cur.close()
        con.close()
    else:
        message = "Url and Short-Link params are needed"
        return_url = "http://localhost:3001/?url=****&short-link=****"
        
    return jsonify(response=message,
                   url=return_url)

@app.route('/<path:path>')
def path_redirect(path):
    #Connecting to the DB
    con = connect_db()
    cur = con.cursor()
    
    #Get Today date in seconds from 1970
    dt = datetime.today()
    today = dt.timestamp()
    
    cur.execute("SELECT url FROM url_link_map WHERE link=? AND expiration_date>=?",(path,today,))
    row = cur.fetchone()
    
    #Closing connection
    cur.close()
    con.close()
    
    if row:
        return redirect(row['url'], code=302)
    else:
        return jsonify(response=("The path '" + path + "' is not registered"))


if __name__ == "__main__":
    #Run application     
    app.run(port=3001, host="localhost")