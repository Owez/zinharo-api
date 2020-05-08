const RED = "bd3e3e"
const YELLOW = "ff9933"
const GREEN = "009933"

function add_alert(title, content, hex_colour) {
    var new_title = document.createElement("h4")
    var new_content = document.createElement("p")

    new_title.innerHTML = title
    new_content.innerHTML = content

    var new_alert = document.createElement("div")

    new_alert.classList.add("alert")
    new_alert.style.backgroundColor = "#" + hex_colour

    new_alert.appendChild(new_title)
    new_alert.appendChild(new_content)

    document.getElementById("alertbox").appendChild(new_alert)

    // Delete after 3 seconds
    setTimeout(function () {
        new_alert.remove()
    }, 5000)
}

// Adds initial console logs
console.log("`base.js` loaded!")
console.log("Hi future self, welcome to the debug console! P.S. A lot of loose wires are exposed in here")
