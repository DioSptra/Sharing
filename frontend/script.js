// ==== GALLERY LOGIC ====
const gallery = document.getElementById("gallery");
const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");

async function fetchImages() {
  try {
    const res = await fetch("/api/images");
    if (!res.ok) throw new Error("list failed");
    const items = await res.json();
    if (!items.length) {
      gallery.innerHTML = "<p>No images uploaded yet 🚀</p>";
      return;
    }
    gallery.innerHTML = items
      .map(
        (it) => `
      <div class="card">
        <img src="${it.url}" alt="${it.key}" />
        <div class="filename">${it.key}</div>
        <button class="delete-btn" onclick="deleteImage('${encodeURIComponent(
          it.key
        )}')">🗑 Delete</button>
      </div>
    `
      )
      .join("");
  } catch (e) {
    gallery.innerHTML = "<p>Error loading images ❌</p>";
    console.error(e);
  }
}

uploadForm.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const file = fileInput.files[0];
  if (!file) return alert("Please select a file first 📂");
  const fd = new FormData();
  fd.append("file", file);

  try {
    const res = await fetch("/api/upload", { method: "POST", body: fd });
    if (res.status === 201) {
      fileInput.value = "";
      fetchImages();
    } else {
      const j = await res.json();
      alert("Upload failed ❌: " + (j.message || JSON.stringify(j)));
    }
  } catch (err) {
    alert("Upload error: " + err.message);
  }
});

async function deleteImage(key) {
  const decoded = decodeURIComponent(key);
  if (!confirm("Hapus " + decoded + " ?")) return;
  try {
    const res = await fetch(`/api/delete/${decoded}`, { method: "DELETE" });
    if (res.ok) {
      fetchImages();
    } else {
      const j = await res.json();
      alert("Delete failed ❌: " + JSON.stringify(j));
    }
  } catch (err) {
    alert("Delete error: " + err.message);
  }
}

// Initial load
fetchImages();


// ==== SLIDER LOGIC ====
let slides = document.querySelectorAll(".slide");
let currentIndex = 0;

function showSlide(index) {
  slides.forEach((s, i) => s.classList.toggle("active", i === index));
}

// Next / Prev controls
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
}, 8000);

// ==== NAVBAR TOGGLE ====
const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");

navToggle.addEventListener("click", () => {
  navLinks.classList.toggle("active");
});
