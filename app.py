from flask import Flask, render_template, request, redirect, url_for, flash
from config import get_connection

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For flash messages

# ======== HOME & DASHBOARD ========
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')
# ======== USERS ========
@app.route('/users')
def users():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, username, email, role, password FROM users")
    users = cur.fetchall()
    conn.close()
    return render_template('users.html', users=users)

@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        hashed_password = generate_password_hash(password)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
            (username, email, hashed_password, role)
        )
        conn.commit()
        conn.close()
        flash("User added successfully!", "success")
        return redirect(url_for('users'))
    
    return render_template('add_user.html')

@app.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        cur.execute(
            "UPDATE users SET username = %s, email = %s, role = %s WHERE id = %s",
            (username, email, role, id)
        )
        conn.commit()
        conn.close()
        flash("User updated successfully!", "success")
        return redirect(url_for('users'))

    conn.close()
    return render_template('edit_user.html', user=user)

@app.route('/users/delete/<int:id>')
def delete_user(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("User deleted successfully!", "success")
    return redirect(url_for('users'))

# ======== EMPLOYEES ========
@app.route('/employees')
def employees():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT e.*, d.name AS department_name "
        "FROM employees e "
        "LEFT JOIN departments d ON e.department_id = d.id"
    )
    employees = cur.fetchall()
    conn.close()
    return render_template('employees.html', employees=employees)

@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['email'],
            request.form['phone'],
            request.form['department_id'],
            request.form['designation'],
            request.form['salary'],
            request.form['join_date']
        )
        cur.execute(
            "INSERT INTO employees "
            "(name, email, phone, department_id, designation, salary, join_date) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            data
        )
        conn.commit()
        conn.close()
        flash("Employee added successfully!", "success")
        return redirect(url_for('employees'))

    # GET: load departments for dropdown
    cur.execute("SELECT * FROM departments")
    departments = cur.fetchall()
    conn.close()
    return render_template('add_employee.html', departments=departments)

@app.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['email'],
            request.form['phone'],
            request.form['department_id'],
            request.form['designation'],
            request.form['salary'],
            request.form['join_date'],
            id
        )
        cur.execute(
            "UPDATE employees SET "
            "name=%s, email=%s, phone=%s, department_id=%s, "
            "designation=%s, salary=%s, join_date=%s WHERE id=%s",
            data
        )
        conn.commit()
        conn.close()
        flash("Employee updated successfully!", "success")
        return redirect(url_for('employees'))

    # GET: load employee and departments
    cur.execute("SELECT * FROM departments")
    departments = cur.fetchall()
    cur.execute("SELECT * FROM employees WHERE id = %s", (id,))
    employee = cur.fetchone()
    conn.close()
    return render_template('edit_employee.html', employee=employee, departments=departments)

@app.route('/employees/delete/<int:id>')
def delete_employee(id):
    conn = get_connection()
    cur = conn.cursor()
    # Unassign assets first to avoid FK errors
    cur.execute("UPDATE assets SET assigned_to = NULL WHERE assigned_to = %s", (id,))
    cur.execute("DELETE FROM employees WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Employee deleted (and assets unassigned) successfully!", "success")
    return redirect(url_for('employees'))

@app.route('/employees/search')
def search_employee():
    keyword = request.args.get('keyword', '')
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT e.*, d.name AS department_name FROM employees e "
        "LEFT JOIN departments d ON e.department_id = d.id "
        "WHERE e.name LIKE %s OR e.email LIKE %s",
        ('%' + keyword + '%', '%' + keyword + '%')
    )
    employees = cur.fetchall()
    conn.close()
    return render_template('employees.html', employees=employees)

# ======== DEPARTMENTS ========
@app.route('/departments')
def departments():
    search_query = request.args.get('search', '')
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    if search_query:
        cur.execute("SELECT * FROM departments WHERE name LIKE %s", ('%' + search_query + '%',))
    else:
        cur.execute("SELECT * FROM departments")

    departments = cur.fetchall()
    conn.close()
    return render_template('departments.html', departments=departments, search_query=search_query)

@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO departments (name, description) VALUES (%s, %s)", (name, description))
        conn.commit()
        conn.close()
        flash('Department added successfully!', 'success')
        return redirect(url_for('departments'))
    return render_template('add_department.html')

@app.route('/edit_department/<int:id>', methods=['GET', 'POST'])
def edit_department(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM departments WHERE id = %s", (id,))
    department = cur.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        cur.execute(
            "UPDATE departments SET name = %s, description = %s WHERE id = %s",
            (name, description, id)
        )
        conn.commit()
        conn.close()
        flash('Department updated successfully!', 'success')
        return redirect(url_for('departments'))

    conn.close()
    return render_template('edit_department.html', department=department)

@app.route('/delete_department/<int:id>')
def delete_department(id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM departments WHERE id = %s", (id,))
        conn.commit()
        flash('Department deleted successfully!', 'success')
    except Exception:
        flash('Error: Department cannot be deleted because it is referenced by other data.', 'danger')
    conn.close()
    return redirect(url_for('departments'))

# ======== PROJECTS ========
@app.route('/projects')
def projects():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM projects")
    projects = cur.fetchall()
    conn.close()
    return render_template('projects.html', projects=projects)

@app.route('/projects/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO projects (title, description, status) VALUES (%s, %s, %s)",
            (title, description, status)
        )
        conn.commit()
        conn.close()
        flash("Project added successfully!", "success")
        return redirect(url_for('projects'))
    return render_template('add_project.html')

@app.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        cur.execute(
            "UPDATE projects SET title=%s, description=%s, status=%s WHERE id=%s",
            (title, description, status, id)
        )
        conn.commit()
        conn.close()
        flash("Project updated successfully!", "success")
        return redirect(url_for('projects'))

    cur.execute("SELECT * FROM projects WHERE id = %s", (id,))
    project = cur.fetchone()
    conn.close()
    return render_template('edit_project.html', project=project)

@app.route('/projects/delete/<int:id>')
def delete_project(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM projects WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Project deleted successfully!", "success")
    return redirect(url_for('projects'))

# ======== TASKS ========
@app.route('/tasks')
def tasks():
    search = request.args.get('search', '')
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    base_q = """
        SELECT t.id, t.title, t.description, t.due_date, t.status,
               e.name AS employee_name, p.title AS project_title
        FROM tasks t
        LEFT JOIN employees e ON t.employee_id = e.id
        LEFT JOIN projects p ON t.project_id = p.id
    """
    if search:
        base_q += " WHERE t.title LIKE %s OR t.description LIKE %s"
        params = ('%'+search+'%', '%'+search+'%')
        cur.execute(base_q, params)
    else:
        cur.execute(base_q)
    tasks = cur.fetchall()
    conn.close()
    return render_template('tasks.html', tasks=tasks, search=search)

@app.route('/tasks/add', methods=['GET', 'POST'])
def add_task():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    # Load employees & projects for dropdowns
    cur.execute("SELECT id, name FROM employees")
    employees = cur.fetchall()
    cur.execute("SELECT id, title FROM projects")
    projects = cur.fetchall()

    if request.method == 'POST':
        data = (
            request.form['title'],
            request.form['description'],
            request.form['due_date'],
            request.form['status'],
            request.form['employee_id'] or None,
            request.form['project_id'] or None
        )
        cur.execute(
            "INSERT INTO tasks (title, description, due_date, status, employee_id, project_id) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            data
        )
        conn.commit()
        conn.close()
        flash("Task added successfully!", "success")
        return redirect(url_for('tasks'))

    conn.close()
    return render_template('add_task.html', employees=employees, projects=projects)

@app.route('/tasks/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Load task
    cur.execute("SELECT * FROM tasks WHERE id = %s", (id,))
    task = cur.fetchone()
    # Load dropdown data
    cur.execute("SELECT id, name FROM employees")
    employees = cur.fetchall()
    cur.execute("SELECT id, title FROM projects")
    projects = cur.fetchall()

    if request.method == 'POST':
        data = (
            request.form['title'],
            request.form['description'],
            request.form['due_date'],
            request.form['status'],
            request.form['employee_id'] or None,
            request.form['project_id'] or None,
            id
        )
        cur.execute(
            "UPDATE tasks SET title=%s, description=%s, due_date=%s, status=%s, "
            "employee_id=%s, project_id=%s WHERE id=%s",
            data
        )
        conn.commit()
        conn.close()
        flash("Task updated successfully!", "success")
        return redirect(url_for('tasks'))

    conn.close()
    return render_template('edit_task.html', task=task, employees=employees, projects=projects)

@app.route('/tasks/delete/<int:id>')
def delete_task(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Task deleted successfully!", "success")
    return redirect(url_for('tasks'))

# ======== ATTENDANCE ========
@app.route('/attendance')
def attendance():
    search = request.args.get('search', '')
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    
    base_q = """
      SELECT a.id, a.date, a.status, e.name AS employee_name
      FROM attendance a
      JOIN employees e ON a.employee_id = e.id
    """
    if search:
        base_q += " WHERE e.name LIKE %s OR a.status LIKE %s"
        params = ('%' + search + '%', '%' + search + '%')
        cur.execute(base_q, params)
    else:
        cur.execute(base_q)
    
    records = cur.fetchall()
    conn.close()
    return render_template('attendance.html', records=records, search=search)

@app.route('/attendance/add', methods=['GET', 'POST'])
def add_attendance():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name FROM employees")
    employees = cur.fetchall()

    if request.method == 'POST':
        data = (
            request.form['employee_id'],
            request.form['date'],
            request.form['status']
        )
        cur.execute(
            "INSERT INTO attendance (employee_id, date, status) VALUES (%s, %s, %s)",
            data
        )
        conn.commit()
        conn.close()
        flash("Attendance record added!", "success")
        return redirect(url_for('attendance'))

    conn.close()
    return render_template('add_attendance.html', employees=employees)

@app.route('/attendance/edit/<int:id>', methods=['GET', 'POST'])
def edit_attendance(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    # Load the record to edit
    cur.execute("SELECT * FROM attendance WHERE id = %s", (id,))
    record = cur.fetchone()
    # Load employees for the dropdown
    cur.execute("SELECT id, name FROM employees")
    employees = cur.fetchall()

    if request.method == 'POST':
        data = (
            request.form['employee_id'],
            request.form['date'],
            request.form['status'],
            id
        )
        cur.execute(
            "UPDATE attendance SET employee_id=%s, date=%s, status=%s WHERE id=%s",
            data
        )
        conn.commit()
        conn.close()
        flash("Attendance record updated!", "success")
        return redirect(url_for('attendance'))

    conn.close()
    return render_template('edit_attendance.html', record=record, employees=employees)

@app.route('/attendance/delete/<int:id>')
def delete_attendance(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM attendance WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Attendance record deleted!", "success")
    return redirect(url_for('attendance'))

# ======== LEAVES ========
@app.route('/leaves')
def leaves():
    search = request.args.get('search', '')
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    
    base_q = """
      SELECT l.id, l.start_date, l.end_date, l.reason, l.status, e.name AS employee_name
      FROM leaves l
      JOIN employees e ON l.employee_id = e.id
    """
    if search:
        base_q += " WHERE e.name LIKE %s OR l.status LIKE %s"
        params = ('%' + search + '%', '%' + search + '%')
        cur.execute(base_q, params)
    else:
        cur.execute(base_q)
    
    records = cur.fetchall()
    conn.close()
    return render_template('leaves.html', records=records, search=search)

@app.route('/leaves/add', methods=['GET', 'POST'])
def add_leaves():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name FROM employees")
    employees = cur.fetchall()

    if request.method == 'POST':
        data = (
            request.form['employee_id'],
            request.form['start_date'],
            request.form['end_date'],
            request.form['reason'],
            request.form['status']
        )
        cur.execute(
            "INSERT INTO leaves (employee_id, start_date, end_date, reason, status) "
            "VALUES (%s, %s, %s, %s, %s)",
            data
        )
        conn.commit()
        conn.close()
        flash("Leave request added!", "success")
        return redirect(url_for('leaves'))

    conn.close()
    return render_template('add_leaves.html', employees=employees)

@app.route('/leaves/edit/<int:id>', methods=['GET', 'POST'])
def edit_leaves(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM leaves WHERE id = %s", (id,))
    record = cur.fetchone()
    cur.execute("SELECT id, name FROM employees")
    employees = cur.fetchall()

    if request.method == 'POST':
        data = (
            request.form['employee_id'],
            request.form['start_date'],
            request.form['end_date'],
            request.form['reason'],
            request.form['status'],
            id
        )
        cur.execute(
            "UPDATE leaves SET employee_id=%s, start_date=%s, end_date=%s, reason=%s, status=%s WHERE id=%s",
            data
        )
        conn.commit()
        conn.close()
        flash("Leave request updated!", "success")
        return redirect(url_for('leaves'))

    conn.close()
    return render_template('edit_leaves.html', record=record, employees=employees)

@app.route('/leaves/delete/<int:id>')
def delete_leaves(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM leaves WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Leave request deleted!", "success")
    return redirect(url_for('leaves'))

# ======== ASSETS ========
@app.route('/assets')
def assets():
    search = request.args.get('search', '')
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    
    base_q = """
      SELECT a.id, a.name, a.description, a.purchase_date, a.status, e.name AS assigned_employee
      FROM assets a
      LEFT JOIN employees e ON a.employee_id = e.id
    """
    if search:
        base_q += " WHERE a.name LIKE %s OR a.status LIKE %s"
        params = ('%' + search + '%', '%' + search + '%')
        cur.execute(base_q, params)
    else:
        cur.execute(base_q)
    
    records = cur.fetchall()
    conn.close()
    return render_template('assets.html', records=records, search=search)

@app.route('/assets/add', methods=['GET', 'POST'])
def add_asset():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name FROM employees")
    employees = cur.fetchall()

    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['description'],
            request.form['purchase_date'],
            request.form['status'],
            request.form['employee_id'] if 'employee_id' in request.form else None
        )
        cur.execute(
            "INSERT INTO assets (name, description, purchase_date, status, employee_id) "
            "VALUES (%s, %s, %s, %s, %s)",
            data
        )
        conn.commit()
        conn.close()
        flash("Asset added successfully!", "success")
        return redirect(url_for('assets'))

    conn.close()
    return render_template('add_asset.html', employees=employees)

@app.route('/assets/edit/<int:id>', methods=['GET', 'POST'])
def edit_asset(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM assets WHERE id = %s", (id,))
    record = cur.fetchone()
    cur.execute("SELECT id, name FROM employees")
    employees = cur.fetchall()

    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['description'],
            request.form['purchase_date'],
            request.form['status'],
            request.form['employee_id'] if 'employee_id' in request.form else None,
            id
        )
        cur.execute(
            "UPDATE assets SET name=%s, description=%s, purchase_date=%s, status=%s, employee_id=%s WHERE id=%s",
            data
        )
        conn.commit()
        conn.close()
        flash("Asset updated successfully!", "success")
        return redirect(url_for('assets'))

    conn.close()
    return render_template('edit_asset.html', record=record, employees=employees)

@app.route('/assets/delete/<int:id>')
def delete_asset(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM assets WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Asset deleted successfully!", "success")
    return redirect(url_for('assets'))

# ======== NOTICES ========
@app.route('/notices')
def notices():
    search = request.args.get('search', '')
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    
    if search:
        cur.execute(
            "SELECT * FROM notices WHERE title LIKE %s OR description LIKE %s ORDER BY posted_at DESC",
            ('%'+search+'%', '%'+search+'%')
        )
    else:
        cur.execute("SELECT * FROM notices ORDER BY posted_at DESC")
    
    records = cur.fetchall()
    conn.close()
    return render_template('notices.html', records=records, search=search)

@app.route('/notices/add', methods=['GET', 'POST'])
def add_notice():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO notices (title, description) VALUES (%s, %s)",
            (title, description)
        )
        conn.commit()
        conn.close()
        flash("Notice posted successfully!", "success")
        return redirect(url_for('notices'))
    return render_template('add_notice.html')

@app.route('/notices/edit/<int:id>', methods=['GET', 'POST'])
def edit_notice(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM notices WHERE id = %s", (id,))
    notice = cur.fetchone()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cur.execute(
            "UPDATE notices SET title = %s, description = %s WHERE id = %s",
            (title, description, id)
        )
        conn.commit()
        conn.close()
        flash("Notice updated successfully!", "success")
        return redirect(url_for('notices'))
    
    conn.close()
    return render_template('edit_notice.html', notice=notice)

@app.route('/notices/delete/<int:id>')
def delete_notice(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notices WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Notice deleted successfully!", "success")
    return redirect(url_for('notices'))

# ======== COMPLAINTS ========
@app.route('/complaints')
def complaints():
    search = request.args.get('search', '')
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    
    if search:
        cur.execute(
            "SELECT * FROM complaints WHERE title LIKE %s OR description LIKE %s ORDER BY created_at DESC",
            ('%'+search+'%', '%'+search+'%')
        )
    else:
        cur.execute("SELECT * FROM complaints ORDER BY created_at DESC")
    
    records = cur.fetchall()
    conn.close()
    return render_template('complaints.html', records=records, search=search)

@app.route('/complaints/add', methods=['GET', 'POST'])
def add_complaint():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO complaints (title, description) VALUES (%s, %s)",
            (title, description)
        )
        conn.commit()
        conn.close()
        flash("Complaint submitted successfully!", "success")
        return redirect(url_for('complaints'))
    return render_template('add_complaint.html')

@app.route('/complaints/edit/<int:id>', methods=['GET', 'POST'])
def edit_complaint(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM complaints WHERE id = %s", (id,))
    complaint = cur.fetchone()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        cur.execute(
            "UPDATE complaints SET title = %s, description = %s, status = %s WHERE id = %s",
            (title, description, status, id)
        )
        conn.commit()
        conn.close()
        flash("Complaint updated successfully!", "success")
        return redirect(url_for('complaints'))
    
    conn.close()
    return render_template('edit_complaint.html', complaint=complaint)

@app.route('/complaints/delete/<int:id>')
def delete_complaint(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM complaints WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Complaint deleted successfully!", "success")
    return redirect(url_for('complaints'))

if __name__ == '__main__':
    app.run(debug=True)
