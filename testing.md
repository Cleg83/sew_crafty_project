# Testing performed for Sew Crafty

## Automated Testing

Some automated tests were written for the [checkout app](/checkout/tests.py), and the [user profile_app](/user_profile/tests.py).

## Manual Testing

### Navbar

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Logo link | Redirects user to home page | Clicked link | User redirected to home page | Pass |
| Home link | Redirects user to home page | Clicked link | User redirected to home page | Pass |
| Shop link | Redirects user to shop page | Clicked link | User redirected to shop page | Pass |
| More Dropdown - Expand | Expands and shows events and login links | Clicked dropdown | Dropdown expands and displays correct links | Pass |
| More Dropdown - Collapse | Collapses and hides events and login links | Clicked dropdown | Dropdown collapses and hides correct links | Pass |
| Upcoming Events link | Redirects user to upcoming events page | Clicked link | User redirected to upcoming events page | Pass |
| Login / Create Account link | Redirects user to login/create account page | Clicked link | User redirected to login/create account page | Pass |
| Basket link | Redirects user to basket page | Clicked link | User redirected to basket page | Pass |

### Navbar - Authenticated User

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Logo link | Redirects user to home page | Clicked link | User redirected to home page | Pass |
| Home link | Redirects user to home page | Clicked link | User redirected to home page | Pass |
| Shop link | Redirects user to shop page | Clicked link | User redirected to shop page | Pass |
| More Dropdown - Expand | Expands and shows events, view profile, and logout links | Clicked dropdown | Dropdown expands and displays correct links | Pass |
| More Dropdown - Collapse | Collapses and hides events, view profile, and logout links | Clicked dropdown | Dropdown collapses and hides correct links | Pass |
| Upcoming Events link | Redirects user to upcoming events page | Clicked link | User redirected to upcoming events page | Pass |
| View Profile link | Redirects user to profile page | Clicked link | User redirected to profile page | Pass |
| Logout link | Logs user out and redirects to home page | Clicked link | User logged out and redirected to home page | Pass |
| Basket link | Redirects user to basket page | Clicked link | User redirected to basket page | Pass |

### Navbar - Superuser

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Logo link | Redirects user to home page | Clicked link | User redirected to home page | Pass |
| Home link | Redirects user to home page | Clicked link | User redirected to home page | Pass |
| Shop link | Redirects user to shop page | Clicked link | User redirected to shop page | Pass |
| More Dropdown - Expand | Expands and shows events, manage shop, manage events, view profile, and logout links | Clicked dropdown | Dropdown expands and displays correct links | Pass |
| More Dropdown - Collapse | Collapses and hides events, manage shop, manage events, view profile, and logout links | Clicked dropdown | Dropdown collapses and hides correct links | Pass |
| Upcoming Events link | Redirects user to upcoming events page | Clicked link | User redirected to upcoming events page | Pass |
| Manage Shop link | Redirects user to manage shop page | Clicked link | User redirected to manage shop page | Pass |
| Manage Events link | Redirects user to manage events page | Clicked link | User redirected to manage events page | Pass |
| View Profile link | Redirects user to profile page | Clicked link | User redirected to profile page | Pass |
| Logout link | Logs user out and redirects to home page | Clicked link | User logged out and redirected to home page | Pass |
| Basket link | Redirects user to basket page | Clicked link | User redirected to basket page | Pass |

### Footer

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Instagram link | Redirects user to Sew Crafty Instagram page in a new tab | Clicked link | User redirected to Sew Crafty Instagram page in a new tab | Pass |
| Etsy link | Redirects user to Sew Crafty Etsy page in a new tab | Clicked link | User redirected to Sew Crafty Etsy page in a new tab | Pass |

### Home Page

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Home image animation | Sew Crafty Logo expands on page load | Loaded home page | Logo animation played as expected | Pass |
| Visit the Shop link | Redirects user to shop page | Clicked link | User redirected to shop page | Pass |
| View Upcoming Events link | Redirects user to upcoming events page | Clicked link | User redirected to upcoming events page | Pass |


### Shop Page

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Search bar - With input criteria | Searches shop and displays related results | Input search criteria and clicked search | Correct results displayed | Pass |
| Search bar  - No input criteria| Shows error message if no search criteria is entered | Clicked search without inputting any search criteria | Correct error message displayed | Pass |
| Category dropdown - Expand | Expands to show all categories | Expanded dropdown | Categories displayed | Pass | 
| Category dropdown - Collapse | Collapses dropdown | Collapsed dropdown | Dropdown collapsed | Pass |
| Category dropdown - Select a category | Filters items to only show items belonging to the selected category | Selected a category | Only items in the selected category are shown | Pass | 
| Sort by dropdown - Expand | Expands to show all sorting options | Expanded dropdown | All sorting options displayed | Pass | 
| Sort by dropdown - Collapse | Collapses dropdown | Collapsed dropdown | Dropdown collapsed | Pass |
| Sort by dropdown - Price: Low to high  | Correctly sorts items by selected parameters - within a category if category selected | Clicked sort by Price: Low to high | Items sorted into correct order | Pass |
| Sort by dropdown - Price: High to Low  | Correctly sorts items by selected parameters - within a category if category selected | Clicked sort by Price: High to Low | Items sorted into correct order | Pass |
| Sort by dropdown - Name: A to Z  | Correctly sorts items by selected parameters - within a category if category selected | Clicked sort by Name: A to Z  | Items sorted into correct order | Pass |
| Sort by dropdown - Name: Z to A  | Correctly sorts items by selected parameters - within a category if category selected | Clicked sort by Name: Z to A  | Items sorted into correct order | Pass |
| Item / product link | Loads correct item page when clicked | Clicked product link | Correct item page loads | Pass | 


### Shop Item Page

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Continue shopping button | Redirects user back to shop page | Clicked button | User redirected back to shop page | Pass | 
| Item info - Out of stock | Item page clearly shows the item as out of stock and purchase options are hidden | Clicked on an out of stock item | Item page loads clearly showing it is out of stock and no purchase options are available | Pass | 
| Item info - In stock | Item page shows price and purchase options (quantity & add to basket) | Loaded an in stock item page | Price and purchase options clearly displayed | Pass |
| Item info - Quantity selector | Allows manual entry as well as selecting with upp and down arrows | Manually entered a number as well as using up and down arrows to select quantity | Quantity updated on manual input as well as when using arrow selectors | Pass |
| Item info - Add to basket button | Adds correct quantity to basket and success message displays | Added item to basket | Basket icon updated to show items have been added and success message shown | Pass |


### Basket Page

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Page load - Empty basket | Clearly shows basket is empty and provides a continue shopping button | Loaded page with an empty basket | Stated clearly that the basket was empty with a continue shopping button | Pass | 
Continue shopping button | redirects user back to shop page | Clicked button | User redirected to shop page | Pass | 
| Page load - Basket contains items | Shows basket table and order summary | Loaded page with items in the basket | Basket table and order summary shown | Pass | 
| Product name / link | Redirects user to the info page for the selected item | Clicked link | User redirected to correct item info page | Pass | 
| Quantity column | Allows user to update quantity, shows success message and refreshes the basket total | Updated quantity | Quantity updated correctly, success message displayed and basket total updated | Pass | 
| Remove button | Removes selected item / quantity of items from the basket | Clicked button | Basket updated correctly | Pass | 
| Proceed to checkout button | Redirects user to checkout page | Clicked button | User redirected to checkout page | Pass | 


### Checkout Page 

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |

### Events Page

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |

### Events Page - List View

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |

### Sign Up Page

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Create account button - required fields incomplete | Prompts user to complete required fields | Clicked button | User prompted to complete required fields | Pass |
| Create account button - required fields complete | Creates account, logs user in and redirects to home page | Clicked button | Account created, logged user in and redirected to home page | Pass |
| Log in here link | User is redirected to login page | Clicked link | User redirected to login page | Pass |


### Login Page

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Login button - required fields incomplete | Prompts user to complete required fields | Clicked button | User prompted to complete required fields | Pass |
| Login button - required fields complete | Logs user in and redirects to home page | Clicked button | Logged user in and redirected to home page | Pass |
| Forgot password link | Redirects user to forgotten password page | Clicked link | User redirected to forgotten password page | Pass |
| Sign up here link | Redirects user to sign up page | Clicked link | User redirected to sign up page | Pass |

### Logout Page

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Sign out button | Logs user out and redirects to home page | Clicked button | User logged out and redirected to home page | Pass |
| Cancel link | Cancels sign out and redirects user to home page | Clicked link | User remained logged in and was redirected to home page | Pass |

### User Profile Page

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |

## Admin Only

### Manage Shop Page

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Page Load | Shows all categories and all products with buttons to add both | Loaded manage shop page | All categories and products displayed with buttons to add both  | Pass |
| Add category button | Redirects user to add category page | Clicked button | User redirected to add category page | Pass |
| Add product button | Redirects user to add product page | Clicked button | User redirected to add product page | Pass |

#### Add Product

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Page load | Loads add product form | Loaded page | Add product form loads | Pass |
| Add product button - required fields incomplete | Prompts user to complete required fields | Clicked button | User prompted to complete required fields | Pass |
| Add product button - required fields complete | Adds product, user is redirected to manage shop page and success message is shown | Clicked button | Category added, user redirected to manage shop page and success message is shown | Pass |
| Cancel button | Redirects user back to manage events page | Clicked button | User redirected back to manage events page | Pass | 

#### Edit Item

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Page load | Loads edit product form | Loaded page | Edit product form loads | Pass |
| Save changes button - required fields incomplete | Prompts user to complete required fields | Clicked button | User prompted to complete required fields | Pass |
| Save changes button - required fields complete | Updates product, user is redirected to manage shop page and success message is shown | Clicked button | Product updated, user redirected to manage shop page and success message is shown | Pass |
| Cancel button | Redirects user back to manage shop page | Clicked button | User redirected back to manage shop page | Pass |
| Delete Product


#### Add Category 

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Page load | Loads add category form | Loaded page | Add category form loads | Pass |
| Add category button - required fields incomplete | Prompts user to complete required fields | Clicked button | User prompted to complete required fields | Pass |
| Add category button - required fields complete | Adds category, user is redirected to manage shop page and success message is shown | Clicked button | Category added, user redirected to manage shop page and success message is shown | Pass |
| Cancel button | Redirects user back to manage shop page | Clicked button | User redirected back to manage shop page | Pass | 


#### Edit Category

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Page load | Loads edit category form | Loaded page | Edit category form loads | Pass |
| Save changes button - required fields incomplete | Prompts user to complete required fields | Clicked button | User prompted to complete required fields | Pass |
| Save changes button - required fields complete | Updates category, user is redirected to manage shop page and success message is shown | Clicked button | Category updated, user redirected to manage shop page and success message is shown | Pass |
| Cancel button | Redirects user back to manage shop page | Clicked button | User redirected back to manage shop page | Pass | 


### Manage Events Page

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Page Load | Shows all events (with button to edit and delete each event) with a button to add an event | Loaded manage events page | All events shown (with edit and delete buttons) and a button to add an event | Pass |
| Add event button | Redirects user to add event page | Clicked button | User redirected to add event page | Pass |
| Edit event button | Redirects user to edit page for selected event | Clicked button | User redirected to correct edit event page | Pass |
| Delete event button | Displays a confirm message asking if the user is sure they want to delete the event| Clicked button | Confirm message displayed | Pass |
| Delete event - Popup cancel button | Closes confirm popup | Clicked cancel button | Popup closed | Pass | 
| Delete event - Popup OK button | Deletes event and success message is shown | Clicked OK button | Event deleted and success message displayed | Pass | 


### Add Event 

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Page load | Loads add event page / form | Navigated to add event page | Add event page loads | Pass |
| Add event button - required fields incomplete | User prompted to complete missing required fields | Tried to add event | User prompted to complete required fields | Pass |
| Add event button - required fields complete | Adds event and shows success message | Tried to add event | Event added and success message displayed | Pass |

### Edit Event 

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Page load | Loads edit event page with pre-populated form | Navigated to edit event page | Edit event page loads with correct information pre-populated | Pass |
| Update event button - required fields incomplete | User prompted to complete missing required fields | Tried to update event | User prompted to complete required fields | Pass |
| Update event button - required fields complete | Updates event and shows success message | Tried to update event | Event added and success message displayed | Pass |
| Cancel button | Redirects user back to manage events page | Clicked button | User redirected back to manage events page | Pass | 