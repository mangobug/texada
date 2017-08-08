# My Product App?

A simple Django application to import product information into a system and run different operations on.

# Deployment

 The project is built using Python 2.7, Django 1.11.4 and Bootstrap3. I have reused a demo bootstrap3 app from a git repo. As the application is very basic, I have carried on using sqlite.

 We will start off by installing pip to configure our packages. Run the following command in your terminal.

	$ easy_install pip


 Go to the project directory /texada and run the following command to setup a virtual environment.

	$ pip install virtualenv
	$ virtualenv env
	$ source env/bin/activate


 Now that the virtual environment is activated, install the packages to use the app


	$ pip install -r requirements.txt


 Create your database tables and set up a superuser:

	$ cd demo
	$ python manage.py migrate
	$ python manage.py createsuperuser


 Launch the development server (this will setup the server on port 8080. You can change it to another port e.g 8000)

	$ python manage.py runserver 8080

 Point your browser at http://127.0.0.1:8080 and you should see the new app.

## Admin Panel
  - Go to http://127.0.0.1:8080/admin and use your superuser credentials (created above) to login as an admin.

## Note

 1. **I was uncertain regarding the requirements for the happiness level. I have assumed there are three distinct levels i.e. 1 (Unhappy) to 3 (Neutral) to 5 (Very Happy)**
 2. **The users belong to different teams, and can be added to a team using the admin panel**
 3. **Links are as such:**

  - **Home:** http://127.0.0.1:8080

  - **Admin:** http://127.0.0.1:8080/admin

  - **Create New Product:** http://127.0.0.1:8080/create/product/

  - **Update Existing Product:** http://127.0.0.1:8080/update/product/<product_id>/

  - **Product Specific Page:** http://127.0.0.1:8080/product/<product_id>/

Happy coding!
