async function uploadResume() {
  const fileInput = document.getElementById("resume");
  const file = fileInput.files[0];
  const output = document.getElementById("output");

  if (!file) {
    output.innerText = "❌ Please select a resume PDF to upload.";
    return;
  }

  output.innerText = "⏳ Uploading and classifying resume...";

  const formData = new FormData();
  formData.append("resume", file);

  try {
    const response = await fetch("https://resumeclassifier.onrender.com/classify", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (result.error) {
      output.innerText = "❌ Error: " + result.error;
    } else {
      output.innerText = `✅ Predicted Category: ${result.category}`;
    }
  } catch (error) {
    output.innerText = "❌ An error occurred. Please try again.";
    console.error("❌ Fetch error:", error);
  }
}

function toggleMode() {
  const currentTheme = document.documentElement.getAttribute("data-theme");
  document.documentElement.setAttribute(
    "data-theme",
    currentTheme === "dark" ? "light" : "dark"
  );
}
