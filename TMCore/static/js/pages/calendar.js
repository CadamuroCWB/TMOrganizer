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

  console.log(new Date(currentWeekDates[0]).toLocaleDateString('pt-BR', { year: 'numeric', month: 'numeric', day: 'numeric' }));

    document.getElementById('todayButton').innerHTML = 'Hoje - ' + new Date().toLocaleDateString('pt-BR', { year: 'numeric', month: 'numeric', day: 'numeric' });
  document.getElementById('monthButton').value = currentWeekDates[0].getMonth() + 1;
  document.getElementById('yearButton').value = yearNow;

  document.getElementById('sunday').innerHTML = 'Dom - ' + currentWeekDates[0].getDay() + (currentWeekDates[0].getDay() == new Date().getDate() ? ' (Hoje)' : '');
  document.getElementById('monday').innerHTML = 'Seg - ' + currentWeekDates[1].getDay() + (currentWeekDates[1].getDay() == new Date().getDate() ? ' (Hoje)' : '');
  document.getElementById('tuesday').innerHTML = 'Ter - ' + currentWeekDates[2].getDay() + (currentWeekDates[2].getDay() == new Date().getDate() ? ' (Hoje)' : '');
  document.getElementById('wednesday').innerHTML = 'Qua - ' + currentWeekDates[3].getDay() + (currentWeekDates[3].getDay() == new Date().getDate() ? ' (Hoje)' : '');
  document.getElementById('thursday').innerHTML = 'Qui - ' + currentWeekDates[4].getDay() + (currentWeekDates[4].getDay() == new Date().getDate() ? ' (Hoje)' : '');
  document.getElementById('friday').innerHTML = 'Sex - ' + currentWeekDates[5].getDay() + (currentWeekDates[5].getDay() == new Date().getDate() ? ' (Hoje)' : '');
  document.getElementById('saturday').innerHTML = 'Sáb - ' + currentWeekDates[6].getDay() + (currentWeekDates[6].getDay() == new Date().getDate() ? ' (Hoje)' : '');
});

function addWeek() {
  let weekNumber = parseInt(document.getElementById('weekButton').value) + 1;
  let yearNow = document.getElementById('yearButton').innerHTML;
  if (weekNumber > 52) {
    weekNumber = 1;
    yearNow = parseInt(yearNow) + 1;
  }
  window.location.href = '/calendar/' + parseInt(weekNumber) + '/' + parseInt(yearNow);
}

function decreaseWeek() {
  let weekNumber = document.getElementById('weekButton').value - 1;
  let yearNow = document.getElementById('yearButton').innerHTML;
  if (weekNumber < 1) {
    weekNumber = 52;
    yearNow = parseInt(yearNow) - 1;
  }
  window.location.href = '/calendar/' + parseInt(weekNumber) + '/' + parseInt(yearNow);
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
  const startOfWeek = new Date(firstDayOfYear.getTime() + daysToAdd * 24 * 60 * 60 * 1000);
  const endOfWeek = new Date(startOfWeek.getTime() + 6 * 24 * 60 * 60 * 1000);

  const dates = [];
  for (let d = startOfWeek; d <= endOfWeek; d.setDate(d.getDate() + 1)) {
    dates.push(d.toISOString().split("T")[0]);
  }
  return dates;
}
