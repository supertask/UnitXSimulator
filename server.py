#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
from flask import Flask, request, url_for, redirect, render_template, send_from_directory
from unitx.example import Example

app = Flask(__name__, template_folder='./static/template', static_url_path='')
#app._static_folder='./static'
intaractive_unitx = Example(is_intaractive_run=True)
io_unitx = Example(is_intaractive_run=False)
tmp_folder = './static/tmp/'
textarea_db = tmp_folder + 'tmp_textarea.txt'

def run_unitx(code):
    # TODO(Tasuku): stand in a line
    stdout_path = tmp_folder + 'stdout_unitx.txt'
    stderr_path = tmp_folder + 'stderr_unitx.txt'
    if os.path.exists(stdout_path): os.remove(stdout_path)
    if os.path.exists(stderr_path): os.remove(stderr_path)

    sys.stdout = open(stdout_path,"w")
    sys.stderr = open(stderr_path,"w")
    with open(textarea_db, 'w') as wf: wf.write(code)
    io_unitx.eat_code(textarea_db)
    sys.stdout.close()
    sys.stderr.close()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    if os.path.getsize(stdout_path):
        return open(stdout_path,"r").read()
    if os.path.getsize(stderr_path):
        return open(stderr_path,"r").read()
    return ""

@app.route("/")
def index():
    return render_template("unitx_template.html", code="", result="")

@app.route('/run', methods=['POST'])
def run():
    unitx_code = request.form['code']   
    res = run_unitx(unitx_code)
    return render_template("unitx_template.html", code=unitx_code, result=res)


@app.route('/static/<path:filepath>')
def do_static(filepath):
    return send_from_directory('./static', filepath)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='localhost', port=port, debug=True)
    #app.run(host='0.0.0.0', port=port, debug=True)
