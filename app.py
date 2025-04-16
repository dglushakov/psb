from flask import Flask
from flask import url_for
from flask import render_template
import db as db

app = Flask(__name__)


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello1.html', person=name)


@app.route("/test/")
def test():
    from cbr_request import get_branch_info_by_id

    context = {
        # 'branches': get_branch_info_by_id(),
    }

    return render_template('branchlist.html', **context)


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
        print(branch)
        print(dict(zip(keys, branch)))
        result.append(dict(zip(keys, branch)))

    context = {
        'branches': result,
    }

    return render_template('branchlist.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
