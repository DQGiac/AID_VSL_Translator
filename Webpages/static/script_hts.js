window.addEventListener('DOMContentLoaded', (event) => {
    async function display_it() { 
        display = document.getElementById("display_hts");
        display.src = "/hand_to_speech"
    }
    function stop_it() { 
        display = document.getElementById("display_hts");
        display.src = "/stop"
    }

    document.getElementById("start_hts").addEventListener("click", display_it)
    document.getElementById("stop_hts").addEventListener("click", stop_it)
});
async function p_hts() {
    p = document.getElementById("p_hts");
    let a = await fetch("/p_hts", { method: "GET" });
    a = await a.json();
    p.innerHTML = a["maintext"]
}
setInterval(p_hts, 700)