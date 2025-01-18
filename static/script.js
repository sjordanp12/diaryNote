// // Ambil username dari session dengan aman menggunakan Jinja2 tojson
// const username = "{{ session['username'] | tojson }}";
// const text = `Welcome, ${username}!`; // Teks yang akan dianimasikan
// const textContainer = document.getElementById('animated-welcome'); // Kontainer animasi
// const delay = 100; // Delay per huruf dalam milidetik
// const pauseTime = 1000; // Waktu jeda sebelum mengulang animasi (1 detik)

// function splitTextToSpans(text) {
//   return text.split('').map((char) => {
//     const span = document.createElement('span');
//     span.textContent = char;
//     span.classList.add('hidden');
//     return span;
//   });
// }

// function showTextPerLetter(spans) {
//   spans.forEach((span, index) => {
//     setTimeout(() => {
//       span.classList.remove('hidden');
//     }, index * delay);
//   });
// }

// function resetText(spans) {
//   spans.forEach((span) => {
//     span.classList.add('hidden');
//   });
// }

// function animateText() {
//   const spans = splitTextToSpans(text);

//   // Kosongkan kontainer sebelum menambahkan ulang spans
//   textContainer.innerHTML = '';
//   spans.forEach((span) => textContainer.appendChild(span));

//   // Mulai menampilkan teks per huruf
//   showTextPerLetter(spans);

//   // Set delay untuk mereset dan memulai ulang animasi
//   setTimeout(() => {
//     resetText(spans);
//     animateText(); // Panggil animasi lagi untuk mengulang
//   }, text.length * delay + pauseTime);
// }

// // Mulai animasi teks
// animateText();
