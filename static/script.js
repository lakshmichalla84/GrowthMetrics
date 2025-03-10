document.addEventListener("DOMContentLoaded", function () {
    const ageDropdown = document.getElementById("age");
    const milestoneContainer = document.getElementById("milestone-container");
    const addMilestoneBtn = document.getElementById("add-milestone-btn");
    const form = document.getElementById("report-form");
    const submitButton = form.querySelector("button[type='submit']");
    const originalButtonText = submitButton.innerHTML;
    let allMilestones = {}; // Store all milestones from the API
    let selectedMilestones = {}; // Track milestones in the form

    // Fetch milestones when age changes
    ageDropdown.addEventListener("change", function () {
        const selectedAge = ageDropdown.value;
        milestoneContainer.innerHTML = ""; // Clear previous milestones
    
        if (selectedAge) {
            fetch(`/get_milestones?age=${selectedAge}`)
                .then(response => response.json())
                .then(data => {
                    allMilestones = data.milestones; // Store all milestones
                    selectedMilestones = {}; // Reset selected milestones
                    
                    if (Object.keys(allMilestones).length > 0) {
                        Object.keys(allMilestones).forEach(area => {
                            selectedMilestones[area] = []; // Initialize empty list
                            
                            // Create area section
                            const areaSection = document.createElement("div");
                            areaSection.classList.add("area-section");
                            areaSection.setAttribute("data-area", area);

                            // Area title
                            const areaHeader = document.createElement("p");
                            areaHeader.textContent = `${area}:`;
                            areaHeader.classList.add("development-area");

                            // Milestone container
                            const milestonesContainer = document.createElement("div");
                            milestonesContainer.classList.add("area-milestones");

                            // Append elements
                            areaSection.appendChild(areaHeader);
                            areaSection.appendChild(milestonesContainer);
                            milestoneContainer.appendChild(areaSection);

                            // Add initial milestones (up to 5)
                            allMilestones[area].slice(0, 5).forEach(milestone => {
                                addMilestoneToForm(area, milestone);
                            });
                        });
                    } else {
                        milestoneContainer.innerHTML = "<p>No milestones available for this age.</p>";
                    }
                })
                .catch(error => {
                    console.error("Error fetching milestones:", error);
                    milestoneContainer.innerHTML = "<p>Failed to load milestones.</p>";
                });
        }
    });

    // Add Milestone Modal
    addMilestoneBtn.addEventListener("click", function () {
        const modalContent = document.createElement("div");
        modalContent.classList.add("milestone-modal-content");

        Object.keys(allMilestones).forEach((area, index) => {
            if (index > 0) {
                modalContent.appendChild(document.createElement("br"));
            }

            const categoryDiv = document.createElement("div");
            categoryDiv.style.marginTop = "10px";

            // Create title
            const areaTitle = document.createElement("span");
            areaTitle.textContent = area;
            areaTitle.style.fontWeight = "bold"; 

            categoryDiv.appendChild(areaTitle);
            
            categoryDiv.appendChild(document.createElement("br"));
            categoryDiv.appendChild(document.createElement("br"));

            // Filter out milestones already in the form
            const availableMilestones = allMilestones[area].filter(milestone => 
                !selectedMilestones[area] || !selectedMilestones[area].includes(milestone)
            );

            availableMilestones.forEach(milestone => {
                const milestoneDiv = document.createElement("div");
                milestoneDiv.classList.add("milestone-option");
                milestoneDiv.innerHTML = 
                    `<span>${milestone}</span>
                    <button type="button" class="add-milestone-btn">+</button>`
                ;

                // Add event listener to add milestone to form
                milestoneDiv.querySelector(".add-milestone-btn").addEventListener("click", function (e) {
                    e.preventDefault();
                    addMilestoneToForm(area, milestone);
                    milestoneDiv.remove(); // Remove from modal
                });

                categoryDiv.appendChild(milestoneDiv);
            });

            modalContent.appendChild(categoryDiv);
        });

        showModal(modalContent);
    });

    // Function to add a milestone to the form
    function addMilestoneToForm(area, milestone) {
        let areaSection = document.querySelector(`.area-section[data-area="${area}"]`);

        // Create section if it doesn't exist
        if (!areaSection) {
            areaSection = document.createElement("div");
            areaSection.classList.add("area-section");
            areaSection.setAttribute("data-area", area);

            const areaHeader = document.createElement("p");
            areaHeader.textContent = `${area}:`;
            areaHeader.classList.add("development-area");

            const milestonesContainer = document.createElement("div");
            milestonesContainer.classList.add("area-milestones");

            areaSection.appendChild(areaHeader);
            areaSection.appendChild(milestonesContainer);
            milestoneContainer.appendChild(areaSection);
        }

        const milestonesContainer = areaSection.querySelector(".area-milestones");

        // Prevent duplicate addition
        if (selectedMilestones[area] && selectedMilestones[area].includes(milestone)) {
            return;
        }

        // Track milestone in form
        if (!selectedMilestones[area]) {
            selectedMilestones[area] = [];
        }
        selectedMilestones[area].push(milestone);

        // Create milestone item
        const milestoneDiv = document.createElement("div");
        milestoneDiv.classList.add("milestone-item");

        const label = document.createElement("label");
        label.textContent = milestone;
        label.classList.add("milestone-label");

        const select = document.createElement("select");
        select.name = "milestone_" + milestone.replace(/\s+/g, "_");
        select.classList.add("milestone-select");
        [1, 2, 3].forEach(num => {
            const option = document.createElement("option");
            option.value = num;
            option.textContent = num;
            select.appendChild(option);
        });

        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.classList.add("btn-close");
        removeBtn.setAttribute("aria-label", "Close");
        removeBtn.addEventListener("click", function (e) {
            e.preventDefault();
            milestoneDiv.remove();
            selectedMilestones[area] = selectedMilestones[area].filter(m => m !== milestone);
        });

        milestoneDiv.appendChild(label);
        milestoneDiv.appendChild(select);
        milestoneDiv.appendChild(removeBtn);
        milestonesContainer.appendChild(milestoneDiv);
    }

    // Function to show modal
    function showModal(content) {
        const existingModal = document.querySelector(".milestone-modal");
        if (existingModal) existingModal.remove();

        const modal = document.createElement("div");
        modal.classList.add("milestone-modal");

        const modalOverlay = document.createElement("div");
        modalOverlay.classList.add("milestone-modal-overlay");

        const modalBox = document.createElement("div");
        modalBox.classList.add("milestone-modal-box");

        const stickyHeader = document.createElement("div");
        stickyHeader.classList.add("sticky-header");

        const closeButton = document.createElement("button");
        closeButton.classList.add("btn-close");
        closeButton.setAttribute("aria-label", "Close");
        closeButton.addEventListener("click", function () {
            modal.remove();
        });

        stickyHeader.appendChild(closeButton);
        modalBox.appendChild(stickyHeader);
        modalBox.appendChild(content);
        modal.appendChild(modalOverlay);
        modal.appendChild(modalBox);
        document.body.appendChild(modal);
    }

    const submitBtn = document.getElementById("submit-btn");

    // Set initial button content with hidden spinner
    submitBtn.innerHTML = `
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" style="display: none;"></span>
        <span class="btn-text">Generate Report</span>
    `;

    const spinner = submitBtn.querySelector(".spinner-border");
    const btnText = submitBtn.querySelector(".btn-text");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        // Disable button and show spinner
        submitBtn.disabled = true;
        spinner.style.display = "inline-block";
        btnText.textContent = "Generating..."; // Change text

        // Use Fetch API to send the form data
        const formData = new FormData(form);
        const nameInput = document.getElementById("name").value.trim();

        fetch(form.action, {
            method: form.method,
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Server error, please try again.");
            }
            return response.blob(); // Expecting a PDF file as response
        })
        .then(blob => {
            // Create a download link for the generated PDF
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `${nameInput}_Progress_Report.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            alert("Error: " + error.message);
        })
        .finally(() => {
            // Re-enable button, hide spinner, and restore text
            submitBtn.disabled = false;
            spinner.style.display = "none";
            btnText.textContent = "Generate Report"; // Restore text
        });
    });
});