window.onload = function () {
    document.getElementById("numClasses").addEventListener("change", generateInputs);
};

function generateInputs() {
    let classes = document.querySelector("#numClasses").value;
    let container = document.querySelector("#container");
    container.innerHTML = "";

    for (let i = 0; i < classes; i++) {
        if (i >= 10) break;

        let div = document.createElement("div");
        div.innerHTML = `
            <label for="class${i}" class="fw-bold">Period ${i + 1}</label>
            <input type="text" autocomplete="off" placeholder="Class Name" id="class${i}" name="class${i}" required>
            <input type="text" autocomplete="off" placeholder="Location" id="classLocation${i}" name="classLocation${i}" required>
            <input type="time" id="time${i}" name="time${i}" required>
        `;
        container.appendChild(div);
    }
}
