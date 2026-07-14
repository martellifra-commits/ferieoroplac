<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Calendario Ferie Polivalente</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      padding: 20px;
      background-color: #f9f9f9;
    }

    .container {
      display: flex;
      gap: 30px;
      max-width: 1000px;
      margin: 0 auto;
      background: white;
      padding: 20px;
      border: 1px solid #ccc;
    }

    /* Legenda Persone */
    .legend-box {
      border: 2px solid #000;
      border-collapse: collapse;
      height: fit-content;
    }

    .legend-box td {
      border: 1px solid #000;
      padding: 8px 14px;
      font-weight: bold;
      cursor: pointer;
      user-select: none;
    }

    .legend-box tr.selected-user {
      outline: 3px solid #000;
    }

    .bg-m { background-color: #00b0f0; color: black; } /* MARTELLI */
    .bg-f { background-color: #ffff00; color: black; } /* FILARDO */
    .bg-c { background-color: #ff0000; color: white; } /* CIAPPI */

    /* Calendario */
    .calendar-container {
      flex-grow: 1;
    }

    .month-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #eee;
      border: 1px solid #000;
      border-bottom: none;
      padding: 8px 15px;
      font-weight: bold;
      font-size: 1.2rem;
    }

    .nav-btn {
      background: #000;
      color: white;
      border: none;
      padding: 5px 12px;
      cursor: pointer;
      font-weight: bold;
      border-radius: 3px;
    }

    .calendar-grid {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      border-top: 1px solid #000;
      border-left: 1px solid #000;
    }

    .header-cell, .day-cell {
      border-right: 1px solid #000;
      border-bottom: 1px solid #000;
      text-align: center;
    }

    .header-cell {
      font-weight: bold;
      padding: 6px;
      background-color: #f0f0f0;
    }

    .day-cell {
      min-height: 75px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      cursor: pointer;
      background: white;
    }

    .day-cell.other-month {
      background-color: #fafafa;
    }

    .day-number {
      text-align: right;
      padding: 3px 6px;
      font-weight: bold;
    }

    .day-number.out-month {
      color: red;
    }

    .day-slots {
      display: flex;
      flex-direction: column;
      gap: 2px;
      padding: 2px;
    }

    .badge {
      font-size: 0.75rem;
      font-weight: bold;
      padding: 2px 4px;
      text-align: center;
      border-radius: 2px;
    }

    .controls {
      margin-top: 15px;
      display: flex;
      justify-content: flex-end;
    }

    .btn-clear {
      padding: 8px 15px;
      background: #d9534f;
      color: white;
      border: none;
      cursor: pointer;
      font-weight: bold;
    }
  </style>
</head>
<body>

<div class="container">
  <!-- LEGENDA SELEZIONE -->
  <div>
    <table class="legend-box">
      <tr onclick="selectUser('MARTELLI', 'bg-m', 'M', this)" class="selected-user">
        <td>MARTELLI</td>
        <td class="bg-m">M</td>
      </tr>
      <tr onclick="selectUser('FILARDO', 'bg-f', 'F', this)">
        <td>FILARDO</td>
        <td class="bg-f">F</td>
      </tr>
      <tr onclick="selectUser('CIAPPI', 'bg-c', 'C', this)">
        <td>CIAPPI</td>
        <td class="bg-c">C</td>
      </tr>
    </table>
    <p style="font-size: 0.8rem; color: #555; margin-top: 12px; width: 140px;">
      Seleziona una persona e clicca sui giorni per assegnare o togliere le ferie.
    </p>
  </div>

  <!-- CALENDARIO DINAMICO -->
  <div class="calendar-container">
    <div class="month-header">
      <button class="nav-btn" onclick="changeMonth(-1)">&lt;</button>
      <span id="month-year-label">LUGLIO 2026</span>
      <button class="nav-btn" onclick="changeMonth(1)">&gt;</button>
    </div>

    <div class="calendar-grid" id="calendar">
      <div class="header-cell">LUN</div>
      <div class="header-cell">MAR</div>
      <div class="header-cell">MER</div>
      <div class="header-cell">GIO</div>
      <div class="header-cell">VEN</div>
      <div class="header-cell">SAB</div>
      <div class="header-cell">DOM</div>
    </div>

    <div class="controls">
      <button class="btn-clear" onclick="clearData()">Reset Tutti i Dati</button>
    </div>
  </div>
</div>

<script>
  const monthsNames = [
    "GENNAIO", "FEBBRAIO", "MARZO", "APRILE", "MAGGIO", "GIUGNO",
    "LUGLIO", "AGOSTO", "SETTEMBRE", "OTTOBRE", "NOVEMBRE", "DICEMBRE"
  ];

  // Stato iniziale: Luglio 2026
  let currentDate = new Date(2026, 6, 1); 
  let currentUser = { name: 'MARTELLI', class: 'bg-m', initial: 'M' };
  
  // Caricamento salvataggi dal LocalStorage
  let vacationState = JSON.parse(localStorage.getItem('vacation_data_v2')) || {};

  function selectUser(name, bgClass, initial, element) {
    currentUser = { name, class: bgClass, initial };
    document.querySelectorAll('.legend-box tr').forEach(tr => tr.classList.remove('selected-user'));
    element.classList.add('selected-user');
  }

  function changeMonth(delta) {
    currentDate.setMonth(currentDate.getMonth() + delta);
    renderCalendar();
  }

  function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    // Aggiorna intestazione Mese Anno
    document.getElementById('month-year-label').innerText = `${monthsNames[month]} ${year}`;

    const calendarEl = document.getElementById('calendar');
    const headers = Array.from(calendarEl.querySelectorAll('.header-cell'));
    calendarEl.innerHTML = '';
    headers.forEach(h => calendarEl.appendChild(h));

    // Primo e ultimo giorno del mese
    const firstDayIndex = (new Date(year, month, 1).getDay() + 6) % 7; // Converti per far iniziare da Lunedì (0)
    const totalDaysMonth = new Date(year, month + 1, 0).getDate();
    const prevMonthDays = new Date(year, month, 0).getDate();

    // Giorni del mese precedente (in rosso/grigio)
    for (let i = firstDayIndex; i > 0; i--) {
      const prevDayNum = prevMonthDays - i + 1;
      const dateKey = formatDateKey(year, month - 1, prevDayNum);
      createDayCell(prevDayNum, true, dateKey, calendarEl);
    }

    // Giorni del mese corrente
    for (let day = 1; day <= totalDaysMonth; day++) {
      const dateKey = formatDateKey(year, month, day);
      createDayCell(day, false, dateKey, calendarEl);
    }

    // Completamento griglia con i giorni del mese successivo
    const totalCellsSoFar = firstDayIndex + totalDaysMonth;
    const nextDays = (7 - (totalCellsSoFar % 7)) % 7;
    for (let j = 1; j <= nextDays; j++) {
      const dateKey = formatDateKey(year, month + 1, j);
      createDayCell(j, true, dateKey, calendarEl);
    }
  }

  function formatDateKey(year, month, day) {
    const d = new Date(year, month, day);
    const yyyy = d.getFullYear();
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd}`;
  }

  function createDayCell(dayNum, isOut, dateKey, container) {
    const cell = document.createElement('div');
    cell.className = `day-cell ${isOut ? 'other-month' : ''}`;

    const numDiv = document.createElement('div');
    numDiv.className = `day-number ${isOut ? 'out-month' : ''}`;
    numDiv.innerText = dayNum;

    const slotsDiv = document.createElement('div');
    slotsDiv.className = 'day-slots';

    // Recupera ferie salvate per QUESTA data specifica
    const activeVacations = vacationState[dateKey] || [];

    activeVacations.forEach(vac => {
      const badge = document.createElement('div');
      badge.className = `badge ${vac.class}`;
      badge.innerText = `${vac.name} (${vac.initial})`;
      slotsDiv.appendChild(badge);
    });

    cell.appendChild(numDiv);
    cell.appendChild(slotsDiv);

    cell.onclick = () => toggleVacation(dateKey);

    container.appendChild(cell);
  }

  function toggleVacation(dateKey) {
    if (!vacationState[dateKey]) {
      vacationState[dateKey] = [];
    }

    const existingIndex = vacationState[dateKey].findIndex(v => v.name === currentUser.name);

    if (existingIndex > -1) {
      vacationState[dateKey].splice(existingIndex, 1);
      if (vacationState[dateKey].length === 0) delete vacationState[dateKey];
    } else {
      vacationState[dateKey].push(currentUser);
    }

    localStorage.setItem('vacation_data_v2', JSON.stringify(vacationState));
    renderCalendar();
  }

  function clearData() {
    if (confirm("Vuoi cancellare TUTTI i dati salvati su qualsiasi mese/anno?")) {
      vacationState = {};
      localStorage.removeItem('vacation_data_v2');
      renderCalendar();
    }
  }

  // Inizializza
  renderCalendar();
</script>

</body>
</html>