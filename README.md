# 🚀 Contact Manager Pro - Quick Start Guide

## Overview
A professional contact management system with advanced data structures:
- **Category Tree**: Hierarchical contact organization  
- **Binary Search Tree**: Fast category lookup
- **Priority Queue (Heap)**: VIP contact management
- **Tabbed Interface**: All features on one elegant page

---

## 📦 Installation & Setup

### 1. Navigate to Project
```bash
cd /Users/aaronowens/Documents/cs_course_project/COP4538-Code
```

### 2. Activate Virtual Environment
```bash
source ~/.venv/bin/activate
# OR
source /Users/aaronowens/Documents/cs_course_project/.venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python3 app.py
```

### 5. Open in Browser
```
http://localhost:5001/manage
```

---

## 📋 Features

### Tab 1: All Contacts
- View all contacts with complete information
- See priority badges (color-coded)
- VIP badge for high-priority contacts
- Delete button for each contact
- Statistics showing totals

### Tab 2: VIP Contacts ⭐
- View only VIP contacts (priority 4-5)
- Gold-themed cards
- Sorted by priority (highest first)
- Quick identification of important contacts

### Tab 3: Categories 🌳
- Visual tree of all categories
- Collapsible/expandable nodes
- Contact count per category
- Hierarchical view (e.g., Work → IT → Development)

### Tab 4: Add Contact ➕
- Simple form to add new contacts
- Name and email (required)
- Category with hierarchy support (e.g., `Work/IT/Dev`)
- Priority selector (1-5)
  - 1-3: Normal
  - 4-5: VIP (appears in VIP tab)

### Tab 5: Search & Filter 🔍
- Multi-criteria filtering:
  - **Search**: By name or email
  - **Filter**: By category or priority
  - **Sort**: By name, email, priority, or category
  - **Order**: Ascending or descending
- Results display on same page instantly

---

## 💡 Examples

### Adding a Contact with Hierarchy
1. Go to "Add Contact" tab
2. Name: `John Smith`
3. Email: `john@company.com`
4. Category: `Work/IT/Development` (creates hierarchy!)
5. Priority: `4` (High - VIP)
6. Click "Add Contact"

Result:
- John appears in All Contacts
- John appears in VIP Contacts tab
- Category tree shows: Work → IT → Development → John (1)

### Searching for Contacts
1. Go to "Search & Filter" tab
2. Search: `john`
3. Filter Category: `Work/IT`
4. Sort by: `Priority`
5. Order: `Descending`
6. Click "Search"

Result: Displays matching contacts filtered and sorted by your criteria

---

## 🎨 UI Features

### Color Scheme
- 🟣 Purple/Gradient: Header and highlights
- 🟡 Gold: VIP elements
- 🟢 Green: Success/Primary actions
- 🔴 Red: Delete/Danger actions

### Priority Badges
- **1 - Low** (Green)
- **2 - Normal** (Blue)
- **3 - Medium** (Yellow)
- **4 - High** (Orange) - VIP
- **5 - Urgent** (Red) - VIP

### Icons
- 📋 All Contacts
- ⭐ VIP Contacts
- 🌳 Categories (Tree)
- ➕ Add Contact
- 🔍 Search & Filter

---

## 📊 Data Structures

| Structure | Used For | Performance |
|-----------|----------|-------------|
| **Linked List** | Store all contacts | O(n) traversal |
| **Hash Table** | O(1) email lookup | O(1) search |
| **Tree** | Category hierarchy | O(h) operations |
| **BST** | Sorted categories | O(log n) search |
| **Priority Queue** | VIP ordering | O(log n) add/remove |

---

## 🧪 Verification

Run the verification script to test all components:
```bash
python3 verify.py
```

Expected output:
```
✓ App imports successful
✓ Contacts loaded: 10 contacts
✓ VIP System: 2 VIP contacts
✓ Category Tree: 2 top-level categories
✓ BST Implementation: 5 categories stored
✓ GET / : Status 200
✓ GET /manage : Status 200
✓ All verifications passed!
```

---

## 📁 File Structure

```
COP4538-Code/
├── app.py                      # Main Flask app with data structures
├── requirements.txt            # Python packages
├── templates/
│   ├── index.html             # Home page
│   └── manage.html            # Tabbed management interface
├── verify.py                  # Verification script
├── FEATURES.md                # Detailed features documentation
└── README.md                  # This file
```

---

## 🛠 Troubleshooting

### Port Already in Use
```bash
# Use different port
python3 app.py --port 5002
```

### Flask Not Found
```bash
pip install flask==3.0.0
```

### Templates Not Found
Make sure you're in the correct directory:
```bash
cd /Users/aaronowens/Documents/cs_course_project/COP4538-Code
```

---

## 📞 Quick Tips

✨ **Pro Tips**:
1. Use `/` in category names to create hierarchies
2. Set priority 4-5 to make contacts VIP
3. Use the tree view to explore your category structure
4. Search by email is instant (uses hash table)
5. All tabs stay on one page - no reloading!

---

## 📚 See Also

- [FEATURES.md](FEATURES.md) - Detailed feature documentation
- [app.py](app.py) - Source code with data structures
- [manage.html](templates/manage.html) - UI template

---

**Version**: 1.0  
**Last Updated**: April 2026  
**Status**: ✅ Complete & Production Ready
