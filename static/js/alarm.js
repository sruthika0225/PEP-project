(() => {
  let activeAlarm = null;
  let polling = false;

  let audioContext = null;
  let alarmInterval = null;

  const overlay = document.getElementById("alarmOverlay");
  const title = document.getElementById("ringingTitle");
  const description = document.getElementById("ringingDescription");
  const ringingTime = document.getElementById("ringingTime");
  const snoozeButton = document.getElementById("snoozeButton");
  const dismissButton = document.getElementById("dismissButton");

  if (!overlay) {
    return;
  }

  function createAlarmSound() {
    try {
      if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
      }

      if (audioContext.state === "suspended") {
        audioContext.resume();
      }

      // Two alternating tones make it sound more like an alarm.
      const oscillator1 = audioContext.createOscillator();
      const oscillator2 = audioContext.createOscillator();

      const gain1 = audioContext.createGain();
      const gain2 = audioContext.createGain();

      oscillator1.type = "square";
      oscillator2.type = "square";

      oscillator1.frequency.value = 880;
      oscillator2.frequency.value = 660;

      gain1.gain.value = 0.0;
      gain2.gain.value = 0.0;

      oscillator1.connect(gain1);
      oscillator2.connect(gain2);

      gain1.connect(audioContext.destination);
      gain2.connect(audioContext.destination);

      oscillator1.start();
      oscillator2.start();

      const now = audioContext.currentTime;

      // First tone
      gain1.gain.setValueAtTime(0.0, now);
      gain1.gain.linearRampToValueAtTime(0.25, now + 0.03);
      gain1.gain.setValueAtTime(0.25, now + 0.35);
      gain1.gain.linearRampToValueAtTime(0.0, now + 0.4);

      // Second tone
      gain2.gain.setValueAtTime(0.0, now + 0.4);
      gain2.gain.linearRampToValueAtTime(0.25, now + 0.43);
      gain2.gain.setValueAtTime(0.25, now + 0.75);
      gain2.gain.linearRampToValueAtTime(0.0, now + 0.8);

      setTimeout(() => {
        oscillator1.stop();
        oscillator2.stop();
      }, 900);
    } catch (error) {
      console.error("Could not play alarm sound:", error);
    }
  }

  function startAlarmSound() {
    stopAlarmSound();

    // Play the alarm pattern repeatedly.
    createAlarmSound();

    alarmInterval = setInterval(() => {
      createAlarmSound();
    }, 1000);
  }

  function stopAlarmSound() {
    if (alarmInterval) {
      clearInterval(alarmInterval);
      alarmInterval = null;
    }
  }

  function showAlarm(task) {
    if (activeAlarm && activeAlarm.id === task.id) {
      return;
    }

    activeAlarm = task;

    title.textContent = task.title;

    description.textContent =
      task.description || "It is time for your reminder.";

    ringingTime.textContent = format12Hour(task.alarm_time);

    overlay.classList.remove("hidden");
    overlay.setAttribute("aria-hidden", "false");

    startAlarmSound();
  }

  function hideAlarm() {
    overlay.classList.add("hidden");
    overlay.setAttribute("aria-hidden", "true");

    stopAlarmSound();

    activeAlarm = null;
  }

  function format12Hour(time24) {
    const [hours, minutes] = time24.split(":").map(Number);

    if (Number.isNaN(hours) || Number.isNaN(minutes)) {
      return time24;
    }

    const period = hours >= 12 ? "PM" : "AM";
    const hour12 = hours % 12 || 12;

    return `${hour12}:${String(minutes).padStart(2, "0")} ${period}`;
  }

  async function snooze() {
    if (!activeAlarm) {
      return;
    }

    try {
      const response = await fetch(`/snooze-task/${activeAlarm.id}`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Snooze failed");
      }

      hideAlarm();
    } catch (error) {
      console.error(error);
      alert("Could not snooze the alarm.");
    }
  }

  async function dismiss() {
    if (!activeAlarm) {
      return;
    }

    try {
      const response = await fetch(`/api/alarm/${activeAlarm.id}/dismiss`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Dismiss failed");
      }

      hideAlarm();

      window.location.reload();
    } catch (error) {
      console.error(error);
      alert("Could not dismiss the alarm.");
    }
  }

  snoozeButton.addEventListener("click", snooze);
  dismissButton.addEventListener("click", dismiss);

  async function checkAlarms() {
    if (polling) {
      return;
    }

    polling = true;

    try {
      const response = await fetch("/api/tasks", {
        cache: "no-store",
      });

      if (!response.ok) {
        return;
      }

      const tasks = await response.json();

      const now = new Date();

      for (const task of tasks) {
        const scheduled = new Date(`${task.alarm_date}T${task.alarm_time}:00`);

        const difference = Math.abs(now.getTime() - scheduled.getTime());

        /*
         * Trigger when the current time is within
         * 15 seconds of the scheduled alarm.
         */
        if (difference < 15000 && task.alarm_triggered === 0) {
          showAlarm(task);
          break;
        }
      }
    } catch (error) {
      console.error("Alarm check failed:", error);
    } finally {
      polling = false;
    }
  }

  // Check every 3 seconds.
  setInterval(checkAlarms, 3000);

  checkAlarms();
})();
