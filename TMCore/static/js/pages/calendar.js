/**
* Author: Cadamuro, Antonio Carlos
* Creation: 2025-09-17
* Component: Calendar
* Description: JavaScript for Calendar page
*/

const dateNow = new Date();
const weekNumber = getWeekOfYear(dateNow);
const weekDay = dateNow.getDay();
const sunday = dateNow.getDate() - weekDay; // First day is the day of the month - the day of the week
const dayNow = dateNow.getDate();
const monthNow = dateNow.getMonth() + 1; //January is 0!
const yearNow = dateNow.getFullYear();

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('todayButton').innerHTML = 'Hoje - ' + dayNow + '/' + monthNow + '/' + yearNow;
  document.getElementById('weekButton').innerHTML = weekNumber;
  document.getElementById('monthSelector').value = monthNow;
  document.getElementById('yearSelector').value = yearNow;

  document.getElementById('sunday').innerHTML = 'Dom - ' + sunday + (sunday == dayNow ? ' (Hoje)' : '');
  document.getElementById('monday').innerHTML = 'Seg - ' + (sunday + 1) + (sunday + 1 == dayNow ? ' (Hoje)' : '');
  document.getElementById('tuesday').innerHTML = 'Ter - ' + (sunday + 2) + (sunday + 2 == dayNow ? ' (Hoje)' : '');
  document.getElementById('wednesday').innerHTML = 'Qua - ' + (sunday + 3) + (sunday + 3 == dayNow ? ' (Hoje)' : '');
  document.getElementById('thursday').innerHTML = 'Qui - ' + (sunday + 4) + (sunday + 4 == dayNow ? ' (Hoje)' : '');
  document.getElementById('friday').innerHTML = 'Sex - ' + (sunday + 5) + (sunday + 5 == dayNow ? ' (Hoje)' : '');
  document.getElementById('saturday').innerHTML = 'Sáb - ' + (sunday + 6) + (sunday + 6 == dayNow ? ' (Hoje)' : '');
});

function addWeek() {
  let weekNumber = parseInt(document.getElementById('weekButton').value) + 1;
  let yearNow = document.getElementById('yearSelector').value;
  if (weekNumber > 52) {
    weekNumber = 1;
    yearNow = parseInt(yearNow) + 1;
  }
  window.location.href = '/calendar/' + parseInt(weekNumber) + '/' + parseInt(yearNow);
}

function decreaseWeek() {
  let weekNumber = document.getElementById('weekButton').value - 1;
  let yearNow = document.getElementById('yearSelector').value;
  if (weekNumber < 1) {
    weekNumber = 52;
    yearNow = parseInt(yearNow) - 1;
  }
  window.location.href = '/calendar/' + parseInt(weekNumber) + '/' + parseInt(yearNow);
}

function monthChange() {
  let month = document.getElementById('monthSelector').value;
  let year = document.getElementById('yearSelector').value;
  let weekNumber = getWeekOfYear(year + '-' + month + '-01');
  window.location.href = '/calendar/' + weekNumber + '/' + year;
}

function yearChange() {
  let month = document.getElementById('monthSelector').value;
  let year = document.getElementById('yearSelector').value;
  let weekNumber = getWeekOfYear(year + '-' + month + '-01');
  window.location.href = '/calendar/' + weekNumber + '/' + year;
}

function getWeekOfYear(date) {
  console.log(date);
  if (!(date instanceof Date)) {
    date = new Date(date);
  }
  console.log(date);
  const firstDayOfAYear = new Date(date.getFullYear(), 0, 1); // Cria uma data para o primeiro dia do ano
  const dayOfWeek = firstDayOfAYear.getDay(); // Obtém o dia da semana (0 para Domingo, 1 para Segunda, etc.)
  let daysToAdd = 1; // Começa a semana na Segunda-feira

  // Se o primeiro dia do ano for Domingo, precisa adicionar 1 dia para começar a semana na Segunda-feira
  if (dayOfWeek === 0) {
    daysToAdd = 1;
  } else {
    // Se o primeiro dia do ano não for Domingo, calcula quantos dias faltam para a Segunda-feira
    daysToAdd = 1 - dayOfWeek;
  }

  // Cria a data da primeira segunda-feira do ano
  const firstMondayOfAYear = new Date(date.getFullYear(), 0, 1 + daysToAdd);

  // Calcula o número de milissegundos entre a data e a primeira segunda-feira do ano
  const diffMilliseconds = date.getTime() - firstMondayOfAYear.getTime();

  // Converte a diferença de milissegundos para dias e depois para semanas
  const diffWeeks = Math.floor(diffMilliseconds / (1000 * 60 * 60 * 24 * 7));

  // Adiciona 1 para obter o número da semana do ano (indexado a partir de 1)
  return diffWeeks + 1;
}

function getCurrentWeekDates() {
  const today = new Date();
  
  // Em JS, getDay() retorna 0=domingo, 1=segunda, ..., 6=sábado
  const dow = today.getDay();
  
  // Voltar até domingo
  const sunday = new Date(today);
  sunday.setDate(today.getDate() - dow);

  // Montar array de 7 dias
  const days = [];
  for (let i = 0; i < 7; i++) {
    const d = new Date(sunday);
    d.setDate(sunday.getDate() + i);
    days.push(d.toISOString().split("T")[0]); // formato YYYY-MM-DD
  }

  return days;
}

console.log(getCurrentWeekDates());

