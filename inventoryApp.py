from flask import Flask, render_template, url_for, redirect, request, flash
from forms import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import timezone
from sqlalchemy.sql.functions import func

app=Flask(__name__)

app.config['SECRET_KEY'] ='e67116a72babd0ee8af882893baa068a'

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///inventorySite.db'

db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#db Tables
class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    product_name = db.Column(db.String(50),nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Product('{self.product_name}','{self.quantity}')"

class Location(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    location_name= db.Column(db.String(100))

    def __repr__(self):
        return f"Location('{self.location_name}')"

class Movement(db.Model):
    movement_id= db.Column(db.Integer,primary_key=True)
    product_id= db.Column(db.Integer,db.ForeignKey('product.id'))
    product = db.relationship("Product")
    to_location_id = db.Column(db.Integer,db.ForeignKey('location.id'))
    to_location = db.relationship("Location",primaryjoin=to_location_id==Location.id)
    from_location_id = db.Column(db.Integer,db.ForeignKey('location.id'))
    from_location = db.relationship("Location",primaryjoin=from_location_id==Location.id)
    quantity = db.Column(db.Integer)
    curr_time = db.Column(db.DateTime, server_default=db.func.now())

    
 


    def __repr__(self):
    	return f"Movement('{self.product}', '{self.to_location}', '{self.from_location}', '{self.quantity}', '{self.curr_time}')"

#routes
#HOMEPAGE
@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')


#Add Products, Locations and Movements
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
	form = ProductForm()
	if form.validate_on_submit():
		new_product = Product(product_name=form.product_name.data, quantity=form.quantity.data)
		db.session.add(new_product)
		db.session.commit()
		flash(f'Product {form.product_name.data} Added!', 'success')
		return redirect(url_for('add_product'))
	return render_template('add_product.html', form=form)

@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
	form = LocationForm()
	if form.validate_on_submit():
		new_location = Location(location_name=form.location_name.data)
		db.session.add(new_location)
		db.session.commit()
		flash(f'Location {form.location_name.data} Added!', 'success')
		return redirect(url_for('add_location'))
	return render_template('add_location.html', form=form)	

@app.route('/movements',methods=["GET","POST"])
def add_movements():
	form = MovementForm()
	form.to_location.choices = [(location.id, location.location_name) for location in Location.query.all()] #for the dropdown boxes
	form.from_location.choices = [(location.id, location.location_name) for location in Location.query.all()] #for the dropdown boxes
	form.product.choices = [(product.id, product.product_name) for product in Product.query.all()] #for the dropdown boxes
	form.from_location.choices.insert(0, (0, 'None'))	#can select 'None' option too
	if form.validate_on_submit():
		new_movement = Movement(to_location_id=form.to_location.data, from_location_id=form.from_location.data, product_id=form.product.data, quantity=form.quantity.data)
		if form.from_location.data==0:
			prod_id=form.product.data
			prod=Product.query.get_or_404(prod_id)
			prodQuantity=prod.quantity-form.quantity.data
			if prodQuantity<0:
				flash('Product cannot be moved, due to insufficient quantity!', 'danger')
			else:
				db.session.add(new_movement)
				prod.quantity=prodQuantity
				db.session.commit()
				flash('Product has been moved!', 'success')
			return redirect(url_for('add_movements'))
		else:
			quantity_check = available_quantity(form.from_location.data, form.product.data)
			if int(form.quantity.data) > quantity_check:
				flash('Product cannot be moved, due to insufficient quantity!', 'danger')
			else:
				new_movement=Movement(to_location_id=form.to_location.data, from_location_id=form.from_location.data, product_id=form.product.data, quantity=form.quantity.data)
				db.session.add(new_movement)
				db.session.commit()
				flash('Product has been moved!', 'success')	
			return redirect(url_for('add_movements'))		
	return render_template('add_movements.html', form=form)	

#to check the available quantity of stocks
def available_quantity(location, product):
	sum_from=Movement.query.filter(Movement.to_location_id==location,Movement.product_id==product).from_self(func.sum(Movement.quantity, )).all()
	sum_to=Movement.query.filter(Movement.from_location_id==location,Movement.product_id==product).from_self(func.sum(Movement.quantity,name="moved")).all()
	sum_from=sum_from[0][0]	
	sum_to=sum_to[0][0]
	if sum_from is None:
		sum_from=0	
	if sum_to is None:
		sum_to=0
	
	quantity_check=sum_from - sum_to
	return quantity_check	

	

#View Added Products, Locations and Movements
@app.route('/view_products', methods=['GET', 'POST'])
def view_products():
	if request.method == 'GET':
		product_list = Product.query.all()
		return render_template('product_list.html', product_list=product_list)

@app.route('/view_locations', methods=['GET', 'POST'])
def view_locations():
	if request.method == 'GET':
		location_list = Location.query.all()
		return render_template('location_list.html', location_list=location_list)

@app.route('/view_movements', methods=['GET', 'POST'])
def view_movements():
	if request.method == 'GET':
		movement_list = Movement.query.all()
		return render_template('movement_list.html', movement_list=movement_list)

#Update Available Products, Locations and Movements
@app.route('/view_products/<int:product_id>/update', methods=['GET', 'POST'])
def update_product(product_id):
	product = Product.query.get_or_404(product_id)
	form = ProductForm()
	if form.validate_on_submit():
		product.product_name = form.product_name.data
		product.quantity = form.quantity.data
		db.session.commit()
		flash('Product has been updated!', 'success')
		return redirect(url_for('view_products', product_id=product.id))
	elif request.method == 'GET':
		form.product_name.data = product.product_name
		form.quantity.data = product.quantity
	return render_template('add_product.html', title='Update Product',
                           form=form, legend='Update Product')


@app.route('/view_locations/<int:location_id>/update', methods=['GET', 'POST'])
def update_location(location_id):
	location = Location.query.get_or_404(location_id)
	form = LocationForm()
	if form.validate_on_submit():
		location.location_name = form.location_name.data
		db.session.commit()
		flash('Location has been updated!', 'success')
		return redirect(url_for('view_locations', location_id=location.id))
	elif request.method == 'GET':
		form.location_name.data = location.location_name
	return render_template('add_location.html', title='Update Location',
                           form=form, legend='Update Location')


@app.route('/view_movements/<int:movement_id>/update', methods=['GET', 'POST'])
def update_movement(movement_id):
	movement = Movement.query.get_or_404(movement_id)
	form = MovementForm()
	form.to_location.choices = [(location.id, location.location_name) for location in Location.query.all()]
	form.from_location.choices = [(location.id, location.location_name) for location in Location.query.all()]
	form.product.choices = [(product.id, product.product_name) for product in Product.query.all()]
	form.from_location.choices.insert(0, (0, 'None'))
	if form.validate_on_submit():
		movement.from_location_id = form.from_location.data
		movement.to_location_id = form.to_location.data
		movement.product_id = form.product.data
		movement.quantity = form.quantity.data
		db.session.commit()
		flash('Movement has been updated!', 'success')
		return redirect(url_for('view_movements', movement_id=movement.movement_id))
	elif request.method == 'GET':
		form.from_location.data = movement.from_location_id
		form.to_location.data = movement.to_location_id
		form.product.data = movement.product_id
		form.quantity.data = movement.quantity
	return render_template('add_movements.html', form=form)



#Return Reports
@app.route('/status')
def status():
	Locations = Location.query.all()
	Products = Product.query.all()
	status_list = []

	for location in Locations:
		for product in Products:
			row = {}
			row["location"] = location.location_name
			row["product"] = product.product_name
			row["quantity"] = available_quantity(location.id,product.id)
			if row["quantity"]<0:
				row["quantity"]=0
			status_list.append(row)

	
	return render_template('status.html',status_list=status_list, unall=Products)



if __name__ == '__main__':
    app.run(debug=True)
