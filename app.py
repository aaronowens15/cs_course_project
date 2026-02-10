from flask import Flask, render_template, request, redirect, url_for
import os

class node:
    """Node class for linked list implementation"""
    def __init__(self, data):
        self.data = data
        self.next = None
    
    def __repr__(self):
        return f"Node({self.data})"

class LinkedList:
    """LinkedList class to manage the linked list structure"""
    def __init__(self):
        self.head = None
    
    def append(self, data):
        """Add a node to the end of the linked list"""
        new_node = node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
    
    def to_list(self):
        """Convert linked list to a Python list for rendering"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def search(self, query):
        """Search for contacts matching the query"""
        results = []
        current = self.head
        while current:
            if isinstance(current.data, dict):
                if query in current.data['name'].lower() or query in current.data['email'].lower():
                    results.append(current.data)
            current = current.next
        return results
    
    def __repr__(self):
        return f"LinkedList({self.to_list()})"
    
app = Flask(__name__)

app.config['FLASK_TITLE'] = ""

# --- IN-MEMORY DATA STRUCTURES (Students will modify this area) ---
# Linked List to store contacts
contacts = LinkedList()

# Initialize with sample contacts
initial_contacts = [
    {'name': 'John Smith', 'email': 'john.smith@email.com'},
    {'name': 'Sarah Johnson', 'email': 'sarah.johnson@email.com'},
    {'name': 'Michael Brown', 'email': 'mbrown@email.com'},
    {'name': 'Emily Davis', 'email': 'emily.davis@email.com'},
    {'name': 'David Wilson', 'email': 'd.wilson@email.com'},
    {'name': 'Jessica Martinez', 'email': 'j.martinez@email.com'},
    {'name': 'Christopher Lee', 'email': 'c.lee@email.com'},
    {'name': 'Amanda Taylor', 'email': 'amanda.t@email.com'},
    {'name': 'Ryan Anderson', 'email': 'ryananderson@email.com'},
    {'name': 'Nicole Garcia', 'email': 'nicole.garcia@email.com'},
]

for contact in initial_contacts:
    contacts.append(contact)

# --- SIMPLE HASH FUNCTION FOR STRINGS ---
def simple_hash(string, table_size=100):
    """
    A simple hash function for strings using the DJB2 algorithm.
    Returns a hash value between 0 and table_size-1.
    """
    hash_value = 5381
    for char in string:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)
    return hash_value % table_size

# --- ROUTES ---

@app.route('/')
def index():
    """
    Displays the main page.
    Displays all contacts from the linked list structure.
    """
    search_query = request.args.get('search', '').lower()
    all_contacts_list = contacts.to_list()
    filtered_contacts = all_contacts_list
    
    if search_query:
        filtered_contacts = contacts.search(search_query)
    
    return render_template('index.html', 
                         contacts=filtered_contacts,
                         all_contacts=all_contacts_list,
                         search_query=search_query,
                         title=app.config['FLASK_TITLE'])

@app.route('/add', methods=['POST'])
def add_contact():
    """
    Endpoint to add a new contact to the linked list.
    Inserts the contact into the linked list structure.
    """
    name = request.form.get('name')
    email = request.form.get('email')
    
    # Append to linked list
    if name and email:  # Validate inputs
        contact_data = {'name': name, 'email': email}
        contacts.append(contact_data)
    
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    """
    Endpoint to search for contacts by name or email in the linked list.
    Traverses the linked list to find matching contacts.
    """
    search_query = request.args.get('search', '').lower()
    filtered_contacts = []
    
    if search_query:
        # Search through the linked list
        filtered_contacts = contacts.search(search_query)
    
    return render_template('index.html',
                         contacts=filtered_contacts,
                         all_contacts=contacts.to_list(),
                         search_query=search_query,
                         search_performed=True,
                         title=app.config['FLASK_TITLE'])

# --- DATABASE CONNECTIVITY (For later phases) ---
# Placeholders for students to fill in during Sessions 5 and 27
def get_postgres_connection():
    pass

def get_mssql_connection():
    pass

if __name__ == '__main__':
    # Run the Flask app on port 5001, accessible externally
    app.run(host='0.0.0.0', port=5001, debug=True)
