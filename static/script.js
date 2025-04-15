
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
  
  // Existing send file functionality
  document.getElementById("sendBtn").addEventListener("click", function() {
    const email = document.getElementById("email").value;
    const expirationDate = document.getElementById("expirationDate").value;
    const expirationTime = document.getElementById("expirationTime").value;
    const fileInput = document.getElementById("fileInput");
  
    if (!email || !expirationDate || !expirationTime || fileInput.files.length === 0) {
      alert("Please fill out all fields and upload a file.");
      return;
    }

  

    const breachCount = Math.floor(Math.random() * 10);
    // (Assume there's an element with id="breachInfo" to show this info if needed)
    // document.getElementById("breachInfo").textContent = `This email has been part of ${breachCount} breaches.`;
  
    // Generate fake link
    const fakeLink = "https://expirer.com/download?id=" + Math.random().toString(36).substr(2, 9);
    // (Assume there's an element with id="pdfLink" to show the link if needed)
    // document.getElementById("pdfLink").value = fakeLink;
  
    // Show confirmation section (if implemented)
    // document.getElementById("confirmationSection").classList.remove("hidden");

    //NEW STUFF
    const formData = new FormData();
    formData.append("email", email);
    formData.append("expiration", expirationDatetime);  // Add expiration datetime to form data
    formData.append("file", fileInput.files[0]);  // Attach the file


 
  });


  
  document.getElementById("email").addEventListener("blur", async function () {
    const email = this.value.trim();
    if (!email) return;

    const url = `http://127.0.0.1:5000/check-breach?email=${encodeURIComponent(email)}`;

    try {
        const response = await fetch(url, { method: "GET" });

        if (response.status === 200) {
            const data = await response.json();
            const breachInfo = document.getElementById("breachInfo");

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
