from flask import Flask, render_template, request, redirect, url_for
import os

class node:
    """Node class for linked list implementation"""
    def __init__(self, data):
        self.data = data
        self.next = None
    
    def __repr__(self):
        return f"Node({self.data})"

class Stack:
    """Stack class for implementing undo functionality"""
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Push an item onto the stack"""
        self.items.append(item)
    
    def pop(self):
        """Pop an item from the stack"""
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def is_empty(self):
        """Check if the stack is empty"""
        return len(self.items) == 0
    
    def size(self):
        """Get the size of the stack"""
        return len(self.items)
    
    def peek(self):
        """Peek at the top item without removing it"""
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def __repr__(self):
        return f"Stack({self.items})"

class LinkedList:
    """LinkedList class to manage the linked list structure with hash table optimization"""
    def __init__(self):
        self.head = None
        self.hash_table = {}  # Hash table: email -> contact_data for O(1) lookup
    
    def append(self, data):
        """Add a node to the end of the linked list and to the hash table"""
        new_node = node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        # Add to hash table for O(1) lookup by email
        self.hash_table[data['email']] = data
    
    def to_list(self):
        """Convert linked list to a Python list for rendering"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def search(self, query):
        """Search for contacts matching the query by name"""
        results = []
        # Iterate over hash table values for O(n) search by name or email
        for contact in self.hash_table.values():
            if isinstance(contact, dict):
                if query in contact['name'].lower() or query in contact['email'].lower():
                    results.append(contact)
        return results
    
    def search_by_email(self, email):
        """Search for a contact by email - O(1) lookup using hash table"""
        return self.hash_table.get(email, None)
    
    def delete(self, name, email):
        """Delete a contact by name and email"""
        if not self.head:
            return False
        
        # Check if the head node matches
        if self.head.data.get('name') == name and self.head.data.get('email') == email:
            self.head = self.head.next
            # Remove from hash table
            if email in self.hash_table:
                del self.hash_table[email]
            return True
        
        # Search through the rest of the list
        current = self.head
        while current.next:
            if current.next.data.get('name') == name and current.next.data.get('email') == email:
                current.next = current.next.next
                # Remove from hash table
                if email in self.hash_table:
                    del self.hash_table[email]
                return True
            current = current.next
        
        return False
    
    def __repr__(self):
        return f"LinkedList({self.to_list()})"
    
app = Flask(__name__)

app.config['FLASK_TITLE'] = ""

# --- IN-MEMORY DATA STRUCTURES (Students will modify this area) ---
# Linked List to store contacts
contacts = LinkedList()

# Stack for undo functionality
undo_stack = Stack()

# Stack for redo functionality
redo_stack = Stack()

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
    Pushes the operation to the undo stack.
    """
    name = request.form.get('name')
    email = request.form.get('email')
    
    # Append to linked list
    if name and email:  # Validate inputs
        contact_data = {'name': name, 'email': email}
        contacts.append(contact_data)
        # Push the operation to the undo stack
        undo_stack.push({'operation': 'add', 'data': contact_data})
        # Clear redo stack when a new operation is performed
        redo_stack.items.clear()
    
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    """
    Endpoint to search for contacts by name or email in the linked list.
    Uses hash table optimization for O(1) lookups.
    Search by name: O(n) where n is number of contacts
    Search by email: O(1) using hash table lookup
    """
    search_query = request.args.get('search', '').lower()
    filtered_contacts = []
    
    if search_query:
        # Check if it's an exact email match for O(1) lookup
        contact_by_email = contacts.search_by_email(search_query)
        if contact_by_email:
            filtered_contacts = [contact_by_email]
        else:
            # Otherwise search by name or partial email match
            filtered_contacts = contacts.search(search_query)
    
    return render_template('index.html',
                         contacts=filtered_contacts,
                         all_contacts=contacts.to_list(),
                         search_query=search_query,
                         search_performed=True,
                         title=app.config['FLASK_TITLE'])

@app.route('/delete', methods=['POST'])
def delete_contact():
    """
    Endpoint to delete a contact from the linked list.
    Removes the contact by matching name and email.
    Pushes the operation to the undo stack.
    """
    name = request.form.get('name')
    email = request.form.get('email')
    
    if name and email:
        # Push the operation to the undo stack before deleting
        undo_stack.push({'operation': 'delete', 'data': {'name': name, 'email': email}})
        contacts.delete(name, email)
        # Clear redo stack when a new operation is performed
        redo_stack.items.clear()
    
    return redirect(url_for('index'))

@app.route('/undo', methods=['POST'])
def undo_last():
    """
    Endpoint to undo the last operation (add or delete).
    Pops from the undo stack and reverses the operation.
    Pushes the operation to the redo stack for redo functionality.
    """
    last_operation = undo_stack.pop()
    
    if last_operation:
        if last_operation['operation'] == 'add':
            # If the last operation was adding, delete that contact
            contact = last_operation['data']
            contacts.delete(contact['name'], contact['email'])
        elif last_operation['operation'] == 'delete':
            # If the last operation was deleting, add that contact back
            contact = last_operation['data']
            contacts.append(contact)
        
        # Push the operation to the redo stack
        redo_stack.push(last_operation)
    
    return redirect(url_for('index'))

@app.route('/redo', methods=['POST'])
def redo_last():
    """
    Endpoint to redo the last undone operation.
    Pops from the redo stack and reapplies the operation.
    """
    last_operation = redo_stack.pop()
    
    if last_operation:
        if last_operation['operation'] == 'add':
            # Redo the add operation
            contact = last_operation['data']
            contacts.append(contact)
        elif last_operation['operation'] == 'delete':
            # Redo the delete operation
            contact = last_operation['data']
            contacts.delete(contact['name'], contact['email'])
        
        # Push the operation back to the undo stack
        undo_stack.push(last_operation)
    
    return redirect(url_for('index'))

# --- DATABASE CONNECTIVITY (For later phases) ---
# Placeholders for students to fill in during Sessions 5 and 27
def get_postgres_connection():
    pass

def get_mssql_connection():
    pass

if __name__ == '__main__':
    # Run the Flask app on port 5001, accessible externally
    app.run(host='0.0.0.0', port=5001, debug=True)
