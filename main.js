const parts = {
  balcony: 5,
  "ice-close": 7,
  "ice-wide": 6,
  "night-ride": 4,
  grain: 2,
};

async function loadPieces(name) {
  const count = parts[name];
  const chunks = await Promise.all(
    Array.from({ length: count }, (_, i) =>
      fetch("photos/" + name + "." + i + ".txt").then((response) => {
        if (!response.ok) throw new Error(name);
        return response.text();
      }),
    ),
  );
  return chunks.join("").replace(/\s+/g, "");
}

const mime = { grain: "image/png" };

async function mountPhotos() {
  const jobs = Object.keys(parts).map(async (name) => {
    const data = await loadPieces(name);
    const url = "data:" + (mime[name] || "image/jpeg") + ";base64," + data;
    if (name === "grain") {
      document.querySelector(".grain").style.backgroundImage = "url(" + url + ")";
      return;
    }
    document.querySelectorAll('img[data-photo="' + name + '"]').forEach((img) => {
      img.src = url;
    });
  });
  await Promise.all(jobs);
}

const progress = document.getElementById("progress");
function onScroll() {
  const height = document.documentElement.scrollHeight - window.innerHeight;
  const value = height > 0 ? Math.min(1, window.scrollY / height) : 0;
  progress.style.transform = "scaleX(" + value + ")";
}
window.addEventListener("scroll", onScroll, { passive: true });
onScroll();

document.querySelectorAll(".track").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".track").forEach((other) => {
      other.setAttribute("aria-pressed", other === button ? "true" : "false");
    });
  });
});

const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightbox-img");

function closeLightbox() {
  lightbox.hidden = true;
  document.body.style.overflow = "";
}

document.querySelectorAll("[data-open]").forEach((button) => {
  button.addEventListener("click", () => {
    const name = button.getAttribute("data-open");
    const source = document.querySelector('img[data-photo="' + name + '"]');
    if (!source || !source.src) return;
    lightboxImg.src = source.src;
    lightboxImg.alt = source.alt;
    lightbox.hidden = false;
    document.body.style.overflow = "hidden";
  });
});

document.getElementById("close").addEventListener("click", closeLightbox);
lightbox.addEventListener("click", (event) => {
  if (event.target === lightbox) closeLightbox();
});
window.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeLightbox();
});

mountPhotos();
