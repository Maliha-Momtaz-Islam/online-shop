from bottle import run, route, template, SimpleTemplate, request, static_file, app, debug, redirect
import bottle_session
import os
import MySQLdb
import hashlib
import json

leapp = app() #init app
plugin = bottle_session.SessionPlugin(cookie_lifetime=600) #setting cookie
leapp.install(plugin)

template_location = os.path.join(os.getcwd(),'templates')
mysql_connection = MySQLdb.connect('localhost', 'root', '11', 'sellbay') # just connection

def loadTemplate(tplName):
	"""
	simple template loading shit
	"""
	insert_template_file = open(os.path.join(template_location,tplName),'r')
	insert_template = insert_template_file.read()
	insert_template_file.close()
	return insert_template

insert_template = loadTemplate('insert.html')
login_template = loadTemplate('login.html')
product_registration_template =  loadTemplate('product_registration.html')
insertSeller_template = loadTemplate('insertSeller.html')
baseTemplate = loadTemplate('generic.tpl')
index_template = loadTemplate('index.html')
product_edit_template = loadTemplate('product_edit.html')
checkout_template = loadTemplate('checkout.html')

def t(text_s):
	"""
	outputs simple text, errors and stuff in a nice way :3
	"""
	return template(baseTemplate, letext=text_s)

# all static files are inside the static folder
@route('/static/<filename:path>')
def serve_static(filename):
	return static_file(filename, root=os.path.join(os.getcwd(),'static'))

@route('/uploads/<filename:path>')
def serve_static(filename):
	return static_file(filename, root=os.path.join(os.getcwd(),'uploads'))


@route('/')
@route('/', method="POST")
def index(session):
	user_name = session.get('email')

	price_min = int(request.forms.get('price_min') or 0)
	price_max = int(request.forms.get('price_max') or 100000)
	stock_min = int(request.forms.get('stock_min') or 0)
	stock_max = int(request.forms.get('stock_max') or 100000)
	order = request.forms.get('order') or 'desc'

	if user_name is not None:
		with mysql_connection:

			mysql_cursor = mysql_connection.cursor();
			query = "SELECT * FROM Product WHERE price BETWEEN %d AND %d AND stock BETWEEN %d AND %d ORDER BY price, stock %s" % (price_min, price_max, stock_min, stock_max, order)
			print query
			mysql_cursor.execute(query)
			r = mysql_cursor.fetchall();

			# mapping the tuple into a list
			r = map(list, r)

			for each_item in r:
				mysql_cursor.execute("SELECT email FROM User_info WHERE id=%d" % each_item[3])
				if session.get("email") == mysql_cursor.fetchone()[0]:
					each_item.append(True)
				else:
					each_item.append(False)
			return template(index_template,
				items=r,
				price_min=price_min,
				price_max=price_max,
				stock_max=stock_max,
				stock_min=stock_min,
				order=order)

	else:
		redirect('/login')

@route('/login')
@route('/login/')
def login_page_show():
	return login_template

@route('/logout')
@route('/logout/')
def logout(session):
	session.destroy()
	return t('Logged out!')

@route('/login/process', method="POST")
def login_process(session):

	with mysql_connection:
		mysql_cursor = mysql_connection.cursor();
		password = request.forms.get('password') 
		email = request.forms.get('email')

		password = hashlib.sha224(password).hexdigest() # hashing the password

		mysql_cursor.execute('SELECT password FROM User_info WHERE email=\'%s\'' % email)
		p = mysql_cursor.fetchone()[0];

		if(p == password):
			session['email']=email
			redirect('/')
		else:
			return t('Login Failed.')


@route('/register')
@route('/register/')
def register_page_show():
	return insert_template
	

@route('/register/process', method="POST")
def register_user():

	with mysql_connection:
		mysql_cursor = mysql_connection.cursor();
		username = request.forms.get('username') 
		password = request.forms.get('password') 
		mail = request.forms.get('mail')
		country = request.forms.get('address')

		password = hashlib.sha224(password).hexdigest()
		
		mysql_cursor.execute('INSERT INTO  User_info(`name`,`password`,`email`,`country`) VALUES (\'%s\',\'%s\',\'%s\',\'%s\')' % (username,password,mail,country))

	return t("Registered!")


#product_registration_routing
@route('/product/add')
@route('/product/add/')
def product_registration_page_show(session):
	if session.get('email') is not None:
		return product_registration_template
	else:
		redirect('/login')
	

@route('/product_registration/process', method="POST")
def register_product(session):

	if session.get('email') is not None:
		with mysql_connection:
			mysql_cursor = mysql_connection.cursor();

			product_name = request.forms.get('product_name')
			product_desc = request.forms.get('product_desc')
			mysql_cursor.execute('SELECT id FROM User_info WHERE email=\'%s\'' % session.get('email'))
			seller_id = mysql_cursor.fetchone()[0];
			stock = request.forms.get('stock')
			price = request.forms.get('price')
			img = request.files.get('img')

			if img:
				name, ext = os.path.splitext(img.filename)
				if ext not in ('.png','.jpg','.jpeg'):
					return t('File extension not allowed.')

				save_path = os.path.join(os.getcwd(), 'uploads')
				try:
					img.save(save_path) # appends upload.filename automatically
				except IOError:
					return t("Please change the file name ^_^") # Dirty hack, no same file name for now :(

			mysql_cursor.execute('INSERT INTO  Product(`product_name`,`product_desc`,`seller_id`,`stock`,`price`,`img`) VALUES (\'%s\',\'%s\',\'%d\',\'%d\',\'%f\',\'%s\')' % \
				(product_name,product_desc,int(seller_id),int(stock),float(price),img.filename))

			return t('Successful!')
	else:
		redirect('/login')

#product_registration_routing
@route('/product/edit/:ids')
def product_edit_page_show(session,ids):
	if session.get('email') is not None:
		with mysql_connection:
			mysql_cursor = mysql_connection.cursor()
			mysql_cursor.execute("SELECT * FROM Product WHERE product_code=%d" % int(ids))
			r = mysql_cursor.fetchone()
			seller_id = r[3]
			mysql_cursor.execute("SELECT email FROM User_info WHERE id=%d" % int(seller_id))
			if session.get("email") == mysql_cursor.fetchone()[0]:
				return template(product_edit_template,
					product_id=ids,
					product_name=r[1],
					product_desc=r[2],
					stock=int(r[4]),
					price=float(r[5]))
			else:
				return t("This is not your product")
	else:
		redirect('/login')
	

@route('/product_edit/process', method="POST")
def edit_product(session):

	if session.get('email') is not None:
		with mysql_connection:
			mysql_cursor = mysql_connection.cursor()

			product_code = request.forms.get('product_code')
			product_name = request.forms.get('product_name')
			product_desc = request.forms.get('product_desc')
			stock = request.forms.get('stock')
			price = request.forms.get('price')
			img = request.files.get('img')

			if img:
				name, ext = os.path.splitext(img.filename)
				if ext not in ('.png','.jpg','.jpeg'):
					return t('File extension not allowed.')

				save_path = os.path.join(os.getcwd(), 'uploads')
				try:
					img.save(save_path) # appends upload.filename automatically
					mysql_cursor.execute("UPDATE Product SET img=\"%s\" WHERE product_code=%d" % (img.filename,product_code))
				except IOError:
					return t("Please change the file name ^_^") # Dirty hack, no same file name for now :(

			mysql_cursor.execute("UPDATE Product SET product_name=\"%s\", product_desc=\"%s\", stock=%d, price=%f WHERE product_code=%d" % (product_name, product_desc, int(stock),float(price), int(product_code)))


			return t("Successfully edited!")
	else:
		redirect('/login')

@route('/product/delete/:ids')
def delete_product(session,ids):
	with mysql_connection:
		mysql_cursor = mysql_connection.cursor();
		user_name = session.get('email')
		if user_name is not None:
			# example of SUBQUERY
			mysql_cursor.execute("SELECT email FROM User_info WHERE id=(SELECT seller_id FROM Product WHERE product_code=%d)" % int(ids))
			if session.get("email") == mysql_cursor.fetchone()[0]:
				mysql_cursor.execute("DELETE from Product WHERE product_code=%s" % int(ids))
				t('Deleted')
			else:
				t('Permission denied')
		else:
			redirect('/login')

@route('/cart/add/:product_id/:number_of_order')
def add_to_cart(session, product_id, number_of_order=1):
	with mysql_connection:
		mysql_cursor = mysql_connection.cursor();
		user_name = session.get('email')
		if user_name is not None:

			# dumping as json since sessions can only keep string
			if session.get('cart') is None:
				session['cart'] = json.dumps({})
			cart = json.loads(session['cart'])

			already_ordered = False
			# cart = {"product_id":"number_of_order"}
			for each_item in cart.keys():
				if(str(each_item) == str(product_id)):
					cart[each_item] = str(int(cart[each_item]) + int(number_of_order))
					already_ordered = True

			if not already_ordered:
				cart[str(product_id)] = str(number_of_order)
			session['cart'] = json.dumps(cart)
			return t(session.get('cart'))
		else:
			redirect('/login')

@route('/cart/remove/:product_id')
def remove_from_cart(session, product_id):
	with mysql_connection:
		mysql_cursor = mysql_connection.cursor();
		user_name = session.get('email')
		if user_name is not None:

			# dumping as json since sessions can only keep string
			if session.get('cart') is not None:
				cart = json.loads(session['cart'])

				del cart[str(product_id)]
			
				session['cart'] = json.dumps(cart)
				return t(session.get('cart'))
		else:
			redirect('/login')

@route('/cart/view')
def view_cart(session):
	with mysql_connection:
		mysql_cursor = mysql_connection.cursor();
		user_name = session.get('email')
		if user_name is not None:
			if session.get('cart') is not None:
				cart = json.loads(session['cart'])

				out = '<link href="/static/css/bootstrap.css" rel="stylesheet"><table border="1" style="width:80%"><thead><tr><td>Product</td><td>Unit</td><td>Amount</td><td>Total</td></tr></thead><tbody>'
				total = 0
				for each_item in cart.keys():
					mysql_cursor.execute('SELECT product_name,price,product_code FROM Product WHERE product_code=%d' % int(each_item))
					r = mysql_cursor.fetchone()
					price = float(cart[each_item]) * r[1]
					out = out +  '<tr><td>' + str(r[0]) + '</td><td>' + str(r[1]) + '</td><td>' + str(cart[each_item]) + '</td><td>' + str(price) + '</td><td>' + '<a class="btn btn-md btn-danger" href="/cart/remove/%s">remove</a>' % str(r[2]) + '</td>' '</tr>'
					total = total + price
					
				out = out + '<tr><td></td><td></td><td></td><td>%s</td></tr></tbody></table>' % str(total)
				out = out + '<br><br><a class="btn btn-md btn-primary" href="/cart/checkout">Checkout</a>'
				return out
			else:
				return t('Cart empty!')
		else:
			redirect('/login')

@route('/cart/checkout')
def checkout(session):
	with mysql_connection:
		mysql_cursor = mysql_connection.cursor();
		user_name = session.get('email')
		if user_name is not None:
			return template(checkout_template)
		else:
			redirect('/login')

@route('/profile')
@route('/profile/')
def view_profiles(session):
	with mysql_connection:
		mysql_cursor = mysql_connection.cursor();
		user_name = session.get('email')
		if user_name is not None:
			mysql_cursor.execute('SELECT id,name from User_info')
			fields = mysql_cursor.fetchall()
			out = "<ul>"
			for each_field in fields:
				out = out + "<li><a href=\"/profile/%d\">%s</a></li>" % (each_field[0], each_field[1])
			out = out + "</ul>"
			return out
		else:
			redirect('/login')

@route('/profile/:pid')
def view_profile(session, pid=1):
	with mysql_connection:
		mysql_cursor = mysql_connection.cursor();
		user_name = session.get('email')
		if user_name is not None:
			mysql_cursor.execute('SELECT COUNT(*) as item_count, product_name,product_code,img, MAX(price) as max_cost, avg (price) as avg_cost from Product where seller_id = %d' % int(pid))
			field = mysql_cursor.fetchall()[0]
			out = '<h2>Number of Products:' + str(field[0]) + "<br>Maximum Price:" +  str(field[4]) + "<br>Average Price:"+str(field[5]) + '</h2><br><br>'
			mysql_cursor.execute("SELECT product_code, product_name, stock, price from Product WHERE seller_id = %d" % int(pid))
			fields = mysql_cursor.fetchall()
			out = out + '<table border="1" style="width:80%">'
			out = out + '<thead><tr><td>Product Code</td><td>Product Name</td><td>Stock</td><td>Price</td></tr></thead>'
			out = out + '<tbody>'
			counter = 0
			for field in fields:
				counter = counter + 1
				out = out +  '<tr><td>' + str(field[0]) + '</td><td>' + str(field[1]) + '</td><td>' + str(field[2]) + '</td><td>' + str(field[3]) + '</td></tr>'
			out = out +  '</tbody>'
			out = out +  '</table>'
			return out
		else:
			redirect('/login')

@route('/customers/regularity')
def view_regularity():
	with mysql_connection:
		mysql_cursor = mysql_connection.cursor();
		user_name = session.get('email')
		if user_name is not None:
			mysql_cursor.execute("SELECT orders.customer_number , orders.order_number , orders.quantity_ordered , payment.payment_date, (orders.quantity_ordered * orders.price_each) AS subTotal , (CASE orders.quantity_ordered WHEN orders.quantity_ordered = 0 THEN \"irregular\" WHEN orders.quantity_ordered >0 AND orders.quantity_ordered <=5 THEN \"average\" ELSE \"regular\" END ) AS customer_status FROM orders LEFT JOIN payment ON payment.order_id=orders.order_number ORDER BY `orders`.`order_number` ASC")
			fields = mysql_cursor.fetchall()
			out = out + '<table border="1" style="width:80%">'
			out = out + '<thead><tr><td>Customer Number</td><td>Order Number</td><td>Quantity Ordered</td><td>Payment date</td><td>Subtotal</td><td>Customer Status</td></tr></thead>'
			out = out + '<tbody>'
			for field in fields:
				out = out +  '<tr><td>' + str(field[0]) + '</td><td>' + str(field[1]) + '</td><td>' + str(field[2]) + '</td><td>' + str(field[3]) + '</td><td>'+ str(field[4]) + '</td><td>'+ str(field[5]) + '</td></tr>'
			out = out +  '</tbody>'
			out = out +  '</table>'
			return out
		else:
			redirect('/login')

@route('/customers/payments')
def view_regularity():
	with mysql_connection:
		mysql_cursor = mysql_connection.cursor();
		user_name = session.get('email')
		if user_name is not None:
			mysql_cursor.execute("SELECT customer_id , payment.check_number , payment.order_id , (orders.quantity_ordered*orders.price_each) AS total_paid , Product.seller_id , now() AS memo_generated_on FROM payment,orders,Product")
			fields = mysql_cursor.fetchall()
			out = out + '<table border="1" style="width:80%">'
			out = out + '<thead><tr><td>Customer ID</td><td>Check Number</td><td>Order ID</td><td>Total Paid</td><td>Seller ID</td><td>Memo Generation Time</td></tr></thead>'
			out = out + '<tbody>'
			for field in fields:
				out = out +  '<tr><td>' + str(field[0]) + '</td><td>' + str(field[1]) + '</td><td>' + str(field[2]) + '</td><td>' + str(field[3]) + '</td><td>'+ str(field[4]) + '</td><td>'+ str(field[5]) + '</td></tr>'
			out = out +  '</tbody>'
			out = out +  '</table>'
			return out
		else:
			redirect('/login')



# @route('/profile/:pid')
# def view_profile(session, pid=1):
# 	with mysql_connection:
# 		mysql_cursor = mysql_connection.cursor();
# 		user_name = session.get('email')
# 		if user_name is not None:
# 			mysql_cursor.execute('SELECT COUNT(*) as item_count, product_name,product_code,img, MAX(price) as max_cost, avg (price) as avg_cost from Product where seller_id = %d' % int(pid))
# 			fields = mysql_cursor.fetchall()
# 			out = '<table border="1" style="width:80%">'
# 			out = out + '<thead><tr><td>#</td><td>Product Name</td><td>Product Code</td><td>Image File</td><td>Maximum Cost</td><td>Average Cost</td></tr></thead>'
# 			out = out + '<tbody>'
# 			counter = 0
# 			for field in fields:
# 				counter = counter + 1
# 				out = out +  '<tr><td>' + str(field[0]) + '</td><td>' + str(field[1]) + '</td><td>' + str(field[2]) + '</td><td>' + str(field[3]) + '</td><td>' + str(field[4]) + '</td><td>' + str(field[5]) + '</td><td></td></tr>'
# 			out = out +  '</tbody>'
# 			out = out +  '</table>'
# 			return out
# 		else:
# 			redirect('/login')

#debug(True)
run(app=leapp, host="localhost",port=8000) 