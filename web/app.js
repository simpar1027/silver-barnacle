let gold = 0;

const goldElement = document.getElementById("gold");
const clickButton = document.getElementById("click-button");

function updateGold() {
    goldElement.textContent = gold;
}

clickButton.addEventListener("click", () => {
    gold += 1;
    updateGold();
});


/* =========================
   ЗАГРУЗКА — 10 СЕКУНД
   ========================= */

const loadingDuration = 10000;
const startTime = Date.now();

const loadingInterval = setInterval(() => {
    const elapsed = Date.now() - startTime;

    const progress = Math.min(
        elapsed / loadingDuration,
        1
    );

    const percent = Math.floor(progress * 100);

    document.getElementById(
        "loading-progress"
    ).style.width = `${percent}%`;

    document.getElementById(
        "loading-percent"
    ).textContent = `${percent}%`;

    if (progress >= 1) {
        clearInterval(loadingInterval);

        document
            .getElementById("loading")
            .classList.add("hidden");

        document
            .getElementById("game")
            .classList.remove("hidden");
    }

}, 50);


/* =========================
   НИЖНЕЕ МЕНЮ
   ========================= */

document.querySelectorAll(".nav-button").forEach(button => {

    button.addEventListener("click", () => {

        document
            .querySelectorAll(".nav-button")
            .forEach(btn => {
                btn.classList.remove("active");
            });

        button.classList.add("active");

        const screen = button.dataset.screen;

        console.log("Раздел:", screen);
    });

});
