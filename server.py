#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
from flask import Flask, request, url_for, redirect, render_template, send_from_directory
from unitx.example import Example

app = Flask(__name__, template_folder='./static/template', static_url_path='')
intaractive_unitx = Example(is_intaractive_run=True)
io_unitx = Example(is_intaractive_run=False)
tmp_folder = './tmp/'
textarea_db = tmp_folder + 'tmp_textarea.txt'
decoding_code = 'utf-8'
default_sample_name = 'unit_converter'
index_template = 'unitx_template.html'

def run_unitx(code):
    # TODO(Tasuku): stand in a line
    stdout_path = tmp_folder + 'stdout_unitx.txt'
    stderr_path = tmp_folder + 'stderr_unitx.txt'
    if os.path.exists(stdout_path): os.remove(stdout_path)
    if os.path.exists(stderr_path): os.remove(stderr_path)
    code = code.replace('\r', '')

    import codecs
    sys.stdout = codecs.open(stdout_path,'w', decoding_code)
    sys.stderr = codecs.open(stderr_path,'w', decoding_code)
    with open(textarea_db,'w') as wf: wf.write(code.encode(decoding_code))
    io_unitx.eat_code(textarea_db)
    sys.stdout.close()
    sys.stderr.close()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    if os.path.getsize(stdout_path):
        return open(stdout_path,"r").read().decode(decoding_code)
    if os.path.getsize(stderr_path):
        return open(stderr_path,"r").read().decode(decoding_code)
    return ''

@app.route("/", methods=['GET'])
def index():
    print "normal or GET!!"
    if request.args.get('name'):
        selected_name = request.args.get('name')
        unitx_code = get_source_code(selected_name)
        return render_template(index_template,
            code = unitx_code,
            selected_name = selected_name,
            result = '')
    else:
        return render_template(index_template,
            code=get_source_code(default_sample_name),
            selected_name=default_sample_name,
            result='')
    """
    elif request.args.get('about'):
        return render_template(index_template,
            code = 'about()',
            selected_name = default_sample_name,
            result = about_unitx)
    """
        

@app.route('/', methods=['POST','GET'])
def run():
    print "POST, GET!!!!!!!"
    unitx_code = request.form['code']   
    res = run_unitx(unitx_code)
    return render_template(index_template,
        code=unitx_code,
        selected_name=request.args.get('name'),
        result=res)

def get_source_code(program_name):
    try:
        return open('%s/%s.unit' % ('demo', program_name), 'r').read()
    except IOError:
        print 'Wrong query.'


@app.route('/static/<path:filepath>')
def do_static(filepath):
    return send_from_directory('./static', filepath)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    #app.run(host='localhost', port=port, debug=True)
    app.run(host='0.0.0.0', port=port, debug=True)
