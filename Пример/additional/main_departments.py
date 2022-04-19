import os

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort
from werkzeug.utils import secure_filename

from data import db_session
from data.add_product import AddProductForm
from data.depart_form import AddDepartForm
from data.departments import Department
from data.login_form import LoginForm
from data.product import Product
from data.register import RegisterForm
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/mars_explorer.sqlite")

    @login_manager.user_loader
    def load_user(user_id):
        session = db_session.create_session()
        return session.query(User).get(user_id)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            user = session.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html', message="Wrong login or password", form=form)
        return render_template('login.html', title='Вход', form=form)

    @app.route("/")
    @app.route("/index")
    def index():
        session = db_session.create_session()
        jobs = session.query(Product).all()
        users = session.query(User).all()
        names = {name.id: (name.surname, name.name) for name in users}
        return render_template("index.html", jobs=jobs, names=names, title='Предложения')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация', form=form,
                                       message="Passwords don't match")
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация', form=form,
                                       message="This user already exists")
            f = form.avatar.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.static_folder, 'img', 'avatars', filename))

            user = User(
                name=form.name.data,
                surname=form.surname.data,
                email=form.email.data,
                tel_num=form.tel_num.data,
                avatar=filename
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)

    @app.route('/addproduct', methods=['GET', 'POST'])
    def addproduct():
        add_form = AddProductForm()
        if add_form.validate_on_submit():
            session = db_session.create_session()

            f = add_form.img.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.static_folder, 'img', 'product_img', filename))

            product = Product(
                product_name=add_form.product_name.data,
                summ=add_form.summ.data,
                using=add_form.using.data,
                address=add_form.address.data,
                img=filename,
                id_User=current_user.id
            )
            session.add(product)
            session.commit()
            return redirect('/')
        return render_template('addproduct.html', title='Добавление товара', form=add_form)

    @app.route('/jobs/<int:id>', methods=['GET', 'POST'])
    @login_required
    def job_edit(id):
        form = AddProductForm()
        if request.method == "GET":
            session = db_session.create_session()
            jobs = session.query(Product).filter(Product.id == id).first()

            if jobs:
                form.product_name.data = jobs.product_name
                form.summ.data = jobs.summ
                form.using.data = jobs.using
                form.address.data = jobs.address
            else:
                abort(404)
        if form.validate_on_submit():
            session = db_session.create_session()
            jobs = session.query(Product).filter(Product.id == id).first()
            if jobs:
                jobs.product_name = form.product_name.data
                jobs.summ = form.summ.data
                jobs.using = form.using.data
                jobs.address = jobs.address.data
                session.commit()
                return redirect('/')
            else:
                abort(404)
        return render_template('addproduct.html', title='Изменение товара', form=form)

    @app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
    @login_required
    def job_delete(id):
        session = db_session.create_session()
        jobs = session.query(Product).filter(Product.id == id, (current_user.id == 1)).first()

        if jobs:
            session.delete(jobs)
            session.commit()
        else:
            abort(404)
        return redirect('/')

    @app.route('/my_profile', methods=['GET', 'POST'])
    def add_depart():
        add_form = AddDepartForm()
        if add_form.validate_on_submit():
            session = db_session.create_session()
            session.add(depart)
            session.commit()
            return redirect('/')
        session = db_session.create_session()
        us_im = session.query(User)
        return render_template('my_profile.html', users=us_im, form=add_form, title='Профиль')

    @app.route("/my_products")
    def depart():

        session = db_session.create_session()
        product = session.query(Product).filter(current_user.id == Product.id_User)
        users = session.query(User).all()
        names = {name.id: (name.surname, name.name) for name in users}
        return render_template("my_product_index.html", jobs=product, names=names, title='Мои товары')

    @app.route('/in_development', methods=['GET', 'POST'])
    @login_required
    def in_development():
        session = db_session.create_session()
        return render_template("in_development.html", title='В разработке')

    @app.route('/my_job_delete/<int:id>', methods=['GET', 'POST'])
    @login_required
    def my_job_delete(id):
        session = db_session.create_session()
        jobs = session.query(Product).filter(Product.id == id).first()

        if jobs:
            session.delete(jobs)
            session.commit()
        else:
            abort(404)
        return redirect('/my_products')

    @app.route("/search", methods=['POST'])
    def search():
        session = db_session.create_session()
        x = request.form["calc"]
        product = session.query(Product).filter(x == Product.product_name).all()
        users = session.query(User).all()
        names = {name.id: (name.surname, name.name) for name in users}
        return render_template("search.html", jobs=product, names=names, title='Товары')

    @app.route("/product_info/<int:id>")
    def product_info(id):
        session = db_session.create_session()
        product = session.query(Product).filter(Product.id == id).first()
        users = session.query(User).all()
        names = {name.id: (name.surname, name.name) for name in users}
        return render_template("product_info.html", job=product, names=names, title='Товары')

    app.run(debug=True)


if __name__ == '__main__':
    main()
