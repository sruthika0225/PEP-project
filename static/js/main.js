document.addEventListener("DOMContentLoaded", () => {
  const dateInput = document.getElementById("alarmDate");

  if (dateInput && !dateInput.value) {
    const now = new Date();
    const localDate = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
      .toISOString()
      .split("T")[0];

    dateInput.min = localDate;
    dateInput.value = localDate;
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const dateInput = document.getElementById("alarmDate");

  if (dateInput && !dateInput.value) {
    const now = new Date();

    const localDate = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
      .toISOString()
      .split("T")[0];

    dateInput.min = localDate;
    dateInput.value = localDate;
  }

  // Convert 24-hour time to 12-hour format
  document.querySelectorAll(".time-12").forEach((element) => {
    const value = element.dataset.time;

    if (!value || !value.includes(":")) {
      return;
    }

    const [hours, minutes] = value.split(":").map(Number);

    if (
      Number.isNaN(hours) ||
      Number.isNaN(minutes) ||
      hours < 0 ||
      hours > 23 ||
      minutes < 0 ||
      minutes > 59
    ) {
      return;
    }

    const period = hours >= 12 ? "PM" : "AM";
    const hour12 = hours % 12 || 12;

    element.textContent = `${hour12}:${String(minutes).padStart(2, "0")} ${period}`;
  });
});
