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

# --- TREE STRUCTURE FOR CATEGORIES ---
class TreeNode:
    """Node for category tree"""
    def __init__(self, name):
        self.name = name
        self.children = {}
        self.contacts = []  # List of contact IDs in this category
    
    def add_child(self, child_name):
        if child_name not in self.children:
            self.children[child_name] = TreeNode(child_name)
        return self.children[child_name]
    
    def add_contact(self, contact_id):
        if contact_id not in self.contacts:
            self.contacts.append(contact_id)

class CategoryTree:
    """Tree structure for organizing contacts by categories"""
    def __init__(self):
        self.root = TreeNode("Root")
    
    def add_contact_to_category(self, contact_id, category_path):
        """Add contact to category path like 'Work/Department/Team'"""
        if not category_path:
            return
        parts = category_path.split('/')
        current = self.root
        for part in parts:
            current = current.add_child(part)
        current.add_contact(contact_id)
    
    def get_contacts_in_category(self, category_path):
        """Get all contact IDs in a category path"""
        if not category_path:
            return []
        parts = category_path.split('/')
        current = self.root
        try:
            for part in parts:
                current = current.children[part]
            return current.contacts
        except KeyError:
            return []

# --- BINARY SEARCH TREE FOR CATEGORIES ---
class BSTNode:
    """Node for Binary Search Tree"""
    def __init__(self, key, value=None):
        self.key = key  # category path
        self.value = value  # list of contact IDs
        self.left = None
        self.right = None

class BST:
    """Binary Search Tree for fast category retrieval"""
    def __init__(self):
        self.root = None
    
    def insert(self, key, value):
        if self.root is None:
            self.root = BSTNode(key, value)
        else:
            self._insert(self.root, key, value)
    
    def _insert(self, node, key, value):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key, value)
            else:
                self._insert(node.left, key, value)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key, value)
            else:
                self._insert(node.right, key, value)
        else:
            # Update value if key exists
            node.value = value
    
    def search(self, key):
        return self._search(self.root, key)
    
    def _search(self, node, key):
        if node is None or node.key == key:
            return node.value if node else None
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)
    
    def inorder_traversal(self):
        """Get all categories in sorted order"""
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append((node.key, node.value))
            self._inorder(node.right, result)

# --- PRIORITY QUEUE (HEAP) FOR VIP CONTACTS ---
import heapq

class PriorityQueue:
    """Priority Queue using heapq for VIP contacts"""
    def __init__(self):
        self.heap = []  # Each element: (-priority, contact_id) for max-heap
        self.entry_count = 0  # To handle duplicate priorities
    
    def push(self, priority, contact_id):
        """Push contact with priority (higher number = higher priority)"""
        heapq.heappush(self.heap, (-priority, self.entry_count, contact_id))
        self.entry_count += 1
    
    def pop(self):
        """Pop highest priority contact"""
        if self.heap:
            return heapq.heappop(self.heap)[2]
        return None
    
    def peek(self):
        """Peek highest priority contact without removing"""
        if self.heap:
            return self.heap[0][2]
        return None
    
    def is_empty(self):
        return len(self.heap) == 0
    
    def get_top_n(self, n):
        """Get top n VIP contacts without removing"""
        return [item[2] for item in heapq.nsmallest(n, self.heap)]

class LinkedList:
    """LinkedList class to manage the linked list structure with hash table optimization"""
    def __init__(self):
        self.head = None
        self.hash_table = {}  # Hash table: email -> contact_data for O(1) lookup
        self.id_counter = 1  # Counter for assigning unique IDs
    
    def append(self, data):
        """Add a node to the end of the linked list and to the hash table"""
        # Assign unique ID
        data['id'] = self.id_counter
        self.id_counter += 1
        
        # Set defaults if not provided
        if 'category' not in data:
            data['category'] = 'General'
        if 'priority' not in data:
            data['priority'] = 1  # Default low priority
        
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

# Category Tree
category_tree = CategoryTree()

# BST for categories
category_bst = BST()

# Priority Queue for VIP contacts
vip_queue = PriorityQueue()

# Dict to track categories for BST updates
category_dict = {}

# Initialize with sample contacts
initial_contacts = [
    {'name': 'John Smith', 'email': 'john.smith@email.com', 'category': 'Work/IT', 'priority': 3},
    {'name': 'Sarah Johnson', 'email': 'sarah.johnson@email.com', 'category': 'Work/HR', 'priority': 2},
    {'name': 'Michael Brown', 'email': 'mbrown@email.com', 'category': 'Personal', 'priority': 1},
    {'name': 'Emily Davis', 'email': 'emily.davis@email.com', 'category': 'Work/IT', 'priority': 4},
    {'name': 'David Wilson', 'email': 'd.wilson@email.com', 'category': 'Work/Finance', 'priority': 2},
    {'name': 'Jessica Martinez', 'email': 'j.martinez@email.com', 'category': 'Personal', 'priority': 1},
    {'name': 'Christopher Lee', 'email': 'c.lee@email.com', 'category': 'Work/Marketing', 'priority': 3},
    {'name': 'Amanda Taylor', 'email': 'amanda.t@email.com', 'category': 'Work/IT', 'priority': 5},
    {'name': 'Ryan Anderson', 'email': 'ryananderson@email.com', 'category': 'Work/Finance', 'priority': 2},
    {'name': 'Nicole Garcia', 'email': 'nicole.garcia@email.com', 'category': 'Personal', 'priority': 1},
]

for contact in initial_contacts:
    contacts.append(contact)

# Build category structures
all_contacts = contacts.to_list()
category_dict = {}
for contact in all_contacts:
    # Add to category tree
    category_tree.add_contact_to_category(contact['id'], contact['category'])
    
    # Collect for BST
    if contact['category'] not in category_dict:
        category_dict[contact['category']] = []
    category_dict[contact['category']].append(contact['id'])
    
    # Add to VIP queue if priority > 3
    if contact['priority'] > 3:
        vip_queue.push(contact['priority'], contact['id'])

# Insert categories into BST
for cat, ids in category_dict.items():
    category_bst.insert(cat, ids)

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

# --- QUICK SORT FOR CONTACTS ---
def quick_sort_contacts(contacts_list, sort_by='name'):
    """
    Sorts contacts using quick sort algorithm.
    
    Args:
        contacts_list: List of contact dictionaries
        sort_by: Field to sort by ('name', 'email', or 'id')
    
    Returns:
        Sorted list of contacts
    
    Time Complexity: O(n log n) average case, O(n^2) worst case
    Space Complexity: O(log n) due to recursion
    """
    # Create a copy to avoid modifying the original
    sorted_contacts = contacts_list.copy()
    
    def partition(arr, low, high):
        pivot = arr[high][sort_by].lower() if sort_by in ['name', 'email'] else arr[high][sort_by]
        i = low - 1
        
        for j in range(low, high):
            comp = arr[j][sort_by].lower() if sort_by in ['name', 'email'] else arr[j][sort_by]
            if comp < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def quick_sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort(arr, low, pi - 1)
            quick_sort(arr, pi + 1, high)
    
    quick_sort(sorted_contacts, 0, len(sorted_contacts) - 1)
    return sorted_contacts

# --- BINARY SEARCH FOR CONTACTS BY ID ---
def find_contact_by_id(contacts_list, target_id):
    """
    Performs binary search on a list of contacts sorted by ID.
    
    Args:
        contacts_list: List of contact dictionaries (assumed sorted by 'id')
        target_id: The ID to search for
    
    Returns:
        Contact dictionary if found, None otherwise
    
    Time Complexity: O(log n)
    """
    left, right = 0, len(contacts_list) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if contacts_list[mid]['id'] == target_id:
            return contacts_list[mid]
        elif contacts_list[mid]['id'] < target_id:
            left = mid + 1
        else:
            right = mid - 1
    
    return None

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
    
    # Get VIP contacts
    vip_contact_ids = vip_queue.get_top_n(5)  # Top 5 VIP
    vip_contacts = [c for c in all_contacts_list if c['id'] in vip_contact_ids]
    
    # Get categories from BST
    categories = category_bst.inorder_traversal()
    
    return render_template('index.html', 
                         contacts=filtered_contacts,
                         all_contacts=all_contacts_list,
                         search_query=search_query,
                         vip_contacts=vip_contacts,
                         categories=categories,
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
    category = request.form.get('category', 'General')
    priority = int(request.form.get('priority', 1))
    
    # Append to linked list
    if name and email:  # Validate inputs
        contact_data = {'name': name, 'email': email, 'category': category, 'priority': priority}
        contacts.append(contact_data)
        
        # Update category structures
        category_tree.add_contact_to_category(contact_data['id'], category)
        if category in category_dict:
            category_dict[category].append(contact_data['id'])
        else:
            category_dict[category] = [contact_data['id']]
            category_bst.insert(category, category_dict[category])
        
        # Add to VIP if high priority
        if priority > 3:
            vip_queue.push(priority, contact_data['id'])
        
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

@app.route('/sort')
def sort_contacts():
    """
    Endpoint to sort all contacts using quick sort algorithm.
    Sorts by name in alphabetical order (case-insensitive).
    """
    all_contacts_list = contacts.to_list()
    sorted_contacts = quick_sort_contacts(all_contacts_list, sort_by='name')
    
    return render_template('index.html',
                         contacts=sorted_contacts,
                         all_contacts=all_contacts_list,
                         sorted=True,
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
