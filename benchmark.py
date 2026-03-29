import time
import random

# Import the functions from app.py
# Since app.py has Flask, we need to import only the functions
# But to avoid running Flask, we'll copy the functions here or import carefully

# For simplicity, define the functions here

def quick_sort_contacts(contacts_list, sort_by='id'):
    """
    Sorts contacts using quick sort algorithm.
    """
    sorted_contacts = contacts_list.copy()
    
    def partition(arr, low, high):
        pivot = arr[high][sort_by]
        i = low - 1
        
        for j in range(low, high):
            if arr[j][sort_by] < pivot:
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

def find_contact_by_id(contacts_list, target_id):
    """
    Performs binary search on a list of contacts sorted by ID.
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

def linear_search_by_id(contacts_list, target_id):
    """
    Performs linear search on a list of contacts by ID.
    """
    for contact in contacts_list:
        if contact['id'] == target_id:
            return contact
    return None

# Generate a large list of contacts for benchmarking
def generate_contacts(n):
    contacts = []
    for i in range(1, n + 1):
        contacts.append({
            'id': i,
            'name': f'Name{i}',
            'email': f'email{i}@example.com'
        })
    random.shuffle(contacts)  # Shuffle to avoid worst-case sorted order
    return contacts

# Benchmarking function
def benchmark_searches(n, num_searches=1000):
    contacts = generate_contacts(n)
    
    # Random target IDs to search for
    target_ids = [random.randint(1, n) for _ in range(num_searches)]
    
    # Linear search time
    start_time = time.time()
    for target_id in target_ids:
        linear_search_by_id(contacts, target_id)
    linear_time = time.time() - start_time
    
    # Binary search time (including sort time)
    sorted_contacts = quick_sort_contacts(contacts, sort_by='id')
    start_time = time.time()
    for target_id in target_ids:
        find_contact_by_id(sorted_contacts, target_id)
    binary_time = time.time() - start_time
    
    print(f"Number of contacts: {n}")
    print(f"Number of searches: {num_searches}")
    print(f"Linear search time: {linear_time:.4f} seconds")
    print(f"Binary search time (including sort): {binary_time:.4f} seconds")
    print(f"Efficiency gain: {linear_time / binary_time:.2f}x faster with binary search")
    
    # Also measure binary search without sort time
    start_time = time.time()
    for target_id in target_ids:
        find_contact_by_id(sorted_contacts, target_id)
    binary_search_only_time = time.time() - start_time
    print(f"Binary search time (search only): {binary_search_only_time:.4f} seconds")
    print(f"Efficiency gain (search only): {linear_time / binary_search_only_time:.2f}x faster")

if __name__ == "__main__":
    # Test with different sizes
    for n in [1000, 10000, 100000]:
        benchmark_searches(n)
        print("-" * 50)