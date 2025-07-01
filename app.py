from flask import Flask
from flask import url_for
from flask import render_template
import db as db
import logging
import os

app = Flask(__name__)

py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.DEBUG)
py_handler = logging.FileHandler(f"logs/{os.path.basename(__file__)}.log", mode='w', encoding='utf-8')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
py_handler.setFormatter(py_formatter)
py_logger.addHandler(py_handler)

@app.route("/create_data/")
def create_data():
    db.create_tables()

    from cbr_request import get_branch_info_by_id
    branches = get_branch_info_by_id()
    for branch in branches:
        db.add_branch(branch)

    return 'Success'


@app.route("/", defaults={"pattern": None})
@app.route("/get_branches/", defaults={"pattern": None})
@app.route("/get_branches/<pattern>")
def get_branches(pattern):
    result = []
    keys = ['id', 'internal_d', 'name', 'visible_name', 'address', 'visible_address', 'opendate', 'parent']
    if pattern is None:
        branches = db.get_branches()
    else:
        branches = db.get_branch_by_pattern(pattern)
    for branch in branches:
        py_logger.debug(branch)
        py_logger.debug(dict(zip(keys, branch)))
        result.append(dict(zip(keys, branch)))

    context = {
        'branches': result,
        'search_pattern': pattern,
    }

    # return context
    return render_template('branchlist.html', **context)


if __name__ == '__main__':
    app.run(debug=True)

