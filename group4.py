<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Timetable Management System</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    .sidebar {
      transition: all 0.3s ease;
    }
    .sidebar.collapsed {
      width: 70px;
    }
    .sidebar.collapsed .nav-text {
      display: none;
    }
    .sidebar.collapsed .logo-text {
      display: none;
    }
    .sidebar.collapsed .toggle-btn i {
      transform: rotate(180deg);
    }
    .content {
      transition: all 0.3s ease;
    }
    .content.expanded {
      margin-left: 70px;
    }
    .fade-in {
      animation: fadeIn 0.3s ease-in-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body class="bg-gray-50">
  <div class="flex h-screen overflow-hidden">
    <!-- Sidebar -->
    <div id="sidebar" class="sidebar bg-white shadow-lg h-full fixed z-10">
      <div class="flex flex-col h-full">
        <!-- Logo -->
        <div class="p-4 flex items-center justify-between border-b">
          <div class="flex items-center space-x-2">
            <i class="fas fa-calendar-alt text-primary text-2xl"></i>
            <span class="logo-text text-xl font-bold text-dark">Timetable</span>
          </div>
          <button class="toggle-btn text-gray-500 hover:text-primary focus:outline-none" id="toggleSidebar">
            <i class="fas fa-chevron-left"></i>
          </button>
        </div>
        <!-- Navigation -->
        <nav class="flex-1 overflow-y-auto py-4 px-2">
          <ul class="space-y-2">
            <li><a href="#" class="nav-link active-nav flex items-center p-3 rounded-lg text-dark hover:bg-primary hover:text-white transition-all duration-200" data-target="dashboard"><i class="fas fa-tachometer-alt mr-3"></i><span class="nav-text">Dashboard</span></a></li>
            <li><a href="#" class="nav-link flex items-center p-3 rounded-lg text-dark hover:bg-primary hover:text-white transition-all duration-200" data-target="departments"><i class="fas fa-building mr-3"></i><span class="nav-text">Departments</span></a></li>
            <li><a href="#" class="nav-link flex items-center p-3 rounded-lg text-dark hover:bg-primary hover:text-white transition-all duration-200" data-target="courses"><i class="fas fa-book mr-3"></i><span class="nav-text">Courses</span></a></li>
            <li><a href="#" class="nav-link flex items-center p-3 rounded-lg text-dark hover:bg-primary hover:text-white transition-all duration-200" data-target="venues"><i class="fas fa-map-marker-alt mr-3"></i><span class="nav-text">Venues</span></a></li>
            <li><a href="#" class="nav-link flex items-center p-3 rounded-lg text-dark hover:bg-primary hover:text-white transition-all duration-200" data-target="settings"><i class="fas fa-cog mr-3"></i><span class="nav-text">Settings</span></a></li>
          </ul>
        </nav>
        <!-- User Profile -->
        <div class="p-4 border-t">
          <div class="flex items-center space-x-3">
            <img src="https://randomuser.me/api/portraits/men/1.jpg" alt="User" class="w-10 h-10 rounded-full">
            <div class="nav-text">
              <p class="font-medium text-dark">Admin User</p>
              <p class="text-xs text-gray-500">Administrator</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="content flex-1 overflow-auto ml-64 p-6" id="content">
      <!-- Sections will be loaded here -->
    </div>
  </div>

  <!-- JavaScript Logic -->
  <script>
    const deptTable = document.getElementById('dept-table-body');
    const courseTable = document.getElementById('course-table-body');
    const venueTable = document.getElementById('venue-table-body');
    const deptCount = document.getElementById('dept-count');
    const courseCount = document.getElementById('course-count');
    const venueCount = document.getElementById('venue-count');
    const recentActivity = document.getElementById('recent-activity');

    let departments = JSON.parse(localStorage.getItem('departments') || '[]');
    let courses = JSON.parse(localStorage.getItem('courses') || '[]');
    let venues = JSON.parse(localStorage.getItem('venues') || '[]');

    function saveData() {
      localStorage.setItem('departments', JSON.stringify(departments));
      localStorage.setItem('courses', JSON.stringify(courses));
      localStorage.setItem('venues', JSON.stringify(venues));
    }

    function updateStats() {
      deptCount.textContent = departments.length;
      courseCount.textContent = courses.length;
      venueCount.textContent = venues.length;
    }

    function addRecentActivity(message) {
      const div = document.createElement('div');
      div.className = "flex items-start";
      div.innerHTML = `
        <div class="bg-blue-100 p-2 rounded-full mr-3"><i class="fas fa-plus text-primary"></i></div>
        <div>
          <p class="font-medium">${message}</p>
          <p class="text-xs text-gray-400">Just now</p>
        </div>`;
      recentActivity.prepend(div);
    }

    function renderDepartments() {
      deptTable.innerHTML = '';
      departments.forEach((d, i) => {
        const tr = document.createElement('tr');
        tr.innerHTML = <td class="px-6 py-4">${d.code}</td><td class="px-6 py-4">${d.name}</td><td class="px-6 py-4">-</td>;
        deptTable.appendChild(tr);
      });
    }

    function renderCourses() {
      courseTable.innerHTML = '';
      courses.forEach(c => {
        const dept = departments.find(d => d.id === c.departmentId);
        const tr = document.createElement('tr');
        tr.innerHTML = <td class="px-6 py-4">${c.code}</td><td class="px-6 py-4">${c.name}</td><td class="px-6 py-4">${dept?.name || '-'}</td><td class="px-6 py-4">${c.level} Level</td><td class="px-6 py-4">-</td>;
        courseTable.appendChild(tr);
      });
    }

    function renderVenues() {
      venueTable.innerHTML = '';
      venues.forEach(v => {
        const tr = document.createElement('tr');
        tr.innerHTML = <td class="px-6 py-4">${v.name}</td><td class="px-6 py-4">${v.capacity}</td><td class="px-6 py-4">${v.type}</td><td class="px-6 py-4">-</td>;
        venueTable.appendChild(tr);
      });
    }

    function renderDeptOptions() {
      const select = document.getElementById('course-dept');
      select.innerHTML = '<option value="">Select Department</option>';
      departments.forEach(d => {
        const opt = document.createElement('option');
        opt.value = d.id;
        opt.textContent = d.name;
        select.appendChild(opt);
      });
    }

    function initApp() {
      updateStats();
      renderDepartments();
      renderCourses();
      renderVenues();
      renderDeptOptions();

      // Show default section
      document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
      document.getElementById('dashboard').classList.remove('hidden');
    }

    window.onload = () => {
      initApp();
    };

    // Sidebar Toggle
    document.getElementById('toggleSidebar').addEventListener('click', () => {
      document.getElementById('sidebar').classList.toggle('collapsed');
      document.querySelector('.content').classList.toggle('expanded');
    });

    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', e => {
        e.preventDefault();
        document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
        document.getElementById(link.dataset.target).classList.remove('hidden');
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active-nav'));
        link.classList.add('active-nav');
      });
    });

    // Add Department
    document.getElementById('add-dept-btn').addEventListener('click', () => {
      document.getElementById('dept-form').reset();
      document.getElementById('dept-id').value = '';
      document.getElementById('dept-modal').classList.remove('hidden');
    });

    document.getElementById('dept-cancel-btn').addEventListener('click', () => {
      document.getElementById('dept-modal').classList.add('hidden');
    });

    document.getElementById('dept-form').addEventListener('submit', e => {
      e.preventDefault();
      const id = document.getElementById('dept-id').value || Date.now().toString();
      const code = document.getElementById('dept-code').value.trim();
      const name = document.getElementById('dept-name').value.trim();

      if (!code || !name) return;

      const index = departments.findIndex(d => d.id === id);
      if (index > -1) {
        departments[index] = { id, code, name };
      } else {
        departments.push({ id, code, name });
        addRecentActivity(Department: ${name} was created);
      }

      saveData();
      initApp();
      document.getElementById('dept-modal').classList.add('hidden');
    });

    // Add Course
    document.getElementById('add-course-btn').addEventListener('click', () => {
      document.getElementById('course-form').reset();
      document.getElementById('course-id').value = '';
      document.getElementById('course-modal').classList.remove('hidden');
    });

    document.getElementById('course-cancel-btn').addEventListener('click', () => {
      document.getElementById('course-modal').classList.add('hidden');
    });

    document.getElementById('course-form').addEventListener('submit', e => {
      e.preventDefault();
      const id = document.getElementById('course-id').value || Date.now().toString();
      const code = document.getElementById('course-code').value.trim();
      const name = document.getElementById('course-name').value.trim();
      const departmentId = document.getElementById('course-dept').value;
      const level = document.getElementById('course-level').value;

      if (!code || !name || !departmentId || !level) return;

      const index = courses.findIndex(c => c.id === id);
      if (index > -1) {
        courses[index] = { id, code, name, departmentId, level };
      } else {
        courses.push({ id, code, name, departmentId, level });
        const dept = departments.find(d => d.id === departmentId);
        addRecentActivity(Course: ${name} added to ${dept.name});
      }

      saveData();
      initApp();
      document.getElementById('course-modal').classList.add('hidden');
    });

    // Add Venue
    document.getElementById('add-venue-btn').addEventListener('click', () => {
      document.getElementById('venue-form').reset();
      document.getElementById('venue-id').value = '';
      document.getElementById('venue-modal').classList.remove('hidden');
    });

    document.getElementById('venue-cancel-btn').addEventListener('click', () => {
      document.getElementById('venue-modal').classList.add('hidden');
    });

    document.getElementById('venue-form').addEventListener('submit', e => {
      e.preventDefault();
      const id = document.getElementById('venue-id').value || Date.now().toString();
      const name = document.getElementById('venue-name').value.trim();
      const capacity = parseInt(document.getElementById('venue-capacity').value);
      const type = document.getElementById('venue-type').value;

      if (!name || isNaN(capacity)) return;

      const index = venues.findIndex(v => v.id === id);
      if (index > -1) {
        venues[index] = { id, name, capacity, type };
      } else {
        venues.push({ id, name, capacity, type });
        addRecentActivity(Venue: ${name} was created);
      }

      saveData();
      initApp();
      document.getElementById('venue-modal').classList.add('hidden');
    });

    // Settings Form
    document.getElementById('settings-form').addEventListener('submit', e => {
      e.preventDefault();
      const schoolName = document.getElementById('school-name').value.trim();
      localStorage.setItem('schoolName', schoolName);
      alert("Settings saved!");
    });

    // Load Dashboard on Startup
    document.getElementById('content').innerHTML = `
      <!-- Dashboard Section -->
      <section id="dashboard" class="section fade-in">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-2xl font-bold text-dark">Dashboard</h1>
          <div class="flex space-x-2">
            <button class="bg-primary text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-all">
              <i class="fas fa-plus mr-2"></i> Generate Timetable
            </button>
          </div>
        </div>
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div class="bg-white p-4 rounded-lg shadow">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-gray-500">Departments</p>
                <h3 class="text-2xl font-bold" id="dept-count">0</h3>
              </div>
              <div class="bg-blue-100 p-3 rounded-full">
                <i class="fas fa-building text-primary text-xl"></i>
              </div>
            </div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-gray-500">Courses</p>
                <h3 class="text-2xl font-bold" id="course-count">0</h3>
              </div>
              <div class="bg-green-100 p-3 rounded-full">
                <i class="fas fa-book text-secondary text-xl"></i>
              </div>
            </div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-gray-500">Venues</p>
                <h3 class="text-2xl font-bold" id="venue-count">0</h3>
              </div>
              <div class="bg-purple-100 p-3 rounded-full">
                <i class="fas fa-map-marker-alt text-purple-600 text-xl"></i>
              </div>
            </div>
          </div>
        </div>
        <!-- Recent Activity -->
        <div class="bg-white rounded-lg shadow p-4 mb-6">
          <h2 class="text-xl font-semibold mb-4">Recent Activity</h2>
          <div class="space-y-4" id="recent-activity">
            <div class="flex items-start">
              <div class="bg-blue-100 p-2 rounded-full mr-3">
                <i class="fas fa-plus text-primary"></i>
              </div>
              <div>
                <p class="font-medium">New department added</p>
                <p class="text-sm text-gray-500">Computer Engineering department was created</p>
                <p class="text-xs text-gray-400">Just now</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Departments Section -->
      <section id="departments" class="section hidden fade-in">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-2xl font-bold text-dark">Departments</h1>
          <button class="bg-primary text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-all" id="add-dept-btn">
            <i class="fas fa-plus mr-2"></i> Add Department
          </button>
        </div>
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Code</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200" id="dept-table-body"></tbody>
            </table>
          </div>
        </div>
        <!-- Modal -->
        <div id="dept-modal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-20 hidden">
          <div class="bg-white rounded-lg shadow-xl w-full max-w-md">
            <div class="p-4 border-b">
              <h3 class="text-lg font-semibold" id="dept-modal-title">Add New Department</h3>
            </div>
            <form id="dept-form" class="p-4">
              <input type="hidden" id="dept-id">
              <div class="mb-4">
                <label for="dept-code" class="block text-sm font-medium text-gray-700 mb-1">Department Code</label>
                <input type="text" id="dept-code" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary">
              </div>
              <div class="mb-4">
                <label for="dept-name" class="block text-sm font-medium text-gray-700 mb-1">Department Name</label>
                <input type="text" id="dept-name" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary">
              </div>
              <div class="p-4 border-t flex justify-end space-x-2">
                <button type="button" id="dept-cancel-btn" class="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50">Cancel</button>
                <button type="submit" id="dept-save-btn" class="px-4 py-2 bg-primary text-white rounded-md hover:bg-indigo-700">Save</button>
              </div>
            </form>
          </div>
        </div>
      </section>

      <!-- Courses Section -->
      <section id="courses" class="section hidden fade-in">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-2xl font-bold text-dark">Courses</h1>
          <button class="bg-primary text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-all" id="add-course-btn">
            <i class="fas fa-plus mr-2"></i> Add Course
          </button>
        </div>
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Code</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Department</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Level</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200" id="course-table-body"></tbody>
            </table>
          </div>
        </div>
        <!-- Modal -->
        <div id="course-modal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-20 hidden">
          <div class="bg-white rounded-lg shadow-xl w-full max-w-md">
            <div class="p-4 border-b">
              <h3 class="text-lg font-semibold" id="course-modal-title">Add New Course</h3>
            </div>
            <form id="course-form" class="p-4">
              <input type="hidden" id="course-id">
              <div class="mb-4">
                <label for="course-code" class="block text-sm font-medium text-gray-700 mb-1">Course Code</label>
                <input type="text" id="course-code" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary">
              </div>
              <div class="mb-4">
                <label for="course-name" class="block text-sm font-medium text-gray-700 mb-1">Course Name</label>
                <input type="text" id="course-name" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary">
              </div>
              <div class="mb-4">
                <label for="course-dept" class="block text-sm font-medium text-gray-700 mb-1">Department</label>
                <select id="course-dept" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"></select>
              </div>
              <div class="mb-4">
                <label for="course-level" class="block text-sm font-medium text-gray-700 mb-1">Level</label>
                <select id="course-level" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary">
                  <option value="100">100 Level</option>
                  <option value="200">200 Level</option>
                  <option value="300">300 Level</option>
                  <option value="400">400 Level</option>
                  <option value="500">500 Level</option>
                </select>
              </div>
              <div class="p-4 border-t flex justify-end space-x-2">
                <button type="button" id="course-cancel-btn" class="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50">Cancel</button>
                <button type="submit" id="course-save-btn" class="px-4 py-2 bg-primary text-white rounded-md hover:bg-indigo-700">Save</button>
              </div>
            </form>
          </div>
        </div>
      </section>

      <!-- Venues Section -->
      <section id="venues" class="section hidden fade-in">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-2xl font-bold text-dark">Venues</h1>
          <button class="bg-primary text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-all" id="add-venue-btn">
            <i class="fas fa-plus mr-2"></i> Add Venue
          </button>
        </div>
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Capacity</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200" id="venue-table-body"></tbody>
            </table>
          </div>
        </div>
        <!-- Modal -->
        <div id="venue-modal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-20 hidden">
          <div class="bg-white rounded-lg shadow-xl w-full max-w-md">
            <div class="p-4 border-b">
              <h3 class="text-lg font-semibold" id="venue-modal-title">Add New Venue</h3>
            </div>
            <form id="venue-form" class="p-4">
              <input type="hidden" id="venue-id">
              <div class="mb-4">
                <label for="venue-name" class="block text-sm font-medium text-gray-700 mb-1">Venue Name</label>
                <input type="text" id="venue-name" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary">
              </div>
              <div class="mb-4">
                <label for="venue-capacity" class="block text-sm font-medium text-gray-700 mb-1">Capacity</label>
                <input type="number" id="venue-capacity" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary">
              </div>
              <div class="mb-4">
                <label for="venue-type" class="block text-sm font-medium text-gray-700 mb-1">Type</label>
                <select id="venue-type" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary">
                  <option value="Lecture Hall">Lecture Hall</option>
                  <option value="Lab">Lab</option>
                  <option value="Seminar Room">Seminar Room</option>
                </select>
              </div>
              <div class="p-4 border-t flex justify-end space-x-2">
                <button type="button" id="venue-cancel-btn" class="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50">Cancel</button>
                <button type="submit" id="venue-save-btn" class="px-4 py-2 bg-primary text-white rounded-md hover:bg-indigo-700">Save</button>
              </div>
            </form>
          </div>
        </div>
      </section>

      <!-- Settings Section -->
      <section id="settings" class="section hidden fade-in">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-2xl font-bold text-dark">Settings</h1>
        </div>
        <div class="bg-white rounded-lg shadow p-6">
          <form id="settings-form">
            <div class="mb-4">
              <label for="school-name" class="block text-sm font-medium text-gray-700 mb-1">School Name</label>
              <input type="text" id="school-name" value="${localStorage.getItem('schoolName') || ''}" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary">
            </div>
            <button type="submit" class="bg-primary text-white px-4 py-2 rounded-lg hover:bg-indigo-700">Save Settings</button>
          </form>
        </div>
      </section>
    `;
  </script>
</body>
</html>
