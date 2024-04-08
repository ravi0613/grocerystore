from flask import Blueprint, render_template, request, flash, jsonify,redirect
from flask_login import login_required, current_user
from .models import User,product,sections,Admin,tester
from . import db
import json,datetime

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    x = datetime.datetime.now()
    if request.method=="POST":
        text=request.form['search']
        
        product1 = product.query.filter_by(product_name=text).first()
        return render_template('productpage.html', product1 = product1,user=current_user,date=int(x.strftime("%d")))

    

    return render_template("home.html", user=current_user)

@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    x = datetime.datetime.now()
    if request.method=="POST":
        text=request.form['search']
        
        product1 = product.query.filter_by(product_name=text).first()
        return render_template('product.html', product1 = product1,user=current_user,date=int(x.strftime("%d")))

    

    return render_template("admin.html", user=current_user)




@views.route('/product/<int:id>',methods=['POST','GET'])
def list(id):
    
    product1 = product.query.filter_by(product_id=id).first()
    section1=sections.query.filter_by(section_id=id)
    x = datetime.datetime.now()
    if request.method == "POST":
        quantity = int(request.form['quantity'])
        total = quantity * int(product1.product_price)
        p_name = product1.product_name
        p_price = int(product1.product_price)

        # Create a new cart item using the 'cart' model
        cart_item = tester(t_name=p_name, t_quantity=quantity, t_price=p_price, t_total=total)

        # Add the cart item to the database
        db.session.add(cart_item)
        db.session.commit()
        #return render_template('cart.html', product = product1,user=current_user,section=section1,date=int(x.strftime("%d")),quantity=quantity,total=total)
    if product1:

        return render_template('productpage.html', product1 = product1,user=current_user,section=section1,date=int(x.strftime("%d")))
    else:
        return f"show with id ={id} Doenst exist"



@views.route('/sections/<int:id>',methods=['POST','GET'])
def listsection(id):
    if request.method =="GET":
        
        section1=sections.query.filter_by(section_id=id)
        products = product.query.filter_by(procat_id=id).all()

        x = datetime.datetime.now()
        print(products)
        return render_template('sectionpage.html', products = products,user=current_user,section=section1,date=int(x.strftime("%d")))
        



@views.route('/list/quantity/<int:id>',methods=['POST','GET'])
def quantity(id):
    x = datetime.datetime.now()
    time=id
    if request.method=="POST":
        no=int(request.form['no_tic'])
        
        
        avl_qua=avl_tic
        if no<=avl_tic:
            avl_tic=avl_tic-no
            text="tickets are booked"
            text2="Continue to payment ....."
        else:
            text="tickets are not avaliable"
            text2=""


        return render_template('quantity.html',time=time,text=text,text2=text2,no=no,x=x,user=current_user,date=int(x.strftime("%d")))


    return render_template('quanity.html',time=time,avl=avl_tic,user=current_user,date=int(x.strftime("%d")))




@views.route('/cart',methods=['POST','GET'])
def cart():

    product1=tester.query.all()
    total=0
    for p in product1:
        total+=p.t_total
    return render_template("cart.html",products =product1,user=current_user,t=total)




@views.route('/admin/product_add' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('product_add.html')
 
    if request.method == 'POST':
        product_id = request.form['product_id']
        product_name = request.form['product_name']
        product_mdate= request.form['product_mdate']
        product_price = request.form['product_price']
        img_link=request.form['img_link']
        procat_id=request.form['procat_id']
        product1 = product(product_id=int(product_id), product_name=product_name, product_mdate=product_mdate, product_price = int(product_price),img_link=img_link,procat_id=int(procat_id))
        db.session.add(product1)
        db.session.commit()
        return redirect('/admin/product_add')


@views.route('/admin/display',methods = ['GET','POST'])
def RetrieveDataList():
    product1 = product.query.all()
    return render_template('product_display.html',product1 = product)







@views.route('/admin/product_delete',methods =['GET','POST'])
def product_delete():
    
    product1=product.query.all()
    if request.method=="GET":
        return render_template('product_delete.html',product1 =product1)

    if request.method=="POST":
        product_id=request.form['product_id']
        product1=product.query.filter_by(product_id=product_id).first()
        if product1:
            db.session.delete(product1)
            db.session.commit()
            return redirect('/admin/product_delete')
        else:
            return f"show with id ={id} Doenst exist"

@views.route('/admin/product_display',methods =['GET'])
def product_display():
    product1=product.query.all()
    return render_template("product_display.html",products =product1)



@views.route('/admin/product_update',methods =['GET','POST'])
def product_update():
    product1=product.query.all()
    if request.method=="GET":
        return render_template('product_update.html',products =product1)
    if request.method=="POST":
        product_id=request.form['product_id']
        product1=product.query.filter_by(product_id=product_id).first()
        if product1:
            db.session.delete(product1)
            db.session.commit()
            product_id = request.form['product_id']
            product_name = request.form['product_name']
            product_mdate= request.form['product_mdate']
            product_price = request.form['product_price']
            img_link=request.form['img_link']
            procat_id=request.form['procat_id']
            product1 = product(product_id=int(product_id), product_name=product_name, product_mdate=product_mdate, product_price = int(product_price),img_link=img_link,procat_id=int(procat_id))
            db.session.add(product1)
            db.session.commit()

            return redirect('/admin/product_update')
        else:
            return f"show with id ={id} Doenst exist"


@views.route('/admin/section_delete',methods =['GET','POST'])
def section_delete():
    
    section1=sections.query.all()
    if request.method=="GET":
        return render_template('section_delete.html',section1=section1)

    if request.method=="POST":
        section_id=request.form['section_id']
        product1=sections.query.filter_by(section_id=section_id).first()
        if product1:
            db.session.delete(product1)
            db.session.commit()
            return redirect('/admin/section_delete')
        else:
            return f"venue with id ={id} Doenst exist"

@views.route('/admin/section_display',methods = ['GET','POST'])
def Retrievesection():
    section1 = sections.query.all()
    return render_template('section_display.html',sections=section1)


@views.route('/admin/section_add' , methods = ['GET','POST'])
def createsection():
    if request.method == 'GET':
        return render_template('section_add.html')
 
    if request.method == 'POST':
        section_id = request.form['section_id']
        section_name = request.form['section_name']
        section_img_link= request.form['section_img_link']
        section = sections(section_id=int(section_id), section_name=section_name, section_img_link=section_img_link)
        db.session.add(section)
        db.session.commit()
       
        return redirect('/admin/section_add')
    

@views.route('/admin/section_update',methods =['GET','POST'])
def section_update():
    section=sections.query.all()
    if request.method=="GET":
        return render_template('section_update.html',section=section)
    if request.method=="POST":
        section_id=request.form['section_id']
        section1=section.query.filter_by(section_id=section_id).first()
        if section1:
            db.session.delete(section1)
            db.session.commit()
            section_id = request.form['section_id']
            section_name = request.form['section_name']
            section_img_link=request.form['section_img_link']

            section1 = section(section_id=int(section_id), section_name=section_name,section_img_link=section_img_link)
            db.session.add(section1)
            db.session.commit()

            return redirect('/admin/product_update')
        else:
            return f"show with id ={id} Doenst exist"
        

@views.route('/admin/create_admin', methods=['GET', 'POST'])
def adminsign_up():
    if request.method=='GET':
        return render_template('signup_admin.html')
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Admin.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = Admin(email=email, first_name=first_name, password=password1)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')

    return render_template("admin.html", user=current_user)
