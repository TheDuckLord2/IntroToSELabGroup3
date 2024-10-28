import sys

import mysql.connector

from IntroToSELabGroup3.ecommerce_store.history import OrderHistory
from IntroToSELabGroup3.ecommerce_store.inventory import Inventory


def create_connection(host_name, user_name, user_password, db_name):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )

        if connection.is_connected():
            print("Connection to MySQL DB successful")
            return connection

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None  # Ensure this returns None on error


class Cart:

    def viewCart(self, user_id):
        try:
            try:
                connection = create_connection("localhost", "root", "Shale951", "ecommerce_store")

            except:
                print("Failed database connection.")

                # exits the program if unsuccessful
                sys.exit()

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM cart WHERE user_id = %s", (user_id,))
            cart_items = cursor.fetchall()
            if cart_items:
                print("User's Cart:")
                for item in cart_items:
                    print(f"item_id: {item[2]}, Quantity: {item[1]}")
            else:
                print("Cart is empty.")

        except Exception as e:
            print("Failed to view cart:", e)
            sys.exit(1)
        finally:
            cursor.close()
            connection.close()

    def addToCart(self, user_id, id, quantity, item_id):

        try:
            connection = create_connection("localhost", "root", "Shale951", "ecommerce_store")
            cursor = connection.cursor()

        except Exception as e:
            print("Failed to add item to cart:", e)
            sys.exit(1)

        stock_query = "SELECT stock_quantity FROM storestock WHERE id = %s"
        cursor.execute(stock_query, (item_id,))
        stock_result = cursor.fetchone()

        if stock_result is None:
            print("Item does not exist.")

        else:
            available_stock = stock_result[0]

            # Check if the requested quantity exceeds available stock
            if quantity > available_stock:
                print(f"Cannot add more than {available_stock} of this item to the cart.")

            else:
                query = "INSERT INTO cart (id, quantity, item_id, user_id) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE quantity = quantity + %s"
                data = (id, quantity, item_id, user_id, quantity)
                try:
                    cursor.execute(query, data)
                    connection.commit()
                    print("Item added to cart.")

                except Exception as e:
                    connection.rollback()  # Rollback in case of error
                    print(f"Error occurred: {e}")

                finally:
                    cursor.close()
                    connection.close()

    def removeFromCart(self, user_id, item_id):
        try:
            connection = create_connection("localhost", "root", "Shale951", "ecommerce_store")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM cart WHERE user_id = %s AND item_id = %s", (user_id, item_id))
            connection.commit()
            print("Item removed from cart.")
        except Exception as e:
            print("Failed to remove item from cart:", e)
            sys.exit(1)
        finally:
            cursor.close()
            connection.close()

    def checkOut(self, user_id):
        try:
            connection = create_connection("localhost", "root", "Shale951", "ecommerce_store")
            cursor = connection.cursor()
            # Retrieve cart items
            cursor.execute("SELECT * FROM cart WHERE user_id = %s", (user_id,))
            cart_items = cursor.fetchall()
            if cart_items:
                # Decrease stock and create order
                inventory = Inventory(self.database_name)
                order_history = OrderHistory(self.database_name)
                for item in cart_items:
                    inventory.decreaseStock(item[1], item[2])  # Decrease stock
                order_history.createOrder(user_id)  # Create order
                order_history.addOrderItems(user_id)  # Add order items
                # Clear cart
                cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
                connection.commit()
                print("Checkout completed.")
            else:
                print("Cart is empty.")
        except Exception as e:
            print("Failed to checkout:", e)
        finally:
            cursor.close()
            connection.close()
