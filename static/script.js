
document.addEventListener("DOMContentLoaded", () => {
    const navLinks = document.querySelectorAll("nav ul li a");
    const sections = document.querySelectorAll(".content");
  
    navLinks.forEach(link => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        const sectionId = link.getAttribute("data-section");
        sections.forEach(section => {
          section.classList.add("hidden");
          section.classList.remove("active");
        });
        document.getElementById(sectionId).classList.remove("hidden");
        document.getElementById(sectionId).classList.add("active");
      });
    });
  
    // Drag and drop functionality for the upload box
    const uploadBox = document.getElementById("uploadBox");
    const fileInput = document.getElementById("fileInput");
  
    ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      uploadBox.addEventListener(eventName, preventDefaults, false);
    });
  
    function preventDefaults (e) {
      e.preventDefault();
      e.stopPropagation();
    }
  
    ;['dragenter', 'dragover'].forEach(eventName => {
      uploadBox.addEventListener(eventName, () => {
        uploadBox.classList.add("hover");
      }, false);
    });
  
    ;['dragleave', 'drop'].forEach(eventName => {
      uploadBox.addEventListener(eventName, () => {
        uploadBox.classList.remove("hover");
      }, false);
    });
  
    uploadBox.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      fileInput.files = files; // Set the dropped files to the input
    });
  });
  
  

  
  const emailInput = document.getElementById("email");
  const checkBreachBtn = document.getElementById("checkBreachBtn");

  emailInput.addEventListener("input", function () {
    const email = this.value.trim();
    const isValidEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

    if (isValidEmail) {
        checkBreachBtn.classList.add("valid-email");
        checkBreachBtn.disabled = false;
    } else {
        checkBreachBtn.classList.remove("valid-email");
        checkBreachBtn.disabled = true;
    }
});

  
  document.getElementById("checkBreachBtn").addEventListener("click", async function () {
    const email = document.getElementById("email").value.trim();
    const breachInfo = document.getElementById("breachInfo");

    // Simple email validation regex
    const isValidEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    if (!email || !isValidEmail) {
        breachInfo.textContent = "❗ Please enter a valid email address.";
        breachInfo.style.color = "orange";
        return;
    }

    const url = `http://127.0.0.1:5000/check-breach?email=${encodeURIComponent(email)}`;

    try {
        const response = await fetch(url, { method: "GET" });

        if (response.status === 200) {
            const data = await response.json();

            if (data.found) {
                breachInfo.textContent = `⚠️ This email has been found in ${data.sources.length} breaches.`;
                breachInfo.style.color = "red";
            } else {
                breachInfo.textContent = "✅ This email is not found in any known breaches.";
                breachInfo.style.color = "green";
            }
        } else {
            alert("Error checking email. Please try again later.");
        }
    } catch (error) {
        console.error("Error fetching breach data:", error);
        alert("Failed to fetch breach data.");
    }
});
