// Fungsi buat nampilin/menyembunyiin form
function toggleForm() {
    const tipe = document.querySelector('input[name="tipe"]:checked').value;
    document.getElementById('form-limit').style.display = tipe === 'limit' ? 'block' : 'none';
    document.getElementById('form-turunan').style.display = tipe === 'turunan' ? 'block' : 'none';
}

// Fungsi utama saat tombol Hitung diklik
async function hitung() {
    const fungsi = document.getElementById('fungsi').value;
    const tipe = document.querySelector('input[name="tipe"]:checked').value;
    
    if (!fungsi) {
        alert("Masukkan fungsi terlebih dahulu!");
        return;
    }

    // Siapin data yang mau dikirim
    let data = { fungsi: fungsi };
    let url = "";

    if (tipe === 'limit') {
        data.titik = document.getElementById('titik').value;
        data.arah = document.getElementById('arah').value;
        url = "/api/limit";
    } else {
        data.orde = document.getElementById('orde').value;
        url = "/api/derivative";
    }

    try {
        // Kirim data ke Backend Flask
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            alert("Error: " + result.error);
            return;
        }

        // Tampilkan Hasil
        document.getElementById('hasil-section').style.display = 'block';
        
        // Render pakai MathJax biar cantik (2*x jadi 2x)
        document.getElementById('hasil-akhir').innerHTML = `\\(${result.hasil}\\)`;
        MathJax.typesetPromise();

        // Tampilkan Langkah-langkah
        const langkahList = document.getElementById('langkah-list');
        langkahList.innerHTML = "";
        result.langkah.forEach(step => {
            const li = document.createElement('li');
            li.textContent = step;
            langkahList.appendChild(li);
        });

        // Gambar Grafik (Opsional, kita panggil fungsi di bawah)
        gambarGrafik(fungsi, result.hasil);

    } catch (error) {
        console.error(error);
        alert("Terjadi kesalahan sistem atau server mati.");
    }
}

// Placeholder untuk grafik Plotly (kita sederhanakan dulu)
function gambarGrafik(fungsi, hasil) {
    document.getElementById('grafik-section').style.display = 'block';
    // Nanti kita bikin grafik beneran di tahap selanjutnya
    document.getElementById('grafik').innerHTML = "<p style='text-align:center; color:gray;'>Grafik akan dirender di sini.</p>";
}