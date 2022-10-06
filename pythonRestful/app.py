from flask import Flask, jsonify, request, Response, json, render_template, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import Student

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def welcome():
    return render_template('login.html')


# router login
@app.route('/login', methods=['POST', 'GET'])
def login():
    # print(request)
    result = None
    one = request.get_json()
    print(one)
    if request.method == 'POST':
        if one['username'] != 'admin' or one['password'] != 'admin':
            result = 'Invalid Credentials. Please try again.'
        else:
            result = 1
    return jsonify(result)
    # return render_template('index.html')


@app.route('/home-page')
def homepage():
    return render_template('index.html')


@app.route('/student', methods=['POST'])
def create_item():
    one = request.get_json()
    name = one['name']
    address = one['address']
    birthday = one['birthday']
    phone = one['phone']
    student = Student.Student(name=name, address=address, birthday=birthday, phone=phone)
    db.session.add(student)
    db.session.commit()
    return jsonify(1)


@app.route('/student-detail/<id>', methods=['GET'])
def get_detail(id_):
    ss = db.session.query(Student.Student).filter(Student.Student.id == id_).first()
    if request.method == "GET" and ss:
        data = {
            "id": ss.id,
            "name": ss.name,
            "address": ss.address,
            "birthday": ss.birthday,
            "phone": ss.phone
        }
        return custom_response(data, 200)
    return "student not exits"


@app.route('/update-student/<id>', methods=['PUT'])
def update_item(id):
    one = request.get_json()
    print(one)
    ss = db.session.query(Student.Student).filter(Student.Student.id == id).first()
    if request.method == "PUT" and ss:
        my_data = ss
        my_data.name = one['name']
        my_data.address = one['address']
        my_data.birthday = one['birthday']
        my_data.phone = one['phone']
        db.session.merge(my_data)
        db.session.commit()
        return jsonify(1)
    return "student not exits"


@app.route('/student', methods=['GET', 'POST'])
def get_items():
    page = int(request.args.get("pages", 1))
    print(page)
    per_page = request.args.get("per-page", 10, type=int)
    print(per_page)
    search_query = request.args.get("q")
    search = "%{0}%".format(search_query)
    if search_query:
        listitems = db.session.query(Student.Student).filter(Student.Student.name.like(search)).order_by(
            Student.Student.id).paginate(page, per_page)
    else:
        listitems = db.session.query(Student.Student).order_by(
            Student.Student.id).paginate(page, per_page)

    results = {

        "pagination": {
            "count": listitems.total,
            "page": page,
            "per_page": per_page,
            "pages": listitems.pages,
            "results": [
                {
                    "id": m.id,
                    "name": m.name,
                    "address": m.address,
                    "birthday": m.birthday,
                    "phone": m.phone
                } for m in listitems.items
            ],
        },
    }
    return custom_response(results, 200)


def custom_response(res, status_code):
    return Response(mimetype="application/json", response=json.dumps(res), status=status_code)


@app.route('/delete-student/<id>', methods=['DELETE'])
def delete_item(id):
    db.session.query(Student.Student).filter(Student.Student.id==id).delete()
    db.session.commit()
    return jsonify(1)


def get_list_student(lists, offset=0, per_page=10):
    return lists[offset: offset + per_page]


if __name__ == "__main__":
    app.run(debug=True)
