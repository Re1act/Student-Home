window.onload = function(){
    document.getElementById("numClasses").addEventListener("change", generateInputs);
    document.getElementById("gpaForm").addEventListener("submit", submitForm);
}


function generateInputs(){
    let classes = document.querySelector("#numClasses").value;
    let container = document.querySelector("#gradesContainer");

    container.innerHTML = "";

    for (let i = 1; i <= classes; i++){
        if (i > 10) return;

        let div = document.createElement('div');
        div.innerHTML = `
            <label for = "grade${i}">Class ${i} </label>
            <input type="text"  autocomplete="off" placeholder="Letter Grade (A, B+, etc.)" id="grade${i}" name="grade${i}" required>
            <select  class = "mb-3 form-select" id="classType${i}" name="classType${i}">
                <option value="regular">Regular</option>
                <option value="honors">Honors (+0.5)</option>
                <option value="ap">AP/IB (+1.0)</option>
            </select>
        `;
        container.appendChild(div);
    }
}

function submitForm(event) {
    event.preventDefault();
    let classes = document.querySelector("#numClasses").value;
    let totalPoints = 0;
    let validGrades = 0;

    let unweightedGradeScale = {
        "A+": 4.0, "A": 4.0, "A-": 3.7,
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7,
        "D+": 1.3, "D": 1.0, "D-": 0.7,
        "F": 0.0
    };

    for (let i = 1; i <= classes; i++) {
        let gradeInput = document.querySelector(`#grade${i}`).value.trim().toUpperCase();
        let classType = document.querySelector(`#classType${i}`).value;

        if (unweightedGradeScale[gradeInput] !== undefined) {
            let baseGPA = unweightedGradeScale[gradeInput];

            if (classType === "honors") {
                baseGPA += 0.5;
            } else if (classType === "ap") {
                baseGPA += 1.0;
            }

            totalPoints += baseGPA;
            validGrades++;
        } else {
            alert(`Invalid grade entered for Class ${i}. Please enter a valid letter grade (A, B+, C-, etc.).`);
            return;
        }
    }

    let gpa = validGrades > 0 ? (totalPoints / validGrades).toFixed(2) : 0;
    document.querySelector("#gpaResult").innerHTML = `Your GPA: <strong>${gpa}</strong>`;
}
