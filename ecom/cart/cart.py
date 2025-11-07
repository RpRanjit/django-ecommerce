
class Cart():
    def __init__(self, request):
        self.session = request.session

        #Get the current session if available
        cart = self.session.get('session_key')

        # If the user is new, then create a new session

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        
        # Make sure cart is available to every part of the project
        self.cart = cart