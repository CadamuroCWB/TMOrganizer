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

document.getElementById('todayButton').innerHTML = 'Hoje - ' + dayNow + '/' + monthNow + '/' + yearNow;
document.getElementById('weekButton').innerHTML = 'Semana ' + weekNumber + ' de ' + yearNow;
document.getElementById('monthSelector').value = monthNow;
document.getElementById('yearSelector').value = yearNow;

document.getElementById('sunday').innerHTML = 'Dom - ' + sunday + (sunday == dayNow ? ' (Hoje)' : '');
document.getElementById('monday').innerHTML = 'Seg - ' + (sunday + 1) + (sunday + 1 == dayNow ? ' (Hoje)' : '');
document.getElementById('tuesday').innerHTML = 'Ter - ' + (sunday + 2) + (sunday + 2 == dayNow ? ' (Hoje)' : '');
document.getElementById('wednesday').innerHTML = 'Qua - ' + (sunday + 3) + (sunday + 3 == dayNow ? ' (Hoje)' : '');
document.getElementById('thursday').innerHTML = 'Qui - ' + (sunday + 4) + (sunday + 4 == dayNow ? ' (Hoje)' : '');
document.getElementById('friday').innerHTML = 'Sex - ' + (sunday + 5) + (sunday + 5 == dayNow ? ' (Hoje)' : '');
document.getElementById('saturday').innerHTML = 'Sáb - ' + (sunday + 6) + (sunday + 6 == dayNow ? ' (Hoje)' : '');

function afterMonthChange() {
    let month = document.getElementById('monthSelector').value;
    let year = document.getElementById('yearSelector').value;
    if (month == 1) {
        month = 12;
        year = year - 1;
    } else {
        month = month - 1;
    }
    document.getElementById('monthSelector').value = month;
    document.getElementById('yearSelector').value = year;
    //window.location.href = '/calendar/' + year + '/' + month;
}

function beforeMonthChange() {
    let month = document.getElementById('monthSelector').value;
    let year = document.getElementById('yearSelector').value;
    if (month == 12) {
        month = 1;
        year = parseInt(year) + 1;
    } else {
        month = parseInt(month) + 1;
    }
    document.getElementById('monthSelector').value = month;
    document.getElementById('yearSelector').value = year;
    //window.location.href = '/calendar/' + year + '/' + month;
}

function getWeekOfYear(date) {
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
