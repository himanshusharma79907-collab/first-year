<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Meridian Hospital — Appointments Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
:root {
  --bg: #F7F9FA; --panel: #FFFFFF; --text: #1C2B33; --text-dim: #6B7B82;
  --teal: #2D6E7E; --teal-dim: #E4EEF0; --brick: #C8553D; --brick-dim: #FBEAE6;
  --green: #4C8C6B; --green-dim: #E7F1EC; --border: #E1E6E8;
}
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--text); font-family:'Inter',sans-serif; font-size:14px; }
h1,h2,h3,.num { font-family:'Fraunces',serif; font-weight:600; letter-spacing:-0.01em; }
a { color:inherit; text-decoration:none; }
.layout { display:flex; min-height:100vh; }
.sidebar { width:220px; flex-shrink:0; background:var(--panel); border-right:1px solid var(--border); padding:28px 20px; }
.sidebar .brand { font-family:'Fraunces',serif; font-size:20px; font-weight:600; margin-bottom:4px; }
.sidebar .brand-sub { color:var(--text-dim); font-size:12px; margin-bottom:32px; }
.sidebar nav { display:flex; flex-direction:column; gap:4px; }
.sidebar nav a { padding:9px 12px; border-radius:7px; color:var(--text-dim); font-weight:500; font-size:14px; cursor:pointer; }
.sidebar nav a:hover { background:var(--teal-dim); color:var(--teal); }
.sidebar nav a.active { background:var(--teal); color:#fff; }
.main { flex:1; padding:32px 40px; max-width:1100px; }
.view { display:none; }
.view.active { display:block; }
.page-header { margin-bottom:24px; }
.page-header h1 { font-size:26px; margin:0 0 4px; }
.page-header p { color:var(--text-dim); margin:0; font-size:14px; }
.flash { padding:10px 14px; border-radius:8px; margin-bottom:18px; font-size:13.5px; font-weight:500; display:none; }
.flash.success { background:var(--green-dim); color:var(--green); }
.flash.error { background:var(--brick-dim); color:var(--brick); }
.stat-row { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:24px; }
.stat-card { background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:16px 18px; }
.stat-card .label { color:var(--text-dim); font-size:12.5px; margin-bottom:6px; }
.stat-card .num { font-size:28px; }
.queue-strip { background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:14px 18px; margin-bottom:24px; overflow-x:auto; display:flex; gap:12px; }
.queue-strip .queue-empty { color:var(--text-dim); font-size:13.5px; padding:6px 0; }
.queue-item { flex-shrink:0; border-left:3px solid var(--teal); padding:4px 12px 4px 10px; min-width:160px; }
.queue-item .qtime { font-family:'Fraunces',serif; font-weight:600; font-size:15px; }
.queue-item .qwho { color:var(--text-dim); font-size:12.5px; margin-top:2px; }
.chart-row { display:grid; grid-template-columns:1.3fr 1fr; gap:14px; margin-bottom:24px; }
.chart-card { background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:18px 20px; }
.chart-card h3 { font-size:15px; margin:0 0 14px; font-weight:600; }
table { width:100%; border-collapse:collapse; }
th, td { text-align:left; padding:10px 12px; border-bottom:1px solid var(--border); font-size:13.5px; }
th { color:var(--text-dim); font-weight:500; font-size:12.5px; }
.panel-card { background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:8px 20px; margin-bottom:20px; }
.form-card { background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:20px; margin-bottom:24px; }
.form-card h3 { font-size:15px; margin:0 0 14px; }
.form-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:12px; align-items:end; }
.field label { display:block; font-size:12.5px; color:var(--text-dim); margin-bottom:5px; }
.field input, .field select { width:100%; padding:8px 10px; border:1px solid var(--border); border-radius:7px; font-family:'Inter',sans-serif; font-size:13.5px; background:var(--bg); color:var(--text); }
.field input:focus, .field select:focus { outline:2px solid var(--teal); outline-offset:1px; }
.btn { padding:9px 16px; border-radius:7px; border:none; background:var(--teal); color:#fff; font-weight:500; font-size:13.5px; cursor:pointer; font-family:'Inter',sans-serif; }
.btn:hover { background:#245A67; }
.btn-danger { background:transparent; color:var(--brick); padding:6px 10px; border:none; cursor:pointer; font-family:'Inter',sans-serif; font-size:13px; }
.btn-danger:hover { background:var(--brick-dim); border-radius:6px; }
.pill { display:inline-block; padding:3px 10px; border-radius:100px; font-size:12px; font-weight:500; }
.pill.Scheduled { background:var(--teal-dim); color:var(--teal); }
.pill.Completed { background:var(--green-dim); color:var(--green); }
.pill.Cancelled { background:var(--brick-dim); color:var(--brick); }
.status-select { border:1px solid var(--border); border-radius:6px; padding:4px 6px; font-size:12.5px; font-family:'Inter',sans-serif; background:var(--bg); }
.row-actions { display:flex; align-items:center; gap:8px; }
.empty-state { color:var(--text-dim); padding:24px 0; text-align:center; font-size:13.5px; }
@media (max-width:900px){ .stat-row{grid-template-columns:repeat(2,1fr);} .chart-row{grid-template-columns:1fr;} .layout{flex-direction:column;} .sidebar{width:100%;border-right:none;border-bottom:1px solid var(--border);} }
</style>
</head>
<body>

<div class="layout">
  <aside class="sidebar">
    <div class="brand">Meridian Hospital</div>
    <div class="brand-sub">Appointments desk</div>
    <nav>
      <a data-view="dashboard" class="active">Dashboard</a>
      <a data-view="appointments">Appointments</a>
      <a data-view="doctors">Doctors</a>
      <a data-view="patients">Patients</a>
    </nav>
  </aside>

  <main class="main">
    <div class="flash" id="flash"></div>

    <!-- DASHBOARD -->
    <section class="view active" id="view-dashboard">
      <div class="page-header"><h1>Dashboard</h1><p>Overview of appointments, doctors, and patients.</p></div>
      <div class="stat-row">
        <div class="stat-card"><div class="label">Total doctors</div><div class="num" id="statDoctors">0</div></div>
        <div class="stat-card"><div class="label">Total patients</div><div class="num" id="statPatients">0</div></div>
        <div class="stat-card"><div class="label">Total appointments</div><div class="num" id="statAppointments">0</div></div>
        <div class="stat-card"><div class="label">Today's appointments</div><div class="num" id="statToday">0</div></div>
      </div>
      <div class="queue-strip" id="queueStrip"></div>
      <div class="chart-row">
        <div class="chart-card"><h3>Appointments, last 7 days</h3><canvas id="trendChart" height="110"></canvas></div>
        <div class="chart-card"><h3>Status breakdown</h3><canvas id="statusChart" height="110"></canvas></div>
      </div>
      <div class="chart-row" style="grid-template-columns:1fr;">
        <div class="chart-card"><h3>Appointments by specialization</h3><canvas id="specChart" height="90"></canvas></div>
      </div>
    </section>

    <!-- DOCTORS -->
    <section class="view" id="view-doctors">
      <div class="page-header"><h1>Doctors</h1><p>Manage the doctors available for appointments.</p></div>
      <div class="form-card">
        <h3>Add a doctor</h3>
        <form id="doctorForm" class="form-grid">
          <div class="field"><label>Name</label><input type="text" id="docName" placeholder="Dr. Asha Verma" required></div>
          <div class="field"><label>Specialization</label><input type="text" id="docSpec" placeholder="Cardiology" required></div>
          <div class="field"><button type="submit" class="btn">Add doctor</button></div>
        </form>
      </div>
      <div class="panel-card"><table><thead><tr><th>Name</th><th>Specialization</th><th></th></tr></thead><tbody id="doctorsTable"></tbody></table><div class="empty-state" id="doctorsEmpty" style="display:none;">No doctors yet — add one above.</div></div>
    </section>

    <!-- PATIENTS -->
    <section class="view" id="view-patients">
      <div class="page-header"><h1>Patients</h1><p>Manage registered patients.</p></div>
      <div class="form-card">
        <h3>Add a patient</h3>
        <form id="patientForm" class="form-grid">
          <div class="field"><label>Name</label><input type="text" id="patName" placeholder="Full name" required></div>
          <div class="field"><label>Age</label><input type="number" id="patAge" min="0" max="130"></div>
          <div class="field"><label>Gender</label>
            <select id="patGender"><option value="">—</option><option value="M">M</option><option value="F">F</option><option value="O">O</option></select>
          </div>
          <div class="field"><label>Phone</label><input type="text" id="patPhone" placeholder="98765 43210"></div>
          <div class="field"><button type="submit" class="btn">Add patient</button></div>
        </form>
      </div>
      <div class="panel-card"><table><thead><tr><th>Name</th><th>Age</th><th>Gender</th><th>Phone</th><th></th></tr></thead><tbody id="patientsTable"></tbody></table><div class="empty-state" id="patientsEmpty" style="display:none;">No patients yet — add one above.</div></div>
    </section>

    <!-- APPOINTMENTS -->
    <section class="view" id="view-appointments">
      <div class="page-header"><h1>Appointments</h1><p>Book and manage patient appointments.</p></div>
      <div class="form-card">
        <h3>Book an appointment</h3>
        <div class="empty-state" id="bookingBlocked" style="display:none;">Add at least one patient and one doctor before booking.</div>
        <form id="appointmentForm" class="form-grid" style="display:none;">
          <div class="field"><label>Patient</label><select id="apptPatient" required></select></div>
          <div class="field"><label>Doctor</label><select id="apptDoctor" required></select></div>
          <div class="field"><label>Date</label><input type="date" id="apptDate" required></div>
          <div class="field"><label>Time</label><input type="time" id="apptTime" required></div>
          <div class="field"><button type="submit" class="btn">Book appointment</button></div>
        </form>
      </div>
      <div class="panel-card"><table><thead><tr><th>Date</th><th>Time</th><th>Patient</th><th>Doctor</th><th>Status</th><th></th></tr></thead><tbody id="appointmentsTable"></tbody></table><div class="empty-state" id="appointmentsEmpty" style="display:none;">No appointments booked yet.</div></div>
    </section>
  </main>
</div>

<script>
// ---------- Data layer (localStorage-backed, mirrors the original SQLite schema) ----------
const STORAGE_KEY = 'meridian_hospital_data';

function loadData() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (raw) return JSON.parse(raw);
  // seed data so the dashboard isn't empty on first load
  return {
    nextDoctorId: 3, nextPatientId: 3, nextAppointmentId: 3,
    doctors: [
      { id: 1, name: 'Asha Verma', specialization: 'Cardiology' },
      { id: 2, name: 'Rohan Mehta', specialization: 'Orthopedics' }
    ],
    patients: [
      { id: 1, name: 'Kabir Singh', age: 34, gender: 'M', phone: '9876543210' },
      { id: 2, name: 'Neha Kapoor', age: 28, gender: 'F', phone: '9123456780' }
    ],
    appointments: [
      { id: 1, patientId: 1, doctorId: 1, date: todayStr(), time: '10:30', status: 'Scheduled' },
      { id: 2, patientId: 2, doctorId: 2, date: addDays(1), time: '14:00', status: 'Scheduled' }
    ]
  };
}

function saveData() { localStorage.setItem(STORAGE_KEY, JSON.stringify(DB)); }

function todayStr() { return new Date().toISOString().slice(0, 10); }
function addDays(n) { const d = new Date(); d.setDate(d.getDate() + n); return d.toISOString().slice(0, 10); }

let DB = loadData();

// ---------- Flash messages ----------
function flash(message, type) {
  const el = document.getElementById('flash');
  el.textContent = message;
  el.className = 'flash ' + type;
  el.style.display = 'block';
  setTimeout(() => { el.style.display = 'none'; }, 2600);
}

// ---------- Navigation ----------
document.querySelectorAll('.sidebar nav a').forEach(link => {
  link.addEventListener('click', () => {
    document.querySelectorAll('.sidebar nav a').forEach(a => a.classList.remove('active'));
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    link.classList.add('active');
    document.getElementById('view-' + link.dataset.view).classList.add('active');
    if (link.dataset.view === 'dashboard') renderDashboard();
  });
});

// ---------- Doctors ----------
document.getElementById('doctorForm').addEventListener('submit', (e) => {
  e.preventDefault();
  const name = document.getElementById('docName').value.trim();
  const specialization = document.getElementById('docSpec').value.trim();
  if (!name || !specialization) { flash('Name and specialization are both required.', 'error'); return; }
  DB.doctors.push({ id: DB.nextDoctorId++, name, specialization });
  saveData();
  e.target.reset();
  flash(`Added Dr. ${name}.`, 'success');
  renderDoctors(); renderAppointmentForm();
});

function deleteDoctor(id) {
  const doc = DB.doctors.find(d => d.id === id);
  if (!confirm(`Remove Dr. ${doc.name}? This also removes their appointments.`)) return;
  DB.doctors = DB.doctors.filter(d => d.id !== id);
  DB.appointments = DB.appointments.filter(a => a.doctorId !== id); // cascade, like ON DELETE CASCADE
  saveData();
  flash('Doctor removed.', 'success');
  renderDoctors(); renderAppointments(); renderAppointmentForm();
}

function renderDoctors() {
  const tbody = document.getElementById('doctorsTable');
  tbody.innerHTML = '';
  const sorted = [...DB.doctors].sort((a, b) => a.name.localeCompare(b.name));
  document.getElementById('doctorsEmpty').style.display = sorted.length ? 'none' : 'block';
  sorted.forEach(d => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>Dr. ${escapeHtml(d.name)}</td><td>${escapeHtml(d.specialization)}</td>
      <td><button class="btn-danger" onclick="deleteDoctor(${d.id})">Remove</button></td>`;
    tbody.appendChild(tr);
  });
}

// ---------- Patients ----------
document.getElementById('patientForm').addEventListener('submit', (e) => {
  e.preventDefault();
  const name = document.getElementById('patName').value.trim();
  const ageRaw = document.getElementById('patAge').value;
  const gender = document.getElementById('patGender').value;
  const phone = document.getElementById('patPhone').value.trim();
  if (!name) { flash('Patient name is required.', 'error'); return; }
  DB.patients.push({ id: DB.nextPatientId++, name, age: ageRaw ? parseInt(ageRaw) : null, gender, phone });
  saveData();
  e.target.reset();
  flash(`Added patient ${name}.`, 'success');
  renderPatients(); renderAppointmentForm();
});

function deletePatient(id) {
  const pat = DB.patients.find(p => p.id === id);
  if (!confirm(`Remove ${pat.name}? This also removes their appointments.`)) return;
  DB.patients = DB.patients.filter(p => p.id !== id);
  DB.appointments = DB.appointments.filter(a => a.patientId !== id);
  saveData();
  flash('Patient removed.', 'success');
  renderPatients(); renderAppointments(); renderAppointmentForm();
}

function renderPatients() {
  const tbody = document.getElementById('patientsTable');
  tbody.innerHTML = '';
  const sorted = [...DB.patients].sort((a, b) => a.name.localeCompare(b.name));
  document.getElementById('patientsEmpty').style.display = sorted.length ? 'none' : 'block';
  sorted.forEach(p => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${escapeHtml(p.name)}</td><td>${p.age ?? '—'}</td><td>${p.gender || '—'}</td><td>${escapeHtml(p.phone || '—')}</td>
      <td><button class="btn-danger" onclick="deletePatient(${p.id})">Remove</button></td>`;
    tbody.appendChild(tr);
  });
}

// ---------- Appointments ----------
function renderAppointmentForm() {
  const patSelect = document.getElementById('apptPatient');
  const docSelect = document.getElementById('apptDoctor');
  const blocked = document.getElementById('bookingBlocked');
  const form = document.getElementById('appointmentForm');

  if (!DB.patients.length || !DB.doctors.length) {
    blocked.style.display = 'block';
    form.style.display = 'none';
    return;
  }
  blocked.style.display = 'none';
  form.style.display = 'grid';

  patSelect.innerHTML = DB.patients.map(p => `<option value="${p.id}">${escapeHtml(p.name)}</option>`).join('');
  docSelect.innerHTML = DB.doctors.map(d => `<option value="${d.id}">Dr. ${escapeHtml(d.name)} (${escapeHtml(d.specialization)})</option>`).join('');
}

document.getElementById('appointmentForm').addEventListener('submit', (e) => {
  e.preventDefault();
  const patientId = parseInt(document.getElementById('apptPatient').value);
  const doctorId = parseInt(document.getElementById('apptDoctor').value);
  const date = document.getElementById('apptDate').value;
  const time = document.getElementById('apptTime').value;
  if (!date || !time) { flash('Date and time are required.', 'error'); return; }
  DB.appointments.push({ id: DB.nextAppointmentId++, patientId, doctorId, date, time, status: 'Scheduled' });
  saveData();
  e.target.reset();
  flash('Appointment booked.', 'success');
  renderAppointments();
});

function setAppointmentStatus(id, status) {
  const appt = DB.appointments.find(a => a.id === id);
  appt.status = status;
  saveData();
  flash('Appointment status updated.', 'success');
  renderAppointments();
}

function deleteAppointment(id) {
  if (!confirm('Delete this appointment?')) return;
  DB.appointments = DB.appointments.filter(a => a.id !== id);
  saveData();
  flash('Appointment removed.', 'success');
  renderAppointments();
}

function renderAppointments() {
  const tbody = document.getElementById('appointmentsTable');
  tbody.innerHTML = '';
  const sorted = [...DB.appointments].sort((a, b) => (a.date + a.time).localeCompare(b.date + b.time));
  document.getElementById('appointmentsEmpty').style.display = sorted.length ? 'none' : 'block';

  sorted.forEach(a => {
    const patient = DB.patients.find(p => p.id === a.patientId);
    const doctor = DB.doctors.find(d => d.id === a.doctorId);
    if (!patient || !doctor) return;
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${a.date}</td><td>${a.time}</td>
      <td>${escapeHtml(patient.name)}</td>
      <td>Dr. ${escapeHtml(doctor.name)} <span style="color:var(--text-dim)">(${escapeHtml(doctor.specialization)})</span></td>
      <td><span class="pill ${a.status}">${a.status}</span></td>
      <td><div class="row-actions">
        <select class="status-select" onchange="setAppointmentStatus(${a.id}, this.value)">
          <option value="Scheduled" ${a.status === 'Scheduled' ? 'selected' : ''}>Scheduled</option>
          <option value="Completed" ${a.status === 'Completed' ? 'selected' : ''}>Completed</option>
          <option value="Cancelled" ${a.status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
        </select>
        <button class="btn-danger" onclick="deleteAppointment(${a.id})">Delete</button>
      </div></td>`;
    tbody.appendChild(tr);
  });
}

// ---------- Dashboard ----------
let trendChartInstance, statusChartInstance, specChartInstance;

function renderDashboard() {
  document.getElementById('statDoctors').textContent = DB.doctors.length;
  document.getElementById('statPatients').textContent = DB.patients.length;
  document.getElementById('statAppointments').textContent = DB.appointments.length;
  document.getElementById('statToday').textContent = DB.appointments.filter(a => a.date === todayStr()).length;

  // queue strip: next scheduled appointments today onward
  const queue = DB.appointments
    .filter(a => a.status === 'Scheduled' && a.date >= todayStr())
    .sort((a, b) => (a.date + a.time).localeCompare(b.date + b.time))
    .slice(0, 6);
  const queueEl = document.getElementById('queueStrip');
  if (!queue.length) {
    queueEl.innerHTML = '<div class="queue-empty">No upcoming scheduled appointments.</div>';
  } else {
    queueEl.innerHTML = queue.map(q => {
      const patient = DB.patients.find(p => p.id === q.patientId);
      const doctor = DB.doctors.find(d => d.id === q.doctorId);
      return `<div class="queue-item"><div class="qtime">${q.date} · ${q.time}</div><div class="qwho">${escapeHtml(patient?.name || '—')} → Dr. ${escapeHtml(doctor?.name || '—')}</div></div>`;
    }).join('');
  }

  // 7-day trend
  const trendLabels = [], trendValues = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date(); d.setDate(d.getDate() - i);
    const dstr = d.toISOString().slice(0, 10);
    trendLabels.push(d.toLocaleDateString('en-US', { weekday: 'short', day: '2-digit' }));
    trendValues.push(DB.appointments.filter(a => a.date === dstr).length);
  }

  // status breakdown
  const statusCounts = {};
  DB.appointments.forEach(a => { statusCounts[a.status] = (statusCounts[a.status] || 0) + 1; });

  // specialization load
  const specCounts = {};
  DB.appointments.forEach(a => {
    const doc = DB.doctors.find(d => d.id === a.doctorId);
    if (!doc) return;
    specCounts[doc.specialization] = (specCounts[doc.specialization] || 0) + 1;
  });
  const specEntries = Object.entries(specCounts).sort((a, b) => b[1] - a[1]);

  const teal = '#2D6E7E', green = '#4C8C6B', brick = '#C8553D', dim = '#6B7B82', border = '#E1E6E8';

  if (trendChartInstance) trendChartInstance.destroy();
  trendChartInstance = new Chart(document.getElementById('trendChart'), {
    type: 'line',
    data: { labels: trendLabels, datasets: [{ data: trendValues, borderColor: teal, backgroundColor: 'rgba(45,110,126,0.08)', fill: true, tension: 0.35, pointRadius: 3, pointBackgroundColor: teal }] },
    options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: border } }, x: { grid: { display: false } } } }
  });

  if (statusChartInstance) statusChartInstance.destroy();
  statusChartInstance = new Chart(document.getElementById('statusChart'), {
    type: 'doughnut',
    data: { labels: Object.keys(statusCounts), datasets: [{ data: Object.values(statusCounts), backgroundColor: [teal, green, brick], borderWidth: 0 }] },
    options: { plugins: { legend: { position: 'bottom', labels: { color: dim, boxWidth: 10, font: { size: 11.5 } } } }, cutout: '65%' }
  });

  if (specChartInstance) specChartInstance.destroy();
  specChartInstance = new Chart(document.getElementById('specChart'), {
    type: 'bar',
    data: { labels: specEntries.map(e => e[0]), datasets: [{ data: specEntries.map(e => e[1]), backgroundColor: teal, borderRadius: 5, maxBarThickness: 36 }] },
    options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: border } }, x: { grid: { display: false } } } }
  });
}

function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ---------- Init ----------
saveData(); // persist seed data on first load
renderDoctors();
renderPatients();
renderAppointmentForm();
renderAppointments();
renderDashboard();
</script>

</body>
</html>
