document.addEventListener('DOMContentLoaded', function() {
  // Вкладкалар (Почта/Телефон)
  const emailTab = document.getElementById('emailTab');
  const phoneTab = document.getElementById('phoneTab');
  const emailForm = document.getElementById('emailForm');
  const phoneForm = document.getElementById('phoneForm');

  // Почта вкладкасы
  emailTab.addEventListener('click', function() {
    emailTab.classList.add('active');
    phoneTab.classList.remove('active');
    emailForm.classList.add('active');
    phoneForm.classList.remove('active');
  });

  // Телефон вкладкасы
  phoneTab.addEventListener('click', function() {
    phoneTab.classList.add('active');
    emailTab.classList.remove('active');
    phoneForm.classList.add('active');
    emailForm.classList.remove('active');
  });

  // Форма жіберу
  emailForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const email = emailForm.querySelector('input[type="email"]').value;
    const password = emailForm.querySelector('input[type="password"]').value;

    if(email && password) {
      alert(`Қош келдіңіз! Пошта: ${email}`);
      // Мұнда Telegram Web App API-ға жіберуге болады
    } else {
      alert('Барлық өрістерді толтырыңыз!');
    }
  });

  phoneForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const phone = phoneForm.querySelector('input[type="tel"]').value;
    const password = phoneForm.querySelector('input[type="password"]').value;

    if(phone && password) {
      alert(`Қош келдіңіз! Телефон: ${phone}`);
      // Мұнда Telegram Web App API-ға жіберуге болады
    } else {
      alert('Барлық өрістерді толтырыңыз!');
    }
  });

  // "Сатып алуға өту" батырмасы
  document.querySelector('.btn-secondary').addEventListener('click', function() {
    alert('Сатып алу бөліміне өту...');
  });

  // "Құпия сөзді ұмыттыңыз ба?"
  document.querySelectorAll('.forgot-link').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      alert('Құпия сөзді қалпына келтіру сілтемесі жіберілді');
    });
  });
});

// Telegram Web App интеграциясы
if (window.Telegram && Telegram.WebApp) {
  Telegram.WebApp.ready();
  Telegram.WebApp.expand(); // Толық экран

  // Пайдаланушы деректерін алу
  const user = Telegram.WebApp.initDataUnsafe?.user;
  if (user) {
    console.log('Telegram пайдаланушысы:', user);
  }
}
