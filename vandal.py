import warnings
from urllib3.exceptions import InsecureRequestWarning
from kernel.__database import *
from kernel.__menu import *
from kernel.__agents import *
from kernel.__listeners import *
from kernel.__utilities import *
from kernel.__routes import initialize_routes

# Suppress only the InsecureRequestWarning from urllib3
warnings.simplefilter('ignore', InsecureRequestWarning)

# Lets call in the endpoints for the listeners
initialize_routes(app)

# Vroom vroom
if __name__ == "__main__":
    reactivate_stored_listeners()
    menu = InteractiveMenu()
    menu.cmdloop()
