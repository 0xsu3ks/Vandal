import cmd,sys
from colorama import init, Fore
from .__listeners import *
from .__agents import *
from .__utilities import intro_art

class InteractiveMenu(cmd.Cmd):
    intro_art()
    intro = """
    \nType help or ? to list commands.\n"""

    prompt = Fore.YELLOW + "vandal$ > " + Fore.RESET 

    def do_quit(self, args):
        print("[-] Quitting")
        return True
    
    def emptyline(self):
        pass

    # def cmdloop(self, intro=""):
    #     print(intro)
    #     while True:
    #         try:
    #             super(InteractiveMenu, self).cmdloop(intro="")
    #             self.postloop()
    #             break
    #         except KeyboardInterrupt:
    #             user_input = input(Fore.RED + "[!] CTRL-C detected, please enter 'killme' to confirm or enter to cancel: " + Fore.RESET)
    #             if user_input == 'killme':
    #                 print("Shutting down...")
    #                 sys.exit(0)

    def cmdloop(self, intro=intro):
        print(intro)
        super(InteractiveMenu, self).cmdloop(intro="")
        self.postloop()


    
    def do_listeners(self, args):
        # Split the arguments
        tokens = args.split()

        # No arguments provided, show the help for listeners
        if len(tokens) == 0:
            self.help_listeners()
            return
        
        if '--list' in tokens:
            list_all_listeners()
            return
        
        if '--types' in tokens:
            listener_types()
            return
        
        if '--create' in tokens:
            try:
                listener_type = tokens[tokens.index('--type') + 1]
                port = int(tokens[tokens.index('--port') + 1])
                key = tokens[tokens.index('--key') + 1]
            
                # Handle --address flag with a default value
                if '--address' in tokens:
                    address = tokens[tokens.index('--address') + 1]
                else:
                    address = '127.0.0.1'  # default

                listener = Listener(listener_type, port, key, address)
                listener.start()
            
            except (ValueError, IndexError):
                print("Error: Invalid arguments for '--create'")
            return
        
        if '--delete' in tokens:
            try:
                listener_id = tokens[tokens.index('--delete') + 1]
                remove_listener(listener_id)
            except IndexError:
                print("Error: Please provide the listener ID to delete.")
        
        # Default
        self.help_listeners()

    def help_listeners(self):
        print("""\nUsage: listeners [OPTIONS]
        
Options:
  --list                   List all listeners
  --types                  List supported listeners and their purpose
  --create                 Create a new listener with specified options:
    --type    [TYPE]       Specify the type of listener (e.g., http)
    --port    [PORT]       Specify the port number for the listener
    --key     [KEY]        Specify the secret key for the listener
    --address [IP ADDRESS] Specify IP address of the listener (default: 127.0.0.1)
  --delete [LISTENER ID]   Delete specified Listener\n""")

    def do_agents(self, args):
        """Manage agents."""
        tokens = args.split()

        if len(tokens) == 0:
            self.help_agents()
            return
        
        if '--list' in tokens:
            list_agents()
            return

        if '--interact' in tokens:
            try:
                agent_id = tokens[tokens.index('--id') + 1]
                interact_with_agent(agent_id)
            except IndexError:
                print("Error: Please provide the agent ID to interact with.")
            except ValueError:
                print("Error: '--id' not found in the provided command.")
            self.help_agents()
            return
        
        if '--commands' in tokens:
            agent_commands()
            return
        
        else:
            self.help_agents()

    def help_agents(self):
        print("""\nUsage: agents [OPTIONS]
        
Options:
  --list                   List all agents
  --interact               Interact with a specific agent:
    --id [AGENT_ID]        Specify the agent ID to interact with\n""")
        
