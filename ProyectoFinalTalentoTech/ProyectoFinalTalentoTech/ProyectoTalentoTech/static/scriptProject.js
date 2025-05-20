// Wait until the full DOM content is loaded
document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById("switchBackgroundColor");

  // If the saved theme in localStorage is "dark", apply dark theme on load
  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-theme");
    toggleBtn.textContent = "☀️ Light Mode"; // Translated from "Modo Claro"
  }

  // Listen for clicks on the dark mode toggle button
  toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme"); // Toggle dark theme class

    const isDark = document.body.classList.contains("dark-theme");
    // Change button text depending on the current theme
    toggleBtn.textContent = isDark ? "☀️ Light Mode" : "🌙 Dark Mode"; // Translated

    // Save the current theme choice in localStorage
    localStorage.setItem("theme", isDark ? "dark" : "light");
  });
});

// Toggle the 'flipped' class on the element with id 'definition' when clicked
document.getElementById('definition').addEventListener('click', function () {
    this.classList.toggle('flipped');
});

// Toggle the 'flipped' class on the element with id 'HowItWorks' when clicked
document.getElementById('HowItWorks').addEventListener('click', function () {
    this.classList.toggle('flipped');
});

// Another DOMContentLoaded event listener for interactive chart buttons
document.addEventListener('DOMContentLoaded', () => {
  // Select all buttons inside #interactive-charts with class chart-buttons
  const buttons = document.querySelectorAll('#interactive-charts .chart-buttons button');
  const chartImg = document.getElementById('chartImage');
  const noChartMsg = document.getElementById('noChartMsg');
  // Read the energy type from the body data attribute
  const energyType = document.body.getAttribute('data-energy');

  buttons.forEach(button => {
    button.addEventListener('click', async () => {
      const chartType = button.getAttribute('data-chart');

      try {
        // Fetch the chart image data from the backend, passing energyType and chartType
        const response = await fetch(`/get_chart/${energyType}?type=${chartType}`);
        const data = await response.json();

        if (data.image) {
          // Show the chart image if available
          chartImg.src = data.image;
          chartImg.style.display = 'block';
          noChartMsg.style.display = 'none';
        } else {
          // Show an error message if image is missing
          chartImg.style.display = 'none';
          noChartMsg.textContent = 'Could not load chart.';
          noChartMsg.style.display = 'block';
        }
      } catch (error) {
        // Handle fetch errors gracefully
        console.error('Error fetching chart:', error);
        chartImg.style.display = 'none';
        noChartMsg.textContent = 'Error loading chart.';
        noChartMsg.style.display = 'block';
      }
    });
  });
});
