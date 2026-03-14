// countdown.js
// Handles the election countdown timer on the homepage

document.addEventListener('DOMContentLoaded', () => {
    // Set the date we're counting down to: Next General Election (Nov 3, 2026 07:00:00 CST)
    const countDownDate = new Date("Nov 3, 2026 07:00:00").getTime();

    // Get the DOM elements
    const daysEl = document.getElementById("cd-days");
    const hoursEl = document.getElementById("cd-hours");
    const minsEl = document.getElementById("cd-minutes");
    const secsEl = document.getElementById("cd-seconds");
    const containerEl = document.getElementById("countdown-container");

    // If elements don't exist on this page, exit early
    if (!daysEl || !hoursEl || !minsEl || !secsEl) return;

    // Update the count down every 1 second
    const x = setInterval(function() {

        // Get today's date and time
        const now = new Date().getTime();

        // Find the distance between now and the count down date
        const distance = countDownDate - now;

        // If the count down is finished, write some text and stop timer
        if (distance < 0) {
            clearInterval(x);
            containerEl.innerHTML = '<h3 style="margin: 0; font-size: 1.5rem; color: #10b981; text-transform: uppercase;">The Election is Here! Go Vote!</h3>';
            return;
        }

        // Time calculations for days, hours, minutes and seconds
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Display the result with leading zeros if necessary
        daysEl.innerText = days < 10 ? "0" + days : days;
        hoursEl.innerText = hours < 10 ? "0" + hours : hours;
        minsEl.innerText = minutes < 10 ? "0" + minutes : minutes;
        secsEl.innerText = seconds < 10 ? "0" + seconds : seconds;

    }, 1000);
});
