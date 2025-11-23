from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        #Get the current session if available
        cart = self.session.get('session_key')

        # If the user is new, then create a new session

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        
        # Make sure cart is available to every part of the project
        self.cart = cart
        
    def db_add(self, product, quantity):
      product_id = str(product)
      product_qty = str(quantity)
       #logic
      if product_id in self.cart:
          pass
      else:
          self.cart[product_id] = int(product_qty)
        
      self.session.modified = True
      #if logged in
      if self.request.user.is_authenticated:
         # get the current user profile
        current_user = Profile.objects.filter(user__id=self.request.user.id)

        #Convert {'3': 2, '2': 3} to {"3": 2, "2": 3}
        carty = str(self.cart)
        carty = carty.replace("\'","\"" )
        #Save carty to the Profile Model
        current_user.update(old_cart = str(carty))
        

    def add(self, product, quantity):
      product_id = str(product.id)
      product_qty = str(quantity)
    #logic
      if product_id in self.cart:
        pass
      else:
          # self.cart[product_id] = {'price': str(product.price)}
          self.cart[product_id] = int(product_qty)

      self.session.modified = True

      # if logged in
      if self.request.user.is_authenticated:
        # get the current user profile
        current_user = Profile.objects.filter(user__id=self.request.user.id)

        #Convert {'3': 2, '2': 3} to {"3": 2, "2": 3}
        carty = str(self.cart)
        carty = carty.replace("\'","\"" )
        #Save carty to the Profile Model
        current_user.update(old_cart = str(carty))


    def cart_totals(self):
       #Get product ids
       product_ids = self.cart.keys()
       #lookup for those keeys in our database
       products = Product.objects.filter(id__in = product_ids)
       quantities = self.cart
       totals = 0
       for key, value in quantities.items():
          #convert key string into integer
          key = int(key)
          for product in products:
             if product.id == key:
                if product.is_sale:
                  totals  = totals + (product.sale_price * value)
                else:
                  totals  = totals + (product.price * value)
       return totals

    




    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
       #Get ids from cart
       product_ids = self.cart.keys()

       #Use ids to lookup products in database model
       products = Product.objects.filter(id__in = product_ids)

       return products
    
    def get_quants(self):
       quantities = self.cart
       return quantities
    
    def update(self, product, quantity):
      product_id = str(product)
      product_qty = int(quantity)

      # Get cart
      ourcart = self.cart
      # Update Dictionary/cart
      ourcart[product_id] = product_qty

      self.session.modified = True


      if self.request.user.is_authenticated:
         # get the current user profile
        current_user = Profile.objects.filter(user__id=self.request.user.id)

        #Convert {'3': 2, '2': 3} to {"3": 2, "2": 3}
        carty = str(self.cart)
        carty = carty.replace("\'","\"" )
        #Save carty to the Profile Model
        current_user.update(old_cart = str(carty))

      thing = self.cart
      return thing
       
    
    def delete(self, product):
      product_id = str(product)
      # Delete from dictionary/cart
      if product_id in self.cart:
        del self.cart[product_id]

      self.session.modified = True

      if self.request.user.is_authenticated:
         # get the current user profile
        current_user = Profile.objects.filter(user__id=self.request.user.id)

        #Convert {'3': 2, '2': 3} to {"3": 2, "2": 3}
        carty = str(self.cart)
        carty = carty.replace("\'","\"" )
        #Save carty to the Profile Model
        current_user.update(old_cart = str(carty))