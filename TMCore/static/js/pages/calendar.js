/**
* Author: Cadamuro, Antonio Carlos
* Creation: 2025-09-17
* Component: Calendar
* Description: JavaScript for Calendar page
*/

document.addEventListener('DOMContentLoaded', function() {
  // Load participants for the dropdown when the modal is shown
  $('#modalNewEvent').on('show.bs.modal', function () {
    loadParticipants();
  });

  // Handle event form submission
  document.getElementById('btnSaveEvent').addEventListener('click', function() {
    saveEvent();
  });
  
  // Carregar eventos da semana atual
  loadWeekEvents();
  
  /**
   * Carrega os eventos da semana selecionada e preenche a agenda
   */
  function loadWeekEvents() {
    // Obter a data de início da semana atual
    const weekNumber = window.location.pathname.split('/')[2];
    const yearNow = window.location.pathname.split('/')[3];
    const weekDates = getCurrentWeekDates(weekNumber, yearNow);
    const weekStart = weekDates[0]; // Domingo
    
    // Limpar células da agenda
    clearWeekCells();
    
    // Mostrar indicador de carregamento
    showLoadingIndicator();
    
    // Fazer requisição para a API
    fetch(`/api/events-by-week/?week_start=${weekStart}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Erro ao carregar eventos');
        }
        return response.json();
      })
      .then(data => {
        // Preencher a agenda com os eventos
        populateWeekCells(data.events_by_day);
      })
      .catch(error => {
        console.error('Erro ao carregar eventos:', error);
        showErrorMessage();
      })
      .finally(() => {
        // Remover indicador de carregamento
        hideLoadingIndicator();
      });
  }
  
  /**
   * Limpa todas as células da agenda
   */
  function clearWeekCells() {
    document.getElementById('sunday-group-items').innerHTML = '';
    document.getElementById('monday-group-items').innerHTML = '';
    document.getElementById('tuesday-group-items').innerHTML = '';
    document.getElementById('wednesday-group-items').innerHTML = '';
    document.getElementById('thursday-group-items').innerHTML = '';
    document.getElementById('friday-group-items').innerHTML = '';
    document.getElementById('saturday-group-items').innerHTML = '';
  }
  
  /**
   * Mostra indicador de carregamento em cada célula da semana
   */
  function showLoadingIndicator() {
    const loadingHTML = '<div class="text-center"><small>Carregando eventos...</small></div>';
    document.getElementById('sunday-group-items').innerHTML = loadingHTML;
    document.getElementById('monday-group-items').innerHTML = loadingHTML;
    document.getElementById('tuesday-group-items').innerHTML = loadingHTML;
    document.getElementById('wednesday-group-items').innerHTML = loadingHTML;
    document.getElementById('thursday-group-items').innerHTML = loadingHTML;
    document.getElementById('friday-group-items').innerHTML = loadingHTML;
    document.getElementById('saturday-group-items').innerHTML = loadingHTML;
  }
  
  /**
   * Esconde o indicador de carregamento
   */
  function hideLoadingIndicator() {
    // Já foi limpo pela função populateWeekCells
  }
  
  /**
   * Mostra mensagem de erro em cada célula da semana
   */
  function showErrorMessage() {
    const errorHTML = '<div class="text-center text-danger"><small>Erro ao carregar eventos</small></div>';
    document.getElementById('sunday-group-items').innerHTML = errorHTML;
    document.getElementById('monday-group-items').innerHTML = errorHTML;
    document.getElementById('tuesday-group-items').innerHTML = errorHTML;
    document.getElementById('wednesday-group-items').innerHTML = errorHTML;
    document.getElementById('thursday-group-items').innerHTML = errorHTML;
    document.getElementById('friday-group-items').innerHTML = errorHTML;
    document.getElementById('saturday-group-items').innerHTML = errorHTML;
  }
  
  /**
   * Preenche as células da semana com os eventos
   */
  function populateWeekCells(eventsByDay) {
    // Limpar células
    clearWeekCells();
    
    // Mapear dias da semana para IDs das células
    const dayMapping = {
      'sunday': 'sunday-group-items',
      'monday': 'monday-group-items',
      'tuesday': 'tuesday-group-items',
      'wednesday': 'wednesday-group-items',
      'thursday': 'thursday-group-items',
      'friday': 'friday-group-items',
      'saturday': 'saturday-group-items'
    };
    
    // Preencher cada dia com seus eventos
    for (const day in eventsByDay) {
      const events = eventsByDay[day];
      const cellId = dayMapping[day];
      const cell = document.getElementById(cellId);
      
      if (events.length === 0) {
        cell.innerHTML = '<div class="text-center text-muted"><small>Nenhum evento</small></div>';
        continue;
      }
      
      // Criar HTML para cada evento
      let eventsHTML = '';
      events.forEach(event => {
        const startTime = new Date(event.start_datetime).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
        const endTime = new Date(event.end_datetime).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
        
        eventsHTML += `
          <div class="event-item mb-2 p-2 border rounded">
            <div class="event-title fw-bold">${event.title}</div>
            <div class="event-time small">${startTime} - ${endTime}</div>
            ${event.location ? `<div class="event-location small text-muted"><i class="fas fa-map-marker-alt"></i> ${event.location}</div>` : ''}
          </div>
        `;
      });
      
      cell.innerHTML = eventsHTML;
    }
  }

  // Função para verificar se uma data é hoje
  function isToday(date) {
    const today = new Date();
    return date.getDate() === today.getDate() && 
           date.getMonth() === today.getMonth() && 
           date.getFullYear() === today.getFullYear();
  }

  const weekNumber = window.location.pathname.split('/')[2];
  const yearNow = window.location.pathname.split('/')[3];
  const currentWeekDates = getCurrentWeekDates(weekNumber, yearNow);
  const weekDaysShort = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
  const weekDaysEN = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  document.getElementById('todayButton').innerHTML = 'Hoje - ' + new Date().toLocaleDateString('pt-BR', { year: 'numeric', month: 'numeric', day: 'numeric' });
  document.getElementById('weekButton').innerHTML = weekNumber;

  document.getElementById('monthButton').innerHTML = (new Date(currentWeekDates[0])).toLocaleString('pt-BR', { month: 'long' });
  document.getElementById('yearButton').innerHTML = new Date(currentWeekDates[0]).getFullYear();
  for (let i = 0; i < 7; i++) {
    const date = new Date(currentWeekDates[i]);
    date.setDate(date.getDate()+1);
    document.getElementById(weekDaysEN[i].toLowerCase()).innerHTML = weekDaysShort[i] + ' - ' + (date.getDate()) + (isToday(date) ? ' (Hoje)' : '');
  }

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
  // Verificar se weekNumber e year são números válidos
  weekNumber = parseInt(weekNumber) || 1;
  year = parseInt(year) || new Date().getFullYear();
  
  const firstDayOfYear = new Date(year, 0, 1);
  const daysToAdd = (weekNumber - 1) * 7;
  const startOfWeek = new Date(firstDayOfYear.getTime() + daysToAdd * 24 * 60 * 60 * 1000);
  
  // Ajustar para começar no domingo
  startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay());
  
  const endOfWeek = new Date(startOfWeek);
  endOfWeek.setDate(startOfWeek.getDate() + 6);
  
  const dates = [];
  const currentDate = new Date(startOfWeek);
  
  for (let i = 0; i < 7; i++) {
    dates.push(currentDate.toISOString().split("T")[0]);
    currentDate.setDate(currentDate.getDate() + 1);
  }
  
  return dates;
}

// Function to load participants into the dropdown
function loadParticipants() {
  // Verificar se o elemento existe antes de tentar carregar participantes
  const participantsSelect = document.getElementById('eventParticipants');
  if (!participantsSelect) {
    console.error('Elemento eventParticipants não encontrado');
    return;
  }

  // Limpar opções existentes
  participantsSelect.innerHTML = '';
  
  // Adicionar opção de carregamento
  const loadingOption = document.createElement('option');
  loadingOption.textContent = 'Carregando participantes...';
  loadingOption.disabled = true;
  loadingOption.selected = true;
  participantsSelect.appendChild(loadingOption);
  
  fetch('/api/persons/')
    .then(response => {
      if (!response.ok) {
        throw new Error('Resposta da rede não foi ok: ' + response.status);
      }
      return response.json();
    })
    .then(data => {
      // Limpar opção de carregamento
      participantsSelect.innerHTML = '';
      
      // Verificar se os dados são um array
      if (!Array.isArray(data)) {
        console.error('Dados recebidos não são um array:', data);
        throw new Error('Formato de dados inválido');
      }
      
      // Adicionar opções para cada participante
      data.forEach(person => {
        if (person && person.id && person.name) {
          const option = document.createElement('option');
          option.value = person.id;
          option.textContent = person.name;
          participantsSelect.appendChild(option);
        }
      });
      
      // Se não houver participantes, mostrar mensagem
      if (data.length === 0) {
        const noDataOption = document.createElement('option');
        noDataOption.textContent = 'Nenhum participante encontrado';
        noDataOption.disabled = true;
        participantsSelect.appendChild(noDataOption);
      }
    })
    .catch(error => {
      console.error('Erro ao carregar participantes:', error);
      
      // Limpar e mostrar erro
      participantsSelect.innerHTML = '';
      const errorOption = document.createElement('option');
      errorOption.textContent = 'Erro ao carregar participantes';
      errorOption.disabled = true;
      participantsSelect.appendChild(errorOption);
    });
}

// Function to save the event with participants
function saveEvent() {
  const title = document.getElementById('eventTitle').value;
  const dateStart = document.getElementById('eventDateStart').value;
  const dateEnd = document.getElementById('eventDateEnd').value;
  const description = document.getElementById('eventDescription').value;
  const location = document.getElementById('eventLocal').value;
  
  // Get selected participants
  const participantsSelect = document.getElementById('eventParticipants');
  let selectedParticipants = [];
  
  // Verificar se o elemento existe e tem a propriedade selectedOptions
  if (participantsSelect && participantsSelect.selectedOptions) {
    // Converter HTMLCollection para Array e extrair valores
    for (let i = 0; i < participantsSelect.selectedOptions.length; i++) {
      selectedParticipants.push(participantsSelect.selectedOptions[i].value);
    }
  }
  
  // Verificar se as datas estão no formato correto
  if (!dateStart || !dateStart.match(/^\d{4}-\d{2}-\d{2}$/)) {
    alert('Por favor, insira uma data de início válida no formato AAAA-MM-DD');
    return;
  }
  
  if (!dateEnd || !dateEnd.match(/^\d{4}-\d{2}-\d{2}$/)) {
    alert('Por favor, insira uma data de término válida no formato AAAA-MM-DD');
    return;
  }
  
  // Create event data object
  const eventData = {
    title: title,
    description: description,
    start_datetime: dateStart + 'T09:00:00Z', // Default to 9 AM with timezone
    end_datetime: dateEnd + 'T10:00:00Z',     // Default to 10 AM with timezone
    location: location,
    participant_ids: selectedParticipants
  };
  
  console.log('Enviando dados do evento:', eventData);
  
  // Send POST request to create event
  fetch('/api/events/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(eventData)
  })
  .then(response => {
    if (!response.ok) {
      return response.text().then(text => {
        console.error('Resposta de erro:', text);
        throw new Error('Resposta da rede não foi ok: ' + response.status);
      });
    }
    return response.json();
  })
  .then(data => {
    console.log('Evento criado com sucesso:', data);
    // Close modal and refresh calendar
    $('#modalNewEvent').modal('hide');
    
    // Limpar o formulário
    document.getElementById('eventTitle').value = '';
    document.getElementById('eventDate').value = '';
    document.getElementById('eventDescription').value = '';
    document.getElementById('eventParticipants').selectedIndex = -1;
    
    alert('Evento criado com sucesso!');
    location.reload();
  })
  .catch(error => {
    console.error('Erro ao salvar o evento:', error);
    alert('Erro ao salvar evento. Por favor, tente novamente.');
  });
}

// Helper function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
