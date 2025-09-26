/**
* Author: Cadamuro, Antonio Carlos
* Creation: 2025-09-17
* Component: Calendar
* Description: JavaScript for Calendar page
*/

document.addEventListener('DOMContentLoaded', function() {
  const weekNumber = window.location.pathname.split('/')[2];
  const yearNow = window.location.pathname.split('/')[3];
  const currentWeekDates = getCurrentWeekDates(weekNumber, yearNow);

  document.getElementById('todayButton').innerHTML = 'Hoje - ' + new Date().toLocaleDateString('pt-BR', { year: 'numeric', month: 'numeric', day: 'numeric' });
  document.getElementById('weekButton').innerHTML = weekNumber;

  document.getElementById('monthButton').innerHTML = (new Date(currentWeekDates[0])).toLocaleString('pt-BR', { month: 'long' });
  document.getElementById('yearButton').innerHTML = new Date(currentWeekDates[0]).getFullYear();

  document.getElementById('sunday').innerHTML = 'Dom - ' + new Date(currentWeekDates[0]).getDate() + (new Date(currentWeekDates[0]).getDate() == new Date().getDate() ? ' (Hoje)' : '');
  document.getElementById('monday').innerHTML = 'Seg - ' + new Date(currentWeekDates[1]).getDate() + (new Date(currentWeekDates[1]).getDate() == new Date().getDate() ? ' (Hoje)' : '');
  document.getElementById('tuesday').innerHTML = 'Ter - ' + new Date(currentWeekDates[2]).getDate() + (new Date(currentWeekDates[2]).getDate() == new Date().getDate() ? ' (Hoje)' : '');
  document.getElementById('wednesday').innerHTML = 'Qua - ' + new Date(currentWeekDates[3]).getDate() + (new Date(currentWeekDates[3]).getDate() == new Date().getDate() ? ' (Hoje)' : '');
  document.getElementById('thursday').innerHTML = 'Qui - ' + new Date(currentWeekDates[4]).getDate() + (new Date(currentWeekDates[4]).getDate() == new Date().getDate() ? ' (Hoje)' : '');
  document.getElementById('friday').innerHTML = 'Sex - ' + new Date(currentWeekDates[5]).getDate() + (new Date(currentWeekDates[5]).getDate() == new Date().getDate() ? ' (Hoje)' : '');
  document.getElementById('saturday').innerHTML = 'Sáb - ' + new Date(currentWeekDates[6]).getDate() + (new Date(currentWeekDates[6]).getDate() == new Date().getDate() ? ' (Hoje)' : '');

  const hourList = document.getElementById('list-group-items');
  for (let i = 7; i < 23; i++) {
    // Formata o número da hora para ter dois dígitos (00, 01, etc.)
    const formatHour = i.toString().padStart(2, '0');
    
    // Cria um item de lista para cada hora
    const itemList = document.createElement('li');
    itemList.className = 'list-group-item';
    itemList.textContent = `${formatHour}:00`;

    // Adiciona o item à lista
    hourList.appendChild(itemList);
}

});

function addWeek() {
  let weekNumber = parseInt(window.location.pathname.split('/')[2]) + 1;
  let yearNow = parseInt(window.location.pathname.split('/')[3]);
  if (weekNumber > 52) {
    weekNumber = 1;
    yearNow = parseInt(yearNow) + 1;
  }
  window.location.href = '/calendar/' + parseInt(weekNumber) + '/' + parseInt(yearNow);
}

function decreaseWeek() {
  let weekNumber = parseInt(window.location.pathname.split('/')[2]) - 1;
  let yearNow = parseInt(window.location.pathname.split('/')[3]);
  if (weekNumber < 1) {
    weekNumber = 52;
    yearNow = parseInt(yearNow) - 1;
  }
  window.location.href = '/calendar/' + parseInt(weekNumber) + '/' + parseInt(yearNow);
}

function goToToday() {
  const today = new Date();
  const yearNow = today.getFullYear();
  const weekNumber = getWeekOfYear(today);

  window.location.href = '/calendar/' + weekNumber + '/' + yearNow;
}

function getWeekOfYear(date) {
  const currentDate = new Date(date);
  const startOfYear = new Date(currentDate.getFullYear(), 0, 1);
  const pastDaysOfYear = (currentDate - startOfYear) / 86400000;
  return Math.ceil((pastDaysOfYear + startOfYear.getDay() + 1) / 7);
}

function monthChange() {
  let month = document.getElementById('monthButton').innerHTML;
  let year = document.getElementById('yearButton').innerHTML;
  let weekNumber = getWeekOfYear(year + '-' + month + '-01');
  window.location.href = '/calendar/' + weekNumber + '/' + year;
}

function yearChange() {
  let month = document.getElementById('monthButton').innerHTML;
  let year = document.getElementById('yearButton').innerHTML;
  let weekNumber = getWeekOfYear(year + '-' + month + '-01');
  window.location.href = '/calendar/' + weekNumber + '/' + year;
}

function getCurrentWeekDates(weekNumber, year) {
  const firstDayOfYear = new Date(year, 0, 1);
  const daysToAdd = (weekNumber - 1) * 7;
  const startOfWeek = new Date(firstDayOfYear.getTime() + (daysToAdd-2) * 24 * 60 * 60 * 1000);
  const endOfWeek = new Date(startOfWeek.getTime() + 6 * 24 * 60 * 60 * 1000);
  const dates = [];
  for (let d = startOfWeek; d <= endOfWeek; d.setDate(d.getDate() + 1)) {
    dates.push(d.toISOString().split("T")[0]);
  }
  return dates;
}
