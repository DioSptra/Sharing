// ==== GALLERY LOGIC ====
const gallery = document.getElementById("gallery");
const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");

async function fetchImages(){
  try {
    const res = await fetch("/api/images");
    if(!res.ok) throw new Error("list failed");
    const items = await res.json();
    gallery.innerHTML = items.map(it => `
      <div class="card">
        <img src="${it.url}" alt="${it.key}" />
        <div style="font-size:12px;word-break:break-all">${it.key}</div>
        <button onclick="deleteImage('${encodeURIComponent(it.key)}')">Delete</button>
      </div>
    `).join("");
  } catch(e){
    gallery.innerHTML = "<p>Error loading images</p>";
    console.error(e);
  }
}

uploadForm.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const file = fileInput.files[0];
  if(!file) return alert("select file");
  const fd = new FormData();
  fd.append("file", file);
  const res = await fetch("/api/upload", { method: "POST", body: fd });
  if (res.status === 201){
    fileInput.value = "";
    fetchImages();
  } else {
    const j = await res.json();
    alert("Upload failed: " + (j.message || JSON.stringify(j)));
  }
});

async function deleteImage(key){
  const decoded = decodeURIComponent(key);
  if(!confirm("Hapus " + decoded + " ?")) return;
  const res = await fetch(`/api/delete/${decoded}`, { method: "DELETE" });
  if(res.ok) fetchImages();
  else {
    const j = await res.json();
    alert("Delete failed: " + JSON.stringify(j));
  }
}

fetchImages();


// ==== SLIDER LOGIC ====
let slides = document.querySelectorAll(".slide");
let currentIndex = 0;

function showSlide(index) {
  slides.forEach((s, i) => s.classList.toggle("active", i === index));
}

document.querySelector(".next").addEventListener("click", () => {
  currentIndex = (currentIndex + 1) % slides.length;
  showSlide(currentIndex);
});

document.querySelector(".prev").addEventListener("click", () => {
  currentIndex = (currentIndex - 1 + slides.length) % slides.length;
  showSlide(currentIndex);
});

// Auto slide every 5s
setInterval(() => {
  currentIndex = (currentIndex + 1) % slides.length;
  showSlide(currentIndex);
}, 5000);

