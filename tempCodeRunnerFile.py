@app.route('/add_item', methods=["POST"])
def add_item():
    item = request.form['item_name'].strip().lower()
    quantity = int(request.form['quantity'])
    name=request.form['user']

    # Fetch all existing items with their IDs
    cursor.execute("SELECT ID, LOWER(ItemName) FROM CulturalInventory")
    existing_items = {name: id for id, name in cursor.fetchall()}

    if item in existing_items:
        # If item exists, update its quantity
        cursor.execute("""
            UPDATE CulturalInventory 
            SET ItemQty = ItemQty + %s 
            WHERE ID = %s;
        """, (quantity, existing_items[item]))
    else:
        # Find the next available ID
        cursor.execute("SELECT MAX(ID) FROM CulturalInventory")
        max_id = cursor.fetchone()[0]  # Get the highest ID
        new_id = (max_id + 1) if max_id else 1  # Assign next ID

        # Insert new item with new ID
        cursor.execute("""
            INSERT INTO CulturalInventory (ID, ItemName, ItemQty)
            VALUES (%s, %s, %s)
        """, (new_id, item, quantity))
        mydb.commit()

    cursor.execute("SELECT Email, Club, Position FROM details WHERE Name = %s", (name,))
    email,club, pos = cursor.fetchone()
    return render_template("admin.html", name=name, position=pos, council=club)