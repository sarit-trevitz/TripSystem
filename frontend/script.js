//listener until all html load
document.addEventListener("DOMContentLoaded", () => {
  //for check :console.log("Script loaded and ready!");

  // The POP-UP  definition:
  // the About Pop-Up
  const aboutBtn = document.getElementById("aboutBtn");
  const aboutpopup = document.getElementById("aboutPopup");
  const aboutspan = document.querySelector(".close");
  // when the user click it seen
  if (aboutBtn && aboutpopup && aboutspan) {
    aboutBtn.onclick = function () {
      aboutpopup.style.display = "block";
    };
    //close when click in the X
    aboutspan.onclick = function () {
      aboutpopup.style.display = "none";
    };
  }

  // the Add student Pop-Up
  const addStudentBtn = document.getElementById("addStudentBtn");
  const addStudentPopup = document.getElementById("addStudentPopup");
  const closeAddStudent = document.getElementById("closeAddStudent");
 // when the user click it seen
  if (addStudentBtn && addStudentPopup) {
    addStudentBtn.onclick = function () {
      addStudentPopup.style.display = "block";
    };
     //close when click in the X
    if (closeAddStudent)
      closeAddStudent.onclick = function () {
        addStudentPopup.style.display = "none";
      };
  }
  //close when click outside the popup
  window.onclick = function (event) {
    if (event.target == aboutpopup) {
      aboutpopup.style.display = "none";
    }
    if (event.target == addStudentPopup) {
      addStudentPopup.style.display = "none";
    }
  };

  //The register button
  const registerBtn = document.querySelector(".actionbtn.enterbtn");
  if (registerBtn && registerBtn.innerText.includes("Register")) {
    //the problem was that the page refresh and didnt get the detail of the user so it prevent it
    registerBtn.onclick = async (event) => {
      event.preventDefault();

      const idVal = document.getElementById("id")?.value;
      const nameVal = document.getElementById("full_name")?.value;
      const classVal = document.getElementById("class_name")?.value;
      const role = document.querySelector('input[name="role"]:checked')?.value;
      if (!idVal || !nameVal || !classVal || !role) {
        alert("Please fill in all fields and select a role!");
        return;
      }

      const endpoint = role === "teacher" ? "/teachers" : "/students";
      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            id: idVal,
            full_name: nameVal,
            class_name: classVal,
          }),
        });

        if (response.ok) {
          window.location.href = "/frontend/login.html";
        } else {
          const errorData = await response.json();
          alert(
            "Registration failed: " + (errorData.detail || "Unknown error"),
          );
        }
      } catch (error) {
        console.error("Network error:", error);
        alert("Could not connect to the server.");
      }
    };
  }

  // The login button
  const loginBtn = document.querySelector(".actionbtn.enterbtn");
  if (loginBtn && loginBtn.innerText.includes("Login")) {
    loginBtn.onclick = async (event) => {
      event.preventDefault();

      const userId = document.getElementById("user-id").value;
      const selectedRole = document.querySelector(
        'input[name="role"]:checked',
      )?.value;

      if (!userId || !selectedRole) {
        alert("Please enter ID and select your role!");
        return;
      }

      const endpoint =
        selectedRole === "teacher"
          ? `/teachers/${userId}`
          : `/students/${userId}`;

      try {
        const response = await fetch(endpoint);
        if (response.ok) {
          const userData = await response.json();

          // store the data in the web(dafdefan)memory
          sessionStorage.setItem("userData", JSON.stringify(userData));
          sessionStorage.setItem("userRole", selectedRole);

          if (selectedRole === "teacher") {
            window.location.href = "/frontend/teacherPage.html";
          } else {
            window.location.href = "/frontend/studentPage.html";
          }
        } else {
          alert("User not found. Please check your ID or Register.");
        }
      } catch (error) {
        console.error("Login error:", error);
        alert("Connection error to the server.");
      }
    };
  }

  // The student page
  const studentIdDisp = document.getElementById("displaySId");
  if (studentIdDisp) {
    //take from the temporery memory of the web
    const data = JSON.parse(sessionStorage.getItem("userData"));
    const role = sessionStorage.getItem("userRole");

    if (data && role === "student") {
      document.getElementById("displaySId").innerText = data.id;
      document.getElementById("displaySName").innerText = data.full_name;
      document.getElementById("displaySClass").innerText = data.class_name;
    } else {
      window.location.href = "/frontend/login.html";
    }
  }

  //the teacher page and the combobox
  const teacherIdDisp = document.getElementById("displayTId");
  if (teacherIdDisp) {
    //take from the temporery memory of the web
    const data = JSON.parse(sessionStorage.getItem("userData"));
    const role = sessionStorage.getItem("userRole");

    if (data && role === "teacher") {
      document.getElementById("displayTId").innerText = data.id;
      document.getElementById("displayTName").innerText = data.full_name;
      document.getElementById("displayTClass").innerText = data.class_name;
      // the choice and what to see
      const selector = document.getElementById("tableSelector");
      const container = document.getElementById("tableContainer");

      if (selector) {
        //listen each time the teacher change
        selector.addEventListener("change", async (e) => {
          const choice = e.target.value;
          if (!choice) return;

          container.innerHTML = "<p>Loading data...</p>";

          try {
            //the teacher id if the table of just her student
            const response = await fetch(
              `/get_table_data?type=${choice}&teacher_id=${data.id}`,
            );
            const tableData = await response.json();

            if (!tableData || tableData.length === 0) {
              container.innerHTML = "<p>No records found.</p>";
              return;
            }

            // bulid the table because it is dynamic
            let html = "<table><thead><tr>";
            // take the first line to see the headers(id,name,ect.)
            Object.keys(tableData[0]).forEach((key) => {
              html += `<th>${key.replace("_", " ").toUpperCase()}</th>`;
            });
            html += "</tr></thead><tbody>";
            // the rows of data
            tableData.forEach((row) => {
              html += "<tr>";
              Object.values(row).forEach((val) => {
                html += `<td>${val}</td>`;
              });
              html += "</tr>";
            });
            html += "</tbody></table>";

            // what we see
            container.innerHTML = html;
          } catch (err) {
            console.error("Error fetching table:", err);
            container.innerHTML = "<p>Error loading data from server.</p>";
          }
        });
      }
    } else {
      window.location.href = "/frontend/login.html";
    }
  }

  //the add student by teachr bottun
  const submitBtn = document.getElementById("submitNewStudent");
  if (submitBtn) {
    submitBtn.onclick = async () => {
      const studentId = document.getElementById("newStudentId").value;
      const studentName = document.getElementById("newStudentName").value;
      const teacherData = JSON.parse(sessionStorage.getItem("userData"));

      if (!studentId || !studentName || !teacherData) {
        alert("Please fill all fields!");
        return;
      }

      try {
        const response = await fetch("/students", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            id: studentId,
            full_name: studentName,
            class_name: teacherData.class_name,
          }),
        });

        if (response.ok) {
          //close the popup
          addStudentPopup.style.display = "none";
          //clean the line in the popup
          document.getElementById("newStudentId").value = "";
          document.getElementById("newStudentName").value = "";

          //because the change refresh the table
          const selector = document.getElementById("tableSelector");
          if (selector) selector.dispatchEvent(new Event("change"));
        } else {
          const errorData = await response.json();
          alert("Failed: " + (errorData.detail || "Unknown error"));
        }
      } catch (error) {
        console.error("Error:", error);
        alert("Server connection error.");
      }
    };
  }

  // the logout button
  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.onclick = (event) => {
      //before go to differnet page,wait
      event.preventDefault();
      //clear all the memory
      sessionStorage.clear();
      //and then go to the page
      window.location.href = "/frontend/login.html";
    };
  }
});
