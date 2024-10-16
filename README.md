# CSE 4214 / 6214 – Introduction to Software Engineering Group 3 

# **Description:**  
This repository contains the implementation of a locally hosted E-commerce platform. 

# **Objective:**
The objective of this project is to create an E-Commerce Website. This website functions as an online shopping space in which users buy items in an effective manner. Users should have no issue finding, buying, and receiving the correct items they have ordered in a timely manner. The website should be quick and secure, wile also allowing users to easily find any products they want.

# **Features:**
User Management - Management of User information including payment details, login info, shipping details, and any other relevant info.

Product Management - Manage a database of every product and its ID, cost, and any other relevant info.

Search and Comparison - Ability for a user to search and compare inventory. Search should allow user to search in an effective way.

Transaction Handling - Ability to get required payment for item from user, while also dealing with adding and removing from cart and other issues.

Admin Management - Manage the list of authorized admins and allow them to perform needed tasks. Also ability to deny non-admins access to critical features.

# **Languages and Technologies:**
**Backend:** Python with Django framework  
**Frontend:** HTML, CSS  
**Database:** MySQL   

# **Team:**  
**Samuel Karahalis(TheDuckLord2)** - Team Lead - sgk103 - samgkarahalis@gmail.com  
**Ashtanyrein Duncan(Ashtanyrein)** - Member - add485 - add485@msstate.edu  
**CJ Parker(Carlos-Parker3000)** - Member - cdp496 - carlos.parker07300@gmail.com  
**Seth Sorgen(Shale951)** - Member - sls1233 - sethsorgen@gmail.com  
**Sam Mclnnis(samstudentacc)** - Member - stm303 - stm303@msstate.edu 


# **Installation**

### **1. Clone the Repository**

To get started, clone the project repository from GitHub:

```bash
git clone https://github.com/your_username/ecommerce-store-project.git
```

Navigate into the project directory:

```bash
cd ecommerce-store
```

### **2. Install Dependencies**

Install the project dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### **3. Set Up the Database**

1. Open your MySQL client or MySQL Workbench.
2. Create a new database:

```sql
CREATE DATABASE ecommerce_store;
```

### **4. Configure the Project**

Update the `DATABASES` settings in the `ecommerce_store/settings.py` file to match your local MySQL setup:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_store',  # Use the name of the database you just created
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### **5. Run Database Migrations**

Apply the migrations to create the necessary tables in your MySQL database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### **6. Run the Development Server**

Start the Django development server:

```bash
python manage.py runserver
```
