Project Overview:Create a Recipe Recommendation API that allows users to search for recipes based on available ingredients, dietary preferences, or cuisine type. The API will retrieve recipes from a database, provide detailed instructions, and allow users to save their favorite recipes.

Users can sign up and log in, using API:
	
 	User: POST/users
	Authetication: POST/login

API User:
  
	GET/users:
    - Admin: Retrieves a paginated list of all users.
    - Staff: Retrieves a paginated list of customers (users with ROLE_CUSTOMER).
    - Customer: Forbidden access with an error message.
  
	POST/users:
    - Creates a new user with the provided data. The password is hashed before being saved to the database.
  
	DELETE/users:
    - Customer role: Allows the user to delete their own account.
    - Staff role: Forbidden access with an error message.
    - Admin: Allows deletion of any user by ID.
    - The deletion is a soft delete, setting the user's status to False.
  
	GET/users/{id}: Retrieves the user's own information based on their ID from the token. Only the user themselves can access their own data.
  
	PATCH/users/id:
    - Updates the user's information based on their own ID from the token. Only the user themselves can update their own data.
    - If a password is provided, it is hashed before updating the user's record.

API Category:
  
	GET/categories:
    - Admin: Retrieves all categories.
    - Non-admin: Retrieves only active categories (status=True).
		- Supports pagination with page_index and page_size query parameters.
 
	POST/categories: Admin only: Allows creating new categories.
  
	PATCH/categories: Admin only: Allows updating existing categories.
  
	DELETE/categories: Admin only: Soft deletes categories by setting their status to False.
  
	GET/categories/{id}: Retrieves a category by ID. Non-admin users only see active categories.

API Menu:
  
	GET/menus: 
		- Admin: Retrieves a paginated list of all menus.
		- Other roles: Retrieves a paginated list of active menus (where status is True).
		- Supports pagination with page_index and page_size query parameters.
  
	POST/menus:
		- Creates one or more new menus.
		- Admin role required: Only users with the ROLE_ADMIN can create new menus.
		- Validates that the provided category_id for each menu is valid and active (where status is True in the Category table).
  
	PATCH/menus:
		- Updates one or more existing menus.
		- Admin role required: Only users with the ROLE_ADMIN can update menus.
		- Updates only the fields provided in the request, and sets the update_at field to the current timestamp.
  
	DELETE/menus:
		- Soft deletes one or more menus by their IDs (sets the status to False and updates update_at).
		- Admin role required: Only users with the ROLE_ADMIN can delete menus.
  
	GET/menus/{id}:
		- Retrieves a specific menu by its ID.
		- Admin: Can access any menu.
		- Other roles: Can only access active menus.

API Order:
  
	GET/orders:
		- Staff/Admin: Retrieves a paginated list of all orders.
		- Customer: Access is forbidden (HTTP 403).
		- Supports pagination with page_index and page_size query parameters.
  
	POST/orders:
		- Creates a new order.
		- Staff/Admin: Only users with ROLE_STAFF can create new orders.
		- Customer: Access is forbidden (HTTP 403).
  
	DELETE/orders:
		- Soft deletes orders by setting their status to False and updating update_at.
		- Staff/Admin: Only users with ROLE_STAFF can delete orders.
		- Customer: Access is forbidden (HTTP 403).
  
	GET/orders/{id}:
		- Retrieves a specific order by its ID, including its associated items.
		- Staff/Admin: Can access any order.
		- Customer: Access is forbidden (HTTP 403).
  
	POST/orders/{order_id}:
		- Creates new items for a specific order.
		- Staff/Admin: Only users with ROLE_STAFF can add items to orders.
		- Customer: Access is forbidden (HTTP 403).
		- For each item, the total is calculated as quantity * price.
		- The order's quantity and total fields are updated based on the items added.
  
	PATCH/orders/{order_id}:
		- Updates the quantity of a specific item in an order.
		- Staff/Admin: Only users with ROLE_STAFF can update order items.
		- Customer: Access is forbidden (HTTP 403).
		- The item's total is recalculated as quantity * price.
		- The order's quantity and total fields are updated accordingly.
  
	DELETE/orders{order_id}:
		- Deletes specific items from an order.
		- Staff/Admin: Only users with ROLE_STAFF can delete order items.
		- Customer: Access is forbidden (HTTP 403).
		- After deletion, the order's quantity and total fields are updated accordingly.
